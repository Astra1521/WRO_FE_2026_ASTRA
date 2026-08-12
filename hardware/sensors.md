# NEO — Sensor System

NEO uses a combination of **Time-of-Flight (ToF) distance sensors** and the **Raspberry Pi Camera 3 Wide** to gather information about its surroundings.

The distance sensors provide direct proximity measurements, while the camera provides visual information for computer-vision-based navigation.

Together, these systems allow NEO to build a more complete understanding of the competition environment.

---

## Sensor Architecture

NEO's sensing architecture can be simplified as:

**Raspberry Pi Camera 3 Wide**  
↓  
**Visual Information**

+

**ToF Distance Sensors**  
↓  
**Distance Information**

↓

**Raspberry Pi 5**

↓

**Autonomous Decision Making**

<!-- UPLOAD HERE: Sensor architecture/block diagram -->

---

## Sensors Used

| Sensor | Purpose |
|---|---|
| Raspberry Pi Camera 3 Wide | Computer vision and obstacle recognition |
| VL53L5X ToF Sensor | Multi-zone distance measurement |
| ToF Laser Ranging Sensors | Distance and proximity measurement |
| TCA9548A I²C Multiplexer | Manages communication between multiple I²C devices |

A BNO055 IMU was also explored during development but is not currently installed in NEO's present configuration.

---

# Time-of-Flight Distance Sensing

Time-of-Flight sensors determine distance by measuring reflected light.

For NEO, these sensors provide direct numerical distance information that can support:

- obstacle avoidance
- front clearance detection
- side clearance detection
- rear clearance detection
- parking
- collision prevention

Unlike the camera, which provides visual information, ToF sensors provide direct distance measurements from specific directions around the vehicle.

---

## Sensor Placement

NEO's distance sensors are positioned around the chassis to provide information from multiple directions.

| Sensor Position | Height from Ground | Position |
|---|---:|---|
| Rear Sensor | 65 mm | 45 mm from rear edge |
| Front-Left Sensor | 70 mm | 170 mm from rear edge |
| Front-Centre Sensor | 68 mm | 190 mm from rear edge |
| Front-Right Sensor | 70 mm | 170 mm from rear edge |

The front-centre sensor is positioned approximately along the centreline of the vehicle.

<!-- UPLOAD HERE: Labelled top-view photograph showing all sensor positions -->

---

## Front-Centre Sensor

The front-centre sensor is positioned:

**68 mm above the ground**

and approximately:

**190 mm from the rear edge**

It is positioned approximately in the centre of NEO's width.

Its forward-facing position provides direct information about the space immediately ahead of the robot.

This can support:

- frontal obstacle detection
- clearance monitoring
- collision prevention
- parking

<!-- UPLOAD HERE: Close-up of front-centre sensor -->

---

## Front-Left Sensor

The front-left sensor is positioned approximately:

**70 mm above the ground**

and:

**170 mm from the rear edge**

This sensor provides additional distance information from the left side of NEO's front section.

<!-- UPLOAD HERE: Close-up of front-left sensor -->

---

## Front-Right Sensor

The front-right sensor is positioned approximately:

**70 mm above the ground**

and:

**170 mm from the rear edge**

Its placement mirrors the front-left sensing position and provides additional information from the right side of NEO.

<!-- UPLOAD HERE: Close-up of front-right sensor -->

---

## Rear Sensor

NEO's rear distance sensor is positioned approximately:

**65 mm above the ground**

and:

**45 mm from the rear edge**

The rear sensor provides information about the space behind NEO.

This is particularly useful for:

- reverse movement
- rear clearance
- parking
- preventing collisions while reversing

<!-- UPLOAD HERE: Close-up of rear sensor -->

---

## Sensor Coverage

The four sensing directions provide NEO with information from different areas around the vehicle.

```text
                 FRONT

          [ FRONT-CENTRE ]

 [ FRONT-LEFT ]       [ FRONT-RIGHT ]


                [ NEO ]


             [ REAR SENSOR ]

                  REAR
```

<!-- UPLOAD HERE: Replace the diagram above with a labelled top-view image of NEO when available -->

