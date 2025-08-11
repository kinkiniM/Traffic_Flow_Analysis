"""
Traffic Flow Analysis - Full Automation Pipeline
-------------------------------------------------
This script automates the **entire traffic flow analysis process** in one run.
It executes each step sequentially and logs all outputs into a file.

Pipeline Steps:
1. Install all required dependencies from `requirements.txt`.
2. Download the full traffic video from YouTube (`video_download.py`).
3. Trim the downloaded video to the first N seconds (`trim_video.py`).
4. Run traffic detection, tracking, and lane counting (`traffic_flow.py`).
5. Verify detected vehicle counts and save verification samples (`varify_counts.py`).

Features:
- Timestamps each step in the log file.
- Logs both standard output and errors/warnings.
- Stops the pipeline immediately if any step fails.
- Designed for **Windows command-line execution**.

Author: Kinkini Majumdar
"""
import subprocess
import sys
import datetime

# Log file path
log_file = "run_pipeline.log"

def log_message(message):
    """Write message to log file and print to console."""
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    full_message = f"[{timestamp}] {message}"
    print(full_message)
    with open(log_file, "a") as f:
        f.write(full_message + "\n")

def run_command(command, description):
    """Run a shell command and log output."""
    log_message(f"--- Starting: {description} ---")
    try:
        result = subprocess.run(command, shell=True, capture_output=True, text=True)
        log_message(result.stdout)
        if result.stderr:
            log_message("ERROR/WARNING: " + result.stderr)
        log_message(f"--- Finished: {description} ---\n")
    except Exception as e:
        log_message(f"XXXX Failed: {description} - {e} XXXX")
        sys.exit(1)

if __name__ == "__main__":
    # Clear old log
    with open(log_file, "w") as f:
        f.write("=== Traffic Flow Automation Log ===\n")

    log_message("#### Starting full pipeline run ####")

    # Step 1: Install dependencies
    run_command("pip install -r requirements.txt", "Install dependencies")

    # Step 2: Download full video
    run_command("python video_download.py", "Download full video")

    # Step 3: Trim video to 1-2 mins
    run_command("python trim_video.py", "Trim video to short clip")

    # Step 4: Run traffic flow analysis
    run_command("python traffic_flow.py", "Traffic flow detection & counting")

    # Step 5: Verify counts
    run_command("python varify_counts.py", "Verify lane assignments")

    log_message("#### Pipeline complete. All logs saved to run_pipeline.log####")
