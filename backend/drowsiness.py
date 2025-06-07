import cv2
import dlib
import threading
from scipy.spatial import distance
from playsound import playsound

# Constants
EAR_THRESHOLD = 0.25  # Eye Aspect Ratio threshold for eye closure
CONSECUTIVE_FRAMES = 15  # Frames with closed eyes to trigger alert

# Initialize counters
frame_counter = 0

# Load Dlib's face detector and facial landmark predictor
detector = dlib.get_frontal_face_detector()
predictor = dlib.shape_predictor("backend/shape_predictor_68_face_landmarks.dat")

# Eye landmarks (as per Dlib's 68 landmark model)
LEFT_EYE_POINTS = list(range(36, 42))
RIGHT_EYE_POINTS = list(range(42, 48))

def calculate_ear(eye):
    """Calculate Eye Aspect Ratio (EAR)"""
    vertical1 = distance.euclidean(eye[1], eye[5])
    vertical2 = distance.euclidean(eye[2], eye[4])
    horizontal = distance.euclidean(eye[0], eye[3])
    return (vertical1 + vertical2) / (2.0 * horizontal)

def play_alert_sound():
    """Play alert sound in a separate thread"""
    playsound("backend/alert.wav")

# Initialize webcam feed
cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()
    if not ret:
        break

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = detector(gray)

    for face in faces:
        landmarks = predictor(gray, face)
        left_eye = [landmarks.part(i) for i in LEFT_EYE_POINTS]
        right_eye = [landmarks.part(i) for i in RIGHT_EYE_POINTS]

        # Convert to coordinates
        left_eye_coords = [(point.x, point.y) for point in left_eye]
        right_eye_coords = [(point.x, point.y) for point in right_eye]

        # Calculate EAR
        left_ear = calculate_ear(left_eye_coords)
        right_ear = calculate_ear(right_eye_coords)
        avg_ear = (left_ear + right_ear) / 2.0

        # Visualize landmarks
        for point in left_eye_coords + right_eye_coords:
            cv2.circle(frame, point, 2, (0, 255, 0), -1)

        # Check drowsiness
        if avg_ear < EAR_THRESHOLD:
            frame_counter += 1
            if frame_counter >= CONSECUTIVE_FRAMES:
                cv2.putText(frame, "DROWSINESS DETECTED!", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
                threading.Thread(target=play_alert_sound, daemon=True).start()  # Play alert sound in background
        else:
            frame_counter = 0

    # Display frame
    cv2.imshow("Driver Drowsiness Detection", frame)

    # Break on 'q' key press
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()
