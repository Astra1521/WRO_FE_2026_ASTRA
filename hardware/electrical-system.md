# NEO — Electrical & Power System

NEO's electrical system distributes power from a single **Bonka 11.1 V 2200 mAh LiPo battery** to the computing, sensing and motor-control systems.

Separate voltage-regulation paths are used for the Raspberry Pi and motor electronics to improve power stability and reduce interference between high-current motor loads and the main controller.

---

## Electrical Architecture

The main electrical architecture consists of:

**Bonka 11.1 V 2200 mAh LiPo Battery**  
↓  
**Power Distribution**  
↓  
**Voltage Regulation**  
↓  
**Computing + Sensors + Control Electronics + Actuators**

The two primary regulated power paths are:

### Raspberry Pi Power

**11.1 V LiPo Battery**  
↓  
**XL4015 5 V 5 A Buck Converter**  
↓  
**Raspberry Pi 5**

### Motor Electronics Power

**11.1 V LiPo Battery**  
↓  
**MP1584 3 A Buck Converter**  
↓  
**Motor Electronics**

<!-- UPLOAD HERE: Power architecture/block diagram -->

---

## Main Electrical Components

| Component | Electrical Function |
|---|---|
| Bonka 11.1 V 2200 mAh LiPo | Main power source |
| XL4015 5 V 5 A Buck Converter | Regulates power for Raspberry Pi 5 |
| MP1584 3 A Buck Converter | Regulates power for motor electronics |
| Raspberry Pi 5 | Main controller |
| TB6612FNG | Drive-motor control |
| PCA9685 | PWM control for steering |
| TCA9548A | I²C communication management |
| SG90 Micro Servo | Steering actuator |
| LEGO EV3 Medium Motor | Drive actuator |
| ToF Sensors | Distance sensing |
| Raspberry Pi Camera 3 Wide | Visual sensing |
| Push Button | Physical control input |

---

## Main Power Source

NEO uses a **Bonka 11.1 V 2200 mAh LiPo battery**.

The LiPo battery provides a high energy density while remaining compact enough to fit within NEO's chassis.

### Battery Specification

| Parameter | Value |
|---|---:|
| Nominal Voltage | 11.1 V |
| Capacity | 2200 mAh |
| Capacity in Ah | 2.2 Ah |
| Nominal Energy | ~24.4 Wh |

<!-- UPLOAD HERE: Photo of Bonka LiPo installed securely in NEO -->

---

## Battery Energy Calculation

Battery energy can be estimated using:

**Energy = Voltage × Capacity**

Therefore:

**Energy = 11.1 V × 2.2 Ah**

**Energy ≈ 24.42 Wh**

NEO therefore has approximately:

**24.4 Wh**

of nominal battery energy.

This value represents stored energy and should not be treated as an exact runtime measurement.

Actual runtime depends on factors including:

- Raspberry Pi processing load
- motor load
- motor speed
- steering activity
- sensor usage
- converter efficiency
- drivetrain resistance

---

## Why We Use Separate Power Regulation

The Raspberry Pi and propulsion electronics have different electrical requirements.

Motor operation can also introduce changes in current demand that may affect the stability of sensitive computing electronics.

NEO therefore uses separate buck converters for its major power systems.

This provides:

- dedicated voltage regulation
- improved Raspberry Pi supply stability
- reduced interaction between computing and motor loads
- easier electrical troubleshooting
- modular power distribution

---

## XL4015 — Raspberry Pi Power

The **XL4015 5 V 5 A buck converter** is used to regulate power for the Raspberry Pi 5.

The power path is:

**11.1 V Battery**  
↓  
**XL4015**  
↓  
**Regulated 5 V Supply**  
↓  
**Raspberry Pi 5**

The Raspberry Pi is one of NEO's most important electrical components because it controls the autonomous system.

Providing it with a dedicated regulated supply helps maintain reliable:

- camera operation
- sensor communication
- computer-vision processing
- autonomous decision-making

<!-- UPLOAD HERE: Photo of XL4015 installed on NEO -->

---

## MP1584 — Motor Electronics Power

The **MP1584 3 A DC-DC buck converter** is used for the motor-electronics power system.

The power path is:

**11.1 V Battery**  
↓  
**MP1584**  
↓  
**Motor Electronics**

Separating this power path from the Raspberry Pi supply helps prevent changes in motor load from directly affecting the main controller's regulated supply.

