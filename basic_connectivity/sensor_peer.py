import socket
import json
import time

BROADCAST_IP = "172.16.3.255"
# BROADCAST_IP = "localhost"
PORT = 5000
# PORT = 5050

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEPORT, 1)
sock.bind(("", 0))

hello_msg = json.dumps({
    "type": "HELLO",
    "device_id": "sensor_1",
    "role": "sensor",
    "status": "online"
}).encode("utf-8")

while True:
    # Broadcast HELLO
    sock.sendto(hello_msg, (BROADCAST_IP, PORT))
    print(f"[SENT] HELLO broadcasted")

    # Wait for replies
    try:
        data, addr = sock.recvfrom(1024)
        msg = json.loads(data.decode('utf-8'))
        print(f"[RECV] From {addr}: {msg}")
    except socket.timeout:
        print("[INFO] No reply yet...")
    time.sleep(5)
