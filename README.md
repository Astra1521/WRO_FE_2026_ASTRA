# TEAM ASTRA — WRO FUTURE ENGINEERS 2026

<p align="center">
  <img src="images/team/astra-logo.png" width="350">
</p>

<p align="center">
  <b>A STAR IN MOTION</b>
</p>

Documentation for **Team Astra's autonomous vehicle, NEO**, developed for the **World Robot Olympiad (WRO) Future Engineers 2026** category.

---

## Team Astra

Team Astra is a three-member robotics team competing in WRO Future Engineers 2026.

Our team brings together experience in autonomous robotics, programming, mechanical assembly, design, and technical documentation.

| Team Member | School | Primary Role |
|---|---|---|
| **Dhruv Patel** | Pune International School | Software & Programming |
| **Shayaan Patel** | Adani International School | Hardware & Assembly |
| **Aarna Shah** | Ahmedabad International School | Design & Documentation |

**Team Mentor:** Mr. Paresh Gambhava

<p align="center">
  <img src="images/team/team-astra.jpg" width="700">
</p>

---

## Our Robot — NEO

<p align="center">
  <img src="images/robot/neo-hero.jpg" width="700">
</p>

**NEO** is Team Astra's autonomous vehicle for WRO Future Engineers 2026.

The robot was designed around three main priorities:

- compact and stable mechanical construction
- reliable autonomous sensing and navigation
- modular hardware that can be modified and tested efficiently

NEO combines a **LEGO Technic drivetrain and differential system** with **custom 3D-printed PLA components**, allowing us to combine rapid LEGO prototyping with purpose-built structural parts.

The vehicle uses **rear-wheel drive**, powered by a **LEGO EV3 Medium Motor**, while an **SG90 Micro Servo** controls the steering system.

A **Raspberry Pi 5** acts as the main processing unit and is designed to process camera and sensor information before making autonomous driving decisions.

---

## NEO at a Glance

| Specification | NEO |
|---|---|
| Length | 195 mm |
| Width | 111 mm |
| Height | 122 mm |
| Wheelbase | 150 mm |
| Front Track Width | 85 mm |
| Rear Track Width | 85 mm |
| Wheel Radius | 30 mm |
| Approximate Weight | ~1.5 kg* |
| Drive | Rear-wheel drive |
| Drive Motor | LEGO EV3 Medium Motor |
| Steering | SG90 Micro Servo |
| Main Controller | Raspberry Pi 5 |
| Camera | Raspberry Pi Camera 3 Wide |
| Battery | Bonka 11.1 V 2200 mAh LiPo |
| Manufacturing | LEGO Technic + custom 3D-printed PLA parts |
| 3D Printer | Bambu Lab A1 |
| Recorded Lap Time | Approximately 8.7 seconds |

\*Weight is currently an estimate and will be updated after final measurement.

---

## Robot Views

| Front | Rear | Left |
|---|---|---|
| ![NEO Front](images/robot/neo-front.jpg) | ![NEO Rear](images/robot/neo-rear.jpg) | ![NEO Left](images/robot/neo-left.jpg) |

| Right | Top | Bottom |
|---|---|---|
| ![NEO Right](images/robot/neo-right.jpg) | ![NEO Top](images/robot/neo-top.jpg) | ![NEO Bottom](images/robot/neo-bottom.jpg) |

[View more pictures of NEO](images/robot/)

---

## Project Overview

WRO Future Engineers requires teams to design an autonomous vehicle capable of navigating the competition field and responding to its surroundings without manual control.

Our approach with NEO separates the vehicle into four major systems:

1. **Mobility** — drivetrain, differential, wheels and steering
2. **Sensing** — camera and Time-of-Flight distance sensors
3. **Control** — Raspberry Pi 5 and supporting control electronics
4. **Power** — LiPo battery and independent voltage regulation

The mechanical platform was designed to remain compact while providing enough space for the drivetrain, sensors, electronics, battery, wiring and custom mounting structures.

The modular design also allows individual components to be removed, adjusted or replaced without rebuilding the complete robot.

---

## Repository Contents

This repository documents the complete development of NEO.

- **Mobility Management** — drivetrain, steering, differential and vehicle geometry
- **Hardware Architecture** — controller, sensors, motor electronics and communication
- **Power Management** — battery, voltage regulation and electrical distribution
- **3D Design & Manufacturing** — custom mounts, structural parts and CAD files
- **Obstacle Management** — environmental sensing and autonomous navigation architecture
- **Software** — autonomous control code and Raspberry Pi environment
- **Building Instructions** — mechanical and electrical assembly
- **Engineering Calculations** — track distance, theoretical speed and wheel RPM
- **Possible Improvements** — planned developments and future optimisation

---
# Mobility Management

NEO uses a compact **rear-wheel-drive configuration** designed for stable movement, tight turns and predictable autonomous control.

The mobility system consists of:

- LEGO EV3 Medium Motor for propulsion
- LEGO differential on the rear axle
- SG90 Micro Servo for front-wheel steering
- 60 mm diameter wheels
- LEGO Technic structural components
- Custom 3D-printed components

The rear wheels provide propulsion while the front wheels are dedicated to steering, keeping the two major mobility functions mechanically separate.

---

## Vehicle Geometry

| Parameter | Measurement |
|---|---:|
| Length | 195 mm |
| Width | 111 mm |
| Height | 122 mm |
| Wheelbase | 150 mm |
| Front Track Width | 85 mm |
| Rear Track Width | 85 mm |
| Wheel Radius | 30 mm |
| Wheel Diameter | 60 mm |
| Approximate Weight | ~1.5 kg |

The **150 mm wheelbase** provides enough space for the drivetrain, battery, electronics and sensors while maintaining a compact vehicle footprint.

The **85 mm front and rear track widths** help keep NEO narrow enough for manoeuvring around the Future Engineers field.

