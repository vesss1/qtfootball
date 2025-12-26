"""
Simple YOLO inference script for testing model predictions
"""
import sys
from ultralytics import YOLO


def main():
    """Run YOLO inference on a video file"""
    # Get video path from command line or use default
    if len(sys.argv) > 1:
        video_path = sys.argv[1]
    else:
        video_path = "input_videos/08fd33_4.mp4"
    
    # Get model path from command line or use default
    if len(sys.argv) > 2:
        model_path = sys.argv[2]
    else:
        model_path = 'models/best.pt'
    
    print(f"Using model: {model_path}")
    print(f"Processing video: {video_path}")
    
    # Load model
    model = YOLO(model_path)
    
    # Run inference
    results = model.predict(
        video_path,
        save=True,
        conf=0.1
    )
    
    # Print results
    print("\nFirst frame results:")
    print(results[0])
    print("\n" + "=" * 60)
    print("Detected boxes:")
    for box in results[0].boxes:
        print(box)


if __name__ == '__main__':
    main()
