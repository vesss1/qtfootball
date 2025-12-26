"""
Unified Football Analysis System
Integrates features from FootBall-main and Football-brench projects
"""

from utils import read_video, save_video
from trackers import Tracker
from team_assigner import TeamAssigner
from player_ball_assigner import PlayerBallAssigner
from camera_movement_estimator import CameraMovementEstimator
from view_transformer import ViewTransformer
from speed_and_distance_estimator import SpeedAndDistanceEstimator
import numpy as np
import config


def main():
    """
    Main function for the unified football video analysis pipeline.
    
    This integrates:
    - Object detection and tracking (players, referees, ball)
    - Team assignment using K-means clustering
    - Ball possession tracking
    - Camera movement estimation
    - View transformation for accurate distance measurements
    - Speed and distance calculations
    """
    
    print("=" * 60)
    print("Football Analysis System - Unified Pipeline")
    print("=" * 60)
    
    # Step 1: Read video frames
    print("\n[1/9] Reading video...")
    video_frames = read_video(config.INPUT_VIDEO_PATH)
    print(f"✓ Loaded {len(video_frames)} frames")
    
    # Step 2: Initialize tracker and detect objects
    print("\n[2/9] Initializing tracker and detecting objects...")
    tracker = Tracker(config.MODEL_PATH)
    tracks = tracker.get_object_tracks(
        video_frames,
        read_from_stub=config.USE_STUBS,
        stub_path=config.TRACK_STUB_PATH
    )
    print("✓ Object tracking complete")
    
    # Step 3: Add position information to tracks
    print("\n[3/9] Adding position information to tracks...")
    tracker.add_position_to_tracks(tracks)
    print("✓ Positions added")
    
    # Step 4: Estimate camera movement
    print("\n[4/9] Estimating camera movement...")
    camera_movement_estimator = CameraMovementEstimator(video_frames[0])
    camera_movement_per_frame = camera_movement_estimator.get_camera_movement(
        video_frames,
        read_from_stub=config.USE_STUBS,
        stub_path=config.CAMERA_STUB_PATH
    )
    camera_movement_estimator.add_adjust_positions_to_tracks(tracks, camera_movement_per_frame)
    print("✓ Camera movement estimated")
    
    # Step 5: Transform view for real-world measurements
    print("\n[5/9] Transforming view perspective...")
    view_transformer = ViewTransformer()
    view_transformer.add_transformed_position_to_tracks(tracks)
    print("✓ View transformation complete")
    
    # Step 6: Interpolate ball positions
    print("\n[6/9] Interpolating ball positions...")
    tracks['ball'] = tracker.interpolate_ball_positions(tracks["ball"])
    print("✓ Ball positions interpolated")
    
    # Step 7: Calculate speed and distance
    print("\n[7/9] Calculating speed and distance...")
    speed_and_distance_estimator = SpeedAndDistanceEstimator()
    speed_and_distance_estimator.add_speed_and_distance_to_tracks(tracks)
    print("✓ Speed and distance calculated")
    
    # Step 8: Assign teams
    print("\n[8/9] Assigning teams...")
    team_assigner = TeamAssigner()
    team_assigner.assign_team_color(video_frames[0], tracks['players'][0])
    
    for frame_num, player_tracks in enumerate(tracks['players']):
        for player_id, track in player_tracks.items():
            team = team_assigner.get_player_team(
                video_frames[frame_num],
                track['bbox'],
                player_id
            )
            tracks['players'][frame_num][player_id]['team'] = team
            tracks['players'][frame_num][player_id]['team_color'] = team_assigner.team_color[team]
    print("✓ Teams assigned")
    
    # Step 9: Assign ball possession
    print("\n[9/9] Assigning ball possession...")
    player_assigner = PlayerBallAssigner()
    team_ball_control = []
    
    for frame_num, player_track in enumerate(tracks['players']):
        ball_bbox = tracks['ball'][frame_num][1]['bbox']
        assigned_player = player_assigner.assign_ball_to_player(player_track, ball_bbox)
        
        if assigned_player != -1:
            tracks['players'][frame_num][assigned_player]['has_ball'] = True
            team_ball_control.append(tracks['players'][frame_num][assigned_player]['team'])
        else:
            team_ball_control.append(team_ball_control[-1] if team_ball_control else 1)
    
    team_ball_control = np.array(team_ball_control)
    print("✓ Ball possession assigned")
    
    # Generate output video with all annotations
    print("\n" + "=" * 60)
    print("Generating output video with annotations...")
    print("=" * 60)
    
    # Draw object tracks
    output_video_frames = tracker.draw_annotations(video_frames, tracks, team_ball_control)
    
    # Draw camera movement
    if config.SHOW_CAMERA_MOVEMENT:
        output_video_frames = camera_movement_estimator.draw_camera_movement(
            output_video_frames,
            camera_movement_per_frame
        )
    
    # Draw speed and distance
    if config.SHOW_SPEED_DISTANCE:
        speed_and_distance_estimator.draw_speed_and_distance(output_video_frames, tracks)
    
    # Save the output video
    print("\nSaving output video...")
    save_video(output_video_frames, config.OUTPUT_VIDEO_PATH, fps=config.OUTPUT_FPS)
    
    print("\n" + "=" * 60)
    print(f"✓ Analysis complete! Output saved to: {config.OUTPUT_VIDEO_PATH}")
    print("=" * 60)


if __name__ == '__main__':
    main()