[View NEO's mobility calculations](mobility/calculations.md)

---

## Drive System

NEO uses a **rear-wheel-drive system** powered by a LEGO EV3 Medium Motor.

The drivetrain can be represented as:

**LEGO EV3 Medium Motor → LEGO Differential → Rear Axle → Rear Wheels**

Using rear-wheel drive separates propulsion from steering:

- **Rear wheels:** propulsion
- **Front wheels:** steering

This simplifies the mechanical architecture and allows the front steering system to operate independently from the driven axle.

<p align="center">
  <img src="images/mobility/drivetrain.jpg" width="650">
</p>

[More information on NEO's drivetrain](mobility/drivetrain.md)

---

## Drive Motor

NEO is propelled by a **LEGO EV3 Medium Motor**.

The motor was selected because its compact size allows it to fit within NEO's small chassis while integrating directly with the LEGO-based drivetrain.

Using a LEGO motor also allows compatible gears, axles and differential components to be connected without requiring a completely custom transmission system.

During current operation, NEO has recorded a lap time of approximately **8.7 seconds** around the mat.

This is an observed performance measurement and is kept separate from our theoretical speed calculations.

[View mobility calculations](mobility/calculations.md)

---

## Differential

A **LEGO differential gear system** is installed on NEO's driven rear axle.

During a turn, the outside wheel travels a greater distance than the inside wheel. The two rear wheels therefore need to rotate at different speeds.

The differential allows this difference while continuing to transfer power from the EV3 Medium Motor to both rear wheels.

This helps:

- reduce wheel slip
- improve cornering
- reduce stress on the drivetrain
- produce smoother movement through turns

<p align="center">
  <img src="images/mobility/differential.jpg" width="550">
</p>

[More information on NEO's drivetrain](mobility/drivetrain.md)

---

## Steering System

NEO uses **front-wheel steering** controlled by an SG90 Micro Servo.

The servo transfers rotational movement through the steering mechanism to change the direction of the front wheels.

This allows the autonomous software to make continuous steering corrections rather than relying only on fixed left, centre and right positions.

The current observed physical steering range is approximately:

| Direction | Approximate Maximum |
|---|---:|
| Left | ~60° |
| Right | Slightly above 45° |

These values are currently approximate and will be replaced with measured values after final steering calibration.

<p align="center">
  <img src="images/mobility/steering.jpg" width="600">
</p>

[More information on NEO's steering system](mobility/steering.md)

---

## Wheels

NEO uses wheels with an approximate radius of **30 mm**, giving a diameter of approximately **60 mm**.

The circumference of each wheel is calculated using:

**C = 2πr**

With:

**r = 0.03 m**

Therefore:

**C = 2π(0.03)**

**C ≈ 0.1885 m**

This means one complete wheel rotation theoretically moves NEO approximately **0.1885 m**, assuming no wheel slip.

Wheel size affects:

- distance travelled per rotation
- vehicle speed
- required motor torque
- ground clearance
- overall chassis geometry

[View full wheel and speed calculations](mobility/calculations.md)

---

## Mobility Calculations

For our theoretical mobility calculations, the estimated distance travelled over three laps was taken as approximately **26.4 m**.

### Theoretical 100% Speed

For three laps completed in approximately **27 seconds**:

**Linear Speed = Distance ÷ Time**

**26.4 ÷ 27 ≈ 0.978 m/s**

Using a wheel circumference of approximately **0.1885 m**:

**Wheel Speed ≈ 311 RPM**

### Theoretical 80% Speed

For three laps completed in approximately **32 seconds**:

**26.4 ÷ 32 ≈ 0.825 m/s**

This corresponds to approximately:

**262 RPM**

| Calculation | 100% | 80% |
|---|---:|---:|
| 3-Lap Distance | 26.4 m | 26.4 m |
| Time | 27 s | 32 s |
| Linear Speed | ~0.978 m/s | ~0.825 m/s |
| Wheel Speed | ~311 RPM | ~262 RPM |

These values are **theoretical estimates** based on the calculated travel distance and wheel circumference. They assume a **1:1 effective drivetrain ratio** and do not account for factors such as wheel slip, drivetrain losses or variations in motor speed.

They are therefore documented separately from NEO's experimentally observed lap time.

<p align="center">
  <img src="images/calculations/mobility-calculations.jpg" width="650">
</p>

[View full engineering calculations](mobility/calculations.md)

---

## Chassis Construction

NEO uses a hybrid construction system combining **LEGO Technic** with **custom 3D-printed PLA components**.

LEGO Technic is used for much of the drivetrain and mechanical assembly because it provides a modular system for:

- wheels
- axles
- gears
- differential components
- structural connections

Custom 3D-printed components are used where dedicated geometry is required for NEO's steering, camera and electronics.

This approach combines the rapid adjustability of LEGO with the design freedom of CAD and additive manufacturing.

---

## Custom 3D-Printed Components

NEO currently uses six custom-designed 3D-printed components.

All custom components are manufactured using:

| Parameter | Specification |
|---|---|
| 3D Printer | Bambu Lab A1 |
| Material | PLA |
| Manufacturing Method | FDM 3D Printing |

The six custom parts are:

| Part | Function |
|---|---|
| FE2026 Custom Chassis | Structural platform for integrating NEO's mechanical and electronic systems |
| Servo Stand | Secures the SG90 steering servo |
| Servo Horn – 13 mm | Transfers servo rotation to the steering mechanism |
| Pi Camera 3 Mount | Holds the Raspberry Pi Camera 3 Wide |
| Camera Stand V2 | Earlier version of the elevated camera-support structure |
| Camera Stand V3 | Refined version of the camera-support structure |

<p align="center">
  <img src="images/3d-printing/all-parts.jpg" width="700">
</p>

[View all 3D-printed parts and files](3d-models/README.md)

---

## Custom Part Design

3D printing allowed us to design components around NEO's geometry rather than adapting the entire robot around standard mounting solutions.

The custom chassis provides a structural interface between the LEGO mechanical system and NEO's electronics.

Dedicated servo components secure the steering mechanism, while the camera stand and Pi Camera 3 mount provide a dedicated structure for the vision system.

Because the parts are modular, individual components can be redesigned and reprinted without rebuilding the entire vehicle.

---

## Camera Stand Development

The camera-support system went through multiple versions during development.

**Camera Stand V2** and **Camera Stand V3** represent successive iterations of the same mounting concept.

The overall concept was retained while the geometry was refined, allowing the camera-support structure to evolve without requiring a redesign of the entire chassis.

| Camera Stand V2 | Camera Stand V3 |
|---|---|
| ![Camera Stand V2](images/3d-printing/camera-stand-v2.png) | ![Camera Stand V3](images/3d-printing/camera-stand-v3.png) |

[View camera stand iterations](3d-models/README.md)

---

## Sensor Placement

NEO's distance sensors are positioned around the chassis to provide information from multiple directions.

| Sensor | Height from Ground | Longitudinal Position |
|---|---:|---:|
| Rear Distance Sensor | 65 mm | 45 mm from rear edge |
| Front-Left Sensor | 70 mm | 170 mm from rear edge |
| Front-Centre Sensor | 68 mm | 190 mm from rear edge |
| Front-Right Sensor | 70 mm | 170 mm from rear edge |

The front-centre sensor is positioned approximately along the centreline of the robot.

The left and right sensors provide additional information around the front of NEO, while the rear sensor provides information behind the vehicle.

<p align="center">
  <img src="images/mobility/sensor-layout.jpg" width="650">
</p>

[View detailed sensor placement](hardware/sensors.md)

---

## Mobility System Summary

NEO's mobility architecture combines:

- rear-wheel drive
- LEGO EV3 Medium Motor propulsion
- LEGO differential
- front servo steering
- 150 mm wheelbase
- 85 mm track width
- 60 mm diameter wheels
- LEGO Technic construction
- custom 3D-printed PLA components

The system was designed to provide a compact and modular mechanical platform on which NEO's sensing, control and autonomous navigation systems can operate.
# Power & Sense Management

NEO's electrical architecture is centred around the **Raspberry Pi 5**, which acts as the main controller for sensing, processing and autonomous decision-making.

The system combines:

- Raspberry Pi 5
- Raspberry Pi Camera 3 Wide
- Time-of-Flight distance sensors
- TCA9548A I²C Multiplexer
- PCA9685 PWM Controller
- TB6612FNG Motor Driver
- SG90 Micro Servo
- LEGO EV3 Medium Motor
- XL4015 Buck Converter
- MP1584 Buck Converter
- Bonka 11.1 V 2200 mAh LiPo Battery

The electrical system is designed so that sensing, processing, steering and propulsion can operate together while maintaining stable power delivery to the Raspberry Pi and motor electronics.

---

## Hardware Architecture

The **Raspberry Pi 5** serves as the central controller of NEO.

It processes sensor data, camera information and autonomous driving algorithms before generating commands for the steering and propulsion systems.

The overall architecture can be represented as:

**Camera + Distance Sensors**  
↓  
**Raspberry Pi 5**  
↓  
**Autonomous Decision Making**  
↓  
**Steering Control + Motor Control**  
↓  
**NEO's Movement**

<p align="center">
  <img src="images/hardware/hardware-architecture.png" width="750">
</p>

[View full hardware architecture](hardware/hardware-architecture.md)

---

## Main Controller — Raspberry Pi 5

The **Raspberry Pi 5** is NEO's main computing platform.

It was selected because autonomous navigation requires significantly more processing than simple sensor-based robotics, particularly when computer vision is involved.

The Raspberry Pi allows NEO to:

- process camera frames
- read distance sensors
- run autonomous navigation algorithms
- calculate steering corrections
- control propulsion
- manage multiple hardware interfaces

It also provides strong compatibility with **Python and OpenCV**, which are used within NEO's software architecture.

### Why We Chose the Raspberry Pi 5

| Requirement | Raspberry Pi 5 Advantage |
|---|---|
| Computer Vision | Sufficient processing capability for OpenCV |
| Programming | Strong Python support |
| Camera | Native CSI camera interface |
| Sensors | Supports I²C and GPIO communication |
| Autonomous Control | Can process sensing and decision-making on one platform |
| Expandability | Supports additional hardware as NEO develops |

<p align="center">
  <img src="images/hardware/raspberry-pi.jpg" width="550">
</p>

[More information on NEO's controller](hardware/hardware-architecture.md)

---

## Computer Vision — Raspberry Pi Camera 3 Wide

NEO uses a **Raspberry Pi Camera 3 Wide** for computer vision.

The wide field of view is useful for autonomous navigation because it allows a larger portion of the competition field to appear within each camera frame.

This helps reduce blind areas and provides more visual information for:

- obstacle detection
- obstacle colour recognition
- navigation
- corner approach
- parking

The camera connects directly to the Raspberry Pi through the **CSI interface**, providing a compact and stable connection without requiring a conventional USB camera.

The current software is designed around camera frames of:

| Parameter | Configuration |
|---|---:|
| Resolution | 640 × 480 |
| Frame Rate | Up to approximately 30 FPS |
| Processing | Python + OpenCV |

The camera's final physical height and angle will be recorded once the final mounting configuration is fixed.

<p align="center">
  <img src="images/hardware/camera.jpg" width="550">
</p>

[View NEO's vision system](software/vision.md)

---

## Distance Sensing

NEO uses **Time-of-Flight (ToF) laser ranging sensors** to obtain direct distance measurements from its surroundings.

The sensing hardware includes the **VL53L5X** and additional ToF ranging hardware used around the vehicle.

Distance sensing complements the camera because it provides numerical proximity information rather than relying entirely on visual estimation.

These measurements can support:

- wall-distance monitoring
- obstacle avoidance
- front clearance detection
- rear clearance detection
- collision prevention
- parking

---

## Sensor Arrangement

Distance sensors are positioned around NEO to provide information from several directions.

| Sensor Position | Height from Ground | Position |
|---|---:|---|
| Rear | 65 mm | 45 mm from rear edge |
| Front-Left | 70 mm | 170 mm from rear edge |
| Front-Centre | 68 mm | 190 mm from rear edge |
| Front-Right | 70 mm | 170 mm from rear edge |

The **front-centre sensor** is positioned approximately along the centreline of NEO.

The front-left and front-right sensors provide additional information from either side of the vehicle, while the rear sensor provides clearance information behind NEO.

<p align="center">
  <img src="images/hardware/sensor-layout.jpg" width="650">
</p>

[View detailed sensor information](hardware/sensors.md)

---

## TCA9548A I²C Multiplexer

NEO uses a **TCA9548A 8-channel I²C multiplexer** to manage communication between multiple I²C devices.

I²C allows several electronic devices to communicate with the Raspberry Pi through a shared communication bus.

However, multiple identical devices may use the same I²C address.

The TCA9548A solves this by allowing devices to be separated across selectable channels.

### Why We Use the TCA9548A

- manages multiple I²C devices
- helps prevent address conflicts
- simplifies sensor communication
- allows individual channels to be selected
- makes the sensing architecture easier to expand

[View NEO's sensor architecture](hardware/sensors.md)

---

## Steering Control — PCA9685

NEO uses a **PCA9685 16-channel PWM controller** as part of the steering-control architecture.

The SG90 servo requires a PWM signal to determine its position.

Using dedicated PWM hardware allows stable servo-control signals to be generated without requiring the Raspberry Pi to continuously handle precise PWM timing in software.

The control path can be represented as:

**Raspberry Pi 5**  
↓  
**PCA9685**  
↓  
**SG90 Micro Servo**  
↓  
**Steering Mechanism**

This allows NEO's autonomous software to translate calculated steering corrections into physical movement of the front wheels.

---

## Motor Control — TB6612FNG

NEO uses a **TB6612FNG motor driver** to control the LEGO EV3 Medium Motor.

The Raspberry Pi cannot directly provide the electrical power required by the drive motor. The motor driver therefore acts as an interface between the control system and the propulsion system.

The motor-control path can be represented as:

**Raspberry Pi 5**  
↓  
**TB6612FNG Motor Driver**  
↓  
**LEGO EV3 Medium Motor**  
↓  
**Differential**  
↓  
**Rear Wheels**

The TB6612FNG allows the control system to manage motor direction and speed while keeping the motor's power demand separate from the Raspberry Pi's control signals.

---

## Power Architecture

NEO is powered by a **Bonka 11.1 V 2200 mAh LiPo battery**.

Because the Raspberry Pi and motor electronics require different regulated supplies, NEO uses two separate DC-DC buck converters.

| Component | Function |
|---|---|
| Bonka 11.1 V 2200 mAh LiPo | Main power source |
| XL4015 5 V 5 A | Raspberry Pi power regulation |
| MP1584 3 A | Motor electronics power regulation |

The power architecture can be simplified as:

**11.1 V LiPo Battery**  
↓  
**Power Distribution**

**Branch 1:**  
Battery → XL4015 → Raspberry Pi 5

**Branch 2:**  
Battery → MP1584 → Motor Electronics

Using separate regulated power paths helps reduce the effect of motor-related voltage fluctuations on the Raspberry Pi.

<p align="center">
  <img src="images/hardware/power-architecture.png" width="700">
</p>

[View full electrical system](hardware/electrical-system.md)

---

## XL4015 Buck Converter

The **XL4015 5 V 5 A buck converter** is used to provide the regulated supply required by the Raspberry Pi.

A stable Raspberry Pi power supply is important because voltage instability can affect:

- processing
- camera operation
- sensor communication
- software reliability

The XL4015 was selected to provide the current capacity required by the Raspberry Pi 5 while stepping down the battery voltage.

---

## MP1584 Buck Converter

The **MP1584 3 A buck converter** is used for NEO's motor-electronics power system.

Using a separate converter for this part of the robot reduces the interaction between motor-related electrical loads and the Raspberry Pi's regulated power supply.

This separation improves the organisation and stability of NEO's power architecture.

---

## Battery Energy

NEO's battery is rated at:

**11.1 V, 2200 mAh**

Battery capacity:

**2200 mAh = 2.2 Ah**

The nominal stored energy can therefore be estimated using:

**Energy = Voltage × Capacity**

**Energy = 11.1 × 2.2**

**Energy ≈ 24.4 Wh**

NEO therefore has approximately **24.4 Wh of nominal battery energy** available from a fully charged battery under idealised conditions.

Actual runtime depends on factors including:

- Raspberry Pi processing load
- motor speed
- steering activity
- sensor usage
- converter efficiency
- drivetrain load

For this reason, the energy calculation is documented separately from measured runtime.

---

## Battery Charging

The LiPo battery is charged using an **iMAX B6AC Dual Power 80 W balance charger**.

A balance charger is used to maintain the LiPo cells correctly during charging and repeated testing.

The battery is checked before operation and securely mounted within the chassis so that it cannot shift significantly during acceleration, braking or cornering.

---

## Push Button

NEO includes a physical **push button** as part of its control system.

The button provides a direct physical input for operating the robot during testing and competition runs.

Its placement allows the team to interact with the vehicle without requiring direct access to the Raspberry Pi interface each time.

<p align="center">
  <img src="images/hardware/push-button.jpg" width="450">
</p>

---

## Electrical Schematic

The electrical schematic documents the connections between NEO's main computing, sensing, control and power systems.

The final schematic includes:

- Raspberry Pi 5
- PCA9685
- TCA9548A
- TB6612FNG
- ToF sensors
- SG90 Micro Servo
- LEGO EV3 Medium Motor
- XL4015
- MP1584
- LiPo battery
- power connections
- signal connections
- I²C communication
- PWM control

<p align="center">
  <img src="images/hardware/circuit-diagram.png" width="800">
</p>

[View full-resolution circuit diagram](hardware/electrical-system.md)

---

## BNO055 Development

A **BNO055 IMU / gyro sensor** was included during NEO's development for orientation and heading sensing.

The BNO055 can provide fused orientation information that may be used for:

- heading estimation
- turn-angle measurement
- orientation correction

The sensor has been part of NEO's development architecture, although it is not currently installed in the present physical configuration.

The related software has been retained as part of the project's development history and may be used again if orientation sensing provides a useful performance improvement.

---

## Safety Measures

NEO incorporates several measures intended to improve electrical and mechanical reliability.

- **Separate power regulation:** Independent converters are used for the Raspberry Pi and motor electronics.
- **Secure battery mounting:** The LiPo battery is fixed within the chassis to prevent movement during operation.
- **Physical push button:** Provides direct control during testing and operation.
- **Secure electronics:** Boards and components are mounted to reduce movement and accidental disconnections.
- **Organised wiring:** Wiring is positioned away from moving drivetrain and steering components.
- **Battery monitoring:** Battery condition is checked before operation to reduce the risk of excessive discharge.
- **Balance charging:** The LiPo battery is charged using an iMAX B6AC balance charger.
- **Software steering limits:** Normal steering commands are restricted to avoid unnecessarily forcing the mechanism against its physical limits.

---

## Power & Sense Management Summary

NEO's power and sensing architecture combines a **Raspberry Pi 5**, camera, multiple distance sensors, dedicated control electronics and independently regulated power paths.

The Raspberry Pi acts as the central processing platform, while the camera and ToF sensors provide environmental information.

The PCA9685 and TB6612FNG translate autonomous control decisions into steering and propulsion, while the XL4015 and MP1584 regulate power for the computing and motor systems.

Together, these systems connect NEO's sensing, decision-making and physical movement into one integrated autonomous platform.
# Obstacle Management

NEO's obstacle-management system combines **computer vision** with **Time-of-Flight distance sensing** to understand the environment and make autonomous navigation decisions.

The Raspberry Pi 5 receives information from the camera and distance sensors, processes this information, and determines the appropriate steering and propulsion response.

The overall process can be represented as:

**Camera + ToF Sensors**  
↓  
**Environmental Perception**  
↓  
**Raspberry Pi 5**  
↓  
**Navigation Decision**  
↓  
**Steering + Motor Control**  
↓  
**Vehicle Movement**

<p align="center">
  <img src="images/obstacle-management/obstacle-architecture.png" width="750">
</p>

[View obstacle-management architecture](software/vision.md)

---

## Environmental Perception

NEO uses two complementary methods to understand its surroundings.

### Computer Vision

The Raspberry Pi Camera 3 Wide provides visual information that can be processed to identify:

- obstacle colour
- obstacle position
- relevant regions of the competition field

### Distance Sensing

The ToF sensors provide direct numerical measurements that can help determine:

- front clearance
- left and right proximity
- rear clearance
- distance from surrounding objects or boundaries

The camera provides richer visual information, while the ToF sensors provide direct distance information.

Using both allows the autonomous system to make decisions using more than one type of environmental input.

---

## Computer Vision Pipeline

NEO's computer-vision system runs on the Raspberry Pi 5 using **Python and OpenCV**.

The basic vision pipeline is:

**Capture Camera Frame**  
↓  
**Prepare Image**  
↓  
**Convert Colour Space**  
↓  
**Apply Colour Masks**  
↓  
**Detect Relevant Regions**  
↓  
**Analyse Obstacle Position**  
↓  
**Provide Information to Navigation Logic**

The current camera-processing configuration uses:

| Parameter | Configuration |
|---|---:|
| Resolution | 640 × 480 |
| Frame Rate | Up to approximately 30 FPS |
| Processing Library | OpenCV |
| Main Processing Platform | Raspberry Pi 5 |

<p align="center">
  <img src="images/obstacle-management/camera-output.jpg" width="700">
</p>

[View computer-vision details](software/vision.md)

---

## HSV Colour Detection

NEO's vision system uses the **HSV colour space** to distinguish relevant coloured obstacles.

HSV separates colour information into:

- **Hue** — type of colour
- **Saturation** — intensity of the colour
- **Value** — brightness

The camera frame can be converted from its original colour representation into HSV before predefined ranges are applied.

For the Obstacle Challenge, the main colours of interest are:

- **Red**
- **Green**

The result is a binary mask that isolates image regions matching the required colour range.

This can be represented as:

**Camera Frame**  
↓  
**Convert to HSV**  
↓  
**Apply Red / Green Thresholds**  
↓  
**Generate Colour Mask**

| Original Frame | Processed Mask |
|---|---|
| ![Original Camera Frame](images/obstacle-management/original-frame.jpg) | ![HSV Mask](images/obstacle-management/hsv-mask.jpg) |

[View vision-processing details](software/vision.md)

---

## Contour Detection

Once the colour masks have been generated, OpenCV can identify connected regions within the processed image.

Contours allow the program to locate potential obstacles and obtain information about their position and size.

For a detected region, a bounding rectangle can be represented using:

- **x** — horizontal starting position
- **y** — vertical starting position
- **w** — width
- **h** — height

The approximate centre of the detected object can then be calculated as:

**Centre X = x + w/2**

**Centre Y = y + h/2**

This allows the program to determine where the obstacle appears relative to the centre of the camera frame.

Small detections can be rejected to reduce the effect of image noise.

<p align="center">
  <img src="images/obstacle-management/obstacle-detection.jpg" width="700">
</p>

---

## Obstacle Classification

After a relevant object has been detected, its colour and position can be passed to NEO's autonomous navigation logic.

The processing sequence can be simplified as:

**Detect Object**  
↓  
**Determine Colour**  
↓  
**Determine Position in Frame**  
↓  
**Evaluate Surrounding Distance Information**  
↓  
**Select Navigation Response**

This means the camera is not used simply to determine whether an object exists. It provides information that can influence how NEO responds to the object.

---

## Time-of-Flight Distance Detection

Computer vision is complemented by NEO's **Time-of-Flight sensors**.

These sensors provide numerical distance measurements that can be used to evaluate the vehicle's clearance from nearby objects and boundaries.

NEO currently has distance sensing positioned toward:

- front-centre
- front-left
- front-right
- rear

The sensor system therefore provides information from several directions around the vehicle.

<p align="center">
  <img src="images/obstacle-management/tof-directions.jpg" width="650">
</p>

[View sensor placement and architecture](hardware/sensors.md)

---

## Front Detection

The front-centre sensor is positioned approximately:

- **68 mm above the ground**
- **190 mm from the rear edge**
- along the centreline of NEO

This provides direct forward-distance information.

The measurement can help identify situations where NEO is approaching an object or boundary directly ahead.

---

## Left and Right Detection

Additional sensors are positioned toward the left and right sides of the front section.

### Front-Left Sensor

- Height: approximately **70 mm**
- Position: approximately **170 mm from the rear edge**

### Front-Right Sensor

- Height: approximately **70 mm**
- Position: approximately **170 mm from the rear edge**

These measurements provide additional information about the space around the front of NEO.

Comparing information from different sensor directions can help the navigation system evaluate the robot's position relative to its surroundings.

---

## Rear Detection

NEO also uses a rear-facing distance sensor positioned approximately:

- **65 mm above the ground**
- **45 mm from the rear edge**

The rear measurement provides information about the space behind the vehicle.

This is particularly useful for behaviours involving reverse movement and parking.

---

## Sensor Fusion

The camera and distance sensors provide different types of information.

| Camera | ToF Sensors |
|---|---|
| Detects obstacle colour | Measures distance |
| Determines visual position | Measures clearance |
| Provides a wide view of the environment | Provides measurements in specific directions |
| Processes visual regions | Provides numerical proximity data |

These inputs can be combined by the autonomous software.

For example:

**Camera detects an obstacle**  
↓  
**Vision determines its colour and position**  
↓  
**ToF sensors provide surrounding clearance information**  
↓  
**Navigation logic evaluates the situation**  
↓  
**Steering and propulsion response is generated**

This allows NEO to use the strengths of both sensing methods rather than relying entirely on one.

---

## Steering Correction

Once the autonomous system determines that a steering correction is required, the desired steering output is sent through NEO's steering-control architecture.

**Navigation Calculation**  
↓  
**Desired Steering Output**  
↓  
**PCA9685 PWM Controller**  
↓  
**SG90 Micro Servo**  
↓  
**Front-Wheel Steering**

Because the servo can move through intermediate positions, NEO can make gradual steering corrections rather than using only full-left, straight and full-right commands.

---

## Proportional Steering

NEO's navigation architecture can use proportional steering to vary the strength of a correction according to the size of the detected error.

The basic relationship is:

**Error = Desired Condition − Measured Condition**

The steering correction is then proportional to this error:

**Steering Correction = Kp × Error**

where **Kp** is the proportional gain.

This means:

- small error → small steering correction
- large error → larger steering correction

The resulting output is constrained by the steering limits before being sent to the servo.

[View steering-control details](software/control.md)

---

## Steering Limits

The current observed physical steering range is approximately:

| Direction | Approximate Maximum |
|---|---:|
| Left | ~60° |
| Right | Slightly above 45° |

These values are approximate and will be replaced with measured values after final calibration.

Software steering limits can be used to prevent normal autonomous commands from unnecessarily forcing the steering mechanism to its physical extremes.

---

## Autonomous Decision Making

NEO continuously repeats a perception and control cycle while operating autonomously.

The simplified process is:

**START**  
↓  
**Read Distance Sensors**  
↓  
**Capture and Process Camera Frame**  
↓  
**Evaluate Environment**  
↓  
**Determine Required Behaviour**  
↓  
**Calculate Steering Output**  
↓  
**Calculate Propulsion Output**  
↓  
**Send Commands**  
↓  
**Repeat**

<p align="center">
  <img src="images/obstacle-management/decision-flowchart.png" width="700">
</p>

[View autonomous control logic](software/control.md)

---

## Finite-State Decision Making

NEO's autonomous software uses a **Finite-State Machine (FSM)** approach to separate different driving behaviours.

Rather than treating every situation identically, the software can transition between defined operating states depending on the current sensor and navigation conditions.

The revised Obstacle Challenge software includes states such as:

| State | Function |
|---|---|
| `DRIVE_STRAIGHT` | Normal forward driving |
| `STEER_PROPORTIONAL` | Applies calculated steering correction |
| `EMERGENCY_DODGE` | Performs urgent collision-avoidance behaviour |
| `STOP` | Stops vehicle movement |

A simplified transition can be represented as:

**DRIVE_STRAIGHT**  
↓  
Correction required  
↓  
**STEER_PROPORTIONAL**

or:

**NORMAL NAVIGATION**  
↓  
Critical proximity condition  
↓  
**EMERGENCY_DODGE**

<p align="center">
  <img src="images/obstacle-management/fsm-diagram.png" width="700">
</p>

[View NEO's control architecture](software/control.md)

---

## Emergency Response

Normal autonomous navigation is designed for smooth and controlled movement.

However, if the sensor information indicates an immediate collision risk, emergency behaviour is given priority over normal navigation.

The control priority can be represented as:

1. **Immediate collision response**
2. **Obstacle response**
3. **Navigation correction**
4. **Normal forward driving**

This prevents a normal steering command from taking priority when a more urgent response is required.

---

## Parking Support

NEO's sensing arrangement also provides information that can support parking behaviour.

The combination of front, side and rear distance measurements can help determine:

- available clearance
- proximity to surrounding boundaries
- rear clearance during reverse movement
- when a movement should be adjusted or stopped

The camera can provide additional visual information while the distance sensors provide direct proximity measurements.

Parking behaviour will continue to be refined as the final camera configuration and autonomous software are completed.

---

## Obstacle Management Summary

NEO's obstacle-management architecture combines:

- Raspberry Pi Camera 3 Wide
- Python
- OpenCV
- HSV colour filtering
- contour detection
- red and green obstacle recognition
- Time-of-Flight distance sensing
- proportional steering
- finite-state decision making
- emergency collision response

The complete autonomous process follows a continuous feedback loop:

**SENSE → PROCESS → DECIDE → ACT → SENSE AGAIN**

This allows NEO to continuously update its understanding of the environment and adjust its movement as conditions change.
# Software Key Components

NEO's autonomous control system runs primarily on the **Raspberry Pi 5** and is developed in **Python**.

The software connects NEO's sensing, decision-making, steering and propulsion systems into one autonomous control architecture.

The overall software flow is:

**Camera + ToF Sensors**  
↓  
**Data Acquisition**  
↓  
**Image & Distance Processing**  
↓  
**Autonomous Decision Making**  
↓  
**Steering + Motor Commands**  
↓  
**Vehicle Movement**

<p align="center">
  <img src="images/software/software-architecture.png" width="750">
</p>

[View NEO's source code](software/)

---

## Software Architecture

NEO's software is divided into separate functions rather than placing the complete autonomous system into one large program.

The main software functions are:

| System | Responsibility |
|---|---|
| Camera Processing | Captures and processes visual information |
| ToF Sensor Processing | Reads distance measurements |
| Vision Processing | Detects and locates relevant obstacles |
| Steering Control | Calculates and sends steering commands |
| Motor Control | Controls propulsion |
| Decision-Making Logic | Selects the appropriate autonomous behaviour |
| Configuration | Stores adjustable thresholds and control parameters |

This modular approach makes individual systems easier to modify and troubleshoot as NEO develops.

---

## Programming Language

NEO's main autonomous software is written in **Python**.

Python was selected because of its compatibility with the Raspberry Pi and the libraries required for autonomous robotics.

It provides support for:

- OpenCV computer vision
- camera control
- GPIO interaction
- I²C communication
- sensor processing
- mathematical calculations
- autonomous decision-making

---

## Computer Vision — OpenCV

NEO uses **OpenCV** to process information captured by the Raspberry Pi Camera 3 Wide.

OpenCV is used for operations including:

- colour-space conversion
- HSV filtering
- colour masking
- contour detection
- bounding-box generation
- obstacle-position estimation

The vision pipeline converts raw camera frames into information that can be used by the navigation system.

**Camera Frame**  
↓  
**OpenCV Processing**  
↓  
**Obstacle Detection**  
↓  
**Position + Colour Information**  
↓  
**Navigation Logic**

[View computer-vision details](software/vision.md)

---

## Camera Processing

The current software is designed around the following camera configuration:

| Parameter | Configuration |
|---|---:|
| Resolution | 640 × 480 |
| Frame Rate | Up to approximately 30 FPS |
| Processing Library | OpenCV |
| Camera | Raspberry Pi Camera 3 Wide |

Camera frames are processed continuously while the autonomous program is operating.

The processed information can then be combined with distance measurements before a navigation decision is made.

<p align="center">
  <img src="images/software/vision-output.jpg" width="700">
</p>

---

## ToF Sensor Processing

NEO's Time-of-Flight sensors provide numerical distance measurements from multiple directions around the vehicle.

The software reads these measurements and makes them available to the autonomous control logic.

The current sensing arrangement provides information from:

- front-centre
- front-left
- front-right
- rear

These readings can be used for:

- proximity detection
- wall-distance monitoring
- obstacle avoidance
- emergency response
- reverse movement
- parking

[View sensor architecture](hardware/sensors.md)

---

## Steering Control

NEO's steering is controlled by an **SG90 Micro Servo** through the **PCA9685 PWM controller**.

The software calculates a desired steering correction and converts it into a servo command.

The control path is:

**Navigation Logic**  
↓  
**Steering Calculation**  
↓  
**PCA9685**  
↓  
**SG90 Servo**  
↓  
**Front Wheels**

This allows NEO to use intermediate steering positions rather than relying only on full-left, straight and full-right commands.

[View steering-control details](software/control.md)

---

## Proportional Control

For navigation corrections, NEO can use proportional control.

The basic relationship is:

**Error = Desired Condition − Measured Condition**

The steering correction is then related to the magnitude of this error:

**Steering Correction = Kp × Error**

where **Kp** represents the proportional gain.

This means:

- small error → small correction
- large error → stronger correction

The resulting steering command is constrained to the usable steering range before being sent to the servo.

---

## Motor Control

NEO's propulsion software controls the **LEGO EV3 Medium Motor** through the **TB6612FNG motor driver**.

The motor-control system allows the autonomous program to control the vehicle's propulsion separately from steering.

The control path is:

**Raspberry Pi 5**  
↓  
**Motor Command**  
↓  
**TB6612FNG**  
↓  
**LEGO EV3 Medium Motor**  
↓  
**Differential + Rear Wheels**

Motor behaviour can be adjusted depending on the current autonomous situation.

---

## Autonomous Control Loop

NEO continuously repeats an autonomous control cycle while driving.

The simplified software loop is:

1. Read the distance sensors.
2. Capture the latest camera information.
3. Process the environmental inputs.
4. Determine the current driving situation.
5. Select the appropriate behaviour.
6. Calculate steering output.
7. Calculate motor output.
8. Send commands to the hardware.
9. Repeat.

This continuous loop allows NEO to react as its surroundings change.

<p align="center">
  <img src="images/software/control-loop.png" width="700">
</p>

---

## Finite-State Machine

NEO's revised Obstacle Challenge software uses a **Finite-State Machine (FSM)** to organise autonomous behaviour.

The FSM separates different driving situations into defined states.

The current architecture includes states such as:

| State | Purpose |
|---|---|
| `DRIVE_STRAIGHT` | Normal forward movement |
| `STEER_PROPORTIONAL` | Applies calculated steering corrections |
| `EMERGENCY_DODGE` | Performs urgent collision avoidance |
| `STOP` | Stops vehicle movement |

The state can change when new sensor or camera information indicates that a different behaviour is required.

For example:

**DRIVE_STRAIGHT**  
↓  
Steering correction required  
↓  
**STEER_PROPORTIONAL**

or:

**NORMAL NAVIGATION**  
↓  
Immediate collision risk  
↓  
**EMERGENCY_DODGE**

<p align="center">
  <img src="images/software/fsm.png" width="700">
</p>

[View autonomous control logic](software/control.md)

---

## Control Priority

Some situations require a more urgent response than others.

NEO's autonomous behaviour therefore follows a priority structure:

1. **Immediate collision response**
2. **Obstacle response**
3. **Navigation correction**
4. **Normal driving**

This allows safety-related behaviour to override lower-priority navigation commands when required.

---

## Configurable Parameters

Important control values are kept adjustable so that NEO can be calibrated without redesigning the entire autonomous algorithm.

These parameters can include:

- HSV colour thresholds
- distance thresholds
- steering limits
- servo centre position
- proportional gain
- motor speed
- emergency-distance thresholds
- camera settings

Keeping these values configurable makes calibration and software refinement easier.

---

## BNO055 Development

Earlier development of NEO included software support for the **BNO055 IMU**.

The sensor can provide orientation and heading information that may be used for:

- heading estimation
- turn detection
- orientation correction

The BNO055 is **not currently installed in NEO's present physical configuration**, but its software remains part of the project's development history.

This allows the team to re-evaluate IMU-based navigation later if it provides a meaningful advantage.

---

## Raspberry Pi Environment

NEO's autonomous software runs directly on the Raspberry Pi 5.

The software environment requires the libraries and interfaces used by the camera, sensors and control electronics.

The general setup process is:

1. Prepare the Raspberry Pi operating system.
2. Update the required system packages.
3. Install Python and the required development tools.
4. Install OpenCV and camera dependencies.
5. Install the required sensor and hardware-control libraries.
6. Transfer NEO's source code to the Raspberry Pi.
7. Verify camera communication.
8. Verify sensor communication.
9. Verify steering control.
10. Verify motor control.
11. Run the autonomous program.

[View Raspberry Pi setup instructions](software/setup.md)

---

## Software Development

NEO's software architecture has evolved during development.

Earlier versions explored greater use of IMU-based heading information. As the autonomous system developed, the architecture moved toward a clearer state-based approach combining:

- camera-based obstacle recognition
- Time-of-Flight distance sensing
- proportional steering
- defined autonomous states
- emergency-response behaviour

This allows individual behaviours to be developed and modified without restructuring the entire program.

---

## Software Safety & Reliability

Several software features are intended to improve NEO's reliability during autonomous operation:

- steering limits prevent unnecessary mechanical extremes
- emergency conditions can override normal navigation
- sensor information is updated continuously
- autonomous behaviours are separated into defined states
- thresholds can be calibrated without changing the overall control structure
- camera and distance information provide complementary environmental inputs

---

## Software Summary

NEO's software connects perception, decision-making and vehicle control into one continuous autonomous system.

The architecture can be summarised as:

**PERCEIVE**  
Camera + ToF sensors

↓

**PROCESS**  
OpenCV + distance processing

↓

**DECIDE**  
Autonomous logic + finite-state machine

↓

**CONTROL**  
Steering + motor commands

↓

**ACT**  
SG90 steering + EV3 propulsion

↓

**REPEAT**

This modular architecture provides the foundation for NEO's autonomous navigation in the WRO Future Engineers challenges.

---
# Parts List / Bill of Materials

NEO combines LEGO Technic components with custom 3D-printed parts and purpose-selected electronics.

This hybrid approach allows the mechanical system to remain modular while providing dedicated mounting solutions for NEO's sensors, camera, steering system and electronics.

## Main Components

| Component | Purpose |
|---|---|
| Raspberry Pi 5 | Main controller for autonomous navigation, sensor processing and decision-making |
| Raspberry Pi Camera 3 Wide | Wide-angle computer vision input |
| LEGO EV3 Medium Motor | Rear-wheel propulsion |
| SG90 Micro Servo | Front steering control |
| TB6612FNG Motor Driver | Controls the EV3 drive motor |
| LEGO Differential Gears | Transfers power to the rear wheels while allowing different wheel speeds during turns |
| BNO055 IMU / Gyro Sensor | Orientation and heading sensing during development |
| ToF Laser Ranging Sensor – 7.8 m | Distance measurement |
| VL53L5X ToF Sensor | Multi-zone distance sensing |
| TCA9548A 8-Channel I²C Multiplexer | Manages communication between multiple I²C devices |
| PCA9685 16-Channel PWM Controller | Provides PWM control for the steering system |
| Push Button | Physical control input |
| Bonka 11.1 V 2200 mAh LiPo Battery | Main power source |
| XL4015 5 V 5 A Buck Converter | Regulated power supply for the Raspberry Pi |
| MP1584 3 A DC-DC Buck Converter | Regulated power supply for the motor electronics |
| iMAX B6AC Dual Power 80 W | Balance charger for the LiPo battery |
| LEGO Technic Components | Mechanical chassis, drivetrain and structural elements |
| Custom 3D-Printed PLA Components | Chassis, steering, camera and electronics-support components |

<p align="center">
  <img src="images/parts/labelled-components.jpg" width="750">
</p>

[View detailed parts information](hardware/parts-list.md)

---

# Building Instructions

NEO was designed as a modular vehicle so that its mechanical, electrical and sensing systems can be assembled and accessed independently.

The basic assembly sequence is:

**Chassis**  
↓  
**Drivetrain**  
↓  
**Steering**  
↓  
**Custom 3D-Printed Components**  
↓  
**Electronics**  
↓  
**Power System**  
↓  
**Sensors**  
↓  
**Camera Assembly**

[View all CAD and 3D-printable files](3d-models/README.md)

---

## 1. Prepare the Required Parts

Before assembly, prepare:

- LEGO Technic structural components
- LEGO EV3 Medium Motor
- LEGO differential gears
- wheels and axles
- SG90 Micro Servo
- Raspberry Pi 5
- Raspberry Pi Camera 3 Wide
- distance sensors
- PCA9685
- TCA9548A
- TB6612FNG
- XL4015
- MP1584
- Bonka LiPo battery
- push button
- wiring and connectors
- all required 3D-printed parts

The custom components should be printed before final assembly.

---

## 2. Print the Custom Components

NEO uses **six custom-designed 3D-printed components**.

All parts are manufactured using:

| Parameter | Specification |
|---|---|
| Printer | Bambu Lab A1 |
| Material | PLA |
| Manufacturing Method | FDM 3D Printing |

The six custom components are:

| Part | Purpose |
|---|---|
| FE2026 Custom Chassis | Main custom structural platform |
| Servo Stand | Holds the SG90 steering servo |
| Servo Horn – 13 mm | Transfers servo rotation to the steering mechanism |
| Pi Camera 3 Mount | Holds the Raspberry Pi Camera 3 Wide |
| Camera Stand V2 | Earlier camera-support design |
| Camera Stand V3 | Refined camera-support design |

<p align="center">
  <img src="images/3d-printing/all-parts.jpg" width="750">
</p>

[View and download the 3D-printable files](3d-models/README.md)

---

## 3. Build the Chassis

Assemble NEO's main chassis using the LEGO Technic structure together with the custom chassis component.

The completed vehicle geometry is:

| Parameter | Measurement |
|---|---:|
| Length | 195 mm |
| Width | 111 mm |
| Height | 122 mm |
| Wheelbase | 150 mm |
| Front Track Width | 85 mm |
| Rear Track Width | 85 mm |
| Wheel Radius | 30 mm |

The chassis should remain rigid while maintaining sufficient space for the drivetrain, battery, electronics and sensors.

<p align="center">
  <img src="images/build/chassis.jpg" width="650">
</p>

---

## 4. Assemble the Rear Drivetrain

Install the **LEGO EV3 Medium Motor** and connect it to the LEGO differential.

The drivetrain follows:

**EV3 Medium Motor → Differential → Rear Axle → Rear Wheels**

Ensure that:

- the differential rotates freely
- both rear wheels rotate without obstruction
- axles are correctly supported
- gears remain properly engaged

The differential allows the two driven wheels to rotate at different speeds during cornering.

<p align="center">
  <img src="images/build/drivetrain.jpg" width="650">
</p>

[View drivetrain details](mobility/drivetrain.md)

---

## 5. Assemble the Steering System

Install the **SG90 Micro Servo** using the custom Servo Stand.

Attach the **13 mm Servo Horn** to transfer the servo's rotational movement to the steering mechanism.

The steering assembly should move freely without the wheels or linkage contacting the chassis.

Before autonomous operation, the servo should be centred and the usable steering range checked.

<p align="center">
  <img src="images/build/steering-assembly.jpg" width="650">
</p>

[View steering details](mobility/steering.md)

---

## 6. Install the Electronics

Mount the Raspberry Pi 5 and supporting electronics onto the chassis.

The electronics include:

- Raspberry Pi 5
- PCA9685
- TCA9548A
- TB6612FNG
- XL4015
- MP1584
- sensor connections
- push button

Components should be firmly secured so that vibration and vehicle movement do not cause boards or connectors to shift.

Wiring should also remain clear of:

- wheels
- axles
- gears
- steering linkage

<p align="center">
  <img src="images/build/electronics.jpg" width="700">
</p>

---

## 7. Connect the Power System

NEO uses a **Bonka 11.1 V 2200 mAh LiPo battery** as its main power source.

Two separate buck converters regulate power for the major electrical systems:

**Battery → XL4015 → Raspberry Pi 5**

**Battery → MP1584 → Motor Electronics**

The separate regulated power paths help reduce the effect of motor-related electrical fluctuations on the Raspberry Pi.

The battery should be securely mounted so that it cannot move during acceleration or cornering.

<p align="center">
  <img src="images/build/power-system.jpg" width="650">
</p>

[View electrical system and circuit diagram](hardware/electrical-system.md)

---

## 8. Connect the Control Electronics

Connect the control and sensing components according to NEO's electrical schematic.

The electrical architecture includes connections between:

- Raspberry Pi 5
- TCA9548A
- PCA9685
- TB6612FNG
- SG90 Micro Servo
- LEGO EV3 Medium Motor
- ToF sensors
- power converters
- battery
- push button

<p align="center">
  <img src="images/hardware/circuit-diagram.png" width="800">
</p>

[View full-resolution electrical schematic](hardware/electrical-system.md)

---

## 9. Install the Distance Sensors

Install the distance sensors at their designated positions.

| Sensor | Height from Ground | Position |
|---|---:|---|
| Rear | 65 mm | 45 mm from rear edge |
| Front-Left | 70 mm | 170 mm from rear edge |
| Front-Centre | 68 mm | 190 mm from rear edge |
| Front-Right | 70 mm | 170 mm from rear edge |

The front-centre sensor should remain approximately centred across the width of the vehicle.

Sensors should be firmly mounted so that their orientation does not change during operation.

<p align="center">
  <img src="images/build/sensor-installation.jpg" width="650">
</p>

[View sensor placement](hardware/sensors.md)

---

## 10. Install the Camera Assembly

The Raspberry Pi Camera 3 Wide is mounted using the custom camera-support system.

The assembly consists of:

**Camera Stand → Pi Camera 3 Mount → Raspberry Pi Camera 3 Wide**

The elevated position is intended to provide a clear view of the competition field for computer-vision processing.

The camera connects directly to the Raspberry Pi through the CSI interface.

The final camera height and angle will be documented once the competition configuration is fixed.

<p align="center">
  <img src="images/build/camera-assembly.jpg" width="600">
</p>

[View camera mount files](3d-models/README.md)

---

## 11. Check the Mechanical Assembly

Before powering NEO, verify that:

- the wheels rotate freely
- the drivetrain does not bind
- the differential operates correctly
- the steering linkage moves freely
- the servo is securely mounted
- the battery cannot move
- sensors are securely positioned
- electronics are firmly mounted
- wiring cannot contact moving components

---

## 12. Check the Electrical System

Before connecting the final power supply:

- verify wiring against the electrical schematic
- check the polarity of power connections
- verify the regulated power paths
- inspect connectors for loose wiring
- ensure the Raspberry Pi and motor electronics receive their intended supplies

The LiPo battery is charged using the **iMAX B6AC Dual Power 80 W balance charger**.

---

## 13. Final Assembly

Once the mechanical and electrical systems have been checked, install any remaining covers, supports and mounting components.

The completed NEO should provide clear access to the electronics while keeping the drivetrain, steering, sensors and wiring securely positioned.

<p align="center">
  <img src="images/robot/neo-hero.jpg" width="750">
</p>

[View more assembly pictures](images/build/)

---

## Assembly Summary

NEO's construction combines three different approaches:

**LEGO Technic**  
for modular mechanical construction

↓

**Custom CAD + 3D Printing**  
for purpose-built structural components

↓

**Raspberry Pi Electronics**  
for sensing, processing and autonomous control

This hybrid architecture allows individual parts of NEO to be modified without requiring the entire vehicle to be rebuilt.

---
# Engineering Development

NEO was developed as an iterative engineering project. Rather than treating the mechanical, electrical and software systems independently, each part of the robot was designed around how it would interact with the complete autonomous vehicle.

Our development process follows a continuous cycle:

**Identify Requirement**  
↓  
**Design**  
↓  
**Build / Program**  
↓  
**Evaluate**  
↓  
**Refine**  
↓  
**Repeat**

This approach allows individual systems to evolve without requiring the entire robot to be redesigned.

---

## Mechanical Development

NEO combines **LEGO Technic** with custom-designed 3D-printed components.

LEGO Technic provides a modular platform for the drivetrain, differential, axles and structural elements, while CAD and 3D printing allow us to create parts specifically around NEO's geometry.

The custom parts currently include:

- FE2026 Custom Chassis
- Servo Stand
- Servo Horn – 13 mm
- Pi Camera 3 Mount
- Camera Stand V2
- Camera Stand V3

All custom components are printed in **PLA using a Bambu Lab A1**.

[View all custom 3D-printed parts](3d-models/README.md)

---

## Camera Mount Iteration

The camera-support structure is one example of NEO's iterative design process.

Two versions of the camera stand were produced:

**Camera Stand V2 → Camera Stand V3**

Rather than redesigning the entire vehicle when the camera-support geometry was refined, only the relevant custom component needed to be modified and reprinted.

| Camera Stand V2 | Camera Stand V3 |
|---|---|
| ![Camera Stand V2](images/3d-printing/camera-stand-v2.png) | ![Camera Stand V3](images/3d-printing/camera-stand-v3.png) |

This modular approach makes mechanical changes faster and allows individual components to evolve independently.

---

## Software Development

NEO's software architecture has also evolved during development.

Earlier versions explored the use of the **BNO055 IMU** for heading and orientation information.

As development continued, the software moved toward an architecture combining:

- camera-based obstacle recognition
- Time-of-Flight distance sensing
- proportional steering
- finite-state decision making
- emergency-response behaviour

The BNO055 is not currently installed in NEO's present physical configuration, but its software remains part of the development history.

This reflects an important part of our engineering process: a component does not need to remain in the final configuration simply because it was explored during development.

---

## Design Trade-Offs

Many of NEO's design decisions required balancing different engineering priorities.

| Design Decision | Advantage | Trade-Off |
|---|---|---|
| Raspberry Pi 5 | High processing capability for computer vision | Higher power requirement |
| Pi Camera 3 Wide | Large field of view | Wide-angle image distortion near edges |
| Multiple ToF sensors | Distance information from several directions | Additional wiring and communication complexity |
| Rear-wheel drive | Separates propulsion from steering | Requires reliable rear-wheel traction |
| LEGO differential | Allows smoother cornering | Adds drivetrain components |
| SG90 Micro Servo | Compact and lightweight | Lower torque than larger servos |
| LEGO + 3D printing | Highly modular and adaptable | Requires integration between two construction systems |
| PLA custom parts | Lightweight and easy to manufacture | Less heat-resistant than some engineering materials |
| Separate buck converters | Better separation of power systems | Additional electronics and wiring |
| Modular electronics | Easier to replace and troubleshoot | Requires more space than an integrated PCB |
| Fixed HSV ranges | Simple and computationally efficient | Can be affected by changing lighting conditions |

These trade-offs helped us evaluate components based on NEO's actual requirements rather than simply selecting the most powerful or complex option.

---

# Possible Improvements

Although NEO's current architecture provides the foundation required for autonomous navigation, several areas could be developed further.

---

## Camera Integration and Calibration

The Raspberry Pi Camera 3 Wide will require final calibration once its competition mounting position is fixed.

The main parameters to optimise are:

- camera height
- camera angle
- field of view
- visibility of nearby obstacles
- visibility during turns
- image stability

Once the final position is selected, the dimensions and angle can be added to the technical documentation.

---

## Steering Calibration

NEO's current observed physical steering range is approximately:

- **Left: ~60°**
- **Right: slightly above 45°**

These values are currently estimates.

A more precise calibration could measure:

- exact maximum left angle
- exact maximum right angle
- true centre position
- steering angle relative to servo command
- minimum turning radius

This would provide a more accurate relationship between software commands and physical wheel movement.

---

## Steering Geometry Refinement

The steering mechanism could be refined further to improve repeatability and reduce mechanical play.

Possible improvements include:

- reducing linkage backlash
- improving left/right steering symmetry
- optimising linkage geometry
- increasing rigidity around the servo
- refining the servo horn geometry

More repeatable mechanical steering would also improve the consistency of software-based steering corrections.

---

## Sensor Position Optimisation

The current distance-sensor positions provide coverage around the front and rear of NEO.

Further calibration could investigate changes to:

- sensor height
- sensor angle
- distance from the chassis edge
- left/right positioning

The objective would be to maximise useful environmental information while reducing unwanted measurements from the floor, wheels or parts of NEO itself.

---

## Dynamic Vision Calibration

NEO currently uses HSV colour filtering for red and green obstacle recognition.

Fixed HSV ranges are efficient, but lighting changes can alter the appearance of colours within the camera image.

A future version could investigate adaptive colour thresholds or other calibration methods to improve recognition under different lighting conditions.

This could improve robustness when:

- lighting intensity changes
- shadows appear
- camera exposure changes
- obstacles appear brighter or darker in different areas of the field

---

## Improved Vision Filtering

Additional image filtering could help reduce false detections.

Possible improvements include:

- stronger contour filtering
- minimum object-area requirements
- position-based filtering
- noise reduction
- confirmation across consecutive frames

Confirming a detection across multiple frames could help prevent the autonomous system from reacting to brief visual noise.

---

## Adaptive Driving Speed

NEO could eventually vary its speed according to the current driving situation.

For example, the vehicle could operate faster when:

- the path ahead is clear
- steering correction is small
- no obstacle is nearby

It could reduce speed when:

- approaching an obstacle
- performing a sharp turn
- entering a parking manoeuvre
- a large steering correction is required

This would allow NEO to balance speed and precision dynamically.

---

## Improved Parking

The combination of front, side and rear distance sensing provides a foundation for more precise parking behaviour.

Future software development could make greater use of the rear sensor to determine:

- rear clearance
- position during reverse movement
- when reverse movement should stop
- final parking position

The camera and distance sensors could then work together during the complete parking manoeuvre.

---

## Cable Management

As NEO's electronics develop, cable management can be improved further.

Future versions could incorporate custom 3D-printed cable guides or clips directly into the chassis and electronics-support structures.

This could:

- reduce loose wiring
- protect connectors
- keep wires away from moving components
- simplify maintenance
- improve access to the electronics

---

## Custom PCB

NEO currently uses separate electronic modules for motor control, PWM control, I²C management and voltage regulation.

A future version could integrate some of these connections into a custom PCB.

Potential advantages include:

- reduced wiring
- fewer connectors
- smaller electronics footprint
- faster assembly
- cleaner internal organisation

However, the current modular architecture remains useful during development because individual boards can be replaced or modified easily.

---

## Weight and Centre of Gravity

NEO's current weight is estimated at approximately **1.5 kg**.

Once the final hardware configuration is complete, the exact mass can be measured and the distribution of heavier components can be evaluated.

Particular attention can be given to the placement of:

- battery
- Raspberry Pi
- electronics
- camera structure

Optimising the centre of gravity could improve stability, cornering and rear-wheel traction.

---

## Data Logging

A future software improvement could record data automatically during autonomous runs.

Useful information could include:

- sensor readings
- detected obstacle colour
- obstacle position
- steering command
- motor command
- current FSM state
- emergency events
- timestamps

This would allow the team to analyse what NEO detected and why a particular decision was made during a run.

---

## Future IMU Integration

The BNO055 IMU was explored during development but is not currently installed.

Future testing could determine whether reintroducing orientation sensing provides a meaningful improvement.

Potential uses include:

- heading estimation
- turn-angle measurement
- orientation correction
- additional navigation redundancy

The IMU would only be reintroduced if it provides a clear advantage over the existing camera and ToF-based architecture.

---

## Future Development

The next stages of NEO's development will focus on:

1. Final camera installation and calibration
2. Precise steering measurement
3. Sensor-position optimisation
4. Vision calibration
5. Autonomous navigation refinement
6. Parking refinement
7. Final weight measurement
8. Performance testing
9. Reliability testing
10. Final competition configuration

As NEO develops, the repository will continue to document changes to its mechanical, electrical and software systems.

---

# Project Resources

Detailed engineering information and project files are available throughout this repository.

| Resource | Link |
|---|---|
| Mobility Calculations | [View Calculations](mobility/calculations.md) |
| Drivetrain | [View Drivetrain](mobility/drivetrain.md) |
| Steering System | [View Steering](mobility/steering.md) |
| Hardware Architecture | [View Hardware Architecture](hardware/hardware-architecture.md) |
| Electrical System | [View Electrical System](hardware/electrical-system.md) |
| Sensors | [View Sensors](hardware/sensors.md) |
| Parts List | [View Parts List](hardware/parts-list.md) |
| 3D Models & STL Files | [View 3D Models](3d-models/README.md) |
| Computer Vision | [View Vision System](software/vision.md) |
| Autonomous Control | [View Control System](software/control.md) |
| Raspberry Pi Setup | [View Setup Instructions](software/setup.md) |
| Source Code | [View Software](software/) |
| Robot Images | [View Images](images/robot/) |

---

# Team Astra

**WRO Future Engineers 2026**

**Robot: NEO**

**A STAR IN MOTION**