This arrangement allows the autonomous software to compare measurements from different directions rather than relying on a single distance reading.

---

# VL53L5X

The **VL53L5X** is used as part of NEO's Time-of-Flight sensing architecture.

It provides multi-zone distance information, allowing the sensing system to obtain more detailed proximity information than a single-point distance measurement.

The sensor communicates with NEO's control system through the I²C architecture.

<!-- UPLOAD HERE: Photo of VL53L5X used on NEO -->

---

# TCA9548A I²C Multiplexer

NEO uses a **TCA9548A 8-channel I²C multiplexer** to manage communication between multiple I²C devices.

The simplified architecture is:

**Raspberry Pi 5**  
↓  
**I²C Bus**  
↓  
**TCA9548A**  
↓  
**Individual Sensor Channels**

The multiplexer allows the Raspberry Pi to select which channel it wants to communicate with.

This is useful when multiple connected devices would otherwise use conflicting I²C addresses.

### Why We Use It

The TCA9548A allows NEO to:

- communicate with multiple I²C devices
- separate devices across different channels
- reduce address conflicts
- expand the sensing system
- organise sensor communication

<!-- UPLOAD HERE: Photo of TCA9548A installed on NEO -->

---

# Raspberry Pi Camera 3 Wide

The **Raspberry Pi Camera 3 Wide** forms the visual part of NEO's sensing system.

The camera is connected directly to the Raspberry Pi 5 through the CSI interface.

Its wide field of view allows a large portion of the competition environment to appear within each frame.

The camera can provide information for:

- obstacle recognition
- red and green colour detection
- obstacle positioning
- navigation
- parking

The current software is designed around:

| Parameter | Configuration |
|---|---:|
| Camera | Raspberry Pi Camera 3 Wide |
| Resolution | 640 × 480 |
| Frame Rate | Up to approximately 30 FPS |
| Processing | Python + OpenCV |

The final physical camera height and mounting angle will be documented once the competition configuration is fixed.

<!-- UPLOAD HERE: Final photograph of Pi Camera 3 Wide mounted on NEO -->

[View NEO's computer-vision system](../software/vision.md)

---

# Combining Camera and Distance Information

The camera and ToF sensors provide different types of environmental information.

| Camera | ToF Sensors |
|---|---|
| Provides visual information | Provides numerical distance measurements |
| Detects obstacle colour | Measures proximity |
| Determines visual obstacle position | Provides directional clearance |
| Covers a wider visual area | Measures specific sensing regions |

The autonomous system can use both types of information when determining how NEO should respond.

A simplified process is:

**Camera detects and identifies obstacle**  
↓  
**ToF sensors provide surrounding distance information**  
↓  
**Raspberry Pi evaluates the environment**  
↓  
**Navigation behaviour is selected**  
↓  
**Steering and motor commands are generated**

[View NEO's autonomous control system](../software/control.md)

---

# BNO055 Development

A **BNO055 IMU** was included during an earlier stage of NEO's development.

The sensor can provide fused orientation information for:

- heading estimation
- orientation monitoring
- turn-angle measurement

The BNO055 is **not currently installed in NEO's present physical configuration**.

The sensor and related software remain documented as part of the project's development history and may be reconsidered if heading information provides a useful performance advantage.

---

# Sensor Calibration

Sensor calibration is an important part of preparing NEO for autonomous operation.

The final calibration process can include:

- checking sensor orientation
- checking physical mounting
- confirming reliable distance readings
- identifying useful detection thresholds
- testing readings at different distances
- checking for interference from NEO's own chassis
- adjusting sensor positions where necessary

The camera also requires final calibration after its physical mounting position has been fixed.

---

# Sensor System Summary

NEO's sensing system combines:

- Raspberry Pi Camera 3 Wide
- VL53L5X Time-of-Flight sensing
- additional ToF ranging sensors
- front-centre distance sensing
- front-left distance sensing
- front-right distance sensing
- rear distance sensing
- TCA9548A I²C communication management

The camera provides visual understanding while the ToF sensors provide direct distance measurements.

Together, these systems provide the environmental information required by NEO's autonomous navigation architecture.

---

[← Back to Main README](../README.md)
