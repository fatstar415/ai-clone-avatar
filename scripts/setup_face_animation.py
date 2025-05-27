#!/usr/bin/env python3
"""
Setup script for face animation models (SadTalker and Wav2Lip).
This script helps download and configure the necessary models.
"""

import os
import subprocess
import sys
import requests
from pathlib import Path
from tqdm import tqdm

# Project root directory
PROJECT_ROOT = Path(__file__).parent.parent.absolute()
MODELS_DIR = PROJECT_ROOT / "models"

# Model URLs
SADTALKER_MODELS = {
    "epoch_20": "https://github.com/OpenTalker/SadTalker/releases/download/v0.0.2/epoch_20.pth",
    "mapping": "https://github.com/OpenTalker/SadTalker/releases/download/v0.0.2/mapping_00109-model.pth.tar",
    "mapping_emo": "https://github.com/OpenTalker/SadTalker/releases/download/v0.0.2/mapping_00229-model.pth.tar",
    "sad": "https://github.com/OpenTalker/SadTalker/releases/download/v0.0.2/SadTalker_V0.0.2_256.safetensors",
    "wav2lip": "https://github.com/OpenTalker/SadTalker/releases/download/v0.0.2/wav2lip.pth",
    "gfpgan": "https://github.com/OpenTalker/SadTalker/releases/download/v0.0.2/GFPGANv1.4.pth",
    "auido2pose_00140-model": "https://github.com/OpenTalker/SadTalker/releases/download/v0.0.2/auido2pose_00140-model.pth",
    "auido2exp_00300-model": "https://github.com/OpenTalker/SadTalker/releases/download/v0.0.2/auido2exp_00300-model.pth",
    "facevid2vid_00189-model": "https://github.com/OpenTalker/SadTalker/releases/download/v0.0.2/facevid2vid_00189-model.pth.tar",
    "shape_predictor_68_face_landmarks": "https://github.com/OpenTalker/SadTalker/releases/download/v0.0.2/shape_predictor_68_face_landmarks.dat",
    "hub": "https://github.com/OpenTalker/SadTalker/releases/download/v0.0.2/hub.zip",
}

WAV2LIP_MODELS = {
    "wav2lip": "https://github.com/Rudrabha/Wav2Lip/releases/download/v1.0/wav2lip.pth",
    "wav2lip_gan": "https://github.com/Rudrabha/Wav2Lip/releases/download/v1.0/wav2lip_gan.pth"
}

def download_file(url, dest_path):
    """Download a file with progress bar."""
    response = requests.get(url, stream=True)
    total_size = int(response.headers.get('content-length', 0))
    
    dest_path.parent.mkdir(parents=True, exist_ok=True)
    
    with open(dest_path, 'wb') as f, tqdm(
        desc=dest_path.name,
        total=total_size,
        unit='iB',
        unit_scale=True
    ) as pbar:
        for data in response.iter_content(chunk_size=1024):
            size = f.write(data)
            pbar.update(size)

def setup_sadtalker():
    """Set up SadTalker model."""
    sadtalker_dir = MODELS_DIR / "sadtalker"
    if not sadtalker_dir.exists():
        print("Cloning SadTalker repository...")
        subprocess.run([
            "git", "clone", 
            "https://github.com/OpenTalker/SadTalker.git",
            str(sadtalker_dir)
        ], check=True)
        
        # Checkout v0.0.2 release
        print("Checking out v0.0.2 release...")
        subprocess.run([
            "git", "-C", str(sadtalker_dir), "fetch", "--tags"
        ], check=True)
        subprocess.run([
            "git", "-C", str(sadtalker_dir), "checkout", "v0.0.2"
        ], check=True)
    
    # Install SadTalker dependencies if not already installed
    print("Checking SadTalker dependencies...")
    subprocess.run([
        sys.executable, "-m", "pip", "install", "-r",
        str(sadtalker_dir / "requirements.txt")
    ], check=True)
    
    # Download pre-trained models
    print("\nDownloading SadTalker pre-trained models...")
    checkpoints_dir = sadtalker_dir / "checkpoints"
    # Create checkpoints directory if it doesn't exist
    try:
        checkpoints_dir.mkdir(exist_ok=True)
    except FileExistsError:
        pass  # Directory already exists, continue
    
    # Define file extensions for each model
    model_extensions = {
        "epoch_20": ".pth",
        "mapping": ".pth.tar",
        "mapping_emo": ".pth.tar",
        "sad": ".safetensors",
        "wav2lip": ".pth",
        "gfpgan": ".pth",
        "auido2pose_00140-model": ".pth",
        "auido2exp_00300-model": ".pth",
        "facevid2vid_00189-model": ".pth.tar",
        "shape_predictor_68_face_landmarks": ".dat",
        "hub": ".zip"
    }
    
    for model_name, url in SADTALKER_MODELS.items():
        ext = model_extensions[model_name]
        model_path = checkpoints_dir / f"{model_name}{ext}"
        
        if not model_path.exists():
            print(f"Downloading {model_name}...")
            download_file(url, model_path)
            
            # Extract zip files
            if ext == ".zip":
                print(f"Extracting {model_name}...")
                import zipfile
                with zipfile.ZipFile(model_path, 'r') as zip_ref:
                    zip_ref.extractall(checkpoints_dir)
        else:
            print(f"{model_name} already downloaded.")
            
            # Ensure zip files are extracted
            if ext == ".zip" and not (checkpoints_dir / "hub").exists():
                print(f"Extracting {model_name}...")
                import zipfile
                with zipfile.ZipFile(model_path, 'r') as zip_ref:
                    zip_ref.extractall(checkpoints_dir)

def setup_wav2lip():
    """Set up Wav2Lip model."""
    wav2lip_dir = MODELS_DIR / "wav2lip"
    if not wav2lip_dir.exists():
        print("Cloning Wav2Lip repository...")
        subprocess.run([
            "git", "clone",
            "https://github.com/Rudrabha/Wav2Lip.git",
            str(wav2lip_dir)
        ], check=True)
        
        # Install Wav2Lip dependencies
        print("Installing Wav2Lip dependencies...")
        subprocess.run([
            sys.executable, "-m", "pip", "install", "-r",
            str(wav2lip_dir / "requirements.txt")
        ], check=True)
    
    # Download pre-trained models
    print("\nDownloading Wav2Lip pre-trained models...")
    checkpoints_dir = wav2lip_dir / "checkpoints"
    for model_name, url in WAV2LIP_MODELS.items():
        model_path = checkpoints_dir / f"{model_name}.pth"
        if not model_path.exists():
            print(f"Downloading {model_name}...")
            download_file(url, model_path)
        else:
            print(f"{model_name} already downloaded.")

def main():
    """Main setup function."""
    print("Setting up face animation models...")
    
    # Create models directory if it doesn't exist
    MODELS_DIR.mkdir(exist_ok=True)
    
    # Install required packages
    subprocess.run([
        sys.executable, "-m", "pip", "install",
        "requests", "tqdm"
    ], check=True)
    
    # Set up each model
    setup_sadtalker()
    setup_wav2lip()
    
    print("\nSetup complete! You can now use SadTalker and Wav2Lip for face animation.")
    print("The following models are available:")
    print("\nSadTalker models:")
    for model in SADTALKER_MODELS.keys():
        print(f"- {model}")
    print("\nWav2Lip models:")
    for model in WAV2LIP_MODELS.keys():
        print(f"- {model}")

if __name__ == "__main__":
    main() 