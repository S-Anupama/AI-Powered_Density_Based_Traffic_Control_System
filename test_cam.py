import cv2
from ultralytics import YOLO

# Load your trained YOLOv8 model
model = YOLO("runs/detect/train13/weights/best.pt")  # Ensure this is your trained model

# Open the camera (Try changing 0 to 1 if the wrong camera opens)
cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("Error: Could not open the camera.")
    exit()

while True:
    ret, frame = cap.read()
    if not ret:
        print("Failed to capture frame")
        break

    # Run YOLO detection on the frame
    results = model(frame, conf=0.5)

    # Draw bounding boxes on detected objects
    for result in results:
        for box in result.boxes:
            x1, y1, x2, y2 = map(int, box.xyxy[0])  # Get bounding box coordinates
            cls = int(box.cls)  # Get class ID
            conf = box.conf[0]  # Get confidence score

            # Define labels based on trained classes
            labels = ["bike", "truck", "car", "bus"]  # Modify according to your dataset
            label = labels[cls] if cls < len(labels) else "Unknown"

            # Draw bounding box and label
            cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
            cv2.putText(frame, f"{label} {conf:.2f}", (x1, y1 - 10),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

    # Show the detection window
    cv2.imshow("YOLOv8m Detection", frame)

    # Press 'q' to exit
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
