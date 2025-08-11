
"""
Traffic Flow Detection & Lane-Based Vehicle Counting
-----------------------------------------------------

This script:
1. Detects vehicles in a traffic video using YOLOv8.
2. Tracks vehicles across frames with the SORT tracking algorithm.
3. Assigns vehicles to predefined polygonal lanes.
4. Counts unique vehicles per lane.
5. Saves results (Vehicle ID, Lane, Frame, Timestamp) to CSV.

Requirements:
- ultralytics (YOLOv8)
- OpenCV (cv2)
- pandas
- numpy
- sort.py (SORT tracker implementation)

Author: Kinkini Majumdar
Date: 11-08-2025
"""

import cv2
import pandas as pd
import numpy as np
from ultralytics import YOLO
from sort import Sort

# -------------------------
# CONFIGURATION
# -------------------------
MODEL_PATH = "yolov8n.pt"
VIDEO_PATH = "traffic_video.mp4"
CONF_THRESH = 0.5
MIN_WIDTH, MIN_HEIGHT = 30, 30
MIN_MOVE_DIST = 15
LANE_CHANGE_COOLDOWN = 60  # frames

# -------------------------
# LOAD MODEL & VIDEO
# -------------------------
model = YOLO(MODEL_PATH)
cap = cv2.VideoCapture(VIDEO_PATH)

frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
fps = cap.get(cv2.CAP_PROP_FPS)

# -------------------------
# DEFINE CURVED LANE POLYGONS (for 1280x720)
# -------------------------
lane_polygons = {
    1: np.array([(0, 720), (400, 400), (500, 0), (0, 0)], np.int32),
    2: np.array([(400, 720), (800, 400), (700, 0), (500, 0)], np.int32),
    3: np.array([(800, 720), (1280, 720), (1280, 0), (700, 0)], np.int32)
}
# If your resolution is different, scale points:
scale_x = frame_width / 1280
scale_y = frame_height / 720
for k in lane_polygons:
    lane_polygons[k] = np.array(
        [(int(x*scale_x), int(y*scale_y)) for x, y in lane_polygons[k]],
        np.int32
    )

# -------------------------
# TRACKER & COUNTERS
# -------------------------
tracker = Sort()
frame_count = 0
lane_counts = {1: set(), 2: set(), 3: set()}
last_positions = {}
last_lane_assignment = {}
csv_data = []

# -------------------------
# PROCESS VIDEO
# -------------------------
while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    frame_count += 1
    results = model(frame, verbose=False)[0]
    detections = []

    for box in results.boxes.data:
        x1, y1, x2, y2, score, cls = box.tolist()
        if score < CONF_THRESH:
            continue
        if int(cls) in [2, 3, 5, 7]:
            if (x2 - x1) >= MIN_WIDTH and (y2 - y1) >= MIN_HEIGHT:
                detections.append([x1, y1, x2, y2, score])

    detections = np.array(detections) if detections else np.empty((0, 5))
    tracked_objects = tracker.update(detections)

    for x1, y1, x2, y2, track_id in tracked_objects:
        cx = int((x1 + x2) / 2)
        cy = int((y1 + y2) / 2)

        # Movement filter
        if track_id in last_positions:
            prev_cx, prev_cy = last_positions[track_id]
            move_dist = np.sqrt((cx - prev_cx) ** 2 + (cy - prev_cy) ** 2)
            if move_dist < MIN_MOVE_DIST:
                continue
        last_positions[track_id] = (cx, cy)

        # Polygon-based lane assignment
        for lane_num, poly in lane_polygons.items():
            if cv2.pointPolygonTest(poly, (cx, cy), False) >= 0:
                last_lane, last_frame = last_lane_assignment.get(track_id, (None, -9999))
                if lane_num != last_lane and frame_count - last_frame < LANE_CHANGE_COOLDOWN:
                    break
                if track_id not in lane_counts[lane_num]:
                    lane_counts[lane_num].add(track_id)
                    csv_data.append([int(track_id), lane_num, frame_count, round(frame_count / fps, 2)])
                last_lane_assignment[track_id] = (lane_num, frame_count)
                break

        # Draw box & ID
        cv2.rectangle(frame, (int(x1), int(y1)), (int(x2), int(y2)), (0, 255, 0), 2)
        cv2.putText(frame, f"ID:{int(track_id)}", (int(x1), int(y1) - 10),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 0), 2)

    # Draw lane polygons & counts
    for lane_num, poly in lane_polygons.items():
        cv2.polylines(frame, [poly], isClosed=True, color=(255, 0, 0), thickness=2)
        text_pos = tuple(poly[0] + np.array([10, -10]))
        cv2.putText(frame, f"Lane {lane_num}: {len(lane_counts[lane_num])}", text_pos,
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)

    cv2.imshow("Traffic Flow", frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()

# Save CSV
df = pd.DataFrame(csv_data, columns=["VehicleID", "LaneNumber", "Frame", "Timestamp"])
df.to_csv("vehicle_counts.csv", index=False)

print("\n--- Final Vehicle Counts ---")
for lane in lane_counts:
    print(f"Lane {lane}: {len(lane_counts[lane])} vehicles")
