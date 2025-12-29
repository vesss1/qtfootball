# Data Export Feature

## Overview

The football analysis system now supports **data extraction** from the output video. All information displayed on the video (player tracking, ball possession, camera movement, speed/distance metrics) can be exported to structured data files for further analysis.

## Exported Data

The system extracts the following information:

### Player Data (per frame)
- Player ID
- Team assignment (1 or 2)
- Team color (RGB)
- Bounding box coordinates (x1, y1, x2, y2)
- Position (x, y)
- Adjusted position (compensated for camera movement)
- Speed (km/h)
- Distance covered (meters)
- Ball possession status

### Ball Data (per frame)
- Bounding box coordinates
- Position (x, y)

### Team Statistics
- Team 1 ball control percentage
- Team 2 ball control percentage
- Frame-by-frame ball possession

### Camera Movement (per frame)
- X-axis movement
- Y-axis movement

## Export Formats

### JSON Format
Complete hierarchical data structure with all information:
- **File**: `output_data/analysis_data.json`
- **Structure**: Frame-by-frame data with nested player/ball/referee information
- **Best for**: Programmatic access, API integration, detailed analysis

### CSV Format
Tabular data split into multiple files for easy analysis:
- **Files**:
  - `output_data/csv/players_tracking.csv` - Player tracking data
  - `output_data/csv/frames_summary.csv` - Frame-level summary (camera, ball)
  - `output_data/csv/ball_control_stats.csv` - Overall statistics
- **Best for**: Excel, data analysis tools, plotting

## Usage

### Automatic Export (Default)

The data export happens automatically when running the main analysis:

```bash
cd football_analysis-main
python main.py
```

After processing, you'll find the exported data in:
- `output_data/analysis_data.json`
- `output_data/csv/` directory

### Programmatic Usage

You can also use the DataExporter class directly in your code:

```python
from utils import DataExporter

# After running the analysis and getting tracks, team_ball_control, camera_movement
exporter = DataExporter()

# Export to JSON
exporter.export_to_json(
    tracks=tracks,
    team_ball_control=team_ball_control,
    camera_movement_per_frame=camera_movement_per_frame,
    output_path='my_data.json'
)

# Export to CSV
exporter.export_to_csv(
    tracks=tracks,
    team_ball_control=team_ball_control,
    camera_movement_per_frame=camera_movement_per_frame,
    output_dir='my_csv_data'
)

# Export to both formats at once
results = exporter.export_all(
    tracks=tracks,
    team_ball_control=team_ball_control,
    camera_movement_per_frame=camera_movement_per_frame,
    json_path='my_data.json',
    csv_dir='my_csv_data'
)
```

## Example Output

### JSON Example
```json
{
  "metadata": {
    "total_frames": 1500,
    "team_1_ball_control_percent": 55.2,
    "team_2_ball_control_percent": 44.8
  },
  "frames": [
    {
      "frame_number": 0,
      "camera_movement": {"x": 0.0, "y": 0.0},
      "team_ball_control": 1,
      "players": [
        {
          "id": 1,
          "bbox": [150.0, 200.0, 200.0, 280.0],
          "team": 1,
          "team_color": [255, 0, 0],
          "has_ball": false,
          "speed_kmh": 15.5,
          "distance_m": 125.3
        }
      ],
      "ball": {
        "id": 1,
        "bbox": [400.0, 300.0, 420.0, 320.0]
      }
    }
  ]
}
```

### CSV Example (players_tracking.csv)
```
frame_number,player_id,team,has_ball,bbox_x1,bbox_y1,bbox_x2,bbox_y2,speed_kmh,distance_m
0,1,1,0,150,200,200,280,15.5,125.3
0,2,1,0,200,200,250,280,17.2,98.7
0,3,2,0,250,200,300,280,12.8,87.4
```

## Use Cases

1. **Performance Analysis**: Export player speed/distance data for training analytics
2. **Tactical Analysis**: Analyze ball possession patterns and player movements
3. **Custom Visualization**: Create custom charts and visualizations using the exported data
4. **Machine Learning**: Use exported data for training ML models
5. **Statistics Generation**: Generate match statistics and reports
6. **Integration**: Integrate with other sports analysis tools

## Notes

- The `output_data/` directory is automatically created if it doesn't exist
- Exported files use UTF-8 encoding
- JSON files are formatted with indentation for readability
- CSV files include headers for easy import into analysis tools
- The export happens after video processing is complete

## Troubleshooting

**Q: Where are the exported files?**
A: By default, files are saved in the `football_analysis-main/output_data/` directory.

**Q: Can I change the export location?**
A: Yes, modify the paths in `main.py` or use the DataExporter class directly with custom paths.

**Q: The CSV file is too large to open in Excel**
A: Use Python/Pandas, R, or specialized data analysis tools for large datasets.

**Q: How do I analyze the exported data?**
A: You can use Python (pandas, matplotlib), R, Excel, or any data analysis tool that supports JSON/CSV.

## Example Analysis Scripts

### Using Python/Pandas
```python
import pandas as pd
import matplotlib.pyplot as plt

# Load player tracking data
df = pd.read_csv('output_data/csv/players_tracking.csv')

# Analyze player speed
player_speeds = df.groupby('player_id')['speed_kmh'].mean()
print("Average speed per player:", player_speeds)

# Plot distance covered
plt.figure(figsize=(10, 6))
df.groupby('player_id')['distance_m'].max().plot(kind='bar')
plt.title('Total Distance Covered by Each Player')
plt.xlabel('Player ID')
plt.ylabel('Distance (meters)')
plt.show()
```

### Using JSON in JavaScript
```javascript
// Load and parse JSON data
fetch('output_data/analysis_data.json')
  .then(response => response.json())
  .then(data => {
    console.log('Total frames:', data.metadata.total_frames);
    console.log('Team 1 control:', data.metadata.team_1_ball_control_percent + '%');
    
    // Access frame data
    data.frames.forEach(frame => {
      console.log(`Frame ${frame.frame_number}: ${frame.players.length} players detected`);
    });
  });
```

## License

This feature is part of the football analysis system and follows the same license as the main project.
