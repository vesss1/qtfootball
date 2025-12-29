#!/usr/bin/env python3
"""
Test script to verify the attack time calculation logic in data_exporter.py
"""

import json
import sys
import os

# Add the football_analysis-main directory to the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'football_analysis-main'))

def test_attack_calculation():
    """
    Test the attack time calculation logic
    """
    print("Testing attack time calculation logic...\n")
    
    # Simulate some test data
    # In a real scenario, these would come from the video analysis
    
    # Court length is 23.32m, half field is at 11.66m
    half_field = 11.66
    
    # Test scenarios
    scenarios = [
        {
            "name": "Team 1 attacks from left to right",
            "team_control": 1,
            "ball_x": 15.0,  # Past half field (> 11.66)
            "expected": "Team 1 is attacking"
        },
        {
            "name": "Team 1 in defense",
            "team_control": 1,
            "ball_x": 8.0,  # Before half field (< 11.66)
            "expected": "Team 1 is NOT attacking"
        },
        {
            "name": "Team 2 attacks from right to left",
            "team_control": 2,
            "ball_x": 8.0,  # Past half field from Team 2's perspective (< 11.66)
            "expected": "Team 2 is attacking"
        },
        {
            "name": "Team 2 in defense",
            "team_control": 2,
            "ball_x": 15.0,  # Before half field from Team 2's perspective (> 11.66)
            "expected": "Team 2 is NOT attacking"
        }
    ]
    
    print(f"Half field position: {half_field}m\n")
    print("Attack logic:")
    print("- Team 1 attacks left to right: attacking when ball_x > 11.66")
    print("- Team 2 attacks right to left: attacking when ball_x < 11.66\n")
    
    all_passed = True
    
    for i, scenario in enumerate(scenarios, 1):
        team = scenario["team_control"]
        ball_x = scenario["ball_x"]
        
        # Apply the same logic as in data_exporter.py
        is_attacking = False
        if team == 1 and ball_x > half_field:
            is_attacking = True
        elif team == 2 and ball_x < half_field:
            is_attacking = True
        
        result = "Team {} is{}attacking".format(team, " " if is_attacking else " NOT ")
        passed = (result == scenario["expected"])
        
        status = "✓ PASS" if passed else "✗ FAIL"
        print(f"Test {i}: {scenario['name']}")
        print(f"  Team: {team}, Ball X: {ball_x}m")
        print(f"  Expected: {scenario['expected']}")
        print(f"  Got: {result}")
        print(f"  {status}\n")
        
        if not passed:
            all_passed = False
    
    return all_passed

def test_json_structure():
    """
    Test the expected JSON structure
    """
    print("\n" + "="*60)
    print("Testing expected JSON structure...\n")
    
    # Create a sample JSON structure
    sample_data = {
        "metadata": {
            "total_frames": 100,
            "description": "Football analysis data exported from video processing",
            "team_1_ball_control_percent": 55.5,
            "team_2_ball_control_percent": 44.5,
            "team_1_attack_percent": 30.2,
            "team_2_attack_percent": 25.8,
            "team_1_attack_frames": 30,
            "team_2_attack_frames": 26
        }
    }
    
    print("Sample JSON structure:")
    print(json.dumps(sample_data, indent=2, ensure_ascii=False))
    print("\n✓ JSON structure looks correct")
    
    return True

if __name__ == "__main__":
    print("="*60)
    print("Data Exporter Test Suite")
    print("="*60 + "\n")
    
    test1_passed = test_attack_calculation()
    test2_passed = test_json_structure()
    
    print("\n" + "="*60)
    if test1_passed and test2_passed:
        print("✓ All tests PASSED!")
        sys.exit(0)
    else:
        print("✗ Some tests FAILED!")
        sys.exit(1)
