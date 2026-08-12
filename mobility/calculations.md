# NEO — Mobility Calculations

This page documents the main calculations used to understand NEO's wheel movement, theoretical speed and required wheel RPM.

These calculations are theoretical and are kept separate from experimentally recorded performance.

---

## Known Values

| Parameter | Value |
|---|---:|
| Wheel Radius | 0.03 m |
| Wheel Diameter | 0.06 m |
| Estimated Distance for 3 Laps | 26.4 m |
| Recorded Lap Time | Approximately 8.7 s |

---

## 1. Wheel Circumference

NEO uses wheels with a radius of approximately:

**r = 0.03 m**

Wheel circumference is calculated using:

**C = 2πr**

Therefore:

**C = 2 × π × 0.03**

**C ≈ 0.1885 m**

This means that one complete wheel rotation theoretically moves NEO approximately:

**0.1885 m**

This assumes no wheel slip.

---

## 2. Estimated Track Distance

For our mobility calculations, the approximate distance travelled over three laps was taken as:

**Distance ≈ 26.4 m**

This value is used to estimate the linear speed and wheel RPM required for different target completion times.

<!-- UPLOAD HERE: Image of handwritten track-distance calculation -->

---

## 3. Theoretical Speed at 100%

For the theoretical calculation, a three-lap time of approximately:

**27 seconds**

was used.

Linear speed is calculated using:

**Speed = Distance ÷ Time**

Therefore:

**Speed = 26.4 ÷ 27**

**Speed ≈ 0.978 m/s**

NEO would therefore require an average theoretical linear speed of approximately:

**0.98 m/s**

---

## 4. Theoretical Wheel RPM at 100%

The wheel circumference is approximately:

**0.1885 m**

The required wheel rotations per second are:

**0.978 ÷ 0.1885 ≈ 5.19 rotations/s**

Converting to RPM:

**5.19 × 60 ≈ 311 RPM**

Therefore:

**Theoretical Wheel Speed ≈ 311 RPM**

---

## 5. Theoretical Speed at 80%

For the second theoretical calculation, a three-lap time of approximately:

**32 seconds**

was used.

Linear speed:

**26.4 ÷ 32**

**≈ 0.825 m/s**

Therefore, the theoretical average linear speed is:

**≈ 0.825 m/s**

---

## 6. Theoretical Wheel RPM at 80%

Using the same wheel circumference:

**0.825 ÷ 0.1885 ≈ 4.38 rotations/s**

Converting to RPM:

**4.38 × 60 ≈ 263 RPM**

Therefore:

**Theoretical Wheel Speed ≈ 263 RPM**

---

## Calculation Summary

| Calculation | 100% | 80% |
|---|---:|---:|
| Estimated 3-Lap Distance | 26.4 m | 26.4 m |
| Target Time | 27 s | 32 s |
| Linear Speed | ~0.978 m/s | ~0.825 m/s |
| Wheel Circumference | ~0.1885 m | ~0.1885 m |
| Wheel Speed | ~311 RPM | ~263 RPM |

---

## Assumptions

These calculations are theoretical estimates.

They assume:

- a wheel radius of 30 mm
- no wheel slip
- constant average speed
- a 1:1 effective drivetrain ratio
- no significant drivetrain losses

In real operation, acceleration, braking, turning, wheel slip, drivetrain resistance and motor loading affect the vehicle's actual speed.

For this reason, these calculations are used as an engineering reference rather than as measured performance data.

---

## Recorded Performance

During testing, NEO has completed one lap of the mat in approximately:

**8.7 seconds**

This is an observed result and is therefore documented separately from the theoretical calculations above.

<!-- UPLOAD HERE: Photo of handwritten mobility calculations -->

<!-- OPTIONAL: Upload a screenshot/photo showing the recorded lap timing -->

---

[← Back to Main README](../README.md)
