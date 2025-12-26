# ⚽ QT Football - Unified Football Analysis System

Welcome to the QT Football Analysis System! This repository contains a comprehensive AI-powered solution for analyzing football match videos.

## 🎯 Quick Start

**Use the unified system in the `football_analyzer/` directory:**

```bash
cd football_analyzer
pip install -r requirements.txt
python main.py
```

See [`football_analyzer/README.md`](football_analyzer/README.md) for detailed documentation.

## 📁 Repository Structure

```
qtfootball/
├── football_analyzer/          # ⭐ MAIN PROJECT - Use this!
│   ├── main.py                # Single entry point for all features
│   ├── trackers/              # Object detection and tracking
│   ├── team_assigner/         # Team identification
│   ├── camera_movement_estimator/  # Camera motion compensation
│   ├── view_transformer/      # Real-world coordinate mapping
│   ├── speed_and_distance_estimator/  # Performance metrics
│   └── utils/                 # Shared utilities
│
├── test foot/                 # ⚠️ DEPRECATED - Old separate projects
│   ├── FootBall-main/        # Legacy project 1
│   └── Football-brench/      # Legacy project 2
│
└── MIGRATION_GUIDE.md         # Guide for migrating from old to new
```

## 🚀 What's New?

This repository has been refactored to merge two previously separate projects (`FootBall-main` and `Football-brench`) into one unified, efficient system called `football_analyzer`.

### Why the Change?

**Before:** Two separate projects that couldn't communicate properly
- FootBall-main called Football-brench as a subprocess (inefficient)
- Duplicate code and inconsistent APIs
- Difficult to maintain and extend

**After:** One integrated pipeline
- ✅ All features in a single, efficient workflow
- ✅ Clean, maintainable code structure
- ✅ Better performance
- ✅ Easier to use and extend

## 🌟 Key Features

The unified `football_analyzer` system provides:

- **Object Detection & Tracking**: YOLO + ByteTrack for accurate player and ball tracking
- **Team Identification**: Automatic team assignment using K-means clustering
- **Ball Possession Analysis**: Track which team has the ball
- **Camera Movement Compensation**: Account for camera panning and movement
- **Real-world Measurements**: Convert pixels to meters on the field
- **Performance Metrics**: Calculate player speed (km/h) and distance covered (m)
- **Comprehensive Visualization**: All metrics displayed in the output video

## 📖 Documentation

- **Main Documentation**: [`football_analyzer/README.md`](football_analyzer/README.md)
- **Migration Guide**: [`MIGRATION_GUIDE.md`](MIGRATION_GUIDE.md) - If you were using the old structure

## 🎓 Getting Started

### Prerequisites

- Python 3.8+
- CUDA-capable GPU (recommended)
- YOLO model weights (place in `football_analyzer/models/`)

### Installation

```bash
# Clone the repository
git clone https://github.com/vesss1/qtfootball.git
cd qtfootball/football_analyzer

# Create virtual environment
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows

# Install dependencies
pip install -r requirements.txt
```

### Basic Usage

1. Place your video in `football_analyzer/input_videos/`
2. Place your YOLO model in `football_analyzer/models/`
3. Update paths in `main.py` if needed
4. Run: `python main.py`

Output will be saved to `football_analyzer/output_videos/`

## 🔧 Advanced Usage

### Using Cached Results

For faster iteration during development:

```python
USE_STUBS = True  # in main.py
```

Intermediate results will be cached in `stubs/` directory.

### Customizing the Pipeline

All components are modular. You can:
- Adjust detection confidence thresholds
- Modify team assignment parameters
- Change speed/distance calculation windows
- Customize visualization styles

See individual module documentation for details.

## 📊 Example Output

The system generates a video with:
- Player tracking (color-coded by team)
- Ball position indicator
- Ball possession markers
- Team statistics (possession %)
- Camera movement overlay
- Player speed and distance metrics

## 🤝 Contributing

Contributions are welcome! Please:
1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## 📝 License

[Specify license here]

## 🙏 Acknowledgments

This project combines and improves upon:
- FootBall-main (original detection and tracking)
- Football-brench (camera movement and metrics)
- Ultralytics YOLO (object detection)
- Supervision (tracking utilities)
- OpenCV (computer vision)

## 📧 Contact

For questions or issues:
- Open an issue on GitHub
- See documentation in `football_analyzer/README.md`

---

**Note**: The `test foot/` directory contains the old separate projects and is kept for reference only. **All new work should use the unified `football_analyzer/` system.**

For migration help, see [`MIGRATION_GUIDE.md`](MIGRATION_GUIDE.md).