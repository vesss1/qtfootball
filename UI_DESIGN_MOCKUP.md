# Qt UI Mockup - Video Analysis Section
# Qt UI 模擬圖 - 視頻分析部分

```
┌─────────────────────────────────────────────────────────────────────┐
│ 足球球員管理系統 (Football Player Management System)                │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│ [Player Management Section - 球員管理區塊]                           │
│ ┌─────────────────────────────────────────────────────────────┐    │
│ │ Name: [____________]  Position: [前鋒 ▼]  Age: [20 ▲▼]      │    │
│ │ [  新增球員  ]                                                │    │
│ └─────────────────────────────────────────────────────────────┘    │
│                                                                     │
│ [Players Table - 球員列表]                                           │
│ ┌─────────────────────────────────────────────────────────────┐    │
│ │ 姓名    │ 位置  │ 年齡                                       │    │
│ │─────────────────────────────────────────────────────────────│    │
│ │ 張三    │ 前鋒  │ 25                                         │    │
│ │ 李四    │ 中場  │ 23                                         │    │
│ └─────────────────────────────────────────────────────────────┘    │
│                                                                     │
│ [Practice Tracking - 進球練習記錄]                                   │
│ ┌─────────────────────────────────────────────────────────────┐    │
│ │ ... (existing practice tracking features) ...               │    │
│ └─────────────────────────────────────────────────────────────┘    │
│                                                                     │
│ [Statistics - 數據分析]                                              │
│ ┌─────────────────────────────────────────────────────────────┐    │
│ │ ... (existing statistics table) ...                         │    │
│ └─────────────────────────────────────────────────────────────┘    │
│                                                                     │
│ ┌─────────────────────────────────────────────────────────────┐    │
│ │ ★ 視頻分析數據 (Video Analysis Data) ★                       │    │
│ ├─────────────────────────────────────────────────────────────┤    │
│ │                                                             │    │
│ │  [  載入視頻分析數據 (Load Video Analysis Data)  ]            │    │
│ │                                                             │    │
│ │  ┌───────────────────────────┬───────────────────────────┐  │    │
│ │  │ 隊伍 1 持球時間: 58.30%    │ 隊伍 2 持球時間: 41.70%   │  │    │
│ │  │ (Team 1 Possession)       │ (Team 2 Possession)      │  │    │
│ │  └───────────────────────────┴───────────────────────────┘  │    │
│ │                                                             │    │
│ │  ┌───────────────────────────┬───────────────────────────┐  │    │
│ │  │ 隊伍 1 進攻時間: 32.50%    │ 隊伍 2 進攻時間: 28.10%   │  │    │
│ │  │ (Team 1 Attack Time)      │ (Team 2 Attack Time)     │  │    │
│ │  │ [Blue colored text]       │ [Blue colored text]      │  │    │
│ │  └───────────────────────────┴───────────────────────────┘  │    │
│ │                                                             │    │
│ │  Summary / 詳細摘要:                                         │    │
│ │  ┌───────────────────────────────────────────────────────┐  │    │
│ │  │ 總幀數: 2500                                           │  │    │
│ │  │ 隊伍 1 持球幀數: 1458                                   │  │    │
│ │  │ 隊伍 2 持球幀數: 1042                                   │  │    │
│ │  │ 隊伍 1 進攻幀數: 812                                    │  │    │
│ │  │ 隊伍 2 進攻幀數: 702                                    │  │    │
│ │  └───────────────────────────────────────────────────────┘  │    │
│ │                                                             │    │
│ └─────────────────────────────────────────────────────────────┘    │
│                                                                     │
└─────────────────────────────────────────────────────────────────────┘
```

## UI Elements Description / UI 元素說明

### Video Analysis Section / 視頻分析部分

1. **Load Button / 載入按鈕**
   - Text: "載入視頻分析數據"
   - Function: Opens file dialog to select JSON analysis file
   - 功能：打開文件對話框選擇 JSON 分析文件

2. **Possession Time Display / 持球時間顯示**
   - Two labels side by side in a grid layout
   - Bold font (11pt)
   - Shows Team 1 and Team 2 possession percentages
   - 並排顯示兩個標籤
   - 粗體字（11pt）
   - 顯示隊伍 1 和隊伍 2 的持球百分比

