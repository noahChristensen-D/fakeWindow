import cv2
import mediapipe as mp
from pythonosc.udp_client import SimpleUDPClient
import signal
import sys

# === OSC Setup ===
client = SimpleUDPClient("127.0.0.1", 8000)

# === Mediapipe Setup ===
mp_face_mesh = mp.solutions.face_mesh
face_mesh = mp_face_mesh.FaceMesh(static_image_mode=False, max_num_faces=1)

# === Webcam Setup ===
cap = cv2.VideoCapture(0)

# === Handle Ctrl+C Gracefully ===
def shutdown_handler(sig, frame):
    print("Shutting down...")
    cap.release()
    cv2.destroyAllWindows()
    sys.exit(0)

signal.signal(signal.SIGINT, shutdown_handler)

print("Press ESC in the camera window or Ctrl+C in the terminal to quit.")

# === Main Loop ===
while cap.isOpened():
    success, frame = cap.read()
    if not success:
        continue

    frame = cv2.flip(frame, 1)
    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = face_mesh.process(rgb)

    if results.multi_face_landmarks:
        landmarks = results.multi_face_landmarks[0].landmark
        nose = landmarks[1]
        x, y, z = nose.x, nose.y, nose.z

        scaled_x = (x - 0.5) * 2
        scaled_y = (y - 0.5) * -2
        scaled_z = z * 5

        client.send_message("/head/x", scaled_x)
        client.send_message("/head/y", scaled_y)
        client.send_message("/head/z", scaled_z)

    cv2.imshow("Head Tracking", frame)
    if cv2.waitKey(1) & 0xFF == 27:  # ESC key
        break

shutdown_handler(None, None)
