# servo.py

import time
import subprocess
from rpi_hardware_pwm import HardwarePWM
import config

servo_pwm = None

def initialize():
    """Initializes the servo motor PWM using hardware timers."""
    global servo_pwm
    try:
        # Force GPIO 12 into PWM mode for the Raspberry Pi 5[cite: 10]
        subprocess.run(["pinctrl", "set", "12", "a0"], check=True)
        
        # rpi_hardware_pwm uses the channel number (Channel 0 = GPIO 12, Channel 1 = GPIO 13)[cite: 10]
        servo_pwm = HardwarePWM(
            pwm_channel=config.SERVO_PWM_CHANNEL, 
            hz=config.SERVO_FREQUENCY
        )
        servo_pwm.start(0)
        
        # Center the wheels on startup[cite: 10]
        set_angle(0.0)
        time.sleep(0.5)
        
        print("INFO: Servo Initialized.")
        return True
    except Exception as e:
        print(f"FATAL: Servo failed to initialize: {e}")
        return False

def angle_to_duty(absolute_angle: float):
    """Converts a 0-180 degree angle into the correct PWM duty cycle."""
    # Safety clamp absolute angle between 0 and 180 for the math formula[cite: 10]
    absolute_angle = max(0.0, min(180.0, absolute_angle))
    
    # Map angle to pulse width in microseconds[cite: 10]
    pulse_us = config.SERVO_MIN_US + (
        absolute_angle / 180.0
    ) * (config.SERVO_MAX_US - config.SERVO_MIN_US)
    
    # Convert microseconds to duty cycle % (20,000us = 20ms period for 50Hz)[cite: 10]
    duty_cycle = (pulse_us / 20000.0) * 100.0
    return duty_cycle

def set_angle(input_angle: float):
    """
    Sets the servo angle, RESPECTING the software limits (-45 to +45).
    input_angle: 0 is straight, negative is left, positive is right.
    """
    if servo_pwm is None:
        return

    # 1. Software Clamp: Limit FSM input to -45 / +45 degrees[cite: 10]
    clamped_input = max(-45.0, min(45.0, input_angle))

    # 2. Convert to Absolute Hardware Angle (Center is 95)[cite: 10]
    absolute_angle = config.SERVO_CENTER + clamped_input

    # 3. Hardware Clamp: Ensure we never exceed physical servo limits[cite: 10]
    absolute_angle = max(config.SERVO_MIN, min(config.SERVO_MAX, absolute_angle))

    # 4. Execute[cite: 10]
    servo_pwm.change_duty_cycle(angle_to_duty(absolute_angle))

def set_angle_unlimited(input_angle: float):
    """
    Sets the servo angle, BYPASSING the -45 to +45 software limits.
    This is for special maneuvers like parking.
    It is still protected by the hardware limits (SERVO_MIN / SERVO_MAX).
    """
    if servo_pwm is None:
        return

    # Skip the -45/+45 clamp and directly calculate absolute angle[cite: 10]
    absolute_angle = config.SERVO_CENTER + input_angle

    # Still strictly enforce physical hardware safety limits (50 to 140)[cite: 10]
    absolute_angle = max(config.SERVO_MIN, min(config.SERVO_MAX, absolute_angle))

    # Execute[cite: 10]
    servo_pwm.change_duty_cycle(angle_to_duty(absolute_angle))

def cleanup():
    """Centers the servo and stops PWM safely."""
    print("--- Cleaning up Servo ---")
    if servo_pwm:
        set_angle(0.0)
        time.sleep(0.5)
        servo_pwm.stop()

if __name__ == "__main__":
    print("--- Testing Unified Servo Module ---")
    if not initialize():
        print("Servo test failed during initialization.")
    else:
        try:
            print("Testing standard angle function (-45 to +45). Press Ctrl+C to exit.")
            while True:
                # Sweep from -45 to 45[cite: 10]
                for angle in range(-45, 46, 5):
                    print(f"\rSetting angle to: {angle}°   ", end="")
                    set_angle(angle)
                    time.sleep(0.05)
                time.sleep(0.5)
                
                # Sweep back from 45 to -45[cite: 10]
                for angle in range(45, -46, -5):
                    print(f"\rSetting angle to: {angle}°   ", end="")
                    set_angle(angle)
                    time.sleep(0.05)
                time.sleep(0.5)
                
        except KeyboardInterrupt:
            print("\nTest interrupted by user.")
        finally:
            cleanup()
