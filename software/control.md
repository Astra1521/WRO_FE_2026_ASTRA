# NEO — Autonomous Control System

NEO's autonomous control system connects its **camera, distance sensors, steering system and drivetrain** through the Raspberry Pi 5.

The objective of the control system is to continuously gather information about the environment, process that information and convert it into steering and propulsion commands.

---

## Control Architecture

NEO's autonomous-control loop can be represented as:

```text
Camera + ToF Sensors
        ↓
   Raspberry Pi 5
        ↓
 Environment Analysis
        ↓
  Driving Decision
        ↓
Steering + Motor Control
        ↓
     Movement
        ↓
 New Sensor Readings
        ↺
```

This process repeats continuously while NEO is operating autonomously.

<!-- UPLOAD HERE: Autonomous control block diagram -->

---

# Main Controller

The **Raspberry Pi 5** acts as NEO's central processing unit.

It coordinates:

- camera processing
- distance-sensor readings
- obstacle detection
- navigation decisions
- steering commands
- motor commands

This allows sensing, decision-making and movement to operate as one integrated system.

---

# Software Architecture

NEO's software can be understood as several connected layers:

```text
PERCEPTION
Camera + ToF Sensors
        ↓
PROCESSING
Computer Vision + Distance Analysis
        ↓
DECISION MAKING
Navigation Logic
        ↓
CONTROL
Steering + Motor Commands
        ↓
ACTUATION
SG90 Servo + EV3 Medium Motor
```

Each layer converts information into a form that can be used by the next stage.

---

# Main Control Loop

At a high level, NEO follows this repeated process:

```text
START
  ↓
Initialise Hardware
  ↓
Read Sensors
  ↓
Capture Camera Frame
  ↓
Process Environment
  ↓
Determine Required Movement
  ↓
Calculate Steering Command
  ↓
Calculate Motor Command
  ↓
Send Commands
  ↓
Repeat
```

This continuous loop allows NEO to react as its position and surroundings change.

---

# Perception

The first stage of autonomous control is understanding the environment.

NEO uses two main sources of information:

### Camera

The **Raspberry Pi Camera 3 Wide** provides visual information that can be processed using OpenCV.

It can contribute information about:

- obstacle colour
- obstacle position
- visual navigation features

### Distance Sensors

The ToF sensors provide direct measurements of surrounding clearance.

NEO currently uses sensing positions covering:

- front-left
- front-centre
- front-right
- rear

