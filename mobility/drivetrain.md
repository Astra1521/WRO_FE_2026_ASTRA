# NEO — Drivetrain

NEO uses a compact **rear-wheel-drive drivetrain** powered by a LEGO EV3 Medium Motor and a LEGO differential.

The drivetrain was designed to provide reliable propulsion while keeping the drive system mechanically separate from the front steering system.

---

## Drivetrain Architecture

NEO's drivetrain follows the basic power path:

**LEGO EV3 Medium Motor**  
↓  
**LEGO Gear System**  
↓  
**LEGO Differential**  
↓  
**Rear Axle**  
↓  
**Rear Wheels**

The rear wheels provide propulsion, while the front wheels are responsible for steering.

<!-- UPLOAD HERE: Clear top or bottom photograph showing the complete drivetrain -->

---

## Rear-Wheel Drive

NEO uses a **rear-wheel-drive configuration**.

In this arrangement:

- the rear axle provides propulsion
- the front wheels provide steering
- the propulsion and steering mechanisms operate independently

Separating these functions simplifies the mechanical architecture and allows changes to the steering system without redesigning the complete drivetrain.

---

## Drive Motor

NEO is powered by a **LEGO EV3 Medium Motor**.

The EV3 Medium Motor was selected because its compact dimensions allow it to fit within NEO's 195 mm × 111 mm chassis while integrating directly with LEGO axles, gears and drivetrain components.

Using a LEGO-based drive motor also allows the drivetrain to remain modular, making mechanical adjustments easier during development.

<!-- UPLOAD HERE: Close-up photo of the LEGO EV3 Medium Motor installed in NEO -->

---

## LEGO Differential

A LEGO differential is installed on NEO's rear driven axle.

When a vehicle turns, the outside wheel must travel a greater distance than the inside wheel. If both driven wheels were mechanically forced to rotate at exactly the same speed, one wheel would need to slip during the turn.

The differential allows the rear wheels to rotate at different speeds while still receiving power from the drive motor.

### Advantages

The differential helps:

- reduce wheel slip during turns
- improve cornering
- reduce mechanical stress
- provide smoother drivetrain movement

<!-- UPLOAD HERE: Close-up photo of NEO's LEGO differential -->

---

## Rear Axle

The differential transfers power to the **rear axle**, which drives NEO's rear wheels.

The rear track width is:

**85 mm**

The drivetrain components are positioned within the chassis to maintain a compact overall vehicle width while leaving sufficient space for the battery and electronics.

---

## Wheels

NEO uses wheels with an approximate radius of:

**30 mm**

Therefore:

**Wheel Diameter = 60 mm**

The theoretical wheel circumference is:

**C = 2πr**

**C = 2π(0.03)**

**C ≈ 0.1885 m**

One complete wheel rotation therefore corresponds to approximately **0.1885 m of theoretical travel**, assuming no wheel slip.

[View full wheel and speed calculations](calculations.md)

---

## Motor Control

The LEGO EV3 Medium Motor is controlled using the **TB6612FNG motor driver**.

The control path is:

**Raspberry Pi 5**  
↓  
**TB6612FNG Motor Driver**  
↓  
**LEGO EV3 Medium Motor**  
↓  
**Differential**  
↓  
**Rear Wheels**

The motor driver allows the Raspberry Pi's autonomous control system to manage propulsion without directly supplying the electrical power required by the motor.

[View NEO's electrical system](../hardware/electrical-system.md)

---

## Drivetrain Geometry

| Parameter | NEO |
|---|---:|
| Drive Type | Rear-wheel drive |
| Drive Motor | LEGO EV3 Medium Motor |
| Differential | LEGO Differential |
| Wheel Radius | 30 mm |
| Wheel Diameter | 60 mm |
| Rear Track Width | 85 mm |
| Wheelbase | 150 mm |

<!-- UPLOAD HERE: Labelled image showing motor, differential, rear axle and rear wheels -->

---

## Recorded Performance

During current testing, NEO has completed one lap of the mat in approximately:

**8.7 seconds**

This is an observed performance result and is kept separate from the theoretical drivetrain calculations.

The theoretical calculations for wheel circumference, linear speed and wheel RPM are documented separately.

[View NEO's mobility calculations](calculations.md)

---

## Drivetrain Design Summary

NEO's drivetrain combines:

- LEGO EV3 Medium Motor propulsion
- rear-wheel drive
- LEGO differential
- 85 mm rear track width
- 60 mm diameter wheels
- modular LEGO drivetrain components

The drivetrain provides a compact propulsion system while allowing the front steering mechanism to operate independently.

---

[← Back to Main README](../README.md)
