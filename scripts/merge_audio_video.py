import sys
import subprocess

def merge_audio_video(video_path, audio_path, output_path):
    cmd = [
        'ffmpeg', '-y', '-i', video_path, '-i', audio_path,
        '-c:v', 'copy', '-c:a', 'aac', output_path
    ]
    subprocess.run(cmd, check=True)
    print(f"Merged {video_path} and {audio_path} into {output_path}")

if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Usage: python merge_audio_video.py <video_path> <audio_path> <output_path>")
        sys.exit(1)
    merge_audio_video(sys.argv[1], sys.argv[2], sys.argv[3]) 