"""
Simple YOLO inference script for testing model predictions
"""
from ultralytics import YOLO


def main():
    """Run YOLO inference on a video file"""
    # Load model
    model = YOLO('models/best.pt')
    
    # Run inference
    results = model.predict(
        "input_videos/08fd33_4.mp4",
        save=True,
        conf=0.1
    )
    
    # Print results
    print("First frame results:")
    print(results[0])
    print("\n" + "=" * 60)
    print("Detected boxes:")
    for box in results[0].boxes:
        print(box)


if __name__ == '__main__':
    main()
