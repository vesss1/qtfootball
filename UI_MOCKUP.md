# UI Mockup - Goal-Scoring Practice Tracker

This document shows what the implemented UI interface will look like when the Qt application is built and run.

## Main Window Layout

```
┌────────────────────────────────────────────────────────────────────────┐
│  足球球員管理系統 (Football Player Management System)                    │
├────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│  ┌─ 球員資訊 (Player Information) ──────────────────────────────────┐  │
│  │                                                                   │  │
│  │  球員姓名:  [_____________________]                                │  │
│  │  位置:      [前鋒 ▼]                                              │  │
│  │  年齡:      [20]                                                  │  │
│  │                                                                   │  │
│  │  [    新增球員    ]                                               │  │
│  └───────────────────────────────────────────────────────────────────┘  │
│                                                                         │
│  ┌─ 球員列表 (Player List) ─────────────────────────────────────────┐  │
│  │ ┌─────────┬────────────┬────────┐                               │  │
│  │ │ 姓名    │ 位置       │ 年齡   │                               │  │
│  │ ├─────────┼────────────┼────────┤                               │  │
│  │ │ 張三    │ 前鋒       │ 25     │                               │  │
│  │ │ 李四    │ 中場       │ 23     │                               │  │
│  │ │ 王五    │ 後衛       │ 27     │                               │  │
│  │ └─────────┴────────────┴────────┘                               │  │
│  └───────────────────────────────────────────────────────────────────┘  │
│                                                                         │
│  ┌─ 進球練習記錄 (Goal Practice Recording) ─────────────────────────┐  │
│  │                                                                   │  │
│  │  選擇球員:       [張三 ▼]                                         │  │
│  │  距離(碼):       [8]                                              │  │
│  │  計劃嘗試次數:   [5]                                              │  │
│  │                                                                   │  │
│  │  [    開始練習    ]                                               │  │
│  │                                                                   │  │
│  │  ┌───────────────────────────────────────────────────────────┐  │  │
│  │  │         尚未開始練習                                       │  │  │
│  │  │  (When active, shows real-time stats:)                    │  │  │
│  │  │  進行中 - 張三                                             │  │  │
│  │  │  距離: 8 碼 | 進度: 3/5                                   │  │  │
│  │  │  成功: 2 | 成功率: 66.7% | 時間: 23.5 秒                 │  │  │
│  │  └───────────────────────────────────────────────────────────┘  │  │
│  │                                                                   │  │
│  │  [  記錄成功進球  ]  [  記錄未進球  ]                             │  │
│  │  [    結束練習    ]                                               │  │
│  └───────────────────────────────────────────────────────────────────┘  │
│                                                                         │
│  ┌─ 數據分析 (Data Analysis) ───────────────────────────────────────┐  │
│  │                                                                   │  │
│  │  [  顯示統計數據  ]                                               │  │
│  │                                                                   │  │
│  │  ┌─────┬────────┬──────┬────────┬──────────┬────────┐          │  │
│  │  │球員 │距離(碼)│總嘗試│成功    │成功率(%) │時間(秒)│          │  │
│  │  ├─────┼────────┼──────┼────────┼──────────┼────────┤          │  │
│  │  │張三 │   8    │  5   │  3     │   60.0   │  45.3  │          │  │
│  │  │張三 │   8    │  5   │  4     │   80.0   │  38.2  │          │  │
│  │  │李四 │  10    │  5   │  2     │   40.0   │  52.1  │          │  │
│  │  │王五 │   8    │  5   │  5     │  100.0   │  35.8  │          │  │
│  │  └─────┴────────┴──────┴────────┴──────────┴────────┘          │  │
│  └───────────────────────────────────────────────────────────────────┘  │
│                                                                         │
└────────────────────────────────────────────────────────────────────────┘
```

## UI States and Flow

### State 1: Initial State
- Practice section shows "尚未開始練習" (Practice not started)
- "開始練習" button is enabled
- "記錄成功進球", "記錄未進球", "結束練習" buttons are disabled
- All input fields are enabled

