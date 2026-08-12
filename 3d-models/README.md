# NEO — 3D Models & Custom Parts

NEO combines LEGO Technic construction with **custom-designed 3D-printed components**. These parts were designed specifically around NEO's mechanical structure, steering system and camera assembly.

All current custom parts are manufactured using a **Bambu Lab A1** 3D printer with **PLA**.

---

## Manufacturing Information

| Parameter | Specification |
|---|---|
| 3D Printer | Bambu Lab A1 |
| Material | PLA |
| Manufacturing Process | FDM 3D Printing |
| Number of Custom Parts | 6 |
| Robot | NEO |
| Team | Team Astra |

<!-- UPLOAD HERE: One photograph showing all six 3D-printed parts -->

---

# Custom 3D-Printed Parts

NEO currently has six custom-designed parts:

1. FE2026 Custom Chassis
2. Servo Stand
3. Servo Horn — 13 mm
4. Pi Camera 3 Mount
5. Camera Stand V2
6. Camera Stand V3

All six STL files are available directly from this repository.

---

## 1. FE2026 Custom Chassis

The **FE2026 Custom Chassis** provides a custom structural platform for integrating NEO's mechanical and electronic systems.

It works together with LEGO Technic components, allowing the robot to retain the flexibility of LEGO construction while providing custom mounting geometry where required.

### Purpose

- supports the main robot structure
- provides mounting locations for components
- assists with compact component placement
- integrates custom components with LEGO Technic
- allows the internal layout to remain organised

<!-- UPLOAD HERE: CAD screenshot of the chassis -->

<!-- UPLOAD HERE: Photograph of the chassis installed on NEO -->

### 3D Model

[Download / View FE2026 Custom Chassis STL](fe2026_chassis_1st.stl)

---

## 2. Servo Stand

The **Servo Stand** was designed to securely position the SG90 Micro Servo used for NEO's front-wheel steering.

Keeping the servo firmly mounted is important because movement of the servo body would reduce the accuracy and repeatability of the steering mechanism.

### Purpose

- securely mounts the SG90 servo
- maintains steering alignment
- supports the steering mechanism
- reduces unwanted servo movement
- allows the servo mounting system to be modified independently

<!-- UPLOAD HERE: CAD screenshot of Servo Stand -->

<!-- UPLOAD HERE: Photograph of Servo Stand installed on NEO -->

### 3D Model

[Download / View Servo Stand STL](wro_fe2026_servostand.stl)

---

## 3. Servo Horn — 13 mm

The custom **13 mm Servo Horn** connects the SG90 Micro Servo to NEO's steering mechanism.

It transfers the rotational movement of the servo into movement of the steering linkage.

### Purpose

- transfers servo rotation
- connects the servo to the steering mechanism
- provides the required linkage geometry
- allows steering geometry to be customised

<!-- UPLOAD HERE: CAD screenshot of 13 mm Servo Horn -->

<!-- UPLOAD HERE: Photograph of Servo Horn installed -->

### 3D Model

[Download / View 13 mm Servo Horn STL](wro_fe2026_servohorn13mm.stl)

---

## 4. Pi Camera 3 Mount

The **Pi Camera 3 Mount** was designed to securely hold the Raspberry Pi Camera 3 Wide used by NEO's computer-vision system.

It connects the camera to the larger camera-support structure while maintaining its orientation relative to the robot.

### Purpose

- securely holds the Pi Camera 3 Wide
- maintains camera orientation
- connects the camera to the camera stand
- allows the camera assembly to remain modular

<!-- UPLOAD HERE: CAD screenshot of Pi Camera 3 Mount -->

<!-- UPLOAD HERE: Photograph of final camera mount once installed -->

### 3D Model

[Download / View Pi Camera 3 Mount STL](picam3mount.stl)

---

## 5. Camera Stand V2

**Camera Stand V2** represents an earlier version of NEO's elevated camera-support structure.

The camera stand was developed to position the camera above the main chassis and provide a useful view of the competition environment.

