# distance.py

import time
import smbus
import TOF_Sense_update_1 # Assumes this is in the same flat directory
import config

# Global variables for hardware state
bus = None
tof = None


def initialize():
    """Initializes the I2C bus and the TOF sensor driver."""
    global bus, tof
    try:
        # Initialize I2C bus 1[cite: 8]
        bus = smbus.SMBus(1)
        
        # Initialize the TOF driver from TOF_Sense_update_1[cite: 8]
        tof = TOF_Sense_update_1.TOF_Sense(1)
        
        print("INFO: TOF Sensors & Multiplexer Initialized.")
        return True
    except Exception as e:
        print(f"FATAL: TOF Sensors failed to initialize: {e}")
        return False

# Alias 'initialise' to 'initialize' to maintain compatibility with 
# the original main_v3.py naming conventions if it calls distance.initialise()[cite: 6].
initialise = initialize

def select_channel(channel):
    """Routes the PCA9548A I2C multiplexer to the correct channel."""
    if bus is not None and channel >= 0:
        # Shift bit to open the specified multiplexer channel
        bus.write_byte(getattr(config, 'MUX_ADDR', 0x70), 1 << channel)
        time.sleep(0.002)  # Required 2ms delay for mux switching


def get_distance(channel):
    """
    Reads distance in millimeters from the specified channel.
    Returns None if the reading is invalid (<= 0).
    """
    if tof is None:
        return None
        
    select_channel(channel)
    distance = tof.get_distance()
    
    # Filter out invalid or zero readings[cite: 8]
    if distance is None or distance <= 0:
        return None
        
    return distance


def cleanup():
    """Releases the I2C bus resources."""
    print("--- Cleaning up TOF Sensors ---")
    global bus
    if bus is not None:
        bus.close()
        bus = None


if __name__ == "__main__":
    print("--- Testing Integrated TOF Multiplexer Module ---")
    if not initialize():
        print("TOF test failed during initialization.")
    else:
        try:
            print("\nReading data from all sensors. Press Ctrl+C to stop.")
            while True:
                # Read left, front, right using config channels
                l = get_distance(config.LEFT_CHANNEL)
                f = get_distance(config.FRONT_CHANNEL)
                r = get_distance(config.RIGHT_CHANNEL)
                
                # Format output strings (handling None values safely)
                l_str = f"{l:4.0f} mm" if l else "---- mm"
                f_str = f"{f:4.0f} mm" if f else "---- mm"
                r_str = f"{r:4.0f} mm" if r else "---- mm"
                
                print(f"\rLeft: {l_str} | Front: {f_str} | Right: {r_str}   ", end="")
                time.sleep(0.05)
                
        except KeyboardInterrupt:
            print("\nTest interrupted by user.")
        finally:
            cleanup()
