import zmq
import threading

class ZMQPubSub:
    def __init__(self, role, port="5556", ip="localhost"):
        self.context = zmq.Context()
        self.role = role
        if role == "pub":
            self.socket = self.context.socket(zmq.PUB)
            self.socket.bind(f"tcp://*:{port}")
        elif role == "sub":
            self.socket = self.context.socket(zmq.SUB)
            self.socket.connect(f"tcp://{ip}:{port}")
            self.socket.setsockopt_string(zmq.SUBSCRIBE, "")

    def publish(self, topic, message):
        if self.role != "pub":
            raise RuntimeError("Only publishers can send messages")
        self.socket.send_string(f"{topic} {message}")

    def listen(self, callback):
        if self.role != "sub":
            raise RuntimeError("Only subscribers can receive messages")
        def loop():
            while True:
                msg = self.socket.recv_string()
                topic, data = msg.split(" ", 1)
                callback(topic, data)
        threading.Thread(target=loop, daemon=True).start()
