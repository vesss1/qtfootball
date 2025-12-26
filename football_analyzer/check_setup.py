#!/usr/bin/env python3
"""
Quick start script for Football Analyzer
This script checks if all dependencies and required files are present
"""

import sys
import os
from pathlib import Path


def check_python_version():
    """Check if Python version is compatible"""
    print("Checking Python version...")
    if sys.version_info < (3, 8):
        print("❌ Python 3.8 or higher is required")
        print(f"   Current version: {sys.version}")
        return False
    print(f"✓ Python {sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}")
    return True


def check_dependencies():
    """Check if required packages are installed"""
    print("\nChecking dependencies...")
    required_packages = [
        'ultralytics',
        'cv2',
        'numpy',
        'supervision',
        'torch',
        'sklearn',
        'pandas',
        'tqdm',
        'PIL'
    ]
    
    missing = []
    for package in required_packages:
        try:
            if package == 'cv2':
                __import__('cv2')
            elif package == 'PIL':
                __import__('PIL')
            else:
                __import__(package)
            print(f"✓ {package}")
        except ImportError:
            print(f"❌ {package}")
            missing.append(package)
    
    if missing:
        print("\n⚠️  Missing packages. Install with:")
        print("   pip install -r requirements.txt")
        return False
    
    return True


def check_directory_structure():
    """Check if required directories exist"""
    print("\nChecking directory structure...")
    required_dirs = [
        'models',
        'input_videos',
        'output_videos',
        'stubs',
        'utils',
        'trackers',
        'team_assigner',
        'camera_movement_estimator',
        'view_transformer',
        'speed_and_distance_estimator',
        'player_ball_assigner'
    ]
    
    all_good = True
    for dir_name in required_dirs:
        if Path(dir_name).exists():
            print(f"✓ {dir_name}/")
        else:
            print(f"❌ {dir_name}/ (missing)")
            all_good = False
    
    return all_good


def check_model_file():
    """Check if model file exists"""
    print("\nChecking for model file...")
    model_dir = Path('models')
    if not model_dir.exists():
        print("❌ models/ directory not found")
        return False
    
    model_files = list(model_dir.glob('*.pt'))
    if not model_files:
        print("❌ No .pt model files found in models/")
        print("   Please download or train a YOLO model and place it in models/")
        return False
    
    print(f"✓ Found {len(model_files)} model file(s):")
    for model in model_files:
        print(f"   - {model.name}")
    
    return True


def check_input_video():
    """Check if input video exists"""
    print("\nChecking for input video...")
    video_dir = Path('input_videos')
    if not video_dir.exists():
        print("❌ input_videos/ directory not found")
        return False
    
    video_extensions = ['.mp4', '.avi', '.mov', '.mkv']
    video_files = []
    for ext in video_extensions:
        video_files.extend(list(video_dir.glob(f'*{ext}')))
    
    if not video_files:
        print("⚠️  No video files found in input_videos/")
        print("   Place your video file in input_videos/ before running")
        return False
    
    print(f"✓ Found {len(video_files)} video file(s):")
    for video in video_files:
        print(f"   - {video.name}")
    
    return True


def check_config():
    """Check if config file exists"""
    print("\nChecking configuration...")
    if not Path('config.py').exists():
        print("❌ config.py not found")
        return False
    
    print("✓ config.py")
    
    # Try to import config
    try:
        import config
        print(f"   Input: {config.INPUT_VIDEO_PATH}")
        print(f"   Output: {config.OUTPUT_VIDEO_PATH}")
        print(f"   Model: {config.MODEL_PATH}")
        return True
    except Exception as e:
        print(f"❌ Error loading config: {e}")
        return False


def main():
    """Run all checks"""
    print("=" * 60)
    print("Football Analyzer - Setup Check")
    print("=" * 60)
    
    checks = [
        ("Python Version", check_python_version),
        ("Dependencies", check_dependencies),
        ("Directory Structure", check_directory_structure),
        ("Model File", check_model_file),
        ("Input Video", check_input_video),
        ("Configuration", check_config)
    ]
    
    results = []
    for name, check_func in checks:
        result = check_func()
        results.append((name, result))
    
    print("\n" + "=" * 60)
    print("Summary:")
    print("=" * 60)
    
    all_passed = True
    for name, result in results:
        status = "✓" if result else "❌"
        print(f"{status} {name}")
        if not result:
            all_passed = False
    
    print("\n" + "=" * 60)
    if all_passed:
        print("✅ All checks passed! Ready to run:")
        print("   python main.py")
    else:
        print("⚠️  Some checks failed. Please address the issues above.")
        print("\nQuick fixes:")
        print("1. Install dependencies: pip install -r requirements.txt")
        print("2. Download/place YOLO model in models/")
        print("3. Place input video in input_videos/")
        print("4. Update paths in config.py if needed")
    print("=" * 60)


if __name__ == '__main__':
    main()
