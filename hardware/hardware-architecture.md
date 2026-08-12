# NEO — Hardware Architecture

NEO's hardware architecture connects its sensing, processing, steering, propulsion and power systems around a **Raspberry Pi 5**.

The Raspberry Pi acts as the central controller, receiving environmental information and generating commands for the vehicle's steering and drive systems.

---

## System Architecture

NEO's overall hardware flow can be represented as:

**Raspberry Pi Camera 3 Wide + ToF Distance Sensors**  
↓  
**Raspberry Pi 5**  
↓  
**Autonomous Processing & Decision Making**  
↓  
**Steering Control + Motor Control**  
↓  
**NEO's Movement**

The supporting electronics allow the Raspberry Pi to communicate with multiple sensors and safely control the vehicle's actuators.

<!-- UPLOAD HERE: Hardware architecture/block diagram -->

---

## Main Hardware Components

| Component | Function |
|---|---|
| Raspberry Pi 5 | Main processing and autonomous control |
| Raspberry Pi Camera 3 Wide | Computer vision |
| VL53L5X / ToF Sensors | Distance sensing |
| TCA9548A I²C Multiplexer | Manages multiple I²C devices |
| PCA9685 PWM Controller | Generates PWM signals for steering |
| SG90 Micro Servo | Controls front-wheel steering |
| TB6612FNG Motor Driver | Controls the drive motor |
| LEGO EV3 Medium Motor | Provides propulsion |
| LEGO Differential | Transfers drive to the rear wheels |
| Bonka 11.1 V 2200 mAh LiPo | Main power source |
| XL4015 5 V 5 A | Raspberry Pi power regulation |
| MP1584 3 A | Motor-electronics power regulation |
| Push Button | Physical control input |

---

## Raspberry Pi 5 — Central Controller

The **Raspberry Pi 5** acts as NEO's main controller.

It is responsible for bringing together the different autonomous systems of the vehicle.

Its tasks include:

- receiving camera information
- reading distance-sensor data
- processing computer vision
- running navigation algorithms
- calculating steering corrections
- generating motor-control commands
- coordinating autonomous behaviours

### Why We Chose the Raspberry Pi 5

The Raspberry Pi 5 was selected because it provides the processing capability required for real-time computer vision while supporting the hardware interfaces required by NEO.

| Requirement | Raspberry Pi 5 |
|---|---|
| Computer Vision | Supports OpenCV processing |
| Programming | Strong Python compatibility |
| Camera Interface | Native CSI support |
| Sensor Communication | Supports I²C and GPIO |
| Control | Can coordinate sensing and actuation |
| Expandability | Allows additional sensors and electronics |

<!-- UPLOAD HERE: Photo of Raspberry Pi 5 installed on NEO -->

---

## Camera Interface

NEO uses a **Raspberry Pi Camera 3 Wide** connected directly to the Raspberry Pi through the CSI interface.

The camera provides visual information for:

- obstacle detection
- obstacle colour recognition
- navigation
- parking

The wide field of view allows a larger portion of the competition environment to be visible within each frame.

The software is currently designed around:

| Parameter | Configuration |
|---|---:|
| Resolution | 640 × 480 |
| Frame Rate | Up to approximately 30 FPS |
| Processing | Python + OpenCV |

<!-- UPLOAD HERE: Photo of final Pi Camera 3 Wide installation -->

