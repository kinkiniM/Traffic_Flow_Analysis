
"""
video_download.py
-----------------
Downloads a YouTube video in MP4 format using yt_dlp.
This version downloads the full video without trimming.
"""

import yt_dlp

# YouTube video URL
VIDEO_URL = "https://www.youtube.com/watch?v=MNn9qKG2UFI"

# Output file name
OUTPUT_FILE = "traffic_video_full.mp4"

# yt_dlp options
ydl_opts = {
    'format': 'best[ext=mp4]',
    'outtmpl': OUTPUT_FILE
}

print(f"Starting full download from {VIDEO_URL}...")
with yt_dlp.YoutubeDL(ydl_opts) as ydl:
    ydl.download([VIDEO_URL])

print(f"### Download complete: {OUTPUT_FILE}")
