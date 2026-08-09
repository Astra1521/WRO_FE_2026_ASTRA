
import time
import board
import busio
from gpiozero import OutputDevice
from adafruit_pca9685 import PCA9685
import config

pca = None
stby = None

def initialize():
    """Initializes the PCA9685 PWM driver and the motor standby GPIO pin."""
    global pca, stby
    try:
        stby = OutputDevice(config.STBY_PIN)
        stby.on()

        i2c = busio.I2C(board.SCL, board.SDA)
        pca = PCA9685(i2c)
        pca.frequency = getattr(config, 'MOTOR_PWM_FREQUENCY', 1000)

        print("INFO: Motor Driver (PCA9685 + TB6612) Initialized.")
        return True
    except Exception as e:
        print(f"FATAL: Motor failed to initialize: {e}")
        pca = None
        stby = None
        return False

def _set_pwm(channel, percent):
    """Internal function to map 0-100% speed to a 16-bit duty cycle (0-65535)."""
    if pca is None:
        return
    percent = max(0.0, min(100.0, float(percent)))
    pca.channels[channel].duty_cycle = int(percent * 65535 / 100)

def _digital_write(channel, state):
    """Internal function to set a PCA9685 channel fully HIGH or LOW."""
    if pca is None:
        return
    pca.channels[channel].duty_cycle = 65535 if state else 0

def forward(speed):
    """Drives the motor forward at a given speed (0-100%)."""
    if stby:
        stby.on()
    _digital_write(config.MOTOR_IN1_CHANNEL, True)
    _digital_write(config.MOTOR_IN2_CHANNEL, False)
    _set_pwm(config.MOTOR_PWM_CHANNEL, speed)

def reverse(speed):
    """Drives the motor in reverse at a given speed (0-100%)."""
    if stby:
        stby.on()
    _digital_write(config.MOTOR_IN1_CHANNEL, False)
    _digital_write(config.MOTOR_IN2_CHANNEL, True)
    _set_pwm(config.MOTOR_PWM_CHANNEL, speed)

def brake():
    """Brakes the motor by shorting its terminals (IN1 and IN2 HIGH)."""
    if stby:
        stby.on()
    _digital_write(config.MOTOR_IN1_CHANNEL, True)
    _digital_write(config.MOTOR_IN2_CHANNEL, True)
    _set_pwm(config.MOTOR_PWM_CHANNEL, 100)

def standby():
    """Puts the motor driver in standby mode (low power, disengaged)."""
    if stby:
        stby.off()
    _set_pwm(config.MOTOR_PWM_CHANNEL, 0)
    _digital_write(config.MOTOR_IN1_CHANNEL, False)
    _digital_write(config.MOTOR_IN2_CHANNEL, False)

def cleanup():
    """Stops the motor and releases I2C/GPIO resources."""
    print("--- Cleaning up Motor ---")
    standby()
    if pca:
        try:
            pca.deinit()
        except Exception:
            pass
    if stby:
        try:
            stby.close()
        except Exception:
            pass

if __name__ == "__main__":
    print("--- Testing Integrated Motor Module ---")
    if not initialize():
        print("Motor test failed during initialization.")
    else:
        try:
            print("Motor forward at 50% for 2 seconds...")
            forward(50)
            time.sleep(2)

            print("Motor forward at 100% for 2 seconds...")
            forward(100)
            time.sleep(2)

            print("Braking motor for 1 second...")
            brake()
            time.sleep(1)

            print("Motor reverse at 50% for 2 seconds...")
            reverse(50)
            time.sleep(2)

            print("Putting motor in standby.")
            standby()
            time.sleep(1)

            print("Motor test complete.")

        except KeyboardInterrupt:
            print("\nTest interrupted by user.")
        finally:
            cleanup()
