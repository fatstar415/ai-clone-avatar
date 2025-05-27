import sys
import os
import subprocess

def convert_to_wav(input_path, output_path):
    cmd = [
        'ffmpeg', '-y', '-i', input_path,
        '-ar', '16000', '-ac', '1', '-vn', output_path
    ]
    subprocess.run(cmd, check=True)
    print(f"Converted {input_path} to {output_path}")

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python preprocess_audio.py <input_audio> <output_wav>")
        sys.exit(1)
    convert_to_wav(sys.argv[1], sys.argv[2]) 