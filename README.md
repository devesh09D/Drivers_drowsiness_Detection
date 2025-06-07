# Driver Drowsiness Detection System 🚗😴

A real-time computer vision system that monitors a driver's eye state using a webcam and detects signs of drowsiness to prevent accidents by triggering an alert.

---

## 🌟 Features

- **Real-time Eye Detection:** Uses Dlib's facial landmark detector to locate and analyze eye positions.
- **Drowsiness Detection:** Calculates Eye Aspect Ratio (EAR) to detect eye closure over consecutive frames.
- **Alert System:** Plays a warning sound if drowsiness is detected to keep the driver awake.
- **Web Interface:** Stream live video feed with overlay landmarks and alert messages using Flask.
- **Cross-platform:** Works on Windows and Linux with Python 3.x.

---

## 🎯 How It Works

1. Captures video frames from the webcam.
2. Detects faces and facial landmarks using Dlib.
3. Calculates Eye Aspect Ratio (EAR) to measure eye openness.
4. If EAR remains below a threshold for a set number of frames, triggers an alert.
5. Displays live video with visual indicators and alerts.

---

## 🛠️ Technologies Used

- Python 3
- OpenCV
- Dlib (for face & landmark detection)
- Flask (for web interface)
- SciPy (for geometric calculations)
- Playsound / Powershell (for alert sound playback)

---

## 🚀 Getting Started

### Prerequisites

- Python 3.6+
- Install dependencies:
  ```bash
  pip install opencv-python dlib flask scipy playsound
Created by DEVESH D
Email: devesh090905@gmail.com

