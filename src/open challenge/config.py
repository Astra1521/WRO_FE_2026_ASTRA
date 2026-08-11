import numpy as np
# ==========================================
# Servo Configuration
# ==========================================

SERVO_PWM_CHANNEL = 0
SERVO_FREQUENCY = 50
SERVO_MIN_US = 500
SERVO_MAX_US = 2400
SERVO_MIN = 50
SERVO_CENTER = 95
SERVO_MAX = 140
MAX_CENTERING_ANGLE = 25
KP_CENTERING = 0.05
GYRO_KP = 0.5


# ==========================================
# Motor Configuration
# ==========================================

MOTOR_PWM_CHANNEL = 0
MOTOR_IN1_CHANNEL = 2
MOTOR_IN2_CHANNEL = 1
MOTOR_PWM_FREQUENCY = 1000
STBY_PIN = 6
BASE_SPEED = 50
MAX_SPEED = 50
CORNERING_SPEED = 30
DODGE_SPEED = 30

# ==========================================
# TOF Sensor Configuration
# ==========================================

MUX_ADDR = 0x70
LEFT_CHANNEL = 5
FRONT_CHANNEL = 3
RIGHT_CHANNEL = 2
GYRO_CHANNEL = 4


# ==========================================
# Dynamic Steering & Flow Variables
# ==========================================
TOTAL_CORNERS = 12           # 3 Laps * 4 Corners
LOOP_DELAY = 0.03
MIN_FRAMES_IN_TURN = 30      # Frames to wait while shifting lanes

# Virtual Bumper & Clear Rules
EMERGENCY_STOP_DISTANCE = 50
FRONT_DODGE_THRESHOLD = 50
MIN_WALL_DIST_MM = 150       # Veto camera if wall is closer than 150mm
TOF_BLOCK_CLEARED_MM = 400   # Block is passed when side ToF reads > 400mm

# Proportional Camera Steering (X-Coordinates for Safe Passing)
SAFE_RED_X_MAX = 200         # Red block must be to the left of X=200
SAFE_GREEN_X_MIN = 440       # Green block must be to the right of X=440

AVOIDANCE_OFFSET = 300  	# Adjust this (in pixels) based on how wide your robot is
KP_STEERING = 0.3      		# Adjust this to make steering more/less aggressive

# ==========================================
# Camera & Vision Settings
# ==========================================
FRAME_WIDTH = 640
FRAME_HEIGHT = 480
MAX_FPS = 30
CROP_TOP_FRAC = 5 / 12
CROP_BOTTOM_FRAC = 0
MIN_CONTOUR_AREA = 2500
MAX_BLOCK_AREA_FRACTION = 0.25
MIN_BLOCK_AREA_FOR_ACTION = 7500 # Threshold to trigger Dodge State
MIN_BLOCK_ROI_OVERLAP = 0.50

# HSV Color Thresholds (Required for find_biggest_block)
LOWER_RED_1 = np.array([0, 150, 40])
UPPER_RED_1 = np.array([10, 255, 200])
LOWER_RED_2 = np.array([175, 150, 40])
UPPER_RED_2 = np.array([180, 255, 200])

LOWER_GREEN = np.array([36, 50, 35])
UPPER_GREEN = np.array([89, 255, 130])

# HSV Color ranges (Adjust these based on your track lighting!)
ORANGE_LOWER = np.array([6, 70, 20])				#([5, 150, 150])
ORANGE_UPPER = np.array([26, 255, 255])				#([15, 255, 255])

BLUE_LOWER = np.array([94, 45, 58])					#([100, 150, 150])
BLUE_UPPER = np.array([140, 226, 185])				#([120, 255, 255])

BOX_COLOR_RED = (0, 0, 255)
BOX_COLOR_GREEN = (0, 255, 0)

# --- Corner Detection Settings ---
CORNER_AREA_THRESHOLD = 5000  # Min pixels to trigger a turn (tune this!)
CORNER_COOLDOWN = 2.0         # Seconds to ignore lines after finishing a turn
CORNER_SPEED = 30             # Slow down a bit for sharp turns
