# Migration Guide: From FootBall-main & Football-brench to Unified System

This guide explains how to migrate from the separate `FootBall-main` and `Football-brench` projects to the new unified `football_analyzer` system.

## What Changed?

### Before (Separate Projects)
```
test foot/
├── FootBall-main/           # Project 1
│   ├── main.py             # Called Football-brench as subprocess
│   └── src/
│       ├── detections/
│       ├── utils/
│       └── keypoint_detection/
│
└── Football-brench/         # Project 2
    ├── main.py             # Separate execution
    ├── trackers/
    ├── team_assigner/
    └── utils/
```

**Problems with old structure:**
- Two separate main.py files that couldn't communicate effectively
- FootBall-main called Football-brench as a subprocess (inefficient)
- Duplicate code (utils, video processing)
- Difficult to maintain and extend
- Confusing project structure

### After (Unified Project)
```
football_analyzer/           # Single unified project
├── main.py                 # One entry point for all features
├── trackers/               # Object tracking
├── team_assigner/          # Team identification
├── player_ball_assigner/   # Ball possession
├── camera_movement_estimator/  # Camera compensation
├── view_transformer/       # Coordinate transformation
├── speed_and_distance_estimator/  # Performance metrics
└── utils/                  # Shared utilities
```

**Benefits of new structure:**
- ✅ Single, integrated pipeline
- ✅ All features work together seamlessly
- ✅ No subprocess overhead
- ✅ Clean, maintainable code structure
- ✅ Better performance
- ✅ Easier to extend

## Feature Comparison

### Features from FootBall-main
| Feature | Status in Unified System |
|---------|-------------------------|
| YOLO Object Detection | ✅ Integrated (using ultralytics) |
| Player Tracking | ✅ Enhanced with ByteTrack |
| Team Classification (K-means) | ✅ Integrated |
| Ball Assignment | ✅ Integrated with improvements |
| Video I/O | ✅ Unified and improved |
| Keypoint Detection | ⚠️ Available but optional* |

*Keypoint detection can be added as an optional feature if needed

### Features from Football-brench
| Feature | Status in Unified System |
|---------|-------------------------|
| ByteTrack Tracking | ✅ Core tracking system |
| Team Assignment | ✅ Fully integrated |
| Ball Possession | ✅ Integrated |
| Camera Movement Estimation | ✅ Integrated |
| View Transformation | ✅ Integrated |
| Speed & Distance Calculation | ✅ Integrated |

## How to Migrate

### Step 1: Understand the New Structure

The new `football_analyzer` directory contains everything you need. There's no need to maintain the old `FootBall-main` and `Football-brench` directories separately.

### Step 2: Move Your Data

1. **Models**: Copy your YOLO model files
   ```bash
   cp "test foot/FootBall-main/models/best.pt" football_analyzer/models/
   # or
   cp "test foot/Football-brench/models/best.pt" football_analyzer/models/
   ```

2. **Videos**: Copy your input videos
   ```bash
   cp "test foot/FootBall-main/test_videos/"*.mp4 football_analyzer/input_videos/
   # or
   cp "test foot/Football-brench/input_videos/"*.mp4 football_analyzer/input_videos/
   ```

3. **Stubs** (optional): Copy cached results if you want to reuse them
   ```bash
   cp "test foot/Football-brench/stubs/"*.pkl football_analyzer/stubs/
   ```

### Step 3: Install Dependencies

```bash
cd football_analyzer
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows
pip install -r requirements.txt
```

### Step 4: Update Configuration

Edit `main.py` to set your paths:

```python
# Before (FootBall-main)
VIDEO_PATH = str(BASE_DIR / "test_videos/trim.mp4")
OBJ_MODEL_PATH = str(BASE_DIR / "models/obj_v8x.pt")

# Before (Football-brench)
video_frames = read_video(r"input_videos\08fd33_4.mp4")
tracker = Tracker("yolo_inference.py")

# After (Unified)
INPUT_VIDEO_PATH = "input_videos/your_video.mp4"
OUTPUT_VIDEO_PATH = "output_videos/output.mp4"
MODEL_PATH = "models/best.pt"
```

