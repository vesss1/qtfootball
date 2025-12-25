import cv2
import os
from tqdm import tqdm

def read_video(video_path):
    """
    Reads a video and returns a list of frames.

    Parameters:
        video_path (str): The path to the video file.

    Returns:
        list: A list of frames in the video.
        
    Raises:
        ValueError: If video_path is invalid or video cannot be opened.
    """
    if not video_path or not isinstance(video_path, str):
        raise ValueError("video_path must be a non-empty string")
    
    if not os.path.exists(video_path):
        raise ValueError(f"Video file does not exist: {video_path}")
    
    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        raise ValueError(f"Error: Could not open video {video_path}")
    
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

def save_video(frames, output_video_path, fps=24.0):
    """
    Saves a list of frames to a video file.

    Parameters:
        frames (list): List of frames to write to the video.
        output_video_path (str): Path to save the output video.
        fps (float, optional): Frames per second for the output video. Default is 24.0.
        
    Raises:
        ValueError: If frames is empty or invalid.
    """
    if not frames or not isinstance(frames, list):
        raise ValueError("frames must be a non-empty list")
    
    if not isinstance(output_video_path, str) or not output_video_path:
        raise ValueError("output_video_path must be a non-empty string")
    
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    frame_size = (frames[0].shape[1], frames[0].shape[0])
    output = cv2.VideoWriter(
        output_video_path,
        fourcc=fourcc,
        fps=fps,
        frameSize=frame_size
    )
    
    if not output.isOpened():
        raise ValueError(f"Could not create video writer for: {output_video_path}")
    
    for frame in tqdm(frames, desc="Saving Video", unit="frame"):
        output.write(frame)
    output.release()

def get_center_of_bbox(bbox):
    """
    Returns the center point of a bounding box.

    Parameters:
        bbox (tuple): A tuple (x1, y1, x2, y2) representing the bounding box coordinates.

    Returns:
        tuple: (center_x, center_y) of the bounding box.
        
    Raises:
        ValueError: If bbox format is invalid.
    """
    if not bbox or len(bbox) != 4:
        raise ValueError("bbox must contain exactly 4 coordinates (x1, y1, x2, y2)")
    
    x1, y1, x2, y2 = bbox
    if x1 >= x2 or y1 >= y2:
        raise ValueError("Invalid bounding box coordinates: x1 < x2 and y1 < y2 required.")
    return (x1 + x2) // 2, (y1 + y2) // 2

def measure_distance(p1, p2):
    """
    Calculates the Euclidean distance between two points.

    Parameters:
        p1 (tuple): The first point (x1, y1).
        p2 (tuple): The second point (x2, y2).

    Returns:
        float: The distance between the two points.
        
    Raises:
        ValueError: If points format is invalid.
    """
    if p1 is None or p2 is None or len(p1) < 2 or len(p2) < 2:
        raise ValueError("Both points must have at least 2 coordinates (x, y)")
    
    return ((p1[0] - p2[0])**2 + (p1[1] - p2[1])**2)**0.5
