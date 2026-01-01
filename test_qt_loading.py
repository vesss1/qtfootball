#!/usr/bin/env python3
"""
Test script to validate the Qt UI data loading logic
"""

import json

def test_qt_data_loading():
    """
    Simulate the Qt UI JSON loading logic
    """
    print("="*60)
    print("Qt UI Data Loading Test")
    print("="*60 + "\n")
    
    # Load the sample JSON file
    with open('sample_data/sample_analysis.json', 'r') as f:
        data = json.load(f)
    
    # Check if 'metadata' exists (like the Qt code does)
    if 'metadata' not in data:
        print("✗ FAIL: No 'metadata' field in JSON")
        return False
    
    metadata = data['metadata']
    
    # Extract all the fields (like the Qt code does)
    video_data = {
        'totalFrames': metadata.get('total_frames', 0),
        'team1PossessionPercent': metadata.get('team_1_ball_control_percent', 0.0),
        'team2PossessionPercent': metadata.get('team_2_ball_control_percent', 0.0),
        'team1PossessionFrames': metadata.get('team_1_frames', 0),
        'team2PossessionFrames': metadata.get('team_2_frames', 0),
        'team1AttackPercent': metadata.get('team_1_attack_percent', 0.0),
        'team2AttackPercent': metadata.get('team_2_attack_percent', 0.0),
        'team1AttackFrames': metadata.get('team_1_attack_frames', 0),
        'team2AttackFrames': metadata.get('team_2_attack_frames', 0),
        'team1TotalDistanceKm': metadata.get('team_1_total_distance_km', 0.0),
        'team2TotalDistanceKm': metadata.get('team_2_total_distance_km', 0.0),
        'team1AvgSpeedKmh': metadata.get('team_1_avg_speed_kmh', 0.0),
        'team2AvgSpeedKmh': metadata.get('team_2_avg_speed_kmh', 0.0),
        'team1PlayerCount': metadata.get('team_1_player_count', 0),
        'team2PlayerCount': metadata.get('team_2_player_count', 0)
    }
    
    print("Loaded data:")
    print(f"  Total Frames: {video_data['totalFrames']}")
    print(f"\nPossession Statistics:")
    print(f"  Team 1: {video_data['team1PossessionPercent']:.2f}% ({video_data['team1PossessionFrames']} frames)")
    print(f"  Team 2: {video_data['team2PossessionPercent']:.2f}% ({video_data['team2PossessionFrames']} frames)")
    print(f"\nAttack Statistics:")
    print(f"  Team 1: {video_data['team1AttackPercent']:.2f}% ({video_data['team1AttackFrames']} frames)")
    print(f"  Team 2: {video_data['team2AttackPercent']:.2f}% ({video_data['team2AttackFrames']} frames)")
    print(f"\nDistance Statistics:")
    print(f"  Team 1 Total: {video_data['team1TotalDistanceKm']:.2f} km ({video_data['team1PlayerCount']} players)")
    print(f"  Team 2 Total: {video_data['team2TotalDistanceKm']:.2f} km ({video_data['team2PlayerCount']} players)")
    print(f"\nSpeed Statistics:")
    print(f"  Team 1 Avg: {video_data['team1AvgSpeedKmh']:.2f} km/h")
    print(f"  Team 2 Avg: {video_data['team2AvgSpeedKmh']:.2f} km/h")
    
    # Simulate the Qt UI display strings
    print("\n" + "="*60)
    print("UI Display Strings (as shown in Qt application):")
    print("="*60)
    
    label1 = f"隊伍 1 持球時間: {video_data['team1PossessionPercent']:.2f}%"
    label2 = f"隊伍 2 持球時間: {video_data['team2PossessionPercent']:.2f}%"
    label3 = f"隊伍 1 進攻時間: {video_data['team1AttackPercent']:.2f}%"
    label4 = f"隊伍 2 進攻時間: {video_data['team2AttackPercent']:.2f}%"
    label5 = f"隊伍 1 總距離: {video_data['team1TotalDistanceKm']:.2f} 公里"
    label6 = f"隊伍 2 總距離: {video_data['team2TotalDistanceKm']:.2f} 公里"
    label7 = f"隊伍 1 平均速度: {video_data['team1AvgSpeedKmh']:.2f} 公里/小時"
    label8 = f"隊伍 2 平均速度: {video_data['team2AvgSpeedKmh']:.2f} 公里/小時"
    
    print(f"\n{label1}")
    print(f"{label2}")
    print(f"{label3}")
    print(f"{label4}")
    print(f"{label5}")
    print(f"{label6}")
    print(f"{label7}")
    print(f"{label8}")
    
    summary = (f"總幀數: {video_data['totalFrames']}\n"
               f"隊伍 1 持球幀數: {video_data['team1PossessionFrames']}\n"
               f"隊伍 2 持球幀數: {video_data['team2PossessionFrames']}\n"
               f"隊伍 1 進攻幀數: {video_data['team1AttackFrames']}\n"
               f"隊伍 2 進攻幀數: {video_data['team2AttackFrames']}")
    
    print(f"\nSummary Box:\n{summary}")
    
    # Validate data consistency
    print("\n" + "="*60)
    print("Data Validation:")
    print("="*60)
    
    all_valid = True
    
    # Check that possession percentages add up to ~100%
    total_possession = video_data['team1PossessionPercent'] + video_data['team2PossessionPercent']
    if abs(total_possession - 100.0) < 0.1:
        print(f"✓ Possession percentages sum to {total_possession:.1f}% (correct)")
    else:
        print(f"✗ Possession percentages sum to {total_possession:.1f}% (should be ~100%)")
        all_valid = False
    
    # Check that attack time is less than possession time
    if video_data['team1AttackPercent'] <= video_data['team1PossessionPercent']:
        print(f"✓ Team 1 attack time ({video_data['team1AttackPercent']:.1f}%) <= possession time ({video_data['team1PossessionPercent']:.1f}%)")
    else:
        print(f"✗ Team 1 attack time > possession time (impossible)")
        all_valid = False
    
    if video_data['team2AttackPercent'] <= video_data['team2PossessionPercent']:
        print(f"✓ Team 2 attack time ({video_data['team2AttackPercent']:.1f}%) <= possession time ({video_data['team2PossessionPercent']:.1f}%)")
    else:
        print(f"✗ Team 2 attack time > possession time (impossible)")
        all_valid = False
    
    # Check frame counts
    total_possession_frames = video_data['team1PossessionFrames'] + video_data['team2PossessionFrames']
    if total_possession_frames <= video_data['totalFrames']:
        print(f"✓ Total possession frames ({total_possession_frames}) <= total frames ({video_data['totalFrames']})")
    else:
        print(f"✗ Total possession frames > total frames (impossible)")
        all_valid = False
    
    print("\n" + "="*60)
    if all_valid:
        print("✓ All validations PASSED!")
        return True
    else:
        print("✗ Some validations FAILED!")
        return False

if __name__ == "__main__":
    import sys
    success = test_qt_data_loading()
    sys.exit(0 if success else 1)
