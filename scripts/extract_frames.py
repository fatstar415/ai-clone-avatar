import cv2
import os
import sys

# Usage: python extract_frames.py <video_path> <output_dir>

def extract_frames(video_path, output_dir):
    os.makedirs(output_dir, exist_ok=True)
    cap = cv2.VideoCapture(video_path)
    count = 0
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        frame_path = os.path.join(output_dir, f"frame_{count:05d}.jpg")
        cv2.imwrite(frame_path, frame)
        count += 1
    cap.release()
    print(f"Extracted {count} frames to {output_dir}")

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python extract_frames.py <video_path> <output_dir>")
        sys.exit(1)
    extract_frames(sys.argv[1], sys.argv[2]) 