<!-- UPLOAD HERE: Photo of MP1584 installed on NEO -->

---

## Motor Driver — TB6612FNG

The LEGO EV3 Medium Motor cannot be powered directly from the Raspberry Pi.

NEO therefore uses a **TB6612FNG motor driver** between the controller and the drive motor.

The control path is:

**Raspberry Pi 5**  
↓  
**TB6612FNG**  
↓  
**LEGO EV3 Medium Motor**

The TB6612FNG allows the autonomous control system to manage motor operation while the motor receives power through the appropriate electrical path.

The driver provides control over:

- motor direction
- motor speed
- motor activation

[View NEO's drivetrain](../mobility/drivetrain.md)

---

## Steering Electronics

NEO's SG90 steering servo is controlled through the **PCA9685 PWM controller**.

The control path is:

**Raspberry Pi 5**  
↓  
**PCA9685**  
↓  
**SG90 Micro Servo**  
↓  
**Steering Mechanism**

The PCA9685 generates the PWM signal used to determine servo position.

This allows NEO to generate intermediate steering positions for autonomous corrections.

[View NEO's steering system](../mobility/steering.md)

---

## I²C Architecture

NEO uses I²C communication for several electronic devices.

The **TCA9548A 8-channel I²C multiplexer** allows multiple I²C devices to be organised across separate selectable channels.

The basic architecture is:

**Raspberry Pi 5**  
↓  
**I²C**  
↓  
**TCA9548A**  
↓  
**Connected I²C Devices**

This is particularly useful when multiple sensors use identical or conflicting I²C addresses.

[View NEO's sensor architecture](sensors.md)

---

## Camera Connection

The **Raspberry Pi Camera 3 Wide** connects directly to the Raspberry Pi through the CSI camera interface.

This means the camera does not require a separate USB connection.

The camera provides visual data directly to the Raspberry Pi for computer-vision processing.

**Pi Camera 3 Wide**  
↓  
**CSI Interface**  
↓  
**Raspberry Pi 5**

[View NEO's computer-vision system](../software/vision.md)

---

## Electrical Schematic

NEO's circuit diagram documents the electrical connections between the main computing, sensing, control and power components.

The schematic includes:

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
- signal connections
- power connections

<!-- UPLOAD HERE: Export FE2026_Schematic as a PNG and place it below -->

<p align="center">
  <img src="../images/hardware/circuit-diagram.png" width="900">
</p>

<!-- UPLOAD HERE: Original FE2026_Schematic.pdf into the hardware folder -->

[Open Full Electrical Schematic](FE2026_Schematic.pdf)

---

## Battery Charging

NEO's LiPo battery is charged using an **iMAX B6AC Dual Power 80 W balance charger**.

A balance charger is used so that the cells within the LiPo battery can be charged appropriately.

Before testing, the battery condition is checked and the pack is securely installed within the chassis.

<!-- UPLOAD HERE: Photo of iMAX B6AC charger -->

---

## Physical Control

NEO includes a **push button** as a physical control input.

This provides a convenient way to interact with the robot during testing and competition operation without requiring direct access to the Raspberry Pi interface.

<!-- UPLOAD HERE: Close-up showing the push-button position on NEO -->

---

## Electrical Safety & Reliability

Several measures are used to improve the reliability of NEO's electrical system.

### Separate Power Regulation

The Raspberry Pi and motor electronics use separate buck converters.

### Secure Battery Mounting

The LiPo battery is secured within the chassis to prevent movement while NEO is driving.

### Secured Electronics

Electronic modules are mounted so that normal vehicle vibration does not cause excessive movement or accidental disconnection.

### Wiring Management

Wiring is routed away from:

- wheels
- gears
- axles
- steering linkage

This reduces the chance of wires interfering with moving mechanical components.

### Battery Checks

Battery voltage and condition are checked before operation to avoid excessive discharge.

### Balance Charging

The battery is charged using the iMAX B6AC balance charger.

---

## Electrical System Summary

NEO's electrical system is designed around a simple principle:

**One Main Battery → Separate Regulated Power Paths → Stable Computing and Motor Control**

The **11.1 V LiPo battery** provides the main energy source.

The **XL4015** regulates power for the Raspberry Pi, while the **MP1584** provides a separate regulated path for the motor electronics.

The Raspberry Pi then communicates with NEO's sensors and control electronics to connect perception, decision-making and physical movement.

---

[← Back to Main README](../README.md)
