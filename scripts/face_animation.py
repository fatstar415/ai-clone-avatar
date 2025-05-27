#!/usr/bin/env python3
"""
Face animation script using SadTalker and Wav2Lip.
This script provides functions to animate faces using either model.
"""

import os
import sys
import subprocess
from pathlib import Path
import argparse

# Project root directory
PROJECT_ROOT = Path(__file__).parent.parent.absolute()
MODELS_DIR = PROJECT_ROOT / "models"
OUTPUT_DIR = PROJECT_ROOT / "outputs"

def animate_with_sadtalker(image_path, audio_path, output_path=None):
    """
    Animate a face using SadTalker.
    
    Args:
        image_path (str): Path to the source image
        audio_path (str): Path to the audio file
        output_path (str, optional): Path for the output video
    """
    if output_path is None:
        output_path = OUTPUT_DIR / "sadtalker_output.mp4"
    
    sadtalker_dir = MODELS_DIR / "sadtalker"
    if not sadtalker_dir.exists():
        raise RuntimeError("SadTalker not set up. Run setup_face_animation.py first.")
    
    # Convert paths to absolute paths
    image_path = Path(image_path).absolute()
    audio_path = Path(audio_path).absolute()
    output_path = Path(output_path).absolute()
    
    # Ensure output directory exists
    output_path.parent.mkdir(parents=True, exist_ok=True)
    
    # Run SadTalker inference with optimized parameters for v0.0.2
    cmd = [
        "python", str(sadtalker_dir / "inference.py"),
        "--driven_audio", str(audio_path),
        "--source_image", str(image_path),
        "--result_dir", str(output_path.parent),
        "--enhancer", "gfpgan",  # Use GFPGAN for face enhancement
        "--preprocess", "full",  # Process the full image for better quality
        "--still",  # Reduce head motion for smoother animation
        "--expression_scale", "0.8",  # Slightly reduce expression intensity
        "--background_enhancer", "realesrgan",  # Enhance the background
        "--checkpoint_dir", "checkpoints"  # Specify checkpoint directory
    ]
    
    print(f"Running SadTalker with command: {' '.join(cmd)}")
    subprocess.run(cmd, check=True)
    
    # Find the generated video in the results directory
    result_dir = output_path.parent
    timestamp_dir = max((d for d in result_dir.iterdir() if d.is_dir()), key=lambda x: x.stat().st_mtime)
    video_file = next(timestamp_dir.glob("*.mp4"))
    
    # Move the video to the desired output location
    video_file.rename(output_path)
    
    return output_path

def animate_with_wav2lip(video_path, audio_path, output_path=None):
    """
    Animate lips using Wav2Lip.
    
    Args:
        video_path (str): Path to the source video
        audio_path (str): Path to the audio file
        output_path (str, optional): Path for the output video
    """
    if output_path is None:
        output_path = OUTPUT_DIR / "wav2lip_output.mp4"
    
    wav2lip_dir = MODELS_DIR / "wav2lip"
    if not wav2lip_dir.exists():
        raise RuntimeError("Wav2Lip not set up. Run setup_face_animation.py first.")
    
    # Convert paths to absolute paths
    video_path = Path(video_path).absolute()
    audio_path = Path(audio_path).absolute()
    output_path = Path(output_path).absolute()
    
    # Ensure output directory exists
    output_path.parent.mkdir(parents=True, exist_ok=True)
    
    # Run Wav2Lip inference
    # Note: You'll need to adjust this command based on Wav2Lip's actual usage
    cmd = [
        "python", str(wav2lip_dir / "inference.py"),
        "--face", str(video_path),
        "--audio", str(audio_path),
        "--outfile", str(output_path),
        "--pads", "0 20 0 0"  # Optional: adjust face detection padding
    ]
    
    print(f"Running Wav2Lip with command: {' '.join(cmd)}")
    subprocess.run(cmd, check=True)
    
    return output_path

def main():
    """Command-line interface for face animation."""
    parser = argparse.ArgumentParser(description="Face animation using SadTalker or Wav2Lip")
    parser.add_argument("--model", choices=["sadtalker", "wav2lip"], required=True,
                      help="Which model to use for animation")
    parser.add_argument("--image", help="Path to source image (for SadTalker)")
    parser.add_argument("--video", help="Path to source video (for Wav2Lip)")
    parser.add_argument("--audio", required=True, help="Path to audio file")
    parser.add_argument("--output", help="Path for output video")
    
    args = parser.parse_args()
    
    try:
        if args.model == "sadtalker":
            if not args.image:
                parser.error("--image is required for SadTalker")
            output = animate_with_sadtalker(args.image, args.audio, args.output)
        else:  # wav2lip
            if not args.video:
                parser.error("--video is required for Wav2Lip")
            output = animate_with_wav2lip(args.video, args.audio, args.output)
        
        print(f"\nAnimation complete! Output saved to: {output}")
    
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main() 