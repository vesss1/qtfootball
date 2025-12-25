import cv2
import os

def read_video(video_path):
    """
    Reads a video file and returns a list of frames.
    
    Args:
        video_path (str): Path to the video file.
        
    Returns:
        list: List of frames from the video.
        
    Raises:
        ValueError: If video_path is invalid or video cannot be opened.
    """
    if not video_path or not isinstance(video_path, str):
        raise ValueError("video_path must be a non-empty string")
    
    if not os.path.exists(video_path):
        raise ValueError(f"Video file does not exist: {video_path}")
    
    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        raise ValueError(f"Could not open video file: {video_path}")
    
    frames = []
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        frames.append(frame)
    
    cap.release()
    
    if len(frames) == 0:
        raise ValueError(f"No frames were read from video: {video_path}")

    return frames 


def save_video(output_video_frames, output_video_path):
    """
    Saves a list of frames to a video file.
    
    Args:
        output_video_frames (list): List of frames to save.
        output_video_path (str): Path where the video will be saved.
        
    Raises:
        ValueError: If frames list is empty or invalid.
    """
    if not output_video_frames or not isinstance(output_video_frames, list):
        raise ValueError("output_video_frames must be a non-empty list")
    
    if not isinstance(output_video_path, str) or not output_video_path:
        raise ValueError("output_video_path must be a non-empty string")
    
    fourcc = cv2.VideoWriter_fourcc(*'XVID')
    out = cv2.VideoWriter(output_video_path, fourcc, 24.0, (output_video_frames[0].shape[1], output_video_frames[0].shape[0]))
    
    if not out.isOpened():
        raise ValueError(f"Could not create video writer for: {output_video_path}")
    
    for frame in output_video_frames:
        out.write(frame)
    out.release()