import asyncio
import websockets
import cv2
import mediapipe as mp

# === MediaPipe face mesh setup ===
mp_face_mesh = mp.solutions.face_mesh
mp_drawing = mp.solutions.drawing_utils
mp_style = mp.solutions.drawing_styles
face_mesh = mp_face_mesh.FaceMesh(static_image_mode=False, max_num_faces=1)

# === OpenCV webcam ===
cap = cv2.VideoCapture(0)

# === Async WebSocket handler ===
async def head_tracking_server(websocket, path):
    print("🟢 Godot connected.")
    try:
        while cap.isOpened():
            success, frame = cap.read()
            if not success:
                continue

            frame = cv2.flip(frame, 1)
            rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            results = face_mesh.process(rgb)

            if results.multi_face_landmarks:
                for face_landmarks in results.multi_face_landmarks:
                    # Draw the face mesh on the frame
                    mp_drawing.draw_landmarks(
                        image=frame,
                        landmark_list=face_landmarks,
                        connections=mp_face_mesh.FACEMESH_TESSELATION,
                        landmark_drawing_spec=None,
                        connection_drawing_spec=mp_style
                            .get_default_face_mesh_tesselation_style()
                    )

                # Send the nose tip position (landmark 1)
                nose = results.multi_face_landmarks[0].landmark[1]
                x = (nose.x - 0.5) * 2
                y = (nose.y - 0.5) * -2
                z = nose.z * 5
                data = f"{x:.3f},{y:.3f},{z:.3f}"

                await websocket.send(data)

            cv2.imshow("Webcam Tracking", frame)
            if cv2.waitKey(1) & 0xFF == 27:  # Esc key to exit
                break

    except websockets.ConnectionClosed:
        print("🔌 Godot disconnected.")
    finally:
        cap.release()
        cv2.destroyAllWindows()

# === Async entry point for newer Python versions ===
async def main():
    print("🚀 Starting WebSocket server at ws://localhost:8765 ...")
    async with websockets.serve(head_tracking_server, "localhost", 8765):
        await asyncio.Future()  # Keeps the server alive

# === Start the server ===
asyncio.run(main())
