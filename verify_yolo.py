import cv2
from ultralytics import YOLO

# Load your trained YOLOv8 model
model = YOLO("runs/detect/train13/weights/best.pt")  # Replace with your trained model path

# Open camera (0 for default webcam, change if using an external camera)
cap = cv2.VideoCapture(1)

if not cap.isOpened():
    print("Error: Could not open the camera.")
    exit()

while True:
    ret, frame = cap.read()
    if not ret:
        print("Error: Failed to capture image")
        break

    # Run YOLOv8 model on the frame
    results = model(frame, conf=0.5)  # Adjust confidence threshold if needed

    # Plot detections on the frame
    for result in results:
        for box in result.boxes:
            x1, y1, x2, y2 = map(int, box.xyxy[0])  # Get bounding box coordinates
            cls = int(box.cls)  # Get class index
            conf = box.conf[0]  # Confidence score

            # Define labels based on training
            labels = {0: "Bike", 1: "Car", 2: "Bus", 3: "Truck"}  # Modify according to your trained classes
            label = labels.get(cls, "Unknown")

            # Draw bounding box and label
            cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
            cv2.putText(frame, f"{label} {conf:.2f}", (x1, y1 - 10),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

    # Show the frame with detections
    cv2.imshow("YOLOv8 Model Verification", frame)

    # Press 'q' to exit the loop
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release camera and close all windows
cap.release()
cv2.destroyAllWindows()
