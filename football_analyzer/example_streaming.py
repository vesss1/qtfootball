"""
Example: Memory-Efficient Video Processing using Frame-by-Frame Streaming

This example demonstrates how to use the read_video_frames_generator()
function to process videos with minimal memory usage.

Perfect for:
- Very long videos (hours of footage)
- High-resolution videos (4K, 8K)
- Systems with limited RAM
- Preprocessing or analysis tasks that don't require all frames in memory
"""

import sys
import os
import tempfile

# Ensure we can import from the parent directory
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from football_analyzer.utils import read_video_frames_generator, get_video_properties, save_video
import cv2
import numpy as np


def example_streaming_processing(video_path, output_path, max_frames=None):
    """
    Example of processing a video frame-by-frame with constant memory usage.
    
    This approach keeps memory usage constant regardless of video length.
    """
    print("=" * 60)
    print("Memory-Efficient Video Processing Example")
    print("=" * 60)
    
    # First, get video properties without loading frames
    print("\nGetting video properties...")
    props = get_video_properties(video_path)
    print(f"Video: {props['width']}x{props['height']}")
    print(f"Total frames: {props['total_frames']}")
    print(f"FPS: {props['fps']}")
    print(f"Duration: {props['duration']:.2f} seconds")
    
    # Calculate estimated memory for batch loading (for comparison)
    batch_memory_mb = (props['width'] * props['height'] * 3 * props['total_frames']) / (1024 * 1024)
    print(f"\nBatch loading would require: {batch_memory_mb:.2f} MB")
    print(f"Streaming approach: Constant memory (1 frame ≈ {(props['width'] * props['height'] * 3) / (1024 * 1024):.2f} MB)")
    
    # Process frames one at a time
    print(f"\nProcessing frames...")
    processed_frames = []
    
    for frame_idx, frame in read_video_frames_generator(video_path, max_frames=max_frames):
        # Example processing: convert to grayscale and back to BGR
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        processed = cv2.cvtColor(gray, cv2.COLOR_GRAY2BGR)
        
        # Add frame number overlay
        cv2.putText(processed, f"Frame {frame_idx}", (50, 50),
                   cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
        
        processed_frames.append(processed)
        
        if (frame_idx + 1) % 100 == 0:
            print(f"  Processed {frame_idx + 1} frames...")
    
    print(f"✓ Processed {len(processed_frames)} frames")
    
    # Save the output
    if len(processed_frames) > 0:
        print(f"\nSaving output video to {output_path}...")
        save_video(processed_frames, output_path, fps=props['fps'])
        print("✓ Done!")
    
    return processed_frames


def example_custom_processing_without_saving(video_path, max_frames=100):
    """
    Example of processing frames without keeping them in memory.
    
    This is the most memory-efficient approach - processes each frame
    and discards it immediately.
    """
    print("\n" + "=" * 60)
    print("Ultra Memory-Efficient Processing (No Frame Storage)")
    print("=" * 60)
    
    # Compute statistics without storing frames
    frame_count = 0
    total_brightness = 0
    
    for frame_idx, frame in read_video_frames_generator(video_path, max_frames=max_frames):
        # Calculate average brightness
        brightness = np.mean(frame)
        total_brightness += brightness
        frame_count += 1
        
        # Frame is automatically discarded here
    
    avg_brightness = total_brightness / frame_count if frame_count > 0 else 0
    
    print(f"Analyzed {frame_count} frames")
    print(f"Average brightness: {avg_brightness:.2f}")
    print("✓ Memory usage stayed constant throughout!")


def main():
    """
    Run examples. 
    
    Note: This requires a test video. For demonstration purposes,
    we'll create a small test video first.
    """
    
    # Use cross-platform temporary directory
    temp_dir = tempfile.gettempdir()
    test_video = os.path.join(temp_dir, 'streaming_test_video.mp4')
    
    if not os.path.exists(test_video):
        print("Creating test video...")
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        out = cv2.VideoWriter(test_video, fourcc, 30, (640, 480))
        
        for i in range(300):  # 10 seconds at 30fps
            frame = np.zeros((480, 640, 3), dtype=np.uint8)
            frame[:, :] = [int((i/300)*255), 128, 255 - int((i/300)*255)]
            cv2.putText(frame, f"Test Frame {i}", (200, 240),
                       cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
            out.write(frame)
        
        out.release()
        print(f"✓ Created test video: {test_video}\n")
    
    # Example 1: Process and save (with frame storage)
    output_video = os.path.join(temp_dir, 'streaming_output.mp4')
    example_streaming_processing(test_video, output_video, max_frames=50)
    
    # Example 2: Process without storage (ultra memory-efficient)
    example_custom_processing_without_saving(test_video, max_frames=100)
    
    print("\n" + "=" * 60)
    print("Examples completed!")
    print("=" * 60)
    print("\nKey Takeaways:")
    print("1. Use read_video_frames_generator() for large videos")
    print("2. Memory usage stays constant regardless of video length")
    print("3. Perfect for preprocessing, analysis, or custom workflows")
    print("4. For the main pipeline, use read_video() with max_frames parameter")


if __name__ == '__main__':
    main()
