
import time
import traceback
import numpy as np
import board
import busio
import smbus
import adafruit_bno055
import config

bus = None
i2c = None
sensor = None

def select_channel():
    """Routes the PCA9548A I2C multiplexer to the gyro channel."""
    global bus
    if bus is not None:
        try:
            mux_addr = getattr(config, 'MUX_ADDR', 0x70)
            gyro_chan = getattr(config, 'GYRO_CHANNEL', 0)
            bus.write_byte(mux_addr, 1 << gyro_chan)
            time.sleep(0.005)
        except Exception:
            pass

def initialize():
    """
    Initializes the I2C bus, multiplexer, and BNO055 sensor with retry logic.
    """
    global bus, i2c, sensor

    if not getattr(config, 'GYRO_ENABLED', True):
        print("INFO: Gyro is disabled in config.")
        return True

    for attempt in range(1, 4):
        try:
            print(f"INFO: Initializing BNO055 Gyro (Attempt {attempt}/3)...")
            
            if bus is None:
                bus = smbus.SMBus(1)

            select_channel()
            time.sleep(0.1)

            if i2c is None:
                i2c = busio.I2C(board.SCL, board.SDA)

            sensor = adafruit_bno055.BNO055_I2C(i2c)
            sensor.mode = adafruit_bno055.NDOF_MODE
            time.sleep(1.0)

            gyro_chan = getattr(config, 'GYRO_CHANNEL', 0)
            print(f"INFO: Gyro (BNO055) Initialized on MUX Channel {gyro_chan}. Temp: {sensor.temperature}°C")
            print(f"INFO: Current calibration status: {sensor.calibration_status}")
            return True
        except Exception as e:
            print(f"bno055.py: ERROR during Gyro initialization: {e}")
            traceback.print_exc()
            time.sleep(0.3)
            sensor = None
            if bus is not None:
                try:
                    bus.close()
                except Exception:
                    pass
                bus = None

    return False

def get_heading():
    """Returns current yaw (heading) in degrees (0-360), or None if unavailable."""
    if sensor is None:
        return None
    try:
        select_channel()
        heading = sensor.euler[0]
        if heading is not None:
            if heading < 0:
                heading += 360
            return heading
    except Exception:
        return None
    return None

def get_initial_heading(num_readings=20):
    """Gets an averaged, stable initial heading."""
    if sensor is None:
        return 0.0

    print("INFO: Acquiring initial heading for gyro zero point...")
    readings = []
    for _ in range(num_readings):
        yaw = get_heading()
        if yaw is not None:
            readings.append(yaw)
        time.sleep(0.05)

    if readings:
        initial_heading = float(np.mean(readings))
        print(f"INFO: Gyro zero point set to: {initial_heading:.2f} degrees.")
        return initial_heading
    else:
        print("WARNING: Could not get initial gyro heading.")
        return 0.0

def get_euler():
    """Returns full Euler angles (yaw, roll, pitch)."""
    if sensor is None:
        return None, None, None
    try:
        select_channel()
        return sensor.euler
    except Exception:
        return None, None, None

def get_quaternion():
    """Returns quaternion data."""
    if sensor is None:
        return None
    try:
        select_channel()
        return sensor.quaternion
    except Exception:
        return None

def get_calibration():
    """Returns calibration status tuple (sys, gyro, accel, mag)."""
    if sensor is None:
        return (0, 0, 0, 0)
    try:
        select_channel()
        return sensor.calibration_status
    except Exception:
        return (0, 0, 0, 0)

def cleanup():
    """Releases I2C bus resources."""
    global bus, sensor, i2c
    print("--- Cleaning up Gyro (BNO055) ---")
    if bus is not None:
        try:
            bus.close()
        except Exception:
            pass
        bus = None
    sensor = None
    i2c = None

if __name__ == "__main__":
    print("--- BNO055 Test Utility ---")
    if not initialize():
        print("Could not initialize sensor.")
    else:
        try:
            print("Reading gyro heading. Press Ctrl+C to exit.")
            while True:
                cal_status = get_calibration()
                heading = get_heading()
                if heading is not None:
                    print(f"\rHeading: {heading:7.2f}° | Cal Status (S,G,A,M): {cal_status}   ", end="")
                else:
                    print("\rCould not read heading.   ", end="")
                time.sleep(0.1)
        except KeyboardInterrupt:
            print("\nTest interrupted by user.")
        finally:
            cleanup()
