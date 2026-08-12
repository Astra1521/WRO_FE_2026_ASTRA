# NEO — Parts List / Bill of Materials

This page documents the main mechanical, electronic, sensing, power and custom-manufactured components used to build NEO.

NEO combines **LEGO Technic components**, **Raspberry Pi-based electronics** and **custom 3D-printed PLA parts**.

---

# Main Electronics

| Component | Quantity | Purpose |
|---|---:|---|
| Raspberry Pi 5 | 1 | Main controller for autonomous navigation and processing |
| Raspberry Pi Camera 3 Wide | 1 | Computer-vision input |
| TB6612FNG Motor Driver | 1 | Controls the LEGO EV3 Medium Motor |
| PCA9685 16-Channel PWM Controller | 1 | Generates PWM signals for steering control |
| TCA9548A 8-Channel I²C Multiplexer | 1 | Manages communication between multiple I²C devices |
| Push Button | 1 | Physical control input |

<!-- UPLOAD HERE: Photo showing NEO's main electronic components -->

---

# Motors & Drivetrain

| Component | Quantity | Purpose |
|---|---:|---|
| LEGO EV3 Medium Motor | 1 | Rear-wheel propulsion |
| SG90 Micro Servo | 1 | Front-wheel steering |
| LEGO Differential | 1 | Allows the rear wheels to rotate at different speeds while cornering |
| LEGO Technic Gears | As required | Transfers mechanical power through the drivetrain |
| LEGO Technic Axles | As required | Transfers rotation through the drivetrain |
| Wheels | 4 | Vehicle movement and traction |

NEO uses a **rear-wheel-drive configuration**, with the EV3 Medium Motor driving the rear axle through the LEGO differential.

[View NEO's drivetrain](../mobility/drivetrain.md)

[View NEO's steering system](../mobility/steering.md)

---

# Sensors

| Component | Quantity | Purpose |
|---|---:|---|
| VL53L5X ToF Sensor | As installed | Multi-zone distance measurement |
| ToF Laser Ranging Sensors | As installed | Front, side and rear proximity measurement |
| BNO055 IMU | Development component | Orientation and heading sensing during development |

The BNO055 was explored during development but is **not currently installed in NEO's present physical configuration**.

[View NEO's sensor system](sensors.md)

---

# Power System

| Component | Quantity | Purpose |
|---|---:|---|
| Bonka 11.1 V 2200 mAh LiPo Battery | 1 | Main power source |
| XL4015 5 V 5 A Buck Converter | 1 | Regulates power for the Raspberry Pi 5 |
| MP1584 3 A DC-DC Buck Converter | 1 | Regulates power for the motor electronics |
| iMAX B6AC Dual Power 80 W | 1 | LiPo balance charger |

The battery has a nominal energy capacity of approximately:

**11.1 V × 2.2 Ah = 24.4 Wh**

[View NEO's electrical system](electrical-system.md)

---

# Mechanical Construction

| Component | Quantity | Purpose |
|---|---:|---|
| LEGO Technic Beams & Structural Components | As required | Main mechanical construction |
| LEGO Technic Connectors & Pins | As required | Structural connections |
| LEGO Differential Gears | As required | Rear differential assembly |
| LEGO Axles | As required | Drivetrain and wheel connections |
| Custom 3D-Printed Components | 6 | Chassis, steering and camera-support structures |

The combination of LEGO Technic and custom 3D printing allows NEO to remain modular while providing purpose-built components where standard LEGO geometry is not sufficient.

---

# Custom 3D-Printed Parts

NEO uses **six custom-designed components**, manufactured in PLA using a **Bambu Lab A1**.

| Part | Purpose |
|---|---|
| FE2026 Custom Chassis | Structural platform for integrating NEO's mechanical and electronic systems |
| Servo Stand | Securely positions the SG90 steering servo |
| Servo Horn – 13 mm | Transfers servo rotation to the steering mechanism |
| Pi Camera 3 Mount | Holds the Raspberry Pi Camera 3 Wide |
| Camera Stand V2 | Earlier version of the elevated camera-support structure |
| Camera Stand V3 | Refined version of the camera-support structure |

### Manufacturing Information

| Parameter | Specification |
|---|---|
| Printer | Bambu Lab A1 |
| Material | PLA |
| Process | FDM 3D Printing |
| Number of Custom Parts | 6 |

<!-- UPLOAD HERE: Photograph of all six printed components -->

[View all 3D models and STL files](../3d-models/README.md)

---

# Component Selection

The components used in NEO were selected according to the requirements of an autonomous competition vehicle.

| Component | Why We Chose It |
|---|---|
| Raspberry Pi 5 | Provides the processing capability required for computer vision and autonomous navigation |
| Pi Camera 3 Wide | Wide field of view provides greater visual coverage of the competition field |
| LEGO EV3 Medium Motor | Compact and integrates easily with the LEGO drivetrain |
| SG90 Micro Servo | Compact and lightweight solution for controlled steering |
| TB6612FNG | Provides an interface between the controller and drive motor |
| LEGO Differential | Allows the driven rear wheels to rotate at different speeds during turns |
| VL53L5X / ToF Sensors | Provide direct distance information for navigation and parking |
| TCA9548A | Allows multiple I²C devices to be organised across selectable channels |
| PCA9685 | Provides dedicated PWM generation for servo control |
| XL4015 | Provides the regulated supply required by the Raspberry Pi |
| MP1584 | Provides a separate regulated supply for motor electronics |
| 11.1 V 2200 mAh LiPo | Compact main energy source for the vehicle |
| LEGO Technic | Provides modular mechanical construction |
| Custom PLA Parts | Allow components to be designed specifically around NEO's geometry |

---

# Component Integration

The major components interact through the following architecture:

**SENSING**

Pi Camera 3 Wide + ToF Sensors

↓

**PROCESSING**

Raspberry Pi 5

↓

**CONTROL**

PCA9685 + TB6612FNG

↓

**ACTUATION**

SG90 Servo + LEGO EV3 Medium Motor

↓

**MECHANICAL OUTPUT**

Front Steering + Rear-Wheel Drive

The complete system is powered by the **11.1 V LiPo battery** through separate regulated power paths.

<!-- UPLOAD HERE: Labelled photograph of NEO identifying the major components -->

---

# Parts List Summary

NEO's construction combines four main groups of components:

1. **Mechanical** — LEGO Technic, drivetrain, differential and wheels
2. **Electronic** — Raspberry Pi 5, motor driver, PWM controller and I²C multiplexer
3. **Sensing** — Pi Camera 3 Wide and Time-of-Flight sensors
4. **Custom Manufactured** — six 3D-printed PLA components

This modular approach allows individual systems to be replaced, repositioned and refined as NEO develops.

---

[← Back to Main README](../README.md)
