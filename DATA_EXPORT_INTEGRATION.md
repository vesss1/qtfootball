# Football Analysis Data Export and Qt UI Integration - Complete Guide

## 概述 (Overview)

本指南說明如何將足球視頻分析的輸出數據（持球時間百分比、進攻時間百分比、總跑步距離、平均速度）與 Qt UI 整合。

This guide explains how to integrate football video analysis output data (possession percentages, attack percentages, total distance, average speed) with the Qt UI.

---

## 新功能 (New Features)

### 1. 數據導出模組 (Data Export Module)

新增 `football_analysis-main/utils/data_exporter.py` 模組，提供完整的數據導出功能。

**功能 (Features):**
- ✅ 持球時間統計 (Ball possession statistics)
- ✅ 進攻時間統計 (Attack time statistics)
- ✅ 距離統計 (Distance statistics) - **新增 (NEW)**
- ✅ 速度統計 (Speed statistics) - **新增 (NEW)**
- ✅ JSON 格式導出 (JSON export)
- ✅ CSV 格式導出 (CSV export)

### 2. Qt UI 增強 (Qt UI Enhancements)

Qt 介面現在可以顯示以下數據：

**原有功能 (Existing):**
- 隊伍 1 & 2 持球時間百分比 (Team 1 & 2 possession %)
- 隊伍 1 & 2 進攻時間百分比 (Team 1 & 2 attack %)

**新增功能 (NEW):**
- 隊伍 1 & 2 總跑步距離 (公里) (Team 1 & 2 total distance in km)
- 隊伍 1 & 2 平均速度 (公里/小時) (Team 1 & 2 average speed in km/h)

---

## 使用方法 (Usage Instructions)

### 步驟 1: 執行視頻分析 (Step 1: Run Video Analysis)

```bash
cd football_analysis-main
python main.py
```

這會：
1. 分析輸入視頻
2. 計算所有統計數據（持球、進攻、距離、速度）
3. 自動導出數據到：
   - `output_data/analysis_data.json` (JSON 格式)
   - `output_data/csv/*.csv` (CSV 格式)

### 步驟 2: 打開 Qt 應用程序 (Step 2: Open Qt Application)

```bash
cd foot
qmake
make
./foot
```

### 步驟 3: 載入分析數據 (Step 3: Load Analysis Data)

1. 點擊「載入視頻分析數據」按鈕
2. 選擇 JSON 文件（如 `output_data/analysis_data.json`）
3. 數據將自動顯示在 UI 上

---

## 數據格式 (Data Format)

### JSON 輸出格式 (JSON Output Format)

```json
{
  "metadata": {
    "total_frames": 2500,
    "description": "Football analysis data exported from video processing",
    
    // 持球統計 (Possession Statistics)
    "team_1_ball_control_percent": 58.3,
    "team_2_ball_control_percent": 41.7,
    "team_1_frames": 1458,
    "team_2_frames": 1042,
    
    // 進攻統計 (Attack Statistics)
    "team_1_attack_percent": 32.5,
    "team_2_attack_percent": 28.1,
    "team_1_attack_frames": 812,
    "team_2_attack_frames": 702,
    
    // 距離統計 (Distance Statistics) - NEW
    "team_1_total_distance_km": 12.45,
    "team_2_total_distance_km": 11.87,
    "team_1_avg_distance_per_player_m": 1245.3,
    "team_2_avg_distance_per_player_m": 1187.2,
    
    // 速度統計 (Speed Statistics) - NEW
    "team_1_avg_speed_kmh": 8.5,
    "team_2_avg_speed_kmh": 8.2,
    "team_1_player_count": 10,
    "team_2_player_count": 10
  },
  "frames": []
}
```

### CSV 輸出文件 (CSV Output Files)

系統會生成以下 CSV 文件：

1. **ball_control_stats.csv** - 持球統計
2. **attack_stats.csv** - 進攻統計
3. **distance_speed_stats.csv** - 距離與速度統計 (NEW)

---

## Qt UI 顯示 (Qt UI Display)

### 視頻分析數據區塊 (Video Analysis Data Section)

