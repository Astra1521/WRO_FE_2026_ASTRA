# NEO — Raspberry Pi 5 Setup

NEO uses a **Raspberry Pi 5** as its main computing platform.

The Raspberry Pi is responsible for running the software required for computer vision, sensor processing and autonomous navigation.

This page documents the general software environment used for NEO.

---

# Hardware Required

For the Raspberry Pi setup:

- Raspberry Pi 5
- microSD card
- Raspberry Pi Camera 3 Wide
- suitable power supply
- keyboard and monitor for initial setup, if required

NEO's final onboard power is supplied through the robot's regulated power system.

[View NEO's electrical system](../hardware/electrical.md)

---

# Operating System

NEO uses Raspberry Pi OS as the software platform for the Raspberry Pi 5.

The operating system provides the environment required to run Python programs, access connected hardware and install the software libraries used by NEO.

<!-- UPDATE HERE: Add exact Raspberry Pi OS version once confirmed -->

---

# Initial Setup

After installing Raspberry Pi OS:

```text
Boot Raspberry Pi
       ↓
Complete Initial Configuration
       ↓
Connect Required Hardware
       ↓
Update System
       ↓
Create Python Environment
       ↓
Install Dependencies
       ↓
Test Individual Components
       ↓
Run NEO Software
```

---

# Update the Raspberry Pi

Before installing the project dependencies, update the package information:

```bash
sudo apt update
sudo apt upgrade
```

---

# Python

NEO's high-level autonomous software is written in **Python**.

Check the installed Python version using:

```bash
python3 --version
```

<!-- UPDATE HERE: Add exact Python version used on final NEO -->

---

# Create a Virtual Environment

A Python virtual environment can be used to keep NEO's project dependencies organised separately from the system Python installation.

Create the environment:

```bash
python3 -m venv neo-env
```

Activate it:

```bash
source neo-env/bin/activate
```

When activated, the environment can be used to install the Python libraries required by NEO.

---

# Install Python Dependencies

The exact final dependency list should match the software used in the competition version of NEO.

Core software includes:

- Python
- OpenCV
- camera-support libraries
- I2C-support libraries
- libraries required by the ToF sensors
- libraries required by the PCA9685

<!-- UPDATE HERE: Insert exact final pip install command / requirements.txt once software environment is frozen -->

---

# OpenCV

OpenCV is used for NEO's computer-vision processing.

It handles operations involved in interpreting frames from the Raspberry Pi Camera 3 Wide.

Verify the OpenCV installation in Python:

```python
import cv2
print(cv2.__version__)
```

[View NEO's computer-vision system](../software/vision.md)

---

# Enable I2C

NEO uses I2C communication for compatible sensors and control electronics.

I2C can be enabled through the Raspberry Pi configuration utility:

```bash
sudo raspi-config
```

Navigate to the interface settings and enable **I2C**.

The Raspberry Pi can then communicate with devices including NEO's I2C electronics.

---

# Check I2C Devices

Once I2C is enabled and the required utilities are installed, connected I2C devices can be checked using:

```bash
i2cdetect -y 1
```

This can help confirm whether connected electronics are visible to the Raspberry Pi during testing.

---

# Camera Setup

Connect the **Raspberry Pi Camera 3 Wide** to the Raspberry Pi using the camera interface.

The camera should be tested before running the complete autonomous software.

A basic camera test confirms that:

- the camera is detected
- frames can be captured
- the image is correctly oriented
- the field of view is suitable
- the image can be processed by the vision software

<!-- UPLOAD HERE: Screenshot of successful camera test -->

---

# ToF Sensor Setup

NEO uses **VL53L5X Time-of-Flight sensors** for distance sensing.

The sensors communicate with the Raspberry Pi through the robot's I2C system.

The **TCA9548A 8-channel I2C multiplexer** is used to manage multiple I2C devices where required.

```text
Raspberry Pi 5
      ↓
     I2C
      ↓
   TCA9548A
      ↓
 VL53L5X Sensors
```

Each sensor should be tested individually before running the complete autonomous program.

[View NEO's sensor system](../hardware/sensors.md)

---

# PCA9685 Setup

The **PCA9685 16-channel PWM controller** is used as part of NEO's steering-control system.

The Raspberry Pi communicates with the PCA9685 through I2C.

```text
Raspberry Pi 5
      ↓
     I2C
      ↓
    PCA9685
      ↓
 SG90 Micro Servo
```

Before autonomous testing, confirm that the servo responds correctly to steering commands.

---

# Test the Steering System

Before running NEO autonomously:

1. Confirm that the SG90 servo is connected correctly.
2. Confirm that the PCA9685 is detected.
3. Move the servo through a small safe range.
4. Determine the centre steering position.
5. Confirm left and right steering directions.
6. Store the final calibrated values in the software.

[View NEO's steering system](../mobility/steering.md)

---

# Test the Motor System

NEO uses the **TB6612FNG motor driver** with the **LEGO EV3 Medium Motor**.

Before a complete autonomous run:

1. Raise or secure NEO so unexpected movement cannot cause a collision.
2. Confirm the motor-driver connections.
3. Run a low-power motor test.
4. Confirm the required direction of rotation.
5. Stop the motor.
6. Proceed to controlled driving tests.

[View NEO's drivetrain](../mobility/drivetrain.md)

---

# Recommended Setup Order

The complete setup process should be performed progressively:

```text
Raspberry Pi OS
      ↓
Python Environment
      ↓
I2C
      ↓
Camera
      ↓
ToF Sensors
      ↓
PCA9685 + Servo
      ↓
Motor Driver + Motor
      ↓
Individual Software Tests
      ↓
Integrated Autonomous Software
```

Testing each subsystem separately makes faults easier to identify.

---

# Software Calibration

After the hardware is operational, several software parameters may require calibration.

These can include:

- camera colour thresholds
- camera detection regions
- steering centre position
- maximum steering values
- motor command values
- ToF sensor thresholds
- obstacle-detection parameters

These values are refined through testing on the competition field.

---

# Running NEO

Once the required software environment has been activated, NEO's autonomous program can be started from the appropriate project directory.

```bash
source neo-env/bin/activate
```

Then run the relevant competition program.

```bash
python3 main.py
```

<!-- UPDATE HERE: Replace main.py with the exact final competition file name/path if different -->

---

# Troubleshooting

## Camera Not Detected

Check:

- camera connection
- ribbon-cable orientation
- camera software configuration
- whether another program is already accessing the camera

## I2C Device Not Detected

Check:

- power
- SDA connection
- SCL connection
- common ground
- I2C configuration
- multiplexer channel selection

## Servo Not Responding

Check:

- PCA9685 connection
- servo power
- PWM configuration
- steering channel
- common ground

## ToF Sensor Not Responding

Check:

- sensor power
- I2C connection
- TCA9548A channel
- software initialisation

---

# Final Competition Environment

Before the final competition submission, Team Astra will freeze the software configuration used by NEO.

The final documentation should record:

- Raspberry Pi OS version
- Python version
- OpenCV version
- installed Python packages
- exact launch command
- final program filenames

<!-- UPDATE HERE: Add final environment information -->

This ensures that NEO's software environment can be understood and reproduced from the documentation.

---

[← Back to Main README](../README.md)