Creating multiple versions allowed the geometry to be refined without requiring changes to the entire robot.

<!-- UPLOAD HERE: CAD screenshot of Camera Stand V2 -->

### 3D Model

[Download / View Camera Stand V2 STL](camerastandv2.stl)

---

## 6. Camera Stand V3

**Camera Stand V3** is a later refinement of NEO's camera-support structure.

This version demonstrates the iterative nature of the design process. Instead of rebuilding the complete chassis when the camera-support geometry required modification, the individual component could be redesigned and reprinted.

<!-- UPLOAD HERE: CAD screenshot of Camera Stand V3 -->

<!-- UPLOAD HERE: Photograph of Camera Stand V3 once installed -->

### 3D Model

[Download / View Camera Stand V3 STL](camerastandv3.stl)

---

# Camera Stand Development

The camera-support structure went through multiple iterations during development.

```text
Camera Stand V2
       ↓
Testing & Evaluation
       ↓
Geometry Adjustments
       ↓
Camera Stand V3
```

This iterative approach allows Team Astra to modify the camera position and support geometry while leaving the rest of NEO's mechanical architecture unchanged.

<!-- UPLOAD HERE: Side-by-side image of Camera Stand V2 and V3 -->

---

# Why We Used 3D Printing

LEGO Technic provides a modular foundation for NEO, but some components require geometry specifically designed around the robot's electronics and mechanical systems.

3D printing allows us to manufacture:

- dedicated electronic mounts
- precise servo supports
- custom steering components
- camera-support structures
- structural parts designed around NEO's dimensions

Another advantage is **rapid iteration**.

If a component does not perform as expected, its CAD model can be modified and the individual component can be reprinted without rebuilding the complete vehicle.

---

# Why We Used PLA

PLA was selected for NEO's current custom components because it is suitable for rapid prototyping and allows parts to be manufactured efficiently during development.

For our application, PLA provides a practical balance between:

- rigidity
- low weight
- dimensional accuracy
- printability
- rapid iteration

---

# Design & Manufacturing Workflow

Our general workflow for custom components is:

```text
Identify Mechanical Requirement
            ↓
       Design in CAD
            ↓
      Export STL File
            ↓
 Prepare Model for Printing
            ↓
   Print on Bambu Lab A1
            ↓
       Install on NEO
            ↓
    Test Fit & Function
            ↓
       Refine if Needed
```

This process allows NEO's mechanical design to evolve alongside the electronics and software.

---

# STL File Directory

The printable files used for NEO are stored directly inside this folder.

```text
3d-models/
│
├── README.md
│
├── fe2026_chassis_1st.stl
│
├── wro_fe2026_servostand.stl
│
├── wro_fe2026_servohorn13mm.stl
│
├── picam3mount.stl
│
├── camerastandv2.stl
│
└── camerastandv3.stl
```

---

# Quick Access to 3D Models

| Component | STL File |
|---|---|
| FE2026 Custom Chassis | [View STL](fe2026_chassis_1st.stl) |
| Servo Stand | [View STL](wro_fe2026_servostand.stl) |
| Servo Horn — 13 mm | [View STL](wro_fe2026_servohorn13mm.stl) |
| Pi Camera 3 Mount | [View STL](picam3mount.stl) |
| Camera Stand V2 | [View STL](camerastandv2.stl) |
| Camera Stand V3 | [View STL](camerastandv3.stl) |

---

# 3D-Printed Parts Summary

| Part | Primary Function |
|---|---|
| FE2026 Custom Chassis | Structural integration |
| Servo Stand | SG90 servo mounting |
| Servo Horn — 13 mm | Steering linkage |
| Pi Camera 3 Mount | Camera mounting |
| Camera Stand V2 | Earlier camera-support design |
| Camera Stand V3 | Refined camera-support design |

NEO's custom parts allow us to combine the **modularity of LEGO Technic** with components designed specifically around the requirements of Team Astra's autonomous vehicle.

---

[← Back to Main README](../README.md)
