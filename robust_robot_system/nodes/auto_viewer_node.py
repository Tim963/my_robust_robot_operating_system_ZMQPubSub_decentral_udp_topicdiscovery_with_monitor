import cv2
import base64
import numpy as np
from core.pubsub import ZMQPubSub
from core.discovery import discover_publisher

def run_auto_viewer_node():
    ip, port = discover_publisher()
    if not ip:
        return

    sub = ZMQPubSub("sub", ip=ip, port=port)

    def on_msg(topic, msg):
        if topic != "camera/image_jpg":
            return
        try:
            img_data = base64.b64decode(msg)
            np_arr = np.frombuffer(img_data, dtype=np.uint8)
            frame = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)
            if frame is not None:
                cv2.imshow("Live Camera Feed", frame)
                cv2.waitKey(1)
        except Exception as e:
            print(f"[ViewerNode] Error decoding image: {e}")

    sub.listen(on_msg)
    print("[ViewerNode] Waiting for image...")
    while True:
        pass

if __name__ == "__main__":
    run_auto_viewer_node()
