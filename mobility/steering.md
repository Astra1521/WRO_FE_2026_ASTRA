# NEO — Steering System

NEO uses **front-wheel steering** controlled by an **SG90 Micro Servo**.

The steering system is mechanically independent from the rear-wheel drivetrain, allowing NEO to control its direction while the rear axle provides propulsion.

---

## Steering Architecture

NEO's steering-control path is:

**Raspberry Pi 5**  
↓  
**PCA9685 PWM Controller**  
↓  
**SG90 Micro Servo**  
↓  
**Servo Horn**  
↓  
**Steering Mechanism**  
↓  
**Front Wheels**

This converts steering decisions made by the autonomous software into physical movement of the front wheels.

<!-- UPLOAD HERE: Clear photo of NEO's complete front steering system -->

---

## SG90 Micro Servo

An **SG90 Micro Servo** controls NEO's steering.

The servo was selected because it is:

- compact
- lightweight
- easy to integrate into the chassis
- capable of controlled angular positioning
- suitable for NEO's small steering mechanism

Unlike a standard DC motor, a servo can be commanded to specific positions. This allows NEO to make intermediate steering corrections rather than relying only on full-left, straight and full-right movement.

<!-- UPLOAD HERE: Close-up photo of the SG90 installed in NEO -->

---

## Custom Servo Mounting

Two custom 3D-printed components are used in NEO's steering assembly:

### Servo Stand

The **Servo Stand** securely positions the SG90 Micro Servo within the vehicle.

A dedicated mount reduces unwanted servo movement and allows the steering system to remain aligned with the chassis.

### 13 mm Servo Horn

The custom **13 mm Servo Horn** connects the servo output to the steering mechanism.

Its purpose is to transfer the rotational movement of the servo into movement of the steering linkage.

| Servo Stand | 13 mm Servo Horn |
|---|---|
| ![Servo Stand](../images/3d-printing/servo-stand.png) | ![13 mm Servo Horn](../images/3d-printing/servo-horn.png) |

[View the 3D-printable steering components](../3d-models/README.md)

---

## Front-Wheel Steering

NEO's rear wheels are responsible for propulsion, while its front wheels determine direction.

When the servo rotates:

1. The servo horn moves.
2. The steering linkage transfers this movement.
3. The front wheels change angle.
4. NEO changes direction.

This separation between propulsion and steering keeps the mechanical system modular and allows each system to be adjusted independently.

<!-- UPLOAD HERE: Top-view photo showing the front wheels and steering linkage -->

---

## Steering Range

The current observed maximum steering range is approximately:

| Direction | Approximate Maximum |
|---|---:|
| Left | ~60° |
| Right | Slightly above 45° |

These values were visually estimated during development and are **not final measured values**.

The exact left and right steering angles will be updated after final calibration.

<!-- OPTIONAL UPLOAD HERE: Photo showing maximum left steering -->

<!-- OPTIONAL UPLOAD HERE: Photo showing maximum right steering -->

---

## Steering Control

The autonomous software calculates the steering correction required from the current sensor and camera information.

The command is then sent through the PCA9685 to the SG90 servo.

**Environmental Input**  
↓  
**Navigation Algorithm**  
↓  
**Desired Steering Correction**  
↓  
**PCA9685**  
↓  
**SG90 Servo**  
↓  
**Front-Wheel Angle**

The use of PWM control allows the servo to move to intermediate positions for smoother autonomous corrections.

[View NEO's autonomous control system](../software/control.md)

---

## Proportional Steering

NEO can use proportional steering so that the size of the steering correction depends on the size of the detected error.

The basic relationship is:

**Error = Desired Condition − Measured Condition**

The correction can then be represented as:

**Steering Correction = Kp × Error**

where **Kp** is the proportional gain.

This means:

- small error → small steering correction
- large error → larger steering correction

This is useful for autonomous navigation because NEO does not always need to make a maximum steering movement.

---

## Steering Limits

The calculated steering output is constrained before being sent to the servo.

Software limits help prevent normal autonomous commands from unnecessarily forcing the steering mechanism beyond its usable range.

This protects the steering assembly and provides more predictable control.

---

## Steering Geometry

NEO's steering geometry is influenced by its overall dimensions.

| Parameter | Measurement |
|---|---:|
| Wheelbase | 150 mm |
| Front Track Width | 85 mm |
| Approximate Maximum Left Steering | ~60° |
| Approximate Maximum Right Steering | >45° |

The relationship between wheelbase, track width and steering angle affects the turning behaviour of the vehicle.

Once the final steering angles are precisely measured, the minimum theoretical turning radius can also be calculated more accurately.

---

## Steering Calibration

Before autonomous operation, the steering system should be calibrated to identify:

- servo centre position
- straight-wheel position
- usable maximum left position
- usable maximum right position

The mechanical centre of the steering system should correspond as closely as possible to the software's straight-ahead command.

Final calibration will also allow the approximate steering-angle values currently documented to be replaced with measured values.

---

## Steering Development

The steering system was designed to remain modular.

Using a dedicated **Servo Stand** and **13 mm Servo Horn** means these components can be redesigned and reprinted independently if the steering geometry needs to be changed.

This allows Team Astra to refine the steering system without rebuilding NEO's complete chassis.

<!-- UPLOAD HERE: CAD or photo showing the servo mounting and steering mechanism -->

---

## Steering System Summary

NEO's steering system combines:

- front-wheel steering
- SG90 Micro Servo
- PCA9685 PWM control
- custom Servo Stand
- custom 13 mm Servo Horn
- proportional steering capability
- configurable software steering limits

Together, the mechanical and software systems allow autonomous navigation commands to be converted into controlled movement of NEO's front wheels.

---

[← Back to Main README](../README.md)
