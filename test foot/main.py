import torch
from tqdm import tqdm
import numpy as np
import cv2

from src.utils.video_utils import read_video, save_video
from src.keypoint_detection.keypoints import KeyPointDetection
from src.utils.team_classifer import TeamClassifier
from src.utils.ball_acquisition import assign_ball_to_player
from src.detections.player_detection import draw_annotation, get_detection

from trackers import Tracker
from team_assigner import TeamAssigner
from player_ball_assigner import PlayerBallAssigner
from camera_movement_estimator import CameraMovementEstimator
from view_transformer import ViewTransformer
from speed_and_distance_estimator import SpeedAndDistanceEstimator

# Global paths
VIDEO_PATH = "./test_videos/trim.mp4"
OBJ_MODEL_PATH = "./models/obj_v8x.pt"
POSE_MODEL_PATH = "./models/pose_v8x.pt"
OUTPUT_PATH = "./output_videos/five_integrated.mp4"
STUBS_PATH_OBJ = "./stub/five_obj.pkl"
STUBS_STATUS = False

def main():
    """Full football video analysis pipeline."""

    # Step 1: Read video frames
    video_frames = read_video(VIDEO_PATH)

    # Step 2: Object detection (for external use / optional)
    detections = get_detection(OBJ_MODEL_PATH, video_frames, STUBS_PATH_OBJ, STUBS_STATUS)

    # Step 3: Tracker for object IDs
    tracker = Tracker(OBJ_MODEL_PATH)
    tracks = tracker.get_object_tracks(video_frames, read_from_stub=False)

    # Step 3.5: Add positions to tracks (required for camera adjustment)
    tracker.add_position_to_tracks(tracks)

    # Step 4: Camera movement estimation
    camera_estimator = CameraMovementEstimator(video_frames[0])
    camera_movement = camera_estimator.get_camera_movement(video_frames, read_from_stub=False)
    camera_estimator.add_adjust_positions_to_tracks(tracks, camera_movement)

    # Step 5: View transformation (field coordinates)
    view_transformer = ViewTransformer()
    view_transformer.add_transformed_position_to_tracks(tracks)

    # Step 6: Speed and distance calculation
    speed_distance_estimator = SpeedAndDistanceEstimator()
    speed_distance_estimator.add_speed_and_distance_to_tracks(tracks)

    # Step 7: Team assignment
    team_assigner = TeamAssigner()
    team_assigner.assign_team_color(video_frames[0], tracks['players'][0])
    for frame_num, player_tracks in enumerate(tracks['players']):
        for player_id, track in player_tracks.items():
            team = team_assigner.get_player_team(video_frames[frame_num], track['bbox'], player_id)
            tracks['players'][frame_num][player_id]['team'] = team
            tracks['players'][frame_num][player_id]['team_color'] = team_assigner.team_color[team]

    # Step 8: Ball assignment
    player_assigner = PlayerBallAssigner()
    team_ball_control = []
    for frame_num, player_tracks in enumerate(tracks['players']):
        ball_bbox = tracks['ball'][frame_num][1]['bbox']
        assigned_player = player_assigner.assign_ball_to_player(player_tracks, ball_bbox)
        if assigned_player != -1:
            tracks['players'][frame_num][assigned_player]['has_ball'] = True
            team_ball_control.append(player_tracks[assigned_player]['team'])
        else:
            team_ball_control.append(team_ball_control[-1] if len(team_ball_control) > 0 else -1)
    team_ball_control = np.array(team_ball_control)

    # Step 9: Keypoint detection
    keypoint_detector = KeyPointDetection(POSE_MODEL_PATH)
    keypoint_frames = keypoint_detector.get_keypoint_detection(
        video_frames=video_frames,
        detections=detections,
        team_assignments=team_assigner
    )

    # Step 10: Draw annotations
    annotated_frames = draw_annotation(
        keypoint_frames,
        detections,
        team_assigner,
        team_ball_control
    )

    # Step 11: Draw camera movement
    annotated_frames = camera_estimator.draw_camera_movement(annotated_frames, camera_movement)

    # Step 12: Draw speed and distance
    speed_distance_estimator.draw_speed_and_distance(annotated_frames, tracks)

    # Step 13: Save annotated video
    save_video(annotated_frames, OUTPUT_PATH)


if __name__ == "__main__":
    main()
