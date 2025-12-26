import cv2
from tqdm import tqdm


def read_video(video_path):
    """
    Reads a video and returns a list of frames.

    Parameters:
        video_path (str): The path to the video file.

    Returns:
        list: A list of frames in the video.
    """
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
    return frames


def save_video(frames, output_video_path, fps=24.0):
    """
    Saves a list of frames to a video file.

    Parameters:
        frames (list): List of frames to write to the video.
        output_video_path (str): Path to save the output video.
        fps (float, optional): Frames per second for the output video. Default is 24.0.
    """
    if len(frames) == 0:
        raise ValueError("No frames to save")
    
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    frame_size = (frames[0].shape[1], frames[0].shape[0])
    output = cv2.VideoWriter(
        output_video_path,
        fourcc=fourcc,
        fps=fps,
        frameSize=frame_size
    )
    for frame in tqdm(frames, desc="Saving Video", unit="frame"):
        output.write(frame)
    output.release()