3. **Attack Time Display / 進攻時間顯示**
   - Two labels side by side in a grid layout
   - Bold font (11pt)
   - Blue colored text (RGB: 0, 120, 215)
   - Shows Team 1 and Team 2 attack time percentages
   - 並排顯示兩個標籤
   - 粗體字（11pt）
   - 藍色文字（RGB: 0, 120, 215）
   - 顯示隊伍 1 和隊伍 2 的進攻時間百分比

4. **Summary Box / 摘要框**
   - Multi-line label with detailed statistics
   - Shows frame counts for each metric
   - Word wrap enabled for better display
   - 多行標籤顯示詳細統計
   - 顯示每個指標的幀數
   - 啟用自動換行以便更好地顯示

## Data Flow / 數據流

```
┌─────────────────┐
│  Input Video    │
│  輸入視頻        │
└────────┬────────┘
         │
         ▼
┌─────────────────────────────────┐
│  Python Analysis                │
│  (football_analysis-main/)      │
│  Python 分析                    │
│  - Track players & ball         │
│  - Calculate possession         │
│  - Calculate attack time        │
└────────┬────────────────────────┘
         │
         ▼
┌─────────────────────────────────┐
│  JSON Export                    │
│  (analysis_data.json)           │
│  JSON 導出                      │
│  - Team possession %            │
│  - Team attack %                │
│  - Frame counts                 │
└────────┬────────────────────────┘
         │
         ▼
┌─────────────────────────────────┐
│  Qt UI Application              │
│  (foot/)                        │
│  Qt UI 應用程序                  │
│  - Load JSON file               │
│  - Parse statistics             │
│  - Display in UI                │
└─────────────────────────────────┘
```

## Color Scheme / 色彩方案

- **Possession Labels**: Black text, bold
  - 持球標籤：黑色文字，粗體
  
- **Attack Labels**: Blue text (RGB: 0, 120, 215), bold
  - 進攻標籤：藍色文字（RGB: 0, 120, 215），粗體
  
- **Summary Text**: Black text, normal weight
  - 摘要文字：黑色文字，正常字重

## Layout Structure / 佈局結構

```
QGroupBox (Video Analysis / 視頻分析數據)
└── QVBoxLayout
    ├── QPushButton (Load Button / 載入按鈕)
    ├── QGridLayout (2x2 grid for statistics / 統計數據 2x2 網格)
    │   ├── QLabel [0,0] (Team 1 Possession / 隊伍 1 持球)
    │   ├── QLabel [0,1] (Team 2 Possession / 隊伍 2 持球)
    │   ├── QLabel [1,0] (Team 1 Attack / 隊伍 1 進攻)
    │   └── QLabel [1,1] (Team 2 Attack / 隊伍 2 進攻)
    └── QLabel (Summary / 摘要)
```

## User Interaction Flow / 用戶交互流程

1. User clicks "載入視頻分析數據" button
   用戶點擊「載入視頻分析數據」按鈕

2. File dialog opens to select JSON file
   打開文件對話框選擇 JSON 文件

3. User selects `analysis_data.json`
   用戶選擇 `analysis_data.json`

4. Application loads and parses JSON
   應用程序載入並解析 JSON

5. UI updates with statistics:
   UI 更新顯示統計數據：
   - Possession percentages / 持球百分比
   - Attack time percentages / 進攻時間百分比
   - Detailed frame counts / 詳細幀數統計

6. User can view all statistics at a glance
   用戶可以一目了然地查看所有統計數據

## Benefits / 優點

✓ **Clear Visual Separation** / 清晰的視覺分離
  - Video analysis data is in its own section
  - 視頻分析數據有自己的專用區域

✓ **Easy to Understand** / 易於理解
  - Percentages are prominently displayed
  - 百分比醒目顯示
  - Attack time uses blue color for emphasis
  - 進攻時間使用藍色突出顯示

✓ **Comprehensive Information** / 全面的資訊
  - Both percentages and frame counts shown
  - 同時顯示百分比和幀數
  - Summary provides detailed breakdown
  - 摘要提供詳細分類

✓ **Flexible Data Source** / 靈活的數據來源
  - Can load any analysis JSON file
  - 可以載入任何分析 JSON 文件
  - Easy to analyze multiple videos
  - 易於分析多個視頻