### Step 5: Run the Unified System

```bash
python main.py
```

That's it! All features now run in a single integrated pipeline.

## Code Migration Examples

### Example 1: Reading and Saving Videos

**Before (FootBall-main):**
```python
from src.utils.video_utils import read_video, save_video
video_frames = read_video(VIDEO_PATH)
save_video(annotated_frames, str(OUTPUT_PATH))
```

**Before (Football-brench):**
```python
from utils import read_video, save_video
video_frames = read_video(r"input_videos\08fd33_4.mp4")
save_video(output_video_frames, "output_videos/output.avi")
```

**After (Unified):**
```python
from utils import read_video, save_video
video_frames = read_video("input_videos/video.mp4")
save_video(output_frames, "output_videos/output.mp4")
```

### Example 2: Object Detection and Tracking

**Before (FootBall-main):**
```python
from src.detections.player_detection import get_detection
detections = get_detection(OBJ_MODEL_PATH, video_frames, STUBS_PATH_OBJ, STUBS_STATUS)
```

**Before (Football-brench):**
```python
from trackers import Tracker
tracker = Tracker("yolo_inference.py")
tracks = tracker.get_object_tracks(video_frames, read_from_stub=True, stub_path="stubs/track_stubs.pkl")
```

**After (Unified):**
```python
from trackers import Tracker
tracker = Tracker("models/best.pt")
tracks = tracker.get_object_tracks(
    video_frames,
    read_from_stub=True,
    stub_path="stubs/track_stubs.pkl"
)
```

### Example 3: Team Assignment

**Before (FootBall-main):**
```python
from src.utils.team_classifer import TeamClassifier
team_classifier = TeamClassifier()
_, team_assignments = team_classifier.classify_players(frame, player_detections)
```

**Before (Football-brench):**
```python
from team_assigner import TeamAssigner
team_assigner = TeamAssigner()
team_assigner.assign_team_color(video_frames[0], tracks['players'][0])
team = team_assigner.get_player_team(video_frames[frame_num], track['bbox'], player_id)
```

**After (Unified):**
```python
from team_assigner import TeamAssigner
team_assigner = TeamAssigner()
team_assigner.assign_team_color(video_frames[0], tracks['players'][0])
# Same API as Football-brench (cleaner and more flexible)
```

## New Features Available

The unified system includes features that weren't available (or were harder to use) before:

1. **Camera Movement Compensation**: Automatically accounts for camera panning
2. **Real-world Coordinates**: Converts pixel positions to meters on the field
3. **Speed Calculation**: Shows player speed in km/h
4. **Distance Tracking**: Tracks total distance covered by each player
5. **Better Ball Interpolation**: Smoother ball tracking
6. **Integrated Visualization**: All metrics shown in one output video

## Troubleshooting Migration Issues

### Issue: Import errors
**Solution**: Make sure you're running from the `football_analyzer` directory and have installed all requirements.

### Issue: Model not found
**Solution**: Check that your model file is in `football_analyzer/models/` and update the path in `main.py`.

### Issue: Different output format
**Solution**: The new system outputs `.mp4` by default. You can change this in `utils/video_utils.py`.

### Issue: Missing cached stubs
**Solution**: Set `USE_STUBS = False` in `main.py` to recompute from scratch.

## Backward Compatibility

If you absolutely need to keep the old projects running:
1. Keep `test foot/FootBall-main` and `test foot/Football-brench` as they are
2. Use `football_analyzer` for new work
3. Gradually migrate your workflows to the unified system

However, we recommend fully migrating to the new system for better maintainability.

## Next Steps

1. ✅ Migrate your data and models
2. ✅ Run the unified system
3. ✅ Verify output matches your expectations
4. ⚠️ Consider archiving the old directories
5. 🎉 Enjoy a cleaner, more powerful system!

## Questions?

If you encounter issues during migration:
1. Check this guide again
2. Review the `README.md` in `football_analyzer/`
3. Open an issue in the repository

---

**Note**: The old `test foot/` structure with separate projects is now deprecated. All new development should use the unified `football_analyzer` system.
