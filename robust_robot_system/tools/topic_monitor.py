# tools/topic_monitor.py
import time
from core.pubsub import ZMQPubSub

last_seen = {}

def run_topic_monitor():
    sub = ZMQPubSub("sub")

    def on_msg(topic, msg):
        last_seen[topic] = time.time()

    sub.listen(on_msg)
    print("[TopicMonitor] Monitoring active topics...")

    try:
        while True:
            print("\033c", end="")  # Clear screen
            print("📡 Active Topics (last 10s):\n")
            now = time.time()
            for topic, ts in sorted(last_seen.items()):
                age = now - ts
                if age < 10:
                    print(f"  {topic:25}  ↪  last seen {age:.1f}s ago")
            time.sleep(1)
    except KeyboardInterrupt:
        print("\n[TopicMonitor] Stopped.")

if __name__ == "__main__":
    run_topic_monitor()
