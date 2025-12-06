# AI---Powered-density-Based-Traffic-Control-system
A real-time density-based traffic control system using Python, YOLO, and ESP32. Automatically detects vehicles, calculates traffic density, and dynamically adjusts signal timing for efficient traffic management.

# 🚦 Density-Based Traffic Control System (DBTCS)  

_A computer vision-powered smart traffic management system using ESP32, Python, and YOLO models._

## Project Overview  

This project implements a **density-based traffic control system** that dynamically adjusts traffic signal timings based on the number of vehicles present on each road. The system combines:

- 🧠 **Python + OpenCV + YOLOv8** for real-time vehicle detection  
- 📷 **USB webcam** for capturing live traffic (top-down view)  
- 🔌 **ESP32 microcontroller** to control traffic lights  
- 🔁 **Serial communication** (Python → ESP32) for sending green-light timing and selected road  
- 🚦 **Arduino traffic light modules** for real-world behavior (Red → Yellow → Green)

The system improves traffic flow, reduces waiting times, and prioritizes roads based on density.

## Features

- Real-time detection of cars, bikes, rickshaws, and trucks  
- Automatic green-light duration based on traffic density  
- Fixed road cycle order: Road 1 → Road 2 → Road 3  
- 10-second initialization delay before the first green signal  
- Python GUI with countdown timer synchronized with ESP32 signals  
- Supports a top-down view for all roads simultaneously  


## 🧠 YOLO Model Files

Due to GitHub’s file size limit, the trained YOLO model weights are stored in **Google Drive**:

https://drive.google.com/drive/folders/1AXIH7Cv-V3ywwcT9G9Pw39NAmzxUEEfp?usp=drive_link


## ⚙️ Hardware Requirements

- ESP32 Dev Module  
- 3× Traffic light modules (Red/Yellow/Green LEDs)  
- USB Webcam  
- Jumper wires & power supply  
- Traffic model setup with cars, bikes, trucks, and rickshaws  


## 💻 Software Requirements

- Python 3.12+  
- OpenCV  
- PySerial  
- Ultralytics YOLOv8  
- Arduino IDE  
- Windows / Linux / macOS  

## ▶️ How It Works

### 1. Vehicle Detection
Python reads frames from the webcam → runs YOLO detection → counts vehicles per road → calculates density using a weighted formula.

### 2. Selecting Road & Duration
The road with the highest density gets priority.  
Green light duration depends on traffic level: Low, Moderate, High, Extremely High.

### 3. Communication (Python → ESP32)
Python sends a code like:
110 → Road 1, 10 seconds
230 → Road 2, 30 seconds


ESP32 reads the code and controls the traffic lights.

### 4. ESP32 Traffic Control
ESP32 triggers traffic lights in real time: Red → Yellow → Green  
Python GUI countdown synchronizes with the ESP32 signal.

<img width="1916" height="1068" alt="image" src="https://github.com/user-attachments/assets/57e8fa64-1602-4ce2-8dd3-0734365b6a2e" />









