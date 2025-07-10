import cv2
import time
import base64
from core.pubsub import ZMQPubSub
from core.discovery import broadcast_identity
import threading

def run_camera_node():
    pub = ZMQPubSub("pub", port="5556")
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("[CameraNode] ❌ Failed to open camera.")
        return

    # start broadcast thread
    threading.Thread(target=broadcast_identity, args=("5556", ["camera/image_jpg"]), daemon=True).start()
    print("[CameraNode] ✅ Camera opened. Publishing frames...")

    while True:
        ret, frame = cap.read()
        if not ret:
            continue
        _, buffer = cv2.imencode('.jpg', frame)
        jpg_bytes = base64.b64encode(buffer).decode("utf-8")
        pub.publish("camera/image_jpg", jpg_bytes)
        time.sleep(0.1)

if __name__ == "__main__":
    run_camera_node()
