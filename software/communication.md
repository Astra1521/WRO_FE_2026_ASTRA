# NEO — Communication System

NEO's electronic systems must exchange information reliably so that sensor data, processing and physical movement can operate together.

The **Raspberry Pi 5** acts as NEO's main processing computer, while the supporting electronics handle sensing, steering and motor control.

---

## Communication Architecture

NEO's communication structure can be represented as:

```text
                  Pi Camera 3 Wide
                         │
                        CSI
                         │
                         ↓
ToF Sensors ─────→ Raspberry Pi 5
                         │
                         │
              Control / Processing
                         │
             ┌───────────┴───────────┐
             ↓                       ↓
         PCA9685                 TB6612FNG
             ↓                       ↓
        SG90 Servo            EV3 Medium Motor
```

<!-- UPLOAD HERE: Final communication architecture diagram -->

---

# Raspberry Pi 5

The Raspberry Pi 5 is the main processing platform used by NEO.

It is responsible for coordinating information from the robot's sensing systems and generating the control decisions required for autonomous movement.

The Raspberry Pi handles:

- computer vision
- sensor information
- autonomous navigation logic
- steering commands
- propulsion commands

---

# Camera Communication

The **Raspberry Pi Camera 3 Wide** connects directly to the Raspberry Pi through the camera interface.

```text
Pi Camera 3 Wide
       ↓
      CSI
       ↓
Raspberry Pi 5
```

This provides the Raspberry Pi with image frames for OpenCV-based visual processing.

[View NEO's computer-vision system](vision.md)

---

# I2C Communication

Several of NEO's electronic components use the **I2C communication protocol**.

I2C allows multiple compatible devices to communicate using a shared communication bus.

NEO includes a **TCA9548A 8-channel I2C multiplexer**, which helps manage multiple I2C devices within the system.

```text
Raspberry Pi 5
      ↓
     I2C
      ↓
   TCA9548A
   Multiplexer
      ↓
 Multiple I2C Devices
```

This is particularly useful when several sensors need to communicate through the same controller.

---

# Time-of-Flight Sensor Communication

NEO uses **VL53L5X Time-of-Flight laser-ranging sensors** for distance measurements.

The sensors provide distance information that can be used by the autonomous-navigation software.

A simplified communication path is:

```text
VL53L5X ToF Sensors
        ↓
      I2C
        ↓
     TCA9548A
        ↓
  Raspberry Pi 5
```

The Raspberry Pi can then combine these distance readings with information obtained from the camera.

[View NEO's sensor system](../hardware/sensors.md)

---

# PCA9685 Communication

NEO uses a **PCA9685 16-channel PWM controller** as part of the steering-control system.

The Raspberry Pi communicates with the PCA9685, which generates the PWM signal required by the SG90 steering servo.

```text
Raspberry Pi 5
      ↓
     I2C
      ↓
    PCA9685
      ↓
     PWM
      ↓
 SG90 Micro Servo
```

This separates the generation of the servo-control signal from the main processing performed by the Raspberry Pi.

---

# Steering Communication

The complete steering-command path can be represented as:

```text
Sensor + Camera Information
           ↓
     Raspberry Pi 5
           ↓
    Steering Decision
           ↓
        PCA9685
           ↓
      PWM Signal
           ↓
     SG90 Micro Servo
           ↓
     Front Steering
```

[View NEO's steering system](../mobility/steering.md)

---

# Motor Communication

NEO's propulsion system uses a **TB6612FNG motor driver** and a **LEGO EV3 Medium Motor**.

The motor driver acts as the interface between the control electronics and the propulsion motor.

```text
Raspberry Pi 5
      ↓
 Motor Command
      ↓
  TB6612FNG
      ↓
EV3 Medium Motor
      ↓
 Differential
      ↓
 Rear Wheels
```

The motor driver allows the low-power control system to command the motor without powering it directly from the Raspberry Pi.

[View NEO's drivetrain](../mobility/drivetrain.md)

---

# Power and Communication Separation

NEO uses separate voltage regulation for different parts of the electronic system.

### Motor Power

An **MP1584 DC-DC 3A buck converter** is used in the motor-power system.

### Raspberry Pi Power

An **XL4015 5V 5A converter** is used to provide suitable power for the Raspberry Pi.

The use of dedicated power-conversion hardware helps ensure that the computing and motor systems receive the voltages required for their respective operation.

```text
             Bonka LiPo Battery
                    ↓
          Power Distribution
             ↙             ↘
        MP1584            XL4015
           ↓                 ↓
     Motor System      Raspberry Pi 5
```

[View NEO's electrical system](../hardware/electrical.md)

---

# Communication During Autonomous Operation

During autonomous operation, communication occurs continuously.

A simplified cycle is:

```text
1. Sensors collect information
            ↓
2. Camera captures visual data
            ↓
3. Raspberry Pi processes inputs
            ↓
4. Navigation decision is calculated
            ↓
5. Steering and motor commands are generated
            ↓
6. NEO moves
            ↓
7. New information is collected
            ↓
          REPEAT
```

This allows NEO to continuously update its behaviour as the environment changes.

---

# Communication Reliability

Reliable communication is important because delays or incorrect data can affect autonomous driving.

During testing, Team Astra checks:

- whether sensors are detected correctly
- whether sensor readings update consistently
- whether the camera provides usable frames
- whether steering commands reach the servo correctly
- whether motor commands produce the expected movement
- whether components remain responsive during a complete run

<!-- UPLOAD HERE: Photo of electronics/wiring during testing -->

---

# Communication Testing

Individual communication systems can be tested before the entire autonomous program is run.

```text
Test Camera
     ↓
Test ToF Sensors
     ↓
Test PCA9685 + Servo
     ↓
Test Motor Driver + Motor
     ↓
Combine Systems
     ↓
Autonomous Test
```

Testing components individually makes communication problems easier to identify.

---

# Communication Summary

NEO uses several communication methods to connect its electronic systems:

| Connection | Purpose |
|---|---|
| CSI | Pi Camera 3 Wide → Raspberry Pi 5 |
| I2C | Communication with compatible control and sensing electronics |
| TCA9548A | Management of multiple I2C devices |
| PCA9685 / PWM | Steering-servo control |
| TB6612FNG | Interface between control system and drive motor |

Together, these connections allow information to move through the robot from **sensing → processing → decision-making → physical movement**.

---

[← Back to Main README](../README.md)
