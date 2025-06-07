from flask import Flask, Response, render_template, request, jsonify
import cv2
import dlib
from scipy.spatial import distance
import threading

app = Flask(__name__)

EAR_THRESHOLD = 0.25
CONSECUTIVE_FRAMES = 15
frame_counter = 0

detector = dlib.get_frontal_face_detector()
predictor = dlib.shape_predictor(r"C:\Users\DEVESH\OneDrive\Desktop\driver\backend\shape_predictor_68_face_landmarks.dat")

LEFT_EYE_POINTS = list(range(36, 42))
RIGHT_EYE_POINTS = list(range(42, 48))

camera = cv2.VideoCapture(0)

streaming = False  # Global flag

def calculate_ear(eye):
    vertical1 = distance.euclidean(eye[1], eye[5])
    vertical2 = distance.euclidean(eye[2], eye[4])
    horizontal = distance.euclidean(eye[0], eye[3])
    return (vertical1 + vertical2) / (2.0 * horizontal)

def play_alert_sound():
    import subprocess, os
    ALERT_SOUND_PATH = os.path.abspath(r"C:\Users\DEVESH\OneDrive\Desktop\driver\backend\alert.wav")
    subprocess.Popen(['powershell', '-c', f'(New-Object Media.SoundPlayer "{ALERT_SOUND_PATH}").PlaySync();'])

def generate_frames():
    global frame_counter
    while streaming:
        success, frame = camera.read()
        if not success:
            break

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = detector(gray)

        for face in faces:
            landmarks = predictor(gray, face)
            left_eye = [landmarks.part(i) for i in LEFT_EYE_POINTS]
            right_eye = [landmarks.part(i) for i in RIGHT_EYE_POINTS]

            left_eye_coords = [(point.x, point.y) for point in left_eye]
            right_eye_coords = [(point.x, point.y) for point in right_eye]

            left_ear = calculate_ear(left_eye_coords)
            right_ear = calculate_ear(right_eye_coords)
            avg_ear = (left_ear + right_ear) / 2.0

            for point in left_eye_coords + right_eye_coords:
                cv2.circle(frame, point, 2, (0, 255, 0), -1)

            if avg_ear < EAR_THRESHOLD:
                frame_counter += 1
                if frame_counter >= CONSECUTIVE_FRAMES:
                    cv2.putText(frame, "DROWSINESS DETECTED!", (10, 30),
                                cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
                    threading.Thread(target=play_alert_sound, daemon=True).start()
            else:
                frame_counter = 0

        _, buffer = cv2.imencode('.jpg', frame)
        frame_bytes = buffer.tobytes()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n')
    # When streaming becomes False, exit generator cleanly

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/video_feed')
def video_feed():
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/start_stream', methods=['POST'])
def start_stream():
    global streaming
    streaming = True
    return jsonify({"status": "started"})

@app.route('/stop_stream', methods=['POST'])
def stop_stream():
    global streaming
    streaming = False
    return jsonify({"status": "stopped"})

if __name__ == "__main__":
    app.run(debug=True)
