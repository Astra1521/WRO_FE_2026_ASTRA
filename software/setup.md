# NEO — Raspberry Pi 5 Setup

NEO uses a **Raspberry Pi 5** as its main computing platform.

The Raspberry Pi runs the software required for computer vision, sensor processing, steering control, motor control and autonomous navigation.

This page documents the general setup process for preparing the Raspberry Pi to run NEO's software.

---

## Setup Overview

The general setup process is:

```text
Prepare Raspberry Pi
        ↓
Install / Configure Raspberry Pi OS
        ↓
Update System
        ↓
Create Python Environment
        ↓
Install Required Libraries
        ↓
Enable Hardware Interfaces
        ↓
Connect Camera & Sensors
        ↓
Test Steering
        ↓
Test Motor
        ↓
Run Autonomous Software
```

---

# Hardware Required

The Raspberry Pi setup requires:

- Raspberry Pi 5
- microSD card
- Raspberry Pi Camera 3 Wide
- ToF distance sensors
- TCA9548A I²C Multiplexer
- PCA9685 PWM Controller
- TB6612FNG Motor Driver
- SG90 Micro Servo
- LEGO EV3 Medium Motor
- suitable power supply during initial setup

During normal operation, the Raspberry Pi is powered through NEO's onboard regulated power system.

