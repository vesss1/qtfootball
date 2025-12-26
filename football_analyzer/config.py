"""
Configuration file for Football Analyzer
Adjust these settings based on your setup and requirements
"""

# ===== INPUT/OUTPUT PATHS =====
# Path to input video file
INPUT_VIDEO_PATH = "input_videos/08fd33_4.mp4"

# Path for output video
OUTPUT_VIDEO_PATH = "output_videos/output.mp4"

# Path to YOLO model weights
MODEL_PATH = "models/best.pt"


# ===== CACHING CONFIGURATION =====
# Use cached intermediate results for faster processing
USE_STUBS = True

# Paths for cached data
TRACK_STUB_PATH = "stubs/track_stubs.pkl"
CAMERA_STUB_PATH = "stubs/camera_movement_stub.pkl"


# ===== TRACKER SETTINGS =====
# Detection confidence threshold (0.0 to 1.0)
DETECTION_CONFIDENCE = 0.1

# Batch size for processing frames
BATCH_SIZE = 20


# ===== SPEED AND DISTANCE SETTINGS =====
# Number of frames to use for speed calculation window
SPEED_FRAME_WINDOW = 5

# Video frame rate (fps)
FRAME_RATE = 24


# ===== CAMERA MOVEMENT SETTINGS =====
# Minimum movement threshold for camera motion detection
MINIMUM_CAMERA_MOVEMENT = 5

# Number of corners to track for optical flow
MAX_CORNERS = 100

# Quality level for corner detection
QUALITY_LEVEL = 0.3


# ===== TEAM ASSIGNMENT SETTINGS =====
# Number of clusters for K-means (should be 2 for two teams)
NUM_TEAMS = 2


# ===== PLAYER BALL ASSIGNMENT SETTINGS =====
# Maximum distance (in pixels) for ball-to-player assignment
MAX_PLAYER_BALL_DISTANCE = 70


# ===== VIEW TRANSFORMER SETTINGS =====
# Football field dimensions in meters
FIELD_WIDTH = 68  # meters
FIELD_LENGTH = 23.32  # meters (this seems small, typical is ~105m)

# Note: You may need to adjust FIELD_LENGTH based on your video
# Standard football pitch: 105m x 68m
# You can customize these based on the actual field in your video


# ===== VIDEO OUTPUT SETTINGS =====
# Output video frame rate
OUTPUT_FPS = 24.0

# Video codec (options: 'mp4v', 'XVID', 'H264', etc.)
OUTPUT_CODEC = 'mp4v'


# ===== VISUALIZATION SETTINGS =====
# Whether to display camera movement overlay
SHOW_CAMERA_MOVEMENT = True

# Whether to display speed and distance metrics
SHOW_SPEED_DISTANCE = True

# Whether to display team ball control statistics
SHOW_BALL_CONTROL = True


# ===== LOGGING =====
# Enable verbose output
VERBOSE = True

# Show progress bars
SHOW_PROGRESS = True
