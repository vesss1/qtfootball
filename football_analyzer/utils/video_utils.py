import cv2
from tqdm import tqdm


# Memory warning threshold in MB (warn if video requires more than this)
MEMORY_WARNING_THRESHOLD_MB = 8000


def read_video(video_path, max_frames=None):
    """
    Reads a video and returns a list of frames.

    Parameters:
        video_path (str): The path to the video file.
        max_frames (int, optional): Maximum number of frames to read. 
                                   If None, reads all frames. Set to 0 to read no frames.
                                   Useful for memory-constrained environments or testing.

    Returns:
        list: A list of frames in the video.
    
    Raises:
        ValueError: If the video file cannot be opened or contains no frames.
        MemoryError: If there's not enough memory to load the video frames.
    """
    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        raise ValueError(f"Error: Could not open video {video_path}")
    
    # Get video properties for memory estimation
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fps = cap.get(cv2.CAP_PROP_FPS)
    
    # Estimate memory requirement (3 bytes per pixel for BGR)
    frames_to_read = min(total_frames, max_frames) if max_frames is not None else total_frames
    estimated_memory_mb = (width * height * 3 * frames_to_read) / (1024 * 1024)
    
    print(f"Video info: {width}x{height}, {total_frames} frames, {fps:.2f} fps")
    print(f"Estimated memory required: {estimated_memory_mb:.2f} MB for {frames_to_read} frames")
    
    # Skip reading if max_frames is 0
    if max_frames is not None and max_frames == 0:
        print(f"max_frames is set to 0, no frames will be loaded")
        cap.release()
        return []
    
    if estimated_memory_mb > MEMORY_WARNING_THRESHOLD_MB:
        print(f"WARNING: Video requires approximately {estimated_memory_mb/1024:.2f} GB of memory")
        print("Consider using max_frames parameter to limit memory usage")
    
    frames = []
    frame_count = 0
    
    try:
        while True:
            ret, frame = cap.read()
            if not ret:
                break
            
            frame_count += 1
            
            # Stop if we've reached the maximum number of frames (before appending)
            if max_frames is not None and len(frames) >= max_frames:
                print(f"Reached maximum frame limit: {max_frames}")
                break
                
            frames.append(frame)
                
    except MemoryError as e:
        cap.release()
        raise MemoryError(
            f"Out of memory after loading {len(frames)} frames. "
            f"Video requires too much memory ({estimated_memory_mb:.2f} MB estimated). "
            f"Try using max_frames parameter to load fewer frames, or process the video in smaller chunks."
        ) from e
    except Exception as e:
        cap.release()
        raise RuntimeError(f"Error reading video at frame {frame_count}: {str(e)}") from e
    
    cap.release()
    
    if len(frames) == 0 and (max_frames is None or max_frames > 0):
        raise ValueError(f"No frames were read from video {video_path}. The video may be empty or corrupted.")
    
    print(f"Successfully loaded {len(frames)} frames")
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
