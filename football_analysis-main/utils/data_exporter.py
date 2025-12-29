import json
import csv
import numpy as np
from pathlib import Path


class DataExporter:
    """
    Utility class to export football analysis data to various formats.
    Extracts all information displayed on the output video including:
    - Player tracking data
    - Ball tracking data
    - Team assignments and ball control
    - Camera movement
    - Speed and distance metrics
    """
    
    def __init__(self):
        pass
    
    def export_to_json(self, tracks, team_ball_control, camera_movement_per_frame, output_path):
        """
        Export all analysis data to a comprehensive JSON file.
        
        Args:
            tracks: Dictionary containing player, ball, and referee tracking data
            team_ball_control: Array of team ball control per frame
            camera_movement_per_frame: List of camera movement [x, y] per frame
            output_path: Path to save the JSON file
        """
        # Prepare data structure
        data = {
            "metadata": {
                "total_frames": len(tracks.get("players", [])),
                "description": "Football analysis data exported from video processing"
            },
            "frames": []
        }
        
        # Calculate cumulative ball control statistics
        total_frames = len(team_ball_control)
        team_1_frames = np.sum(team_ball_control == 1)
        team_2_frames = np.sum(team_ball_control == 2)
        total_controlled = team_1_frames + team_2_frames
        
        if total_controlled > 0:
            data["metadata"]["team_1_ball_control_percent"] = float(team_1_frames / total_controlled * 100)
            data["metadata"]["team_2_ball_control_percent"] = float(team_2_frames / total_controlled * 100)
        else:
            data["metadata"]["team_1_ball_control_percent"] = 0.0
            data["metadata"]["team_2_ball_control_percent"] = 0.0
        
        # Calculate attack time (possession past half field)
        # Half field is at 11.66 meters (half of 23.32m court length)
        half_field = 11.66
        team_1_attack_frames = 0
        team_2_attack_frames = 0
        
        for frame_num in range(len(tracks["players"])):
            if frame_num >= len(team_ball_control):
                break
            
            # Get ball position for this frame
            ball_frame = tracks["ball"][frame_num]
            if ball_frame:
                for ball_id, ball_info in ball_frame.items():
                    ball_pos_transformed = ball_info.get("position_transformed")
                    if ball_pos_transformed is not None and len(ball_pos_transformed) >= 1:
                        ball_x = ball_pos_transformed[0]
                        
                        # Team 1 attacks from left (x=0) to right
                        # Team 2 attacks from right (x=23.32) to left
                        # Team 1 is in attack when ball x > 11.66
                        # Team 2 is in attack when ball x < 11.66
                        
                        if team_ball_control[frame_num] == 1 and ball_x > half_field:
                            team_1_attack_frames += 1
                        elif team_ball_control[frame_num] == 2 and ball_x < half_field:
                            team_2_attack_frames += 1
        
        if total_controlled > 0:
            data["metadata"]["team_1_attack_percent"] = float(team_1_attack_frames / total_controlled * 100)
            data["metadata"]["team_2_attack_percent"] = float(team_2_attack_frames / total_controlled * 100)
            data["metadata"]["team_1_attack_frames"] = int(team_1_attack_frames)
            data["metadata"]["team_2_attack_frames"] = int(team_2_attack_frames)
        else:
            data["metadata"]["team_1_attack_percent"] = 0.0
            data["metadata"]["team_2_attack_percent"] = 0.0
            data["metadata"]["team_1_attack_frames"] = 0
            data["metadata"]["team_2_attack_frames"] = 0
        
        # Process each frame
        for frame_num in range(len(tracks["players"])):
            frame_data = {
                "frame_number": frame_num,
                "camera_movement": {
                    "x": float(camera_movement_per_frame[frame_num][0]),
                    "y": float(camera_movement_per_frame[frame_num][1])
                },
                "team_ball_control": int(team_ball_control[frame_num]) if frame_num < len(team_ball_control) else None,
                "players": [],
                "ball": None,
                "referees": []
            }
            
            # Add player data
            for player_id, player_info in tracks["players"][frame_num].items():
                player_data = {
                    "id": int(player_id),
                    "bbox": [float(x) for x in player_info["bbox"]],
                    "team": int(player_info.get("team", 0)),
                    "team_color": [int(c) for c in player_info.get("team_color", [0, 0, 0])],
                    "has_ball": bool(player_info.get("has_ball", False)),
                    "position": [float(x) for x in player_info.get("position", [0, 0])],
                    "position_adjusted": [float(x) for x in player_info.get("position_adjusted", [0, 0])],
                    "speed_kmh": float(player_info.get("speed", 0)),
                    "distance_m": float(player_info.get("distance", 0))
                }
                frame_data["players"].append(player_data)
            
            # Add ball data
            for ball_id, ball_info in tracks["ball"][frame_num].items():
                frame_data["ball"] = {
                    "id": int(ball_id),
                    "bbox": [float(x) for x in ball_info["bbox"]],
                    "position": [float(x) for x in ball_info.get("position", [0, 0])]
                }
            
            # Add referee data
            for referee_id, referee_info in tracks["referees"][frame_num].items():
                referee_data = {
                    "id": int(referee_id),
                    "bbox": [float(x) for x in referee_info["bbox"]],
                    "position": [float(x) for x in referee_info.get("position", [0, 0])]
                }
                frame_data["referees"].append(referee_data)
            
            data["frames"].append(frame_data)
        
        # Save to JSON file
        output_path = Path(output_path)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        
        print(f"Data exported to JSON: {output_path}")
        return str(output_path)
    
    def export_to_csv(self, tracks, team_ball_control, camera_movement_per_frame, output_dir):
        """
        Export analysis data to CSV files (one for players, one for frames).
        
        Args:
            tracks: Dictionary containing player, ball, and referee tracking data
            team_ball_control: Array of team ball control per frame
            camera_movement_per_frame: List of camera movement [x, y] per frame
            output_dir: Directory to save the CSV files
        """
        output_dir = Path(output_dir)
        output_dir.mkdir(parents=True, exist_ok=True)
        
        # Export player tracking data
        players_csv_path = output_dir / "players_tracking.csv"
        with open(players_csv_path, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow([
                "frame_number", "player_id", "team", "has_ball",
                "bbox_x1", "bbox_y1", "bbox_x2", "bbox_y2",
                "position_x", "position_y",
                "position_adjusted_x", "position_adjusted_y",
                "speed_kmh", "distance_m"
            ])
            
            for frame_num in range(len(tracks["players"])):
                for player_id, player_info in tracks["players"][frame_num].items():
                    bbox = player_info["bbox"]
                    position = player_info.get("position", [0, 0])
                    position_adjusted = player_info.get("position_adjusted", [0, 0])
                    
                    writer.writerow([
                        frame_num,
                        player_id,
                        player_info.get("team", 0),
                        1 if player_info.get("has_ball", False) else 0,
                        bbox[0], bbox[1], bbox[2], bbox[3],
                        position[0], position[1],
                        position_adjusted[0], position_adjusted[1],
                        player_info.get("speed", 0),
                        player_info.get("distance", 0)
                    ])
        
        print(f"Player tracking data exported to: {players_csv_path}")
        
        # Export frame summary data (camera movement, ball control)
        frames_csv_path = output_dir / "frames_summary.csv"
        with open(frames_csv_path, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow([
                "frame_number", "camera_movement_x", "camera_movement_y",
                "team_ball_control", "ball_bbox_x1", "ball_bbox_y1",
                "ball_bbox_x2", "ball_bbox_y2", "ball_position_x", "ball_position_y"
            ])
            
            for frame_num in range(len(tracks["players"])):
                camera_x, camera_y = camera_movement_per_frame[frame_num]
                team_control = team_ball_control[frame_num] if frame_num < len(team_ball_control) else 0
                
                # Get ball data if available (ball ID is always 1 per tracker convention)
                ball_data = tracks["ball"][frame_num].get(1, {})
                ball_bbox = ball_data.get("bbox", [0, 0, 0, 0])
                ball_position = ball_data.get("position", [0, 0])
                
                writer.writerow([
                    frame_num,
                    camera_x, camera_y,
                    team_control,
                    ball_bbox[0], ball_bbox[1], ball_bbox[2], ball_bbox[3],
                    ball_position[0], ball_position[1]
                ])
        
        print(f"Frame summary data exported to: {frames_csv_path}")
        
        # Export ball control and attack statistics
        stats_csv_path = output_dir / "ball_control_stats.csv"
        team_1_frames = np.sum(team_ball_control == 1)
        team_2_frames = np.sum(team_ball_control == 2)
        total_controlled = team_1_frames + team_2_frames
        
        # Calculate attack time (possession past half field)
        half_field = 11.66
        team_1_attack_frames = 0
        team_2_attack_frames = 0
        
        for frame_num in range(len(tracks["players"])):
            if frame_num >= len(team_ball_control):
                break
            
            # Get ball position for this frame
            ball_frame = tracks["ball"][frame_num]
            if ball_frame:
                for ball_id, ball_info in ball_frame.items():
                    ball_pos_transformed = ball_info.get("position_transformed")
                    if ball_pos_transformed is not None and len(ball_pos_transformed) >= 1:
                        ball_x = ball_pos_transformed[0]
                        
                        if team_ball_control[frame_num] == 1 and ball_x > half_field:
                            team_1_attack_frames += 1
                        elif team_ball_control[frame_num] == 2 and ball_x < half_field:
                            team_2_attack_frames += 1
        
        with open(stats_csv_path, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(["metric", "value"])
            writer.writerow(["total_frames", len(team_ball_control)])
            writer.writerow(["team_1_frames", team_1_frames])
            writer.writerow(["team_2_frames", team_2_frames])
            if total_controlled > 0:
                writer.writerow(["team_1_control_percent", team_1_frames / total_controlled * 100])
                writer.writerow(["team_2_control_percent", team_2_frames / total_controlled * 100])
                writer.writerow(["team_1_attack_frames", team_1_attack_frames])
                writer.writerow(["team_2_attack_frames", team_2_attack_frames])
                writer.writerow(["team_1_attack_percent", team_1_attack_frames / total_controlled * 100])
                writer.writerow(["team_2_attack_percent", team_2_attack_frames / total_controlled * 100])
            else:
                writer.writerow(["team_1_control_percent", 0])
                writer.writerow(["team_2_control_percent", 0])
                writer.writerow(["team_1_attack_frames", 0])
                writer.writerow(["team_2_attack_frames", 0])
                writer.writerow(["team_1_attack_percent", 0])
                writer.writerow(["team_2_attack_percent", 0])
        
        print(f"Ball control and attack statistics exported to: {stats_csv_path}")
        
        return str(output_dir)
    
    def export_all(self, tracks, team_ball_control, camera_movement_per_frame, 
                   json_path=None, csv_dir=None):
        """
        Export data to both JSON and CSV formats.
        
        Args:
            tracks: Dictionary containing player, ball, and referee tracking data
            team_ball_control: Array of team ball control per frame
            camera_movement_per_frame: List of camera movement [x, y] per frame
            json_path: Path for JSON file (default: output_data/analysis_data.json)
            csv_dir: Directory for CSV files (default: output_data/csv/)
        """
        if json_path is None:
            json_path = "output_data/analysis_data.json"
        if csv_dir is None:
            csv_dir = "output_data/csv"
        
        json_result = self.export_to_json(tracks, team_ball_control, 
                                          camera_movement_per_frame, json_path)
        csv_result = self.export_to_csv(tracks, team_ball_control, 
                                        camera_movement_per_frame, csv_dir)
        
        return {
            "json": json_result,
            "csv": csv_result
        }