[View NEO's electrical system](../hardware/electrical-system.md)

---

# Operating System

NEO uses **Raspberry Pi OS** as the operating environment for the Raspberry Pi 5.

The operating system provides the software platform required to:

- run Python
- access the camera
- communicate with sensors
- communicate with control electronics
- run OpenCV
- execute NEO's autonomous programs

<!-- UPDATE HERE: Add exact Raspberry Pi OS version used on final competition robot -->

---

# Update the Raspberry Pi

After Raspberry Pi OS has been configured, update the available packages:

```bash
sudo apt update
sudo apt upgrade
```

This ensures that the system packages are up to date before the project dependencies are installed.

---

# Python Environment

NEO's main autonomous software is written in **Python**.

The installed Python version can be checked using:

```bash
python3 --version
```

<!-- UPDATE HERE: Add exact Python version used on final competition robot -->

---

# Create a Virtual Environment

A Python virtual environment can be used to keep NEO's project libraries separate from the Raspberry Pi's system Python installation.

Create a virtual environment:

```bash
python3 -m venv neo-env
```

Activate it:

```bash
source neo-env/bin/activate
```

Once activated, the libraries required by NEO can be installed inside this environment.

---

# Required Software

NEO's software environment includes libraries required for:

- computer vision
- camera access
- I²C communication
- ToF distance sensing
- PCA9685 control
- hardware communication
- numerical processing

Important software includes:

- Python
- OpenCV
- Raspberry Pi camera libraries
- I²C support
- ToF sensor libraries
- PCA9685 control libraries

<!-- UPDATE HERE: Add exact requirements.txt / package list from final software -->

---

# OpenCV

NEO uses **OpenCV** for computer-vision processing.

OpenCV is responsible for operations including:

- image processing
- colour conversion
- colour masking
- contour detection
- object localisation
- obstacle recognition

The OpenCV installation can be checked in Python using:

```python
import cv2

print(cv2.__version__)
```

[View NEO's computer-vision system](vision.md)

---

# Enable I²C

NEO uses I²C communication for several sensors and control devices.

Open the Raspberry Pi configuration utility:

```bash
sudo raspi-config
```

Enable **I²C** through the interface settings.

After I²C is enabled, compatible devices can communicate with the Raspberry Pi.

---

# Check I²C Devices

Connected I²C devices can be checked using:

```bash
i2cdetect -y 1
```

The resulting table can help confirm whether connected electronics are visible to the Raspberry Pi.

This is useful when checking:

- TCA9548A
- PCA9685
- ToF sensors
- other compatible I²C hardware

---

# TCA9548A Setup

NEO uses a **TCA9548A 8-channel I²C multiplexer** to manage multiple I²C devices.

The communication architecture is:

```text
Raspberry Pi 5
      ↓
     I²C
      ↓
   TCA9548A
      ↓
Individual I²C Channels
      ↓
Connected Sensors
```

The required channel is selected before communicating with a sensor connected through the multiplexer.

[View NEO's sensor system](../hardware/sensors.md)

---

# Camera Setup

NEO uses the **Raspberry Pi Camera 3 Wide**.

The camera connects directly to the Raspberry Pi through the CSI interface.

Before running the complete autonomous software, confirm that:

- the camera is detected
- frames can be captured
- the image orientation is correct
- the image is stable
- the required competition-field area is visible

<!-- UPLOAD HERE: Screenshot of successful camera test -->

The final camera height and angle will be documented after the physical camera position is fixed.

---

# Camera Processing

The camera is used together with Python and OpenCV.

The general software pipeline is:

```text
Pi Camera 3 Wide
        ↓
Capture Frame
        ↓
Raspberry Pi 5
        ↓
OpenCV Processing
        ↓
Visual Information
        ↓
Navigation Logic
```

[View NEO's vision system](vision.md)

---

# ToF Sensor Setup

NEO uses Time-of-Flight sensors to measure surrounding distances.

The sensors provide information from:

- front-left
- front-centre
- front-right
- rear

The general communication path is:

```text
ToF Sensor
     ↓
    I²C
     ↓
TCA9548A
     ↓
Raspberry Pi 5
```

Each sensor should be checked individually before the complete autonomous program is run.

[View NEO's sensor system](../hardware/sensors.md)

---

# PCA9685 Setup

NEO uses the **PCA9685 16-channel PWM controller** to generate the PWM signal required by the SG90 steering servo.

The communication path is:

```text
Raspberry Pi 5
      ↓
     I²C
      ↓
    PCA9685
      ↓
     PWM
      ↓
SG90 Micro Servo
```

Before autonomous testing, confirm that the PCA9685 is detected and that the servo responds correctly.

---

# Steering Setup

The SG90 servo should be calibrated before autonomous operation.

The calibration process includes:

1. Determine the servo centre position.
2. Align the front wheels approximately straight.
3. Test a small left steering movement.
4. Test a small right steering movement.
5. Determine safe software limits.
6. Store the calibrated values in the control software.

NEO's currently observed physical steering range is approximately:

| Direction | Approximate Maximum |
|---|---:|
| Left | ~60° |
| Right | Slightly above 45° |

These values will be replaced with precise measurements after final calibration.

[View NEO's steering system](../mobility/steering.md)

---

# Motor Setup

NEO's propulsion system consists of:

```text
Raspberry Pi 5
      ↓
  TB6612FNG
      ↓
LEGO EV3 Medium Motor
      ↓
LEGO Differential
      ↓
Rear Wheels
```

Before autonomous operation:

1. Check the motor-driver connections.
2. Ensure the drivetrain can rotate freely.
3. Perform an initial low-speed motor test.
4. Confirm the required motor direction.
5. Verify that the motor stops correctly.
6. Proceed to controlled driving tests.

[View NEO's drivetrain](../mobility/drivetrain.md)

---

# Recommended Hardware Test Order

Rather than immediately running the complete autonomous system, NEO's hardware should be checked progressively.

```text
Raspberry Pi
      ↓
Camera
      ↓
I²C Communication
      ↓
ToF Sensors
      ↓
PCA9685
      ↓
SG90 Servo
      ↓
TB6612FNG
      ↓
EV3 Medium Motor
      ↓
Integrated Autonomous System
```

Testing individual systems first makes faults easier to identify.

---

# Software Calibration

Once all hardware is communicating correctly, the autonomous software can be calibrated.

Important adjustable parameters can include:

- camera colour thresholds
- obstacle-detection thresholds
- minimum contour size
- steering centre
- steering limits
- proportional steering gain
- ToF distance thresholds
- motor commands
- emergency-response thresholds

These values can be refined during testing on the competition field.

---

# Running NEO

Activate the virtual environment:

```bash
source neo-env/bin/activate
```

Navigate to the folder containing NEO's software.

The relevant autonomous program can then be launched using Python.

For example:

```bash
python3 main.py
```

<!-- UPDATE HERE: Replace main.py with the exact final competition program/file name -->

---

# Troubleshooting

## Camera Not Detected

Check:

- camera ribbon cable
- cable orientation
- CSI connection
- camera configuration
- whether another process is using the camera

---

## I²C Device Not Detected

Check:

- device power
- SDA connection
- SCL connection
- common ground
- I²C configuration
- TCA9548A channel selection

---

## ToF Sensor Not Responding

Check:

- sensor power
- I²C wiring
- multiplexer channel
- software initialisation
- sensor connection

---

## Servo Not Responding

Check:

- PCA9685 communication
- servo connection
- servo power
- PWM channel
- common ground
- software steering command

---

## Motor Not Responding

Check:

- TB6612FNG connections
- motor-power supply
- control signals
- motor wiring
- drivetrain movement
- software motor command

---

# Final Competition Environment

Once NEO's competition software is finalised, Team Astra will document the exact environment used on the robot.

The final information should include:

| Item | Final Version |
|---|---|
| Raspberry Pi OS | To be confirmed |
| Python | To be confirmed |
| OpenCV | To be confirmed |
| Camera Libraries | To be confirmed |
| ToF Libraries | To be confirmed |
| PCA9685 Libraries | To be confirmed |
| Main Program | To be confirmed |

<!-- UPDATE HERE: Complete this table once the final software environment is frozen -->

Recording the final environment will make NEO's software configuration easier to understand and reproduce.

---

# Setup Summary

NEO's Raspberry Pi setup follows a progressive process:

```text
INSTALL
   ↓
CONFIGURE
   ↓
CONNECT
   ↓
TEST
   ↓
CALIBRATE
   ↓
INTEGRATE
   ↓
RUN
```

The Raspberry Pi 5 provides the central environment in which NEO's camera processing, sensor communication and autonomous-control software operate together.

---

[← Back to Main README](../README.md)