```
┌─ 視頻分析數據 ─────────────────────────────┐
│                                           │
│  [載入視頻分析數據]                        │
│                                           │
│  隊伍 1 持球時間: 58.30%  │ 隊伍 2 持球時間: 41.70%  │
│  隊伍 1 進攻時間: 32.50%  │ 隊伍 2 進攻時間: 28.10%  │
│  隊伍 1 總距離: 12.45 公里 │ 隊伍 2 總距離: 11.87 公里 │  ← NEW
│  隊伍 1 平均速度: 8.50 公里/小時 │ 隊伍 2 平均速度: 8.20 公里/小時 │  ← NEW
│                                           │
│  總幀數: 2500                             │
│  隊伍 1 持球幀數: 1458 | 進攻幀數: 812      │
│  隊伍 2 持球幀數: 1042 | 進攻幀數: 702      │
│  隊伍 1 球員數: 10 | 平均每人距離: 1245.3 公尺 │  ← NEW
│  隊伍 2 球員數: 10 | 平均每人距離: 1187.2 公尺 │  ← NEW
│                                           │
└───────────────────────────────────────────┘
```

---

## 技術細節 (Technical Details)

### 修改的文件 (Modified Files)

#### Python 端 (Python Side):

1. **football_analysis-main/utils/data_exporter.py** (NEW)
   - 新增完整的數據導出類別
   - 實現持球、進攻、距離、速度統計計算
   - 支援 JSON 和 CSV 格式導出

2. **football_analysis-main/utils/__init__.py**
   - 加入 DataExporter 導出

3. **football_analysis-main/main.py**
   - 整合 DataExporter
   - 在視頻分析完成後自動導出數據

#### Qt 端 (Qt Side):

4. **foot/mainwindow.h**
   - VideoAnalysisData 結構新增距離和速度欄位

5. **foot/mainwindow.cpp**
   - loadVideoAnalysisData() 解析新的 JSON 欄位
   - displayVideoAnalysisData() 顯示距離和速度數據

6. **foot/mainwindow.ui**
   - 新增 4 個標籤顯示距離和速度數據
   - 使用不同顏色區分不同類型的數據

#### 測試文件 (Test Files):

7. **sample_data/sample_analysis.json**
   - 更新範例數據包含新欄位

8. **test_qt_loading.py**
   - 更新測試腳本驗證新欄位

### 距離和速度計算邏輯 (Distance and Speed Calculation Logic)

```python
# 從最後一幀獲取累積數據
for player_id, player_data in last_frame.items():
    team = player_data.get('team')
    distance = player_data.get('distance', 0)  # 公尺 (meters)
    speed = player_data.get('speed', 0)        # 公里/小時 (km/h)
    
    if team == 1:
        team_1_distances.append(distance)
        team_1_speeds.append(speed)
    elif team == 2:
        team_2_distances.append(distance)
        team_2_speeds.append(speed)

# 計算總距離和平均值
team_1_total_distance_km = sum(team_1_distances) / 1000  # 轉換為公里
team_1_avg_speed_kmh = mean(team_1_speeds)
```

---

## 測試 (Testing)

### 測試 Python 邏輯 (Test Python Logic)

```bash
# 測試數據導出邏輯
python3 test_data_exporter.py

# 測試 Qt 數據載入
python3 test_qt_loading.py
```

### 使用範例數據測試 (Test with Sample Data)

範例 JSON 文件可用於測試 Qt UI：
```
sample_data/sample_analysis.json
```

在 Qt 應用程序中載入此文件以查看數據顯示效果。

---

## 故障排除 (Troubleshooting)

### 問題: 距離或速度顯示為 0

**可能原因:**
1. 視頻分析未完成速度和距離計算
2. tracks 數據中缺少 'distance' 或 'speed' 欄位

**解決方案:**
1. 確保 `speed_and_distance_estimator.add_speed_and_distance_to_tracks(tracks)` 已執行
2. 檢查 `view_transformer.add_transformed_position_to_tracks(tracks)` 已執行
3. 確認輸入視頻品質足夠進行追蹤

### 問題: JSON 文件無法載入

**解決方案:**
1. 驗證 JSON 文件存在
2. 檢查文件結構包含 "metadata" 欄位
3. 確認所有必要欄位都存在
4. 確保文件路徑正確

### 問題: Qt UI 不顯示新標籤

**解決方案:**
1. 確保已重新編譯 Qt 應用程序
2. 檢查 mainwindow.ui 是否包含新標籤
3. 運行 `qmake && make clean && make`

---

## 未來增強 (Future Enhancements)

可能的改進方向：

1. **即時分析** - 在視頻分析過程中即時更新 UI
2. **歷史比較** - 比較多場比賽的統計數據
3. **球員個人統計** - 顯示個別球員的詳細數據
4. **圖表可視化** - 使用圖表展示統計數據
5. **導出報告** - 生成 PDF 或 Word 格式的分析報告

---

## 聯絡資訊 (Contact)

如有問題或建議，請在 GitHub 上開 issue。

For questions or suggestions, please open an issue on GitHub.
