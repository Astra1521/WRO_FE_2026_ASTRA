# Open_main_V2.py
# This WRO_OPEN working perfect with all positions Dt.02/08/2026
# Direction Detection = Gyro (Straight + Turn + Straight)
# Wall Following  = Using Sensor Left or Right
# Corner Counting = Using Left or Right Sensors
# Stop Section = Timer Base
# coding: UTF-8

import sys
import time
import smbus
import board
import busio

# Import our finalized hardware modules
import config
import camera
import motor
import servo
import tof_sensor
import bno055


from gpiozero import OutputDevice
from gpiozero import LED, Button  # Replaced RPi.GPIO with gpiozero

from adafruit_pca9685 import PCA9685
import subprocess
subprocess.run(["pinctrl", "set", "12", "a0"], check=True)
from rpi_hardware_pwm import HardwarePWM

sys.path.append("..")
import TOF_Sense_update_1

# ==========================================================
# PCA9548A
# ==========================================================

MUX_ADDR = 0x70

LEFT_CHANNEL = 5
FRONT_CHANNEL = 3
RIGHT_CHANNEL = 2

bus = smbus.SMBus(1)

def select_channel(channel):
    bus.write_byte(MUX_ADDR, 1 << channel)
    time.sleep(0.002)

tof = TOF_Sense_update_1.TOF_Sense(1)

def get_distance(channel):
    select_channel(channel)
    d = tof.get_distance()

    if d <= 0:
        return None

    return d

# ==========================================================
# Motor
# ==========================================================

stby = OutputDevice(6)
stby.on()

i2c = busio.I2C(board.SCL, board.SDA)

pca = PCA9685(i2c)

# Motor PWM
pca.frequency = 1000

# Servo Hardware PWM (GPIO12)
servo = HardwarePWM(
    pwm_channel=0,
    hz=50
)

servo.start(7.99)      # Center duty

PWMA = 0
AIN2 = 1
AIN1 = 2


# motor frequency
pca.frequency = 1000				####################

def set_pwm(ch, percent):
    percent = max(0, min(100, percent))
    pca.channels[ch].duty_cycle = int(percent * 65535 / 100)

def digital(ch, state):
    pca.channels[ch].duty_cycle = 65535 if state else 0

def motor_forward(speed):
    digital(AIN1, True)
    digital(AIN2, False)
    set_pwm(PWMA, speed)

def motor_stop():
    set_pwm(PWMA, 0)
    digital(AIN1, False)
    digital(AIN2, False)

# ==========================================================
# Servo
# ==========================================================

SERVO_MIN_US = 500
SERVO_MAX_US = 2400

SERVO_MIN = 50
SERVO_CENTER = 95
SERVO_MAX = 140

    
def angle_to_duty_percent(angle):

    angle = max(SERVO_MIN, min(SERVO_MAX, angle))

    pulse = SERVO_MIN_US + (
        angle / 180.0
    ) * (SERVO_MAX_US - SERVO_MIN_US)

    duty = pulse / 20000.0 * 100.0

    return duty


def set_servo(angle):

    servo.change_duty_cycle(
        angle_to_duty_percent(angle)
    )

# ==========================================================
# Wall Following Parameters
# ==========================================================

TARGET_DISTANCE = 180      # mm

KP_FAR = 0.30
KP_NEAR = 0.65
KD = 0.02

BASE_SPEED = 100

previous_error = 0

# ==========================================================
# Lap / Corner Counter
# ==========================================================

CORNER_THRESHOLD = 500      # left wall disappeared
FRONT_CORNER = 220          # approaching next wall
 
CORNER_HIGH = 550
CORNER_END = 300

corner_state = 0            # state machine
corner_count = 0

TOTAL_CORNERS = 11

finish_timer = None

# ==========================================================
# Main
# ==========================================================