[View NEO's vision system](../software/vision.md)

---

## Distance Sensor Interface

NEO uses Time-of-Flight distance sensing around the vehicle.

The current sensor arrangement provides measurements from:

- front-left
- front-centre
- front-right
- rear

These measurements provide numerical information about surrounding clearance.

The distance-sensing system complements the camera by providing direct proximity measurements.

[View detailed sensor architecture](sensors.md)

---

## I²C Communication

Several of NEO's electronic devices communicate using **I²C**.

I²C allows multiple devices to exchange information with the Raspberry Pi using a shared communication bus.

NEO uses a **TCA9548A 8-channel I²C multiplexer** as part of this architecture.

The simplified communication path is:

**Raspberry Pi 5**  
↓  
**I²C Bus**  
↓  
**TCA9548A Multiplexer**  
↓  
**Connected I²C Devices**

The multiplexer allows different channels to be selected when communicating with connected devices.

This is particularly useful when multiple devices would otherwise create I²C address conflicts.

---

## TCA9548A I²C Multiplexer

The **TCA9548A** expands NEO's I²C architecture by providing eight selectable channels.

It is used to:

- organise communication with multiple sensors
- prevent address conflicts
- allow individual sensor channels to be selected
- make the sensing architecture easier to expand

<!-- UPLOAD HERE: Close-up photo of TCA9548A installed on NEO -->

---

## Steering Hardware

NEO's steering architecture consists of:

**Raspberry Pi 5**  
↓  
**PCA9685 PWM Controller**  
↓  
**SG90 Micro Servo**  
↓  
**Custom Servo Horn**  
↓  
**Front Steering Mechanism**

The Raspberry Pi determines the required steering correction.

The **PCA9685** then provides the PWM signal required to position the SG90 servo.

Using a dedicated PWM controller allows the servo-control signal to be handled separately from the Raspberry Pi's main processing workload.

[View NEO's steering system](../mobility/steering.md)

---

## PCA9685 PWM Controller

The **PCA9685** is a 16-channel PWM controller used as part of NEO's steering system.

Its primary role in NEO is to generate the PWM signal required by the SG90 Micro Servo.

The controller allows precise servo-position commands while reducing the need for software-generated PWM timing directly from the Raspberry Pi.

---

## Propulsion Hardware

NEO's propulsion-control architecture consists of:

**Raspberry Pi 5**  
↓  
**TB6612FNG Motor Driver**  
↓  
**LEGO EV3 Medium Motor**  
↓  
**LEGO Differential**  
↓  
**Rear Wheels**

The Raspberry Pi generates the required motor command, while the TB6612FNG provides the interface required to control the drive motor.

[View NEO's drivetrain](../mobility/drivetrain.md)

---

## TB6612FNG Motor Driver

The **TB6612FNG** acts as the interface between NEO's control electronics and the LEGO EV3 Medium Motor.

The Raspberry Pi cannot directly supply the electrical power required by the drive motor.

The motor driver therefore allows the low-power control system to control the higher-power propulsion system.

Its role includes:

- motor direction control
- motor speed control
- electrical separation between control signals and motor power

<!-- UPLOAD HERE: Close-up photo of TB6612FNG -->

---

## Physical Actuators

NEO has two primary actuators.

| Actuator | Function |
|---|---|
| LEGO EV3 Medium Motor | Propulsion |
| SG90 Micro Servo | Steering |

This keeps NEO's basic movement architecture simple:

**EV3 Motor = Speed / Propulsion**

**SG90 Servo = Direction / Steering**

The two systems are controlled independently by the autonomous software.

---

## Power Architecture

NEO's hardware is powered by a **Bonka 11.1 V 2200 mAh LiPo battery**.

Because different systems require regulated power, two buck converters are used.

### Raspberry Pi Power

**11.1 V LiPo**  
↓  
**XL4015 5 V 5 A Buck Converter**  
↓  
**Raspberry Pi 5**

### Motor Electronics Power

**11.1 V LiPo**  
↓  
**MP1584 3 A Buck Converter**  
↓  
**Motor Electronics**

Separating these power paths helps reduce the effect of motor-related voltage fluctuations on the Raspberry Pi.

<!-- UPLOAD HERE: Power architecture diagram -->

[View NEO's complete electrical system](electrical-system.md)

---

## Push Button

NEO includes a physical **push button** as part of the control architecture.

The button provides a direct physical input that can be used during testing and competition operation.

This allows interaction with the robot without requiring direct access to the Raspberry Pi interface each time.

<!-- UPLOAD HERE: Photo showing push-button position -->

---

## BNO055 Development

A **BNO055 IMU** was explored during NEO's development.

The sensor can provide fused orientation and heading information for applications such as:

- heading estimation
- turn-angle measurement
- orientation correction

The BNO055 is **not currently installed in NEO's present physical configuration**.

Its previous inclusion remains documented because it formed part of the development and evaluation of NEO's sensing architecture.

---

## Hardware Integration

NEO's hardware was designed as a modular system.

Rather than permanently integrating every electronic function into a single board, the current architecture uses separate modules.

This allows individual components to be:

- replaced
- repositioned
- tested independently
- upgraded
- removed if no longer required

This modularity is particularly useful during development, when sensor positions and control hardware may need to change.

<!-- UPLOAD HERE: Clear top-view photo of NEO with electronics exposed -->

---

## Hardware Architecture Summary

NEO's hardware architecture can be divided into five layers:

### 1. Sensing
**Pi Camera 3 Wide + ToF Sensors**

↓

### 2. Processing
**Raspberry Pi 5**

↓

### 3. Communication & Control
**TCA9548A + PCA9685 + TB6612FNG**

↓

### 4. Actuation
**SG90 Servo + LEGO EV3 Medium Motor**

↓

### 5. Movement
**Front Steering + Rear-Wheel Drive**

The complete system connects environmental sensing directly to autonomous physical movement while maintaining a modular architecture that can continue to evolve during development.

---

[← Back to Main README](../README.md)
