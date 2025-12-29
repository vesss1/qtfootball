# Video Analysis Integration Guide
# 視頻分析整合指南

## Overview / 概述

This document explains how to integrate football video analysis output with the Qt UI interface to display possession time and attack time statistics for both teams.

本文檔說明如何將足球視頻分析輸出與 Qt UI 介面整合，以顯示兩隊的持球時間和進攻時間統計數據。

## Features / 功能

### 1. Attack Time Calculation / 進攻時間計算

**New Feature**: The Python analysis system now calculates attack time for both teams.

**新功能**：Python 分析系統現在可以計算兩隊的進攻時間。

- **Team 1 Attack / 隊伍 1 進攻**: When Team 1 has possession AND the ball is past the half field line (x > 11.66m)
- **Team 2 Attack / 隊伍 2 進攻**: When Team 2 has possession AND the ball is past the half field line (x < 11.66m)

**Field Layout / 場地佈局**:
```
Team 1 Side         Half Field          Team 2 Side
│                      │                      │
│<------ 11.66m ------>│<------ 11.66m ------>│
│                      │                      │
x=0                 x=11.66               x=23.32
```

### 2. Data Export / 數據導出

The `data_exporter.py` now exports additional metrics:

`data_exporter.py` 現在導出額外的指標：

**JSON Format** (`output_data/analysis_data.json`):
```json
{
  "metadata": {
    "total_frames": 2500,
    "team_1_ball_control_percent": 58.3,
    "team_2_ball_control_percent": 41.7,
    "team_1_attack_percent": 32.5,
    "team_2_attack_percent": 28.1,
    "team_1_attack_frames": 812,
    "team_2_attack_frames": 702
  }
}
```

**CSV Format** (`output_data/csv/ball_control_stats.csv`):
```csv
metric,value
team_1_attack_frames,812
team_2_attack_frames,702
team_1_attack_percent,32.5
team_2_attack_percent,28.1
```

### 3. Qt UI Integration / Qt UI 整合

A new "Video Analysis Data" section has been added to the Qt UI:

Qt UI 中新增了「視頻分析數據」部分：

**Features / 功能**:
- Load JSON analysis data / 載入 JSON 分析數據
- Display possession time for both teams / 顯示兩隊持球時間
- Display attack time for both teams / 顯示兩隊進攻時間
- Show detailed frame statistics / 顯示詳細幀統計

## Usage Instructions / 使用說明

### Step 1: Run Python Analysis / 步驟 1：運行 Python 分析

```bash
cd football_analysis-main
python main.py
```

This will:
1. Analyze the video
2. Calculate possession and attack time
3. Export data to `output_data/analysis_data.json`

這將：
1. 分析視頻
2. 計算持球和進攻時間
3. 將數據導出到 `output_data/analysis_data.json`

### Step 2: Open Qt Application / 步驟 2：打開 Qt 應用程序

```bash
cd foot
# Build and run the application
qmake
make
./foot
```

### Step 3: Load Analysis Data / 步驟 3：載入分析數據

1. Click "載入視頻分析數據" button / 點擊「載入視頻分析數據」按鈕
2. Select the JSON file (e.g., `output_data/analysis_data.json`)
3. View the statistics displayed in the UI

1. 點擊「載入視頻分析數據」按鈕
2. 選擇 JSON 文件（例如 `output_data/analysis_data.json`）
3. 查看 UI 中顯示的統計數據

## UI Display / UI 顯示

The Video Analysis section shows:

視頻分析部分顯示：

1. **隊伍 1 持球時間** (Team 1 Possession Time): Percentage of time Team 1 has the ball
2. **隊伍 2 持球時間** (Team 2 Possession Time): Percentage of time Team 2 has the ball
3. **隊伍 1 進攻時間** (Team 1 Attack Time): Percentage of time Team 1 is attacking (possession past half field)
4. **隊伍 2 進攻時間** (Team 2 Attack Time): Percentage of time Team 2 is attacking (possession past half field)
5. **Summary / 摘要**: Detailed frame counts for possession and attack

## Testing / 測試

### Test the Python Logic / 測試 Python 邏輯

A test script is provided to verify the attack time calculation:

提供了一個測試腳本來驗證進攻時間計算：

```bash
python3 test_data_exporter.py
```

### Test with Sample Data / 使用示例數據測試

A sample JSON file is provided for testing the Qt UI:

提供了一個示例 JSON 文件用於測試 Qt UI：

```
sample_data/sample_analysis.json
```

You can load this file in the Qt application to see how the data is displayed.

您可以在 Qt 應用程序中載入此文件以查看數據的顯示方式。

## Technical Details / 技術細節

### Modified Files / 修改的文件

1. **football_analysis-main/utils/data_exporter.py**
   - Added attack time calculation logic
   - Updated JSON and CSV export to include attack metrics

2. **foot/mainwindow.h**
   - Added `VideoAnalysisData` struct
   - Added methods for loading and displaying video analysis data

3. **foot/mainwindow.cpp**
   - Implemented JSON data loading
   - Implemented UI display updates
   - Added file dialog for selecting JSON files

4. **foot/mainwindow.ui**
   - Added "Video Analysis Data" group box
   - Added labels for possession and attack time
   - Added button to load analysis data

### Attack Time Logic / 進攻時間邏輯

```python
half_field = 11.66  # meters

for each frame:
    if team_control == 1 and ball_x > half_field:
        team_1_attack_frames += 1
    elif team_control == 2 and ball_x < half_field:
        team_2_attack_frames += 1
```

## Troubleshooting / 故障排除

### Issue: JSON file won't load / 問題：JSON 文件無法載入

**Solution / 解決方案**:
1. Verify the JSON file exists
2. Check that the file has the correct structure with "metadata" field
3. Ensure the file path is correct

### Issue: Attack time shows 0% / 問題：進攻時間顯示為 0%

**Solution / 解決方案**:
1. Check if the video analysis completed successfully
2. Verify that `position_transformed` data is available in the tracks
3. Ensure the view transformer is properly initialized in `main.py`

## Future Enhancements / 未來增強功能

Possible improvements:
- Add graphical visualization of possession/attack time over time
- Add player heatmaps
- Add more detailed statistics (e.g., average attack duration)
- Real-time video playback with statistics overlay

可能的改進：
- 添加持球/進攻時間隨時間變化的圖形化視覺效果
- 添加球員熱圖
- 添加更詳細的統計數據（例如平均進攻持續時間）
- 實時視頻播放與統計疊加

## Support / 支持

For issues or questions, please:
- Check this documentation
- Review the test scripts
- Examine the sample data files

如有問題或疑問，請：
- 查看本文檔
- 查看測試腳本
- 檢查示例數據文件
