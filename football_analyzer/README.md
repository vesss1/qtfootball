# ⚽ Football Analysis System - Unified

A comprehensive AI-powered football video analysis system that combines advanced computer vision and machine learning techniques to provide detailed match analytics.

## 🎯 Overview

This unified system integrates the best features from two football analysis projects, providing a complete solution for:
- Player and ball detection and tracking
- Team identification and assignment
- Ball possession analysis
- Camera movement compensation
- Speed and distance measurements
- Real-world coordinate transformation

## 🌟 Key Features

### Core Detection & Tracking
- **YOLO Object Detection**: Real-time detection of players, referees, and ball using YOLOv8
- **ByteTrack Tracking**: Advanced multi-object tracking for consistent player identification across frames
- **Ball Interpolation**: Smooth ball trajectory estimation even when detection is lost

### Team Analysis
- **Automatic Team Assignment**: Uses K-means clustering on player jersey colors to identify teams
- **Ball Possession Tracking**: Determines which player has the ball and calculates team possession percentages
- **Visual Team Indicators**: Color-coded player markers based on team assignment

### Advanced Features
- **Camera Movement Compensation**: Uses optical flow to account for camera panning and movement
- **Perspective Transformation**: Converts pixel coordinates to real-world field positions
- **Speed & Distance Calculation**: Tracks player speed (km/h) and distance covered (meters)
- **Real-time Annotations**: Comprehensive visual overlay showing all metrics

## 📋 Requirements

- Python 3.8 or higher
- CUDA-capable GPU (recommended for faster processing)

### Dependencies

```bash
pip install -r requirements.txt
```

Main dependencies:
- `ultralytics` - YOLO model
- `opencv-python` - Video processing
- `supervision` - Object tracking utilities
- `scikit-learn` - K-means clustering
- `numpy`, `pandas` - Data processing
- `torch`, `torchvision` - Deep learning framework

## 🚀 Installation

1. **Clone the repository:**
   ```bash
   git clone <repository-url>
   cd football_analyzer
   ```

2. **Create virtual environment (recommended):**
   ```bash
   python -m venv venv
   source venv/bin/activate  # Linux/Mac
   # or
   venv\Scripts\activate  # Windows
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Download YOLO model:**
   - Place your trained YOLO model (e.g., `best.pt`) in the `models/` directory
   - Or train your own using the provided training notebooks

## 📂 Project Structure

```
football_analyzer/
├── main.py                          # Main entry point
├── config.py                        # Configuration settings
├── check_setup.py                   # Setup verification script
├── requirements.txt                 # Python dependencies
├── README.md                        # This file
│
├── utils/                           # Utility functions
│   ├── __init__.py
│   ├── video_utils.py              # Video I/O operations
│   └── bbox_utils.py               # Bounding box utilities
│
├── trackers/                        # Object tracking
│   ├── __init__.py
│   └── tracker.py                  # Main tracker with ByteTrack
│
├── team_assigner/                   # Team identification
│   ├── __init__.py
│   └── team_assigner.py            # K-means based team assignment
│
├── player_ball_assigner/            # Ball possession
│   ├── __init__.py
│   └── player_ball_assigner.py     # Ball-to-player assignment
│
├── camera_movement_estimator/       # Camera compensation
│   ├── __init__.py
│   └── camera_movement_estimator.py # Optical flow based estimation
│
├── view_transformer/                # Coordinate transformation
│   ├── __init__.py
│   └── view_transformer.py         # Perspective transformation
│
├── speed_and_distance_estimator/    # Performance metrics
│   ├── __init__.py
│   └── speed_and_distance_estimator.py
│
├── models/                          # YOLO models
├── input_videos/                    # Input video files
├── output_videos/                   # Generated output videos
└── stubs/                          # Cached intermediate results
```

## 🎮 Usage

### Basic Usage

1. **Check your setup** (recommended first step):
   ```bash
   python check_setup.py
   ```

2. **Place your video** in the `input_videos/` directory

3. **Configure paths** in `config.py`:
   ```python
   INPUT_VIDEO_PATH = "input_videos/your_video.mp4"
   OUTPUT_VIDEO_PATH = "output_videos/output.mp4"
   MODEL_PATH = "models/best.pt"
   ```

4. **Run the analysis:**
   ```bash
   python main.py
   ```

### Processing Steps

The system processes videos through these stages:

1. **Video Loading** - Reads all frames from the input video
2. **Object Detection & Tracking** - Detects and tracks all objects
3. **Position Tracking** - Adds position information to each tracked object
4. **Camera Movement** - Estimates and compensates for camera motion
5. **View Transformation** - Converts to real-world coordinates
6. **Ball Interpolation** - Fills gaps in ball detection
7. **Speed & Distance** - Calculates player performance metrics
8. **Team Assignment** - Identifies and assigns team colors
9. **Ball Possession** - Determines ball control for each frame

### Using Cached Results

For faster iteration, intermediate results can be cached. Edit `config.py`:

```python
USE_STUBS = True  # Set to False to recompute everything
```

Cached files are stored in the `stubs/` directory.

## 📊 Output

The output video includes:

- **Player Tracking**: Ellipses at player feet with ID numbers
- **Team Colors**: Color-coded based on jersey colors
- **Ball Indicator**: Triangle marker showing ball position
- **Ball Possession**: Triangle on player who has the ball
- **Team Statistics**: Ball control percentages
- **Camera Movement**: X/Y movement values
- **Player Metrics**: Speed (km/h) and distance (m) for each player

## 🔧 Configuration

### Adjusting Parameters

Key parameters can be adjusted in each module:

**Tracker** (`trackers/tracker.py`):
- Detection confidence threshold
- Batch size for processing

**Camera Estimator** (`camera_movement_estimator/camera_movement_estimator.py`):
- Feature detection parameters
- Minimum movement threshold

**View Transformer** (`view_transformer/view_transformer.py`):
- Field dimensions
- Perspective points

**Speed Estimator** (`speed_and_distance_estimator/speed_and_distance_estimator.py`):
- Frame window size
- Frame rate

## 🎓 Training Custom Models

If you need to train your own YOLO model for specific use cases:

1. Collect and annotate your football match dataset
2. Use platforms like Roboflow for annotation
3. Train using YOLOv8:
   ```bash
   yolo train data=your_data.yaml model=yolov8x.pt epochs=100
   ```

## 🤝 Credits

This unified system combines features and insights from:
- Original FootBall-main project (keypoint detection, team classification)
- Football-brench project (tracking, camera movement, speed calculation)
- YOLO (Ultralytics) - Object detection
- ByteTrack (Supervision) - Multi-object tracking
- OpenCV - Computer vision operations

## 📝 License

[Specify your license here]

## 🐛 Troubleshooting

**Issue**: CUDA out of memory
- **Solution**: Reduce batch size in tracker or process fewer frames at once

**Issue**: Inaccurate team assignment
- **Solution**: Adjust K-means parameters or ensure good lighting/color contrast

**Issue**: Ball not detected
- **Solution**: Retrain model with more ball examples or adjust confidence threshold

## 📧 Contact

For questions or issues, please open an issue in the repository.

---

Made with ⚽ and 💻