try:
    set_servo(SERVO_CENTER)
    time.sleep(1)

    print("Initializing Gyro for Startup Sequence...")
    bno055.initialize()
    time.sleep(1) 
    
    target_heading = bno055.get_heading()
    if target_heading is None:
        target_heading = 0 
        
    print("Driving straight to determine initial direction...")
    motor_forward(BASE_SPEED)
    
    wall_direction = "LEFT" # Fallback default
    
    # Startup Loop
    while True:
        left = get_distance(LEFT_CHANNEL)
        right = get_distance(RIGHT_CHANNEL)
        current_heading = bno055.get_heading()
        
        # 1. Steer straight using Gyro
        if current_heading is not None and target_heading is not None:
            error_heading = target_heading - current_heading
            
            # Normalize error
            while error_heading <= -180: error_heading += 360
            while error_heading > 180: error_heading -= 360
                
            # Straight drive P-control
            gyro_kp = 0.8 
            steer_correction = gyro_kp * error_heading
            angle = SERVO_CENTER + steer_correction
            angle = max(SERVO_MIN, min(SERVO_MAX, angle))
            set_servo(angle)
            
        # 2. Check for open track direction
        if left is not None and right is not None:
            diff = abs(left - right)
            
            if diff > 1000:
                motor_stop()
                if left > right:
                    wall_direction = "LEFT"
                    turn_servo_angle = SERVO_MIN  # Full Left Lock
                    heading_change = -90          # Gyro shift for Left turn
                    print("Result: Left side open. Executing 90-deg LEFT turn.")
                else:
                    wall_direction = "RIGHT"
                    turn_servo_angle = SERVO_MAX  # Full Right Lock
                    heading_change = 90           # Gyro shift for Right turn
                    print("Result: Right side open. Executing 90-deg RIGHT turn.")
                time.sleep(0.5) 
                break # Exit direction-finding loop
                
        time.sleep(0.015)
        
    # ==========================================================
    # TRANSITION PHASE 1: 90-Degree Turn
    # ==========================================================
    current_heading = bno055.get_heading()
    if current_heading is not None:
        # Calculate target heading and handle 0-360 wrap around
        target_turn_heading = (current_heading + heading_change) % 360 
        
        set_servo(turn_servo_angle)
        motor_forward(BASE_SPEED) 
        
        while True:
            current = bno055.get_heading()
            if current is not None:
                # Calculate difference accounting for 360 wrap
                diff = current - target_turn_heading
                while diff <= -180: diff += 360
                while diff > 180: diff -= 360
                
                # Stop turning when within 5 degrees of the 90-deg target
                if abs(diff) < 5: 
                    break
            time.sleep(0.01)

    # ==========================================================
    # TRANSITION PHASE 2: Settle Parallel (2 Seconds Straight)
    # ==========================================================
    print("Turn complete. Driving straight to align with wall...")
    new_straight_heading = bno055.get_heading()
    straight_end_time = time.time() + 1.0  # Run for exactly 1 seconds
    
    while time.time() < straight_end_time:
        current = bno055.get_heading()
        if current is not None and new_straight_heading is not None:
            error_heading = new_straight_heading - current
            
            # Normalize error
            while error_heading <= -180: error_heading += 360
            while error_heading > 180: error_heading -= 360
                
            # Straight drive P-control
            gyro_kp = 0.8 
            steer_correction = gyro_kp * error_heading
            angle = SERVO_CENTER + steer_correction
            angle = max(SERVO_MIN, min(SERVO_MAX, angle))
            set_servo(angle)
            
        motor_forward(BASE_SPEED)
        time.sleep(0.015)

    print("Starting Main Wall Following...")
    previous_error = 0
    

    while True:

        left = get_distance(LEFT_CHANNEL)
        front = get_distance(FRONT_CHANNEL)
        right = get_distance(RIGHT_CHANNEL)
        
        # Assign dynamic sensor reading based on determined direction
        if wall_direction == "LEFT":
            if left is None: continue
            current_distance = left
        else:
            if right is None: continue
            current_distance = right
        
        # ----------------------------------------------------------
        # Corner Detection
        # ----------------------------------------------------------

        if current_distance is not None and front is not None:

            # State 0
            # Waiting until left wall disappears
            if corner_state == 0:

                if current_distance is not None and current_distance > CORNER_HIGH:
                    corner_state = 1


            # State 1
            # Wait until front wall appears
            elif corner_state == 1:

                if current_distance is not None and current_distance < CORNER_END:
                    corner_count += 1
                    print("Corner =", corner_count)
                    #print(f"\n***** CORNER {corner_count} *****\n")
                    corner_state = 2


            # State 2
            # Wait until robot is back following wall
            elif corner_state == 2:
                if current_distance is not None and abs(current_distance - TARGET_DISTANCE) < 30:
                    corner_state = 0

            

        # ----------------------------------------------------------
        # Finish after 12 corners
        # ----------------------------------------------------------

        if corner_count >= TOTAL_CORNERS:

            if finish_timer is None:
                finish_timer = time.time()

            # continue following wall for 1 second
            elif time.time() - finish_timer >= 1.0:
                print("\nFinished 3 laps!")
                break
        
        
        if front is not None and front < 50:

            print("Obstacle Emergency STOP..!")
            motor_stop()
            # steer straight
            set_servo(SERVO_CENTER)
            break

        error = TARGET_DISTANCE - current_distance
        
        if error > 0:
            KP = KP_NEAR      # Robot is too close to the wall
        else:
            KP = KP_FAR       # Robot is too far from the wall

        derivative = error - previous_error

        steering = KP * error + KD * derivative

        previous_error = error

        # Apply steering (Invert the steering logic for the right wall)
        if wall_direction == "LEFT":
            angle = SERVO_CENTER + steering
        else:
            angle = SERVO_CENTER - steering

        angle = max(SERVO_MIN, min(SERVO_MAX, angle))

        set_servo(angle)

        motor_forward(BASE_SPEED)

        print(f"Left:{left:4}  Front:{front:4}  Right:{right:4}  Error:{error:5}  Servo:{angle:6.1f} Corner:{corner_count:2}")
    
        time.sleep(0.015)

except KeyboardInterrupt:

    print("Stopping...")

finally:

    motor_stop()
    set_servo(SERVO_CENTER)
    servo.stop()
    stby.off()
    pca.deinit()

