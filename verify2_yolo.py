import cv2
import numpy as np
from ultralytics import YOLO

# Load trained YOLOv8 model
model = YOLO("yolov8n.pt")

# Load video file instead of webcam
video_path ="C:\\Users\\kalyani\\Downloads\\testvideo.mp4"   # Change to your video file
cap = cv2.VideoCapture(video_path)

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break  # Stop if video ends

    # Run YOLO on the frame
    results = model(frame, conf=0.4)

    # Draw bounding boxes
    for result in results:
        for box in result.boxes:
            x1, y1, x2, y2 = map(int, box.xyxy[0])  # Bounding box coordinates
            cls = int(box.cls)
            label = model.names[cls]
            conf = box.conf[0]  # Confidence score

            # Draw bounding box
            cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
            cv2.putText(frame, f"{label} {conf:.2f}", (x1, y1 - 10),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

    # Show the video with detections
    cv2.imshow("Traffic Detection", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break  # Press 'q' to exit

cap.release()
cv2.destroyAllWindows()
