# Video Analysis UI Integration - Quick Start Guide
# 視頻分析 UI 整合 - 快速入門指南

## What's New? / 新功能

This update integrates the football video analysis system with the Qt UI interface, allowing you to view:
- **Possession Time** (持球時間): How long each team controls the ball
- **Attack Time** (進攻時間): How long each team has possession past the half field

本次更新將足球視頻分析系統與 Qt UI 介面整合，讓您可以查看：
- **持球時間**：每隊控球的時長
- **進攻時間**：每隊在過半場後持球的時長

## Quick Start / 快速開始

### Step 1: Analyze a Video / 步驟 1：分析視頻

```bash
cd football_analysis-main
python main.py
```

This creates: `output_data/analysis_data.json`

### Step 2: View Results in Qt UI / 步驟 2：在 Qt UI 中查看結果

```bash
cd ../foot
qmake
make
./foot
```

In the application:
1. Scroll to the "視頻分析數據" section
2. Click "載入視頻分析數據"
3. Select `output_data/analysis_data.json`
4. View the statistics!

## What You'll See / 您將看到什麼

```
┌─────────────────────────────────────────┐
│ 視頻分析數據                              │
├─────────────────────────────────────────┤
│                                         │
│ 隊伍 1 持球時間: 58.30%                  │
│ 隊伍 2 持球時間: 41.70%                  │
│                                         │
│ 隊伍 1 進攻時間: 32.50%                  │
│ 隊伍 2 進攻時間: 28.10%                  │
│                                         │
│ 詳細摘要:                                │
│ 總幀數: 2500                             │
│ 隊伍 1 持球幀數: 1458                    │
│ 隊伍 2 持球幀數: 1042                    │
│ 隊伍 1 進攻幀數: 812                     │
│ 隊伍 2 進攻幀數: 702                     │
└─────────────────────────────────────────┘
```

## Understanding the Metrics / 理解指標

### Possession Time / 持球時間
The percentage of time each team has control of the ball.
**Formula**: (Team frames with ball / Total controlled frames) × 100%

每隊控球的時間百分比。
**公式**：(該隊持球幀數 / 總控球幀數) × 100%

### Attack Time / 進攻時間
The percentage of time each team has possession in the attacking half (past the half field line).
**Formula**: (Team attack frames / Total controlled frames) × 100%

每隊在進攻半場（過半場線）持球的時間百分比。
**公式**：(該隊進攻幀數 / 總控球幀數) × 100%

**Attack Definition / 進攻定義:**
- Team 1 attacks left → right: attacking when ball x > 11.66m
- Team 2 attacks right → left: attacking when ball x < 11.66m

## Testing Without Video Analysis / 不運行視頻分析的測試

Want to test the UI without running the full analysis? Use the sample data:

想在不運行完整分析的情況下測試 UI？使用示例數據：

```bash
cd foot
./foot
# Load: ../sample_data/sample_analysis.json
```

## Documentation / 文檔

Detailed documentation is available in:
- `VIDEO_ANALYSIS_INTEGRATION.md` - Complete user guide
- `UI_DESIGN_MOCKUP.md` - UI design and layout
- `IMPLEMENTATION_SUMMARY.md` - Technical implementation details

詳細文檔可查看：
- `VIDEO_ANALYSIS_INTEGRATION.md` - 完整用戶指南
- `UI_DESIGN_MOCKUP.md` - UI 設計和佈局
- `IMPLEMENTATION_SUMMARY.md` - 技術實現細節

## Testing / 測試

Run the test suite to verify everything works:
運行測試套件以驗證一切正常：

```bash
# Test attack time calculation logic
python3 test_data_exporter.py

# Test Qt data loading logic
python3 test_qt_loading.py
```

Both should output: ✓ All tests PASSED!

## Troubleshooting / 故障排除

### Problem: JSON file won't load
**Solution**: Make sure you selected the correct file from `output_data/analysis_data.json`

### Problem: Attack time shows 0%
**Solution**: This might be normal if teams rarely cross the half field line. Check that the video analysis completed successfully.

### Problem: Qt application won't build
**Solution**: Make sure Qt development tools are installed:
```bash
# Ubuntu/Debian
sudo apt-get install qt5-default

# macOS
brew install qt5
```

## Support / 支持

For more help:
- Check the documentation files listed above
- Review the test scripts for examples
- Examine the sample data structure

需要更多幫助：
- 查看上述列出的文檔文件
- 查看測試腳本以獲取示例
- 檢查示例數據結構

---

**Version**: 1.0
**Date**: 2025-12-29
**Status**: ✅ Complete and Tested
