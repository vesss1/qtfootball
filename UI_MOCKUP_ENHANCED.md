# Qt UI Layout - Video Analysis Section

## Visual Mockup of the Enhanced UI

```
┌─────────────────────────────────────────────────────────────────────────┐
│  足球球員管理系統 (Football Player Management System)                      │
└─────────────────────────────────────────────────────────────────────────┘

... (Player Management Section) ...

┌─────────────────────────────────────────────────────────────────────────┐
│  視頻分析數據 (Video Analysis Data)                                       │
│                                                                         │
│  ┌─────────────────────────────────────────────────────────────────┐   │
│  │  載入視頻分析數據 (Load Video Analysis Data)                      │   │
│  └─────────────────────────────────────────────────────────────────┘   │
│                                                                         │
│  ┌─────────────────────────────────┬─────────────────────────────────┐ │
│  │  隊伍 1 持球時間: 58.30%        │  隊伍 2 持球時間: 41.70%        │ │
│  │  (Team 1 Possession)           │  (Team 2 Possession)           │ │
│  └─────────────────────────────────┴─────────────────────────────────┘ │
│                                                                         │
│  ┌─────────────────────────────────┬─────────────────────────────────┐ │
│  │  隊伍 1 進攻時間: 32.50%        │  隊伍 2 進攻時間: 28.10%        │ │
│  │  (Team 1 Attack Time)          │  (Team 2 Attack Time)          │ │
│  │  🔵 Blue color                 │  🔵 Blue color                 │ │
│  └─────────────────────────────────┴─────────────────────────────────┘ │
│                                                                         │
│  ┌─────────────────────────────────┬─────────────────────────────────┐ │
│  │  隊伍 1 總距離: 12.45 公里      │  隊伍 2 總距離: 11.87 公里      │ │
│  │  (Team 1 Total Distance)       │  (Team 2 Total Distance)       │ │
│  │  🟢 Green color                │  🟢 Green color                │ │
│  └─────────────────────────────────┴─────────────────────────────────┘ │
│                                                                         │
│  ┌─────────────────────────────────┬─────────────────────────────────┐ │
│  │  隊伍 1 平均速度: 8.50 公里/小時 │  隊伍 2 平均速度: 8.20 公里/小時 │ │
│  │  (Team 1 Avg Speed)            │  (Team 2 Avg Speed)            │ │
│  │  🟣 Purple color               │  🟣 Purple color               │ │
│  └─────────────────────────────────┴─────────────────────────────────┘ │
│                                                                         │
│  ┌─────────────────────────────────────────────────────────────────┐   │
│  │  詳細統計 (Detailed Statistics)                                  │   │
│  │                                                                 │   │
│  │  總幀數: 2500                                                    │   │
│  │  隊伍 1 持球幀數: 1458 | 進攻幀數: 812                            │   │
│  │  隊伍 2 持球幀數: 1042 | 進攻幀數: 702                            │   │
│  │  隊伍 1 球員數: 10 | 平均每人距離: 1245.3 公尺                     │   │
│  │  隊伍 2 球員數: 10 | 平均每人距離: 1187.2 公尺                     │   │
│  └─────────────────────────────────────────────────────────────────┘   │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
```

## Key Features

### 🎨 Color Coding
- **Black (Bold)** - Possession time (primary metric)
- **Blue** - Attack time (offensive metrics)
- **Green** - Distance metrics (movement data)
- **Purple** - Speed metrics (performance data)

### 📊 Data Display

#### Possession Statistics
- Shows percentage of time each team controls the ball
- Calculated from frame-by-frame ball assignment

#### Attack Statistics
- Shows percentage of time each team is in attacking position
- Defined as possession in opponent's half (past midfield)

#### Distance Statistics ⭐ NEW
- Shows total distance covered by all players on each team
- Measured in kilometers (km)
- Useful for assessing team work rate

#### Speed Statistics ⭐ NEW
- Shows average speed of players on each team
- Measured in kilometers per hour (km/h)
- Useful for assessing team intensity

### 📝 Detailed Summary Box
Provides additional context:
- Total frames analyzed
- Frame counts for possession and attack
- Number of players tracked per team
- Average distance per player

## User Workflow

1. **Run Analysis**
   ```bash
   cd football_analysis-main
   python main.py
   ```
   This generates: `output_data/analysis_data.json`

2. **Open Qt Application**
   ```bash
   cd foot
   ./foot
   ```

3. **Load Data**
   - Click "載入視頻分析數據" button
   - Select the JSON file
   - Data automatically populates all fields

4. **View Results**
   - All statistics displayed at once
   - Color-coded for easy reading
   - Detailed summary at bottom

## Data Interpretation Guide

### Possession Time
- **High % (>60%)** = Dominant team
- **Balanced (45-55%)** = Even match
- **Low % (<40%)** = Defensive team

### Attack Time
- Should always be ≤ Possession time
- **High attack %** = Aggressive playing style
- **Low attack %** = Cautious/defensive style

### Total Distance
- **High distance (>12 km)** = High work rate
- **Typical range: 10-13 km** per team
- More distance = more active team

### Average Speed
- **Typical range: 7-10 km/h**
- Higher speed = faster game pace
- Lower speed = slower/tactical game

## Technical Notes

### UI Components Used
- `QGroupBox` - Main container for video analysis section
- `QPushButton` - Load data button
- `QGridLayout` - 2-column layout for team comparisons
- `QLabel` - Display statistics (8 main labels + 1 summary)

### Font Styling
- **Size:** 11pt for all metric labels
- **Weight:** Bold for emphasis
- **Colors:** RGB values for visual distinction

### Layout Structure
```
QGroupBox (groupBoxVideoAnalysis)
  ├── QPushButton (pushButtonLoadVideoAnalysis)
  ├── QGridLayout (gridLayout)
  │   ├── Row 0: Possession labels (Team 1 & 2)
  │   ├── Row 1: Attack labels (Team 1 & 2)
  │   ├── Row 2: Distance labels (Team 1 & 2) ⭐ NEW
  │   └── Row 3: Speed labels (Team 1 & 2) ⭐ NEW
  └── QLabel (labelVideoAnalysisSummary)
```

## Example Output

### Sample Data Display
When loading `sample_data/sample_analysis.json`:

```
隊伍 1 持球時間: 58.30%     隊伍 2 持球時間: 41.70%
隊伍 1 進攻時間: 32.50%     隊伍 2 進攻時間: 28.10%
隊伍 1 總距離: 12.45 公里   隊伍 2 總距離: 11.87 公里
隊伍 1 平均速度: 8.50 公里/小時   隊伍 2 平均速度: 8.20 公里/小時

總幀數: 2500
隊伍 1 持球幀數: 1458 | 進攻幀數: 812
隊伍 2 持球幀數: 1042 | 進攻幀數: 702
隊伍 1 球員數: 10 | 平均每人距離: 1245.3 公尺
隊伍 2 球員數: 10 | 平均每人距離: 1187.2 公尺
```

## Benefits of This Integration

1. ✅ **Complete Picture** - All key metrics in one view
2. ✅ **Easy Comparison** - Side-by-side team statistics
3. ✅ **Visual Clarity** - Color coding for quick understanding
4. ✅ **Detailed Context** - Summary box provides full picture
5. ✅ **Professional Look** - Clean, organized layout
6. ✅ **User Friendly** - Simple one-button data loading
