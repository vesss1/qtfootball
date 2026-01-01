"""
Data exporter module for football analysis
Exports analysis results including possession, attack time, distance, and speed metrics
"""

import json
import csv
import os
import numpy as np
from typing import Dict, List, Any

# Field dimensions constant
HALF_FIELD_LENGTH = 11.66  # meters - half of the football field length


class DataExporter:
    """
    Export football analysis data to JSON and CSV formats
    """
    
    def __init__(self, output_dir: str = "output_data"):
        """
        Initialize the data exporter
        
        Args:
            output_dir: Directory where output files will be saved
        """
        self.output_dir = output_dir
        self.ensure_output_directory()
    
    def ensure_output_directory(self):
        """Create output directory if it doesn't exist"""
        if not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir)
        
        csv_dir = os.path.join(self.output_dir, "csv")
        if not os.path.exists(csv_dir):
            os.makedirs(csv_dir)
    
    def calculate_possession_stats(self, team_ball_control: np.ndarray) -> Dict[str, Any]:
        """
        Calculate ball possession statistics for both teams
        
        Args:
            team_ball_control: Array of team control per frame (1 or 2)
            
        Returns:
            Dictionary with possession statistics
        """
        total_frames = len(team_ball_control)
        team_1_frames = np.sum(team_ball_control == 1)
        team_2_frames = np.sum(team_ball_control == 2)
        
        team_1_percent = (team_1_frames / total_frames * 100) if total_frames > 0 else 0.0
        team_2_percent = (team_2_frames / total_frames * 100) if total_frames > 0 else 0.0
        
        return {
            "total_frames": int(total_frames),
            "team_1_frames": int(team_1_frames),
            "team_2_frames": int(team_2_frames),
            "team_1_ball_control_percent": round(team_1_percent, 2),
            "team_2_ball_control_percent": round(team_2_percent, 2)
        }
    
    def calculate_attack_stats(self, tracks: Dict, team_ball_control: np.ndarray) -> Dict[str, Any]:
        """
        Calculate attack time statistics for both teams
        
        Attack is defined as:
        - Team 1: Has possession AND ball is past half field (x > HALF_FIELD_LENGTH)
        - Team 2: Has possession AND ball is past half field (x < HALF_FIELD_LENGTH)
        
        Args:
            tracks: Tracking data including ball positions
            team_ball_control: Array of team control per frame
            
        Returns:
            Dictionary with attack statistics
        """
        team_1_attack_frames = 0
        team_2_attack_frames = 0
        total_frames = len(team_ball_control)
        
        # Check ball position for each frame
        for frame_num in range(total_frames):
            if frame_num >= len(tracks['ball']):
                continue
                
            ball_frame = tracks['ball'][frame_num]
            if not ball_frame or 1 not in ball_frame:
                continue
            
            ball_data = ball_frame[1]
            if 'position_transformed' not in ball_data or ball_data['position_transformed'] is None:
                continue
            
            ball_x = ball_data['position_transformed'][0]
            team_control = team_ball_control[frame_num]
            
            # Team 1 attacks left to right (x increases)
            if team_control == 1 and ball_x > HALF_FIELD_LENGTH:
                team_1_attack_frames += 1
            # Team 2 attacks right to left (x decreases)
            elif team_control == 2 and ball_x < HALF_FIELD_LENGTH:
                team_2_attack_frames += 1
        
        team_1_attack_percent = (team_1_attack_frames / total_frames * 100) if total_frames > 0 else 0.0
        team_2_attack_percent = (team_2_attack_frames / total_frames * 100) if total_frames > 0 else 0.0
        
        return {
            "team_1_attack_frames": int(team_1_attack_frames),
            "team_2_attack_frames": int(team_2_attack_frames),
            "team_1_attack_percent": round(team_1_attack_percent, 2),
            "team_2_attack_percent": round(team_2_attack_percent, 2)
        }
    
    def calculate_distance_and_speed_stats(self, tracks: Dict) -> Dict[str, Any]:
        """
        Calculate distance and speed statistics for all players
        
        Note: Assumes the last frame contains cumulative statistics for each player.
        Distance is measured in meters, speed in km/h.
        
        Args:
            tracks: Tracking data including player positions, distances, and speeds
            
        Returns:
            Dictionary with distance and speed statistics per team
        """
        team_1_distances = []
        team_2_distances = []
        team_1_speeds = []
        team_2_speeds = []
        
        # Collect data from the last frame (contains cumulative data)
        if 'players' in tracks and len(tracks['players']) > 0:
            last_frame = tracks['players'][-1]
            
            for player_id, player_data in last_frame.items():
                # Get team assignment
                team = player_data.get('team', None)
                if team is None:
                    continue
                
                # Get distance (in meters) - only include if present
                distance = player_data.get('distance', None)
                # Get speed (in km/h) - only include if present
                speed = player_data.get('speed', None)
                
                if team == 1:
                    # Include all distance values, even zero (player may not have moved much)
                    if distance is not None:
                        team_1_distances.append(distance)
                    if speed is not None:
                        team_1_speeds.append(speed)
                elif team == 2:
                    if distance is not None:
                        team_2_distances.append(distance)
                    if speed is not None:
                        team_2_speeds.append(speed)
        
        # Calculate averages and totals
        team_1_total_distance = sum(team_1_distances) if team_1_distances else 0
        team_2_total_distance = sum(team_2_distances) if team_2_distances else 0
        team_1_avg_distance = np.mean(team_1_distances) if team_1_distances else 0
        team_2_avg_distance = np.mean(team_2_distances) if team_2_distances else 0
        team_1_avg_speed = np.mean(team_1_speeds) if team_1_speeds else 0
        team_2_avg_speed = np.mean(team_2_speeds) if team_2_speeds else 0
        
        # Convert distances from meters to kilometers
        return {
            "team_1_total_distance_km": round(team_1_total_distance / 1000, 2),
            "team_2_total_distance_km": round(team_2_total_distance / 1000, 2),
            "team_1_avg_distance_per_player_m": round(team_1_avg_distance, 2),
            "team_2_avg_distance_per_player_m": round(team_2_avg_distance, 2),
            "team_1_avg_speed_kmh": round(team_1_avg_speed, 2),
            "team_2_avg_speed_kmh": round(team_2_avg_speed, 2),
            "team_1_player_count": len(team_1_distances),
            "team_2_player_count": len(team_2_distances)
        }
    
    def export_to_json(self, data: Dict[str, Any], filename: str = "analysis_data.json"):
        """
        Export analysis data to JSON format
        
        Args:
            data: Dictionary containing all analysis data
            filename: Output filename
        """
        filepath = os.path.join(self.output_dir, filename)
        
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        
        print(f"Data exported to JSON: {filepath}")
    
    def export_to_csv(self, data: Dict[str, Any]):
        """
        Export analysis data to CSV format
        
        Args:
            data: Dictionary containing all analysis data
        """
        csv_dir = os.path.join(self.output_dir, "csv")
        
        # Export ball control stats
        ball_control_file = os.path.join(csv_dir, "ball_control_stats.csv")
        with open(ball_control_file, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(['metric', 'value'])
            
            metadata = data.get('metadata', {})
            for key in ['team_1_ball_control_percent', 'team_2_ball_control_percent',
                       'team_1_frames', 'team_2_frames']:
                if key in metadata:
                    writer.writerow([key, metadata[key]])
        
        # Export attack stats
        attack_stats_file = os.path.join(csv_dir, "attack_stats.csv")
        with open(attack_stats_file, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(['metric', 'value'])
            
            metadata = data.get('metadata', {})
            for key in ['team_1_attack_percent', 'team_2_attack_percent',
                       'team_1_attack_frames', 'team_2_attack_frames']:
                if key in metadata:
                    writer.writerow([key, metadata[key]])
        
        # Export distance and speed stats
        distance_speed_file = os.path.join(csv_dir, "distance_speed_stats.csv")
        with open(distance_speed_file, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(['metric', 'value'])
            
            metadata = data.get('metadata', {})
            for key in ['team_1_total_distance_km', 'team_2_total_distance_km',
                       'team_1_avg_distance_per_player_m', 'team_2_avg_distance_per_player_m',
                       'team_1_avg_speed_kmh', 'team_2_avg_speed_kmh',
                       'team_1_player_count', 'team_2_player_count']:
                if key in metadata:
                    writer.writerow([key, metadata[key]])
        
        print(f"Data exported to CSV files in: {csv_dir}")
    
    def export_analysis_data(self, tracks: Dict, team_ball_control: np.ndarray,
                           export_json: bool = True, export_csv: bool = True):
        """
        Export complete analysis data
        
        Args:
            tracks: Tracking data from analysis
            team_ball_control: Array of team control per frame
            export_json: Whether to export JSON format
            export_csv: Whether to export CSV format
        """
        # Calculate all statistics
        possession_stats = self.calculate_possession_stats(team_ball_control)
        attack_stats = self.calculate_attack_stats(tracks, team_ball_control)
        distance_speed_stats = self.calculate_distance_and_speed_stats(tracks)
        
        # Combine all data
        metadata = {
            **possession_stats,
            **attack_stats,
            **distance_speed_stats,
            "description": "Football analysis data exported from video processing"
        }
        
        data = {
            "metadata": metadata,
            "frames": []  # Can be extended to include per-frame data if needed
        }
        
        # Export to requested formats
        if export_json:
            self.export_to_json(data)
        
        if export_csv:
            self.export_to_csv(data)
        
        return data
