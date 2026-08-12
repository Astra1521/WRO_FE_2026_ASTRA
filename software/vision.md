# NEO — Computer Vision System

NEO uses a **Raspberry Pi Camera 3 Wide** together with the **Raspberry Pi 5** for visual perception.

The camera provides information about the competition field, while Python and OpenCV process the captured frames so that NEO can identify relevant visual features and use them during autonomous navigation.

---

## Vision Architecture

NEO's computer-vision pipeline can be represented as:

```text
Raspberry Pi Camera 3 Wide
            ↓
       Camera Frame
            ↓
       Raspberry Pi 5
            ↓
      OpenCV Processing
            ↓
   Visual Feature Detection
            ↓
 Position / Colour Information
            ↓
   Autonomous Decision Making
            ↓
 Steering + Motor Commands
```

<!-- UPLOAD HERE: Computer vision block diagram -->

---

# Camera

NEO uses the **Raspberry Pi Camera 3 Wide** as its primary visual sensor.

The wide-angle camera was selected to provide a larger field of view in front of the robot, allowing more of the competition environment to be visible within each frame.

### Current Camera Configuration

| Parameter | Configuration |
|---|---|
| Camera | Raspberry Pi Camera 3 Wide |
| Main Processor | Raspberry Pi 5 |
| Resolution | 640 × 480 |
| Frame Rate | Up to approximately 30 FPS |
| Processing Language | Python |
| Vision Library | OpenCV |
| Interface | CSI |

<!-- UPLOAD HERE: Photo of Pi Camera 3 Wide -->

<!-- UPLOAD LATER: Final photo of camera mounted on NEO -->

---

# Camera Mount

The Pi Camera 3 Wide is supported using custom 3D-printed components developed specifically for NEO.

The camera assembly includes:

- Pi Camera 3 Mount
- Camera Stand V2
- Camera Stand V3

The camera-support system went through multiple versions so that its position could be refined independently from the rest of the robot.

