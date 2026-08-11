# bno055.py

import time
import board
import busio
import smbus
import adafruit_bno055

import config
import servo

# Import the channel directly from config.py
from config import MUX_ADDR, GYRO_CHANNEL

# Global state variables
bus = None
i2c = None
sensor = None

def select_channel():
    """Routes the PCA9548A I2C multiplexer to the gyro channel."""
    if bus is not None:
        bus.write_byte(MUX_ADDR, 1 << GYRO_CHANNEL)
        time.sleep(0.01)

def initialize():
    """Initializes the I2C bus, multiplexer, and BNO055 sensor."""
    global bus, i2c, sensor
    
    if getattr(config, 'GYRO_ENABLED', True) is False:
        print("INFO: Gyro is disabled in config.")
        return True

    try:
        # I2C bus for MUX
        bus = smbus.SMBus(1)

        # Route MUX to the gyro channel defined in config.py
        select_channel()
        time.sleep(0.2)

        # Create I2C object for BNO055
        i2c = busio.I2C(board.SCL, board.SDA)

        # Create BNO055 sensor object
        sensor = adafruit_bno055.BNO055_I2C(i2c)
        time.sleep(1) # Allow sensor to boot up
        
        print(f"INFO: Gyro (BNO055) Initialized on MUX Channel {GYRO_CHANNEL}.")
        return True
    except Exception as e:
        print(f"FATAL: Gyro initialization failed: {e}")
        sensor = None
        return False

def get_heading():
    """Returns the current yaw (heading) in degrees."""
    if sensor is None: 
        return None
        
    try:
        select_channel()
        heading = sensor.euler[0]
        
        if heading is None: 
            return None
            
        if heading < 0: 
            heading += 360
            
        return heading
    except Exception:
        return None

def get_euler():
    """Returns full Euler angles (yaw, roll, pitch)."""
    if sensor is None: return None, None, None
    try:
        select_channel()
        return sensor.euler
    except Exception:
        return None, None, None

def get_quaternion():
    """Returns quaternion data."""
    if sensor is None: return None
    try:
        select_channel()
        return sensor.quaternion
    except Exception:
        return None

def get_calibration():
    """Returns calibration status."""
    if sensor is None: return (0,0,0,0)
    try:
        select_channel()
        return sensor.calibration_status
    except Exception:
        return (0,0,0,0)

def get_gyro():
    """Returns gyroscope data (rad/s)."""
    if sensor is None: return None
    try:
        select_channel()
        return sensor.gyro
    except Exception:
        return None

def get_acceleration():
    """Returns accelerometer data (m/s^2)."""
    if sensor is None: return None
    try:
        select_channel()
        return sensor.acceleration
    except Exception:
        return None

def get_angular_difference(angle1, angle2):
    """Calculates the shortest angular difference between two headings."""
    if angle1 is None or angle2 is None: return 360
    diff = angle1 - angle2
    while diff <= -180: diff += 360
    while diff > 180: diff -= 360
    return abs(diff)

def steer_with_gyro(current_heading_goal, current_yaw, clip_right=-45, clip_left=45):
    """Calculates heading error and commands the servo to correct drift."""
    if getattr(config, 'GYRO_ENABLED', True) and current_heading_goal is not None and current_yaw is not None:
        error = current_heading_goal - current_yaw
        
        # Normalize error to -180 to +180
        while error <= -180: error += 360
        while error > 180: error -= 360
        
        # Apply Proportional (P) control
        steer = getattr(config, 'GYRO_KP', 0.5) * error
        
        print(f"DEBUG Gyro | Target: {current_heading_goal:.1f}° | Current: {current_yaw:.1f}° | Error: {error:.1f} | Steer: {steer:.1f}")
        
        # Clip the steering angle to mechanical limits
        steer = max(clip_right, min(clip_left, steer))
        
        servo.set_angle(steer)
        return steer
        
    servo.set_angle(0.0)
    return 0.0

def cleanup():
    """Releases the I2C bus resources."""
    print("--- Cleaning up Gyro (BNO055) ---")
    global bus
    if bus is not None:
        bus.close()
        bus = None

if __name__ == "__main__":
    print("--- Testing Integrated BNO055 Module ---")
    if not initialize():
        print("Gyro test failed during initialization.")
    else:
        try:
            print("\nReading yaw data. Press Ctrl+C to stop.")
            while True:
                yaw = get_heading()
                if yaw is not None:
                    print(f"\rYaw (Heading): {yaw:7.2f}°   ", end="")
                else:
                    print("\rYaw: ERROR        ", end="")
                time.sleep(0.1)
        except KeyboardInterrupt:
            print("\nTest interrupted by user.")
        finally:
            cleanup()