### State 2: Practice In Progress
- Timer is running
- Real-time display shows:
  - Current player name
  - Distance setting
  - Progress (e.g., 3/5)
  - Successful goals count
  - Current success rate
  - Elapsed time
- "開始練習" button is disabled
- "記錄成功進球", "記錄未進球", "結束練習" buttons are enabled
- Player selection and distance/attempts fields are disabled

### State 3: Practice Completed
- Summary dialog appears showing:
  ```
  練習完成！
  
  球員: 張三
  距離: 8 碼
  總嘗試: 5 次
  成功進球: 3 次
  成功率: 60.0%
  花費時間: 45.3 秒
  ```
- Returns to State 1
- Statistics table is automatically updated

## User Interaction Flow

```
Start
  │
  ├─→ 1. Add players (if not already added)
  │     │
  │     └─→ Enter name, position, age → Click "新增球員"
  │
  ├─→ 2. Start practice session
  │     │
  │     ├─→ Select player from dropdown
  │     ├─→ Set distance (default: 8 yards)
  │     ├─→ Set planned attempts (default: 5)
  │     └─→ Click "開始練習"
  │
  ├─→ 3. Record attempts
  │     │
  │     ├─→ For each kick:
  │     │     │
  │     │     ├─→ If goal: Click "記錄成功進球"
  │     │     └─→ If miss: Click "記錄未進球"
  │     │
  │     └─→ System updates real-time display after each attempt
  │
  ├─→ 4. End practice
  │     │
  │     ├─→ Manual: Click "結束練習" anytime
  │     └─→ Automatic: When reaching planned attempts count
  │           │
  │           └─→ System shows completion notification
  │
  ├─→ 5. View summary
  │     │
  │     └─→ Dialog shows complete practice session results
  │
  └─→ 6. View statistics
        │
        └─→ Click "顯示統計數據" to see all practice sessions
```

## Color Scheme (Default Qt Theme)
- Background: Light gray (#F0F0F0)
- Buttons: Blue when enabled (#0078D7), Gray when disabled
- Text: Black (#000000)
- Tables: White background with gray borders
- Group boxes: Light border with title

## Button States

### "開始練習" (Start Practice)
- **Enabled**: When no practice is in progress
- **Disabled**: During active practice session

### "記錄成功進球" / "記錄未進球" (Record Goal/Miss)
- **Enabled**: During active practice session
- **Disabled**: When no practice is in progress

### "結束練習" (End Practice)
- **Enabled**: During active practice session
- **Disabled**: When no practice is in progress

### "顯示統計數據" (Show Statistics)
- **Always Enabled**: Can view statistics anytime

## Window Size
- Width: 900 pixels
- Height: 800 pixels
- Resizable: Yes (standard Qt window)

## Accessibility Features
- Tab navigation through all input fields
- Keyboard shortcuts for buttons
- Clear visual feedback for button states
- Large, readable fonts
- Logical tab order

## Example Usage Scenario

**Scenario**: Coach wants to track player's 8-yard goal-scoring practice

1. Coach opens the application
2. Adds player "張三" (if not already in system)
3. Navigates to "進球練習記錄" section
4. Selects "張三" from dropdown
5. Confirms distance is 8 yards
6. Sets planned attempts to 5
7. Clicks "開始練習"
8. Timer starts, real-time display begins updating
9. For each kick:
   - Ball goes in → Clicks "記錄成功進球"
   - Ball misses → Clicks "記錄未進球"
10. After 5 attempts, system automatically shows completion dialog
11. Reviews the summary (e.g., 3 out of 5 = 60% success rate in 45.3 seconds)
12. Clicks "顯示統計數據" to see all practice history
13. Can compare this session with previous sessions

## Data Persistence Note
⚠️ **Important**: In the current implementation, data is stored in memory only. When the application closes, all practice session data is lost. For production use, consider adding:
- Database storage (SQLite)
- File export/import (CSV, JSON)
- Auto-save functionality
- Session recovery after crash

## Future Enhancement Possibilities
- Charts showing progress over time
- Comparison between players
- Goal probability heatmaps by distance
- Practice recommendations based on performance
- Export reports to PDF
- Video recording integration
- Multi-session training programs