[View NEO's 3D-printed camera components](../3d-models/README.md)

The final camera height and mounting angle will be documented after the competition configuration is fixed.

---

# Image Acquisition

During operation, frames from the Pi Camera are captured and passed to the Raspberry Pi 5.

Each frame becomes an input to NEO's computer-vision pipeline.

```text
Camera
   ↓
Capture Frame
   ↓
Prepare Image
   ↓
Process with OpenCV
   ↓
Extract Useful Information
```

The goal is not simply to record video. The captured images are converted into information that NEO's autonomous-control software can use.

---

# Image Processing

OpenCV is used to process camera frames.

Depending on the autonomous behaviour being executed, the vision pipeline can perform operations such as:

- frame acquisition
- colour-space conversion
- image masking
- contour detection
- object localisation
- position estimation
- filtering of irrelevant detections

This reduces the raw camera image into information useful for navigation.

<!-- UPLOAD HERE: Screenshot showing an example raw camera frame -->

<!-- UPLOAD HERE: Screenshot showing the same frame after OpenCV processing -->

---

# Colour Detection

Colour detection is used to distinguish relevant visual features within the competition environment.

A simplified colour-processing pipeline is:

```text
Camera Frame
      ↓
Colour-Space Conversion
      ↓
Apply Colour Threshold
      ↓
Generate Mask
      ↓
Find Relevant Regions
      ↓
Determine Position
```

The exact threshold values can be adjusted during testing to account for changes in:

- lighting
- camera position
- exposure
- competition-field conditions

This makes calibration an important part of the final vision setup.

---

# Red and Green Recognition

NEO's vision system is designed to distinguish relevant **red and green obstacles**.

After colour filtering, the software can determine where a detected obstacle appears within the camera frame.

For example:

```text
Detected Object
      ↓
Determine Colour
      ↓
Determine Position
      ↓
Send Information to Navigation Logic
```

The navigation system can then use this information when deciding the required steering response.

<!-- UPLOAD HERE: Screenshot of red obstacle detection -->

<!-- UPLOAD HERE: Screenshot of green obstacle detection -->

---

# Object Position

Once a relevant region has been detected, its position within the frame can be estimated.

A common representation is the centre of the detected region:

```text
Object Centre = (x, y)
```

The horizontal position is particularly useful for steering decisions.

For a frame width of **640 pixels**, the approximate image centre is:

```text
x = 320
```

The difference between the desired position and detected position can then be used as an error value.

```text
Error = Desired Position - Detected Position
```

This error can contribute to NEO's steering correction.

---

# Contour Detection

After creating a colour mask, OpenCV can identify connected regions or contours.

Contours allow the software to estimate properties such as:

- object position
- bounding region
- centre point
- apparent size

Small or irrelevant detections can be filtered so that the navigation system focuses on useful visual information.

<!-- UPLOAD HERE: Screenshot showing detected contour/bounding box -->

---

# Vision and Steering

The information generated by the camera is passed to NEO's autonomous-control system.

A simplified control sequence is:

```text
Camera
   ↓
Obstacle Detection
   ↓
Obstacle Position
   ↓
Calculate Error
   ↓
Calculate Steering Correction
   ↓
SG90 Servo
```

The size and direction of the detected error can therefore influence the steering command.

[View NEO's steering system](../mobility/steering.md)

---

# Vision and Distance Sensors

NEO does not rely only on camera information.

The camera works alongside the Time-of-Flight distance sensors.

The two sensing systems provide complementary information:

| Camera | ToF Sensors |
|---|---|
| Identifies visual features | Measures distance |
| Distinguishes colour | Measures proximity |
| Estimates object position in image | Provides directional clearance |
| Covers a wide visual region | Measures specific regions around NEO |

A simplified sensor-fusion concept is:

```text
        Camera
          ↓
 Visual Information
          ↓
     Raspberry Pi 5
          ↑
 Distance Information
          ↑
      ToF Sensors
```

The Raspberry Pi can use both sources when determining the appropriate autonomous behaviour.

[View NEO's sensor system](../hardware/sensors.md)

---

# Vision Calibration

Computer vision can be affected by environmental conditions.

Before competition operation, the vision system can be calibrated for:

- camera position
- camera angle
- colour thresholds
- lighting conditions
- useful detection area
- minimum relevant contour size
- obstacle visibility

The final calibration values depend on the completed physical camera installation and testing conditions.

---

# Why Raspberry Pi 5?

Computer vision requires significantly more processing than simple sensor readings.

The Raspberry Pi 5 was selected as NEO's main controller because it can run the Python and OpenCV processing required by the vision system while also coordinating the rest of the autonomous vehicle.

This allows the main sequence to remain:

```text
SEE
 ↓
PROCESS
 ↓
DECIDE
 ↓
MOVE
```

---

# Development & Testing

The computer-vision system is tested using camera frames containing the visual features NEO is expected to encounter.

During development, Team Astra can evaluate:

- whether the required colours are detected
- whether false detections occur
- whether object positions are calculated correctly
- whether detection remains stable as NEO moves
- whether steering responds appropriately to visual information

The camera mounting position can then be adjusted alongside the software parameters.

<!-- UPLOAD HERE: Photo/screenshot of Team Astra testing the vision system -->

---

# Example Vision Output

Once the final vision system is tested, this section will contain examples of NEO's processed camera output.

<!-- UPLOAD HERE: RAW FRAME -->

<!-- UPLOAD HERE: COLOUR MASK -->

<!-- UPLOAD HERE: FINAL DETECTION WITH CONTOUR / CENTRE POINT -->

These images will demonstrate the progression from the original camera input to the information used by the autonomous navigation software.

---

# Vision System Summary

NEO's computer-vision system combines:

- Raspberry Pi Camera 3 Wide
- Raspberry Pi 5
- Python
- OpenCV
- colour processing
- contour detection
- obstacle localisation
- visual steering information
- ToF distance sensing

The camera allows NEO to visually interpret the competition environment, while the Raspberry Pi converts that visual information into data that can contribute to autonomous navigation decisions.

---

[← Back to Main README](../README.md)
