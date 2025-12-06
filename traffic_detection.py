import cv2
import serial
import time
from ultralytics import YOLO

# Load YOLO model
model = YOLO(r"C:\Users\kalyani\PycharmProjects\DBTCS\runs\detect\train19\weights\best.pt")

# Serial communication
ser = serial.Serial('COM3', 9600, timeout=1)
time.sleep(2)

# Class labels and weights
class_names = {0: "bike", 1: "truck", 2: "car"}
class_weights = {"bike": 1, "car": 2, "truck": 3}

# Adjusted for your setup: 1 bike (1), 2 trucks (8), 7 cars (7) = 16 max CEV
MAX_VEHICLES = 21

# Capture video
cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1920)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 1080)

def calculate_green_time(vehicle_counts):
    CEV = sum(vehicle_counts[cls] * class_weights[cls] for cls in vehicle_counts)
    if CEV <= 0.25 * MAX_VEHICLES:
        return "Low", 5
    elif CEV <= 0.5 * MAX_VEHICLES:
        return "Medium", 10
    elif CEV <= 0.75 * MAX_VEHICLES:
        return "High", 20
    else:
        return "Extreme", 30

def annotate_and_count(zone_img, result):
    counts = {"bike": 0, "car": 0, "truck": 0}
    for box in result[0].boxes:
        cls_id = int(box.cls)
        label = class_names.get(cls_id, str(cls_id))
        if label in counts:
            counts[label] += 1

        conf = float(box.conf)
        color = {
            "bike": (255, 0, 0),
            "truck": (0, 255, 255),
            "car": (0, 255, 0)
        }.get(label, (0, 255, 255))

        x1, y1, x2, y2 = map(int, box.xyxy[0])
        cv2.rectangle(zone_img, (x1, y1), (x2, y2), color, 2)
        cv2.putText(zone_img, f"{label} {conf:.2f}", (x1, y1 - 10),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.6, color, 2)
    return zone_img, counts

start_time = time.time()
initial_delay = 15
current_road = 0

while True:
    ret, frame = cap.read()
    if not ret:
        break

    height, width, _ = frame.shape
    zone_width = width // 3

    # Define zones
    zone1 = frame[:, :zone_width]
    zone2 = frame[:, zone_width:2 * zone_width]
    zone3 = frame[:, 2 * zone_width:]

    # YOLO detection
    results1 = model(zone1, conf=0.5, verbose=False)
    results2 = model(zone2, conf=0.5, verbose=False)
    results3 = model(zone3, conf=0.5, verbose=False)

    # Annotate and count vehicles
    annotated_zone1, counts1 = annotate_and_count(zone1.copy(), results1)
    annotated_zone2, counts2 = annotate_and_count(zone2.copy(), results2)
    annotated_zone3, counts3 = annotate_and_count(zone3.copy(), results3)

    # Delay logic
    elapsed = time.time() - start_time
    if elapsed < initial_delay:
        combined = cv2.hconcat([annotated_zone1, annotated_zone2, annotated_zone3])
        zone_width = combined.shape[1] // 3
        lane_color = (255, 255, 255)
        thickness = 2
        cv2.line(combined, (zone_width, 0), (zone_width, height), lane_color, thickness)
        cv2.line(combined, (2 * zone_width, 0), (2 * zone_width, height), lane_color, thickness)

        for i in range(3):
            x_pos = i * zone_width + 20
            cv2.putText(combined, f"Road {i + 1}", (x_pos, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 0, 255), 2)

        # Add "Initializing..." label at the bottom left in black color
        cv2.putText(combined, f"Initializing... {int(initial_delay - elapsed)}s",
                    (20, height - 30), cv2.FONT_HERSHEY_SIMPLEX, 1.2, (0, 0, 0), 3)

        cv2.imshow("Traffic Detection", combined)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
        continue

    # Green time calculation in fixed order: Road 1 → Road 2 → Road 3
    road_counts = [counts1, counts2, counts3]
    current_counts = road_counts[current_road]
    _, selected_duration = calculate_green_time(current_counts)

    # Send signal to ESP32
    ser.write(f"{current_road + 1}{selected_duration}\n".encode())
    print(f"ROAD {current_road + 1} GREEN | Time: {selected_duration}s")

    time.sleep(2)  # Sync with Arduino yellow delay

    # Countdown
    for sec_left in range(selected_duration, 0, -1):
        display_zone1 = annotated_zone1.copy()
        display_zone2 = annotated_zone2.copy()
        display_zone3 = annotated_zone3.copy()

        label1 = f"Road 1: {sec_left}s" if current_road == 0 else "Road 1"
        label2 = f"Road 2: {sec_left}s" if current_road == 1 else "Road 2"
        label3 = f"Road 3: {sec_left}s" if current_road == 2 else "Road 3"

        color1 = (0, 255, 0) if current_road == 0 else (0, 0, 255)
        color2 = (0, 255, 0) if current_road == 1 else (0, 0, 255)
        color3 = (0, 255, 0) if current_road == 2 else (0, 0, 255)

        cv2.putText(display_zone1, label1, (20, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.9, color1, 2)
        cv2.putText(display_zone2, label2, (20, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.9, color2, 2)
        cv2.putText(display_zone3, label3, (20, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.9, color3, 2)

        combined = cv2.hconcat([display_zone1, display_zone2, display_zone3])

        zone_width = combined.shape[1] // 3
        cv2.line(combined, (zone_width, 0), (zone_width, height), (255, 255, 255), 2)
        cv2.line(combined, (2 * zone_width, 0), (2 * zone_width, height), (255, 255, 255), 2)

        cv2.imshow("Traffic Detection", combined)
        if cv2.waitKey(1000) & 0xFF == ord('q'):
            break

    # Move to next road
    current_road = (current_road + 1) % 3

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Cleanup
cap.release()
cv2.destroyAllWindows()
ser.close()

