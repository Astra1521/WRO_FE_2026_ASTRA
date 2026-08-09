
import time
import subprocess
from rpi_hardware_pwm import HardwarePWM
import config

servo_pwm = None

def initialize():
    """Initializes the servo motor PWM using hardware timers."""
    global servo_pwm
    try:
        subprocess.run(["pinctrl", "set", "12", "a0"], check=True)
        
        servo_pwm = HardwarePWM(
            pwm_channel=config.SERVO_PWM_CHANNEL,
            hz=config.SERVO_FREQUENCY
        )
        servo_pwm.start(0)
        
        set_angle(0.0)
        time.sleep(0.5)
        
        print("INFO: Servo Initialized.")
        return True
    except Exception as e:
        print(f"FATAL: Servo failed to initialize: {e}")
        return False

def angle_to_duty(absolute_angle: float):
    """Converts a 0-180 degree angle into the correct PWM duty cycle."""
    absolute_angle = max(0.0, min(180.0, absolute_angle))
    
    pulse_us = config.SERVO_MIN_US + (
        absolute_angle / 180.0
    ) * (config.SERVO_MAX_US - config.SERVO_MIN_US)
    
    duty_cycle = (pulse_us / 20000.0) * 100.0
    return duty_cycle

def set_angle(input_angle: float):
    """
    Sets the servo angle, RESPECTING the software limits (-45 to +45).
    input_angle: 0 is straight, negative is left, positive is right.
    """
    if servo_pwm is None:
        return

    clamped_input = max(-45.0, min(45.0, input_angle))

    absolute_angle = config.SERVO_CENTER + clamped_input

    absolute_angle = max(config.SERVO_MIN, min(config.SERVO_MAX, absolute_angle))

    servo_pwm.change_duty_cycle(angle_to_duty(absolute_angle))

def set_angle_unlimited(input_angle: float):
    """
    Sets the servo angle, BYPASSING the -45 to +45 software limits.
    This is for special maneuvers like parking.
    It is still protected by the hardware limits (SERVO_MIN / SERVO_MAX).
    """
    if servo_pwm is None:
        return

    absolute_angle = config.SERVO_CENTER + input_angle

    absolute_angle = max(config.SERVO_MIN, min(config.SERVO_MAX, absolute_angle))

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
                for angle in range(-45, 46, 5):
                    print(f"\rSetting angle to: {angle}°   ", end="")
                    set_angle(angle)
                    time.sleep(0.05)
                time.sleep(0.5)
                
                for angle in range(45, -46, -5):
                    print(f"\rSetting angle to: {angle}°   ", end="")
                    set_angle(angle)
                    time.sleep(0.05)
                time.sleep(0.5)
                
        except KeyboardInterrupt:
            print("\nTest interrupted by user.")
        finally:
            cleanup()
