#!/usr/bin/env python3
"""
Test script to validate data_exporter.py functionality
"""

import sys
import os
import json

# Direct import to avoid loading other utils dependencies
import importlib.util
spec = importlib.util.spec_from_file_location(
    "data_exporter",
    os.path.join(os.path.dirname(__file__), 'football_analysis-main/utils/data_exporter.py')
)
data_exporter_module = importlib.util.module_from_spec(spec)

# Mock numpy if not available
try:
    import numpy as np
except ImportError:
    print("Warning: numpy not available, using mock")
    class MockNumpy:
        @staticmethod
        def sum(arr):
            return sum(arr)
        @staticmethod
        def mean(arr):
            return sum(arr) / len(arr) if arr else 0
        class ndarray:
            pass
    np = MockNumpy()
    sys.modules['numpy'] = np

spec.loader.exec_module(data_exporter_module)
DataExporter = data_exporter_module.DataExporter


def create_mock_tracks():
    """
    Create mock tracking data for testing
    """
    tracks = {
        'ball': [],
        'players': []
    }
    
    # Create 100 frames of mock data
    for frame_num in range(100):
        # Add ball position (mock data)
        ball_x = 11.66 + (5.0 if frame_num % 2 == 0 else -3.0)  # Alternating sides
        tracks['ball'].append({
            1: {
                'position_transformed': [ball_x, 5.0]
            }
        })
        
        # Add player data for last frame (to simulate cumulative stats)
        if frame_num == 99:
            players_frame = {}
            # Team 1 players
            for i in range(1, 6):
                players_frame[i] = {
                    'team': 1,
                    'distance': 500.0 + i * 50,  # meters
                    'speed': 8.0 + i * 0.5  # km/h
                }
            # Team 2 players
            for i in range(6, 11):
                players_frame[i] = {
                    'team': 2,
                    'distance': 450.0 + i * 40,  # meters
                    'speed': 7.5 + i * 0.4  # km/h
                }
            tracks['players'].append(players_frame)
        else:
            tracks['players'].append({})
    
    return tracks


def test_data_exporter():
    """
    Test the DataExporter class
    """
    print("="*60)
    print("Data Exporter Test")
    print("="*60 + "\n")
    
    # Create output directory for test
    test_output_dir = '/tmp/test_output'
    exporter = DataExporter(output_dir=test_output_dir)
    
    # Create mock data
    tracks = create_mock_tracks()
    team_ball_control = np.array([1 if i % 3 != 0 else 2 for i in range(100)])
    
    print("Mock data created:")
    print(f"  - Total frames: 100")
    print(f"  - Team 1 control: {np.sum(team_ball_control == 1)} frames")
    print(f"  - Team 2 control: {np.sum(team_ball_control == 2)} frames")
    print(f"  - Players: 10 (5 per team)")
    print()
    
    # Test possession stats
    print("Testing possession statistics calculation...")
    possession_stats = exporter.calculate_possession_stats(team_ball_control)
    print(f"  Team 1: {possession_stats['team_1_ball_control_percent']:.2f}%")
    print(f"  Team 2: {possession_stats['team_2_ball_control_percent']:.2f}%")
    print(f"  ✓ Possession stats calculated\n")
    
    # Test attack stats
    print("Testing attack statistics calculation...")
    attack_stats = exporter.calculate_attack_stats(tracks, team_ball_control)
    print(f"  Team 1 attack: {attack_stats['team_1_attack_percent']:.2f}%")
    print(f"  Team 2 attack: {attack_stats['team_2_attack_percent']:.2f}%")
    print(f"  ✓ Attack stats calculated\n")
    
    # Test distance and speed stats
    print("Testing distance and speed statistics calculation...")
    distance_speed_stats = exporter.calculate_distance_and_speed_stats(tracks)
    print(f"  Team 1 total distance: {distance_speed_stats['team_1_total_distance_km']:.2f} km")
    print(f"  Team 2 total distance: {distance_speed_stats['team_2_total_distance_km']:.2f} km")
    print(f"  Team 1 avg speed: {distance_speed_stats['team_1_avg_speed_kmh']:.2f} km/h")
    print(f"  Team 2 avg speed: {distance_speed_stats['team_2_avg_speed_kmh']:.2f} km/h")
    print(f"  ✓ Distance and speed stats calculated\n")
    
    # Test full export
    print("Testing full data export...")
    data = exporter.export_analysis_data(tracks, team_ball_control)
    print(f"  ✓ JSON exported to: {test_output_dir}/analysis_data.json")
    print(f"  ✓ CSV files exported to: {test_output_dir}/csv/\n")
    
    # Verify JSON file
    json_path = os.path.join(test_output_dir, 'analysis_data.json')
    if os.path.exists(json_path):
        with open(json_path, 'r') as f:
            loaded_data = json.load(f)
        
        print("Verifying exported JSON structure...")
        required_fields = [
            'total_frames', 'team_1_ball_control_percent', 'team_2_ball_control_percent',
            'team_1_attack_percent', 'team_2_attack_percent',
            'team_1_total_distance_km', 'team_2_total_distance_km',
            'team_1_avg_speed_kmh', 'team_2_avg_speed_kmh'
        ]
        
        metadata = loaded_data.get('metadata', {})
        all_present = True
        for field in required_fields:
            if field in metadata:
                print(f"  ✓ {field}: {metadata[field]}")
            else:
                print(f"  ✗ {field}: MISSING")
                all_present = False
        
        if all_present:
            print("\n✓ All required fields present in exported data!")
            return True
        else:
            print("\n✗ Some required fields missing!")
            return False
    else:
        print(f"✗ JSON file not created at {json_path}")
        return False


if __name__ == "__main__":
    success = test_data_exporter()
    sys.exit(0 if success else 1)
