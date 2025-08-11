"""
Video Trimming Utility
----------------------
This script trims the first N seconds from a given traffic video file.
It automatically downloads and sets up a local `ffmpeg` binary if it’s not already available.

Workflow:
1. Check if `traffic_video_full.mp4` exists (full-length source video).
2. Ensure ffmpeg is installed locally (downloads portable binary if missing).
3. Use ffmpeg to trim the first `TRIM_DURATION` seconds and save as a shorter clip.

Dependencies:
- Python standard library (os, subprocess, urllib, zipfile)
- ffmpeg (downloaded automatically if not available)

Author: Kinkini Majumdar
"""

import os
import subprocess
import urllib.request
import zipfile

# -----------------------------
# CONFIGURATION
# -----------------------------
INPUT_FILE = "traffic_video_full.mp4"  # full-length video
OUTPUT_FILE = "traffic_video.mp4"      # trimmed video (first 120s)
TRIM_DURATION = 120                    # seconds
FFMPEG_DIR = "ffmpeg-bin"
FFMPEG_ZIP_URL = "https://www.gyan.dev/ffmpeg/builds/ffmpeg-release-essentials.zip"

# -----------------------------
# Step 1: Ensure ffmpeg is available locally
# -----------------------------
def ensure_ffmpeg():
    if not os.path.exists(FFMPEG_DIR):
        os.makedirs(FFMPEG_DIR, exist_ok=True)
        print("### Downloading ffmpeg.exe...")
        zip_path = os.path.join(FFMPEG_DIR, "ffmpeg.zip")
        urllib.request.urlretrieve(FFMPEG_ZIP_URL, zip_path)

        print("### Extracting ffmpeg...")
        with zipfile.ZipFile(zip_path, "r") as zip_ref:
            zip_ref.extractall(FFMPEG_DIR)
        os.remove(zip_path)

        # Find ffmpeg.exe inside extracted folders
        for root, dirs, files in os.walk(FFMPEG_DIR):
            if "ffmpeg.exe" in files:
                exe_path = os.path.join(root, "ffmpeg.exe")
                # Move it to ffmpeg-bin folder root
                os.rename(exe_path, os.path.join(FFMPEG_DIR, "ffmpeg.exe"))
                break
        print("### ffmpeg ready!")

# -----------------------------
# Step 2: Trim video
# -----------------------------
def trim_video():
    if not os.path.exists(INPUT_FILE):
        raise FileNotFoundError(f"XXX Input file '{INPUT_FILE}' not found. Run video_download.py first.")

    ffmpeg_path = os.path.join(FFMPEG_DIR, "ffmpeg.exe")
    if not os.path.exists(ffmpeg_path):
        ensure_ffmpeg()

    print(f"### Trimming first {TRIM_DURATION} seconds from {INPUT_FILE}...")
    subprocess.run([
        ffmpeg_path,
        "-ss", "0",
        "-i", INPUT_FILE,
        "-t", str(TRIM_DURATION),
        "-c", "copy",
        OUTPUT_FILE
    ], check=True)
    print(f"### Trim complete! Saved to '{OUTPUT_FILE}'")

# -----------------------------
# MAIN
# -----------------------------
if __name__ == "__main__":
    trim_video()
