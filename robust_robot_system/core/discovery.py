import socket
import json
import time

def get_own_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    ip = s.getsockname()[0]
    s.close()
    return ip

def broadcast_identity(port, topics, interval=3):
    ip = get_own_ip()
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
    msg = json.dumps({"ip": ip, "port": port, "topics": topics})
    while True:
        sock.sendto(msg.encode(), ('255.255.255.255', 9999))
        print(f"[Broadcast] {ip}:{port} announced with topics {topics}")
        time.sleep(interval)

def discover_publisher(timeout=5):
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind(('', 9999))
    sock.settimeout(timeout)
    try:
        data, addr = sock.recvfrom(1024)
        info = json.loads(data)
        print(f"[Discovery] Found publisher at {info['ip']}:{info['port']} with topics {info['topics']}")
        return info["ip"], info["port"]
    except socket.timeout:
        print("[Discovery] No publisher found.")
        return None, None