[View NEO's sensor system](../hardware/sensors.md)

[View NEO's computer-vision system](vision.md)

---

# Decision Making

Once sensor and camera information has been processed, the software determines how NEO should respond.

A simplified decision process is:

```text
Read Environment
       ↓
Is a Correction Required?
       ↓
Determine Direction
       ↓
Determine Steering Amount
       ↓
Determine Motor Command
       ↓
Execute Movement
```

The exact response depends on the current autonomous behaviour and the information available from the sensing system.

---

# Steering Control

NEO uses an **SG90 Micro Servo** for steering.

The Raspberry Pi determines the required steering position and the **PCA9685 PWM controller** generates the PWM signal used to control the servo.

```text
Raspberry Pi 5
      ↓
Steering Command
      ↓
PCA9685
      ↓
PWM Signal
      ↓
SG90 Servo
      ↓
Front Steering
```

The steering system supports:

- straight driving
- left corrections
- right corrections
- larger turning movements

NEO's measured maximum steering is approximately:

- **Left: 60°**
- **Right: slightly above 45°**

These values are approximate physical observations rather than precision measurements.

[View NEO's steering system](../mobility/steering.md)

---

# Propulsion Control

NEO uses a **LEGO EV3 Medium Motor** for propulsion.

The vehicle uses a rear-wheel-drive layout.

```text
Raspberry Pi 5
      ↓
Motor Command
      ↓
TB6612FNG
      ↓
EV3 Medium Motor
      ↓
LEGO Differential
      ↓
Rear Wheels
```

The differential allows the two driven rear wheels to rotate at different speeds while NEO turns.

[View NEO's drivetrain](../mobility/drivetrain.md)

---

# Camera-Based Steering

Visual information can contribute to steering decisions.

After an obstacle or relevant visual feature is detected, the software can estimate its horizontal position in the camera frame.

For a **640 × 480** frame:

```text
Image Centre ≈ 320 px
```

A simplified error calculation can be represented as:

```text
Error = Desired Position - Detected Position
```

The sign and magnitude of this error can then contribute to the required steering correction.

```text
Detected Position
       ↓
Calculate Error
       ↓
Determine Correction
       ↓
Steering Command
```

This allows steering decisions to respond to where an object appears within the camera view.

---

# Distance-Based Control

The ToF sensors provide additional information about the available space around NEO.

A simplified distance-control process is:

```text
Read ToF Sensors
       ↓
Compare Distances
       ↓
Determine Available Space
       ↓
Select Appropriate Movement
```

This information can support:

- obstacle clearance
- wall-distance monitoring
- collision prevention
- parking
- reverse movement

The ToF system therefore complements the visual information from the camera.

---

# Sensor Fusion

Camera and ToF information provide different types of data.

```text
Camera
   ↓
Colour + Visual Position
   ↓
           Raspberry Pi 5
   ↑
Distance + Clearance
   ↑
ToF Sensors
```

The control system can use both sources when determining the required response.

This reduces reliance on a single sensing method.

---

# Open Challenge Control

For the Open Challenge, NEO must autonomously navigate the competition field.

The control structure can be represented as:

```text
Start
  ↓
Detect Environment
  ↓
Maintain Course
  ↓
Detect Upcoming Turn
  ↓
Adjust Steering
  ↓
Complete Turn
  ↓
Continue Navigation
  ↓
Complete Required Laps
```

<!-- UPLOAD HERE: Open Challenge control-flow diagram -->

<!-- UPLOAD HERE: Open Challenge performance video/GIF -->

---

# Obstacle Challenge Control

For the Obstacle Challenge, visual obstacle information becomes an important part of the navigation process.

A simplified structure is:

```text
Capture Camera Frame
        ↓
Detect Relevant Obstacle
        ↓
Identify Colour
        ↓
Determine Position
        ↓
Check Distance Information
        ↓
Select Navigation Response
        ↓
Steer Around Obstacle
        ↓
Continue Course
```

The exact steering response depends on the detected environment and NEO's position relative to the obstacle.

<!-- UPLOAD HERE: Obstacle Challenge control-flow diagram -->

<!-- UPLOAD HERE: Obstacle Challenge performance video/GIF -->

---

# Physical Start Control

NEO includes a **push button** as a physical control input.

This allows the robot to receive a direct physical command during testing and competition preparation without requiring repeated interaction with the Raspberry Pi interface.

The button can form part of the start procedure:

```text
System Ready
     ↓
Button Input
     ↓
Begin Autonomous Routine
```

---

# Performance

During testing, NEO has completed approximately one round of the mat in:

**8.7 seconds**

This is an observed performance value rather than a calculated theoretical maximum speed.

The final performance can vary depending on:

- motor command
- battery condition
- steering corrections
- course configuration
- sensor behaviour
- obstacle placement

---

# Control System Testing

The control software is tested progressively rather than only as a complete system.

Individual testing can include:

### Sensor Testing

Confirm that distance measurements are being received correctly.

### Camera Testing

Confirm that the required visual features are detected reliably.

### Steering Testing

Confirm that requested steering positions produce the expected wheel movement.

### Motor Testing

Confirm that propulsion responds correctly to control commands.

### Integrated Testing

Combine sensing, decision-making and movement on the competition field.

This makes faults easier to isolate before full autonomous testing.

<!-- UPLOAD HERE: Photo of NEO during autonomous testing -->

---

# Fail-Safe Behaviour

Reliable autonomous operation requires NEO to avoid acting on clearly unusable information where possible.

During development, the software can account for conditions such as:

- missing sensor readings
- invalid distance measurements
- no relevant camera detection
- temporary loss of a visual target

Where useful information is unavailable, the control logic should avoid making unnecessarily aggressive corrections based on unreliable input.

---

# Control Development

NEO's control system is continuously refined through testing.

The development cycle follows:

```text
Run NEO
   ↓
Observe Behaviour
   ↓
Identify Problem
   ↓
Adjust Software / Hardware
   ↓
Test Again
```

This allows the control parameters to evolve alongside changes to sensor placement, steering geometry and the camera system.

---

# Autonomous Control Summary

NEO's autonomous-control system combines:

- Raspberry Pi 5
- Raspberry Pi Camera 3 Wide
- OpenCV-based visual processing
- Time-of-Flight distance sensing
- PCA9685 steering control
- SG90 Micro Servo
- TB6612FNG motor control
- LEGO EV3 Medium Motor
- rear-wheel-drive differential system

Together, these systems create the central autonomous loop:

```text
SENSE → PROCESS → DECIDE → ACT → REPEAT
```

This allows NEO to convert information from its environment into physical steering and propulsion commands without manual control.

---

[← Back to Main README](../README.md)
