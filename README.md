# 🚗 Traffic Flow Analysis & Vehicle Counting

## 📌 Project Overview
This project detects and counts vehicles in a traffic video, categorizing them into **three lanes**.  
It automates the entire process — from downloading the video to generating CSV reports — with a **single command**.

**Key Features:**
- **Vehicle Detection**: YOLOv8 pre-trained on COCO dataset.
- **Lane Definition & Counting**: Counts vehicles separately for each of three lanes.
- **Vehicle Tracking**: Prevents duplicate counts using SORT tracking algorithm.
- **Real-time Processing**: Optimized for smooth performance on standard hardware.
- **Full Automation**: One script runs the entire pipeline.

---

## 📂 Deliverables
1. **Python Scripts**:
   - `run_all.py` → Main pipeline (one-command execution)
   - `video_download.py` → Downloads full traffic video
   - `trim_video.py` → Creates short 1–2 min clip
   - `traffic_flow.py` → Detection, tracking, lane counting
   - `varify_counts.py` → Verification and sample frame extraction
2. **README.md** → Setup and usage guide (this file)
3. **Demo Video** → Processed output with overlay and counts
4. **GitHub Repository** → Organized with all code, requirements, and assets
5. **vehicle_counts.csv** → Output CSV with:
   - Vehicle ID
   - Lane number
   - Frame count
   - Timestamp

---

## 🛠 Installation

### 1. Clone the Repository
```bash
git clone https://github.com/yourusername/traffic-flow-analysis.git
cd traffic-flow-analysis

### 2️. Create Virtual Environment (Windows)
```bash
python -m venv venv
venv\Scripts\activate

### 3. Install Dependencies
```bash
pip install -r requirements.txt

### 4. Execution Instructions
Run Entire Pipeline
Run the entire workflow (download → trim → process → verify) with a ```bash
python run_all.py

This will:
1. Install dependencies from requirements.txt
2. Download the full traffic video
3. Trim it to a short clip
4. Run traffic detection & lane counting (traffic_flow.py)
5. Verify lane assignments & save sample frames (varify_counts.py)

A full log will be saved in:
run_pipeline.log