import socket
import json

PORT = 5000
# PORT = 5050

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEPORT, 1)
sock.bind(("", PORT))
print(f"[INFO] Controller listening on UDP {PORT}...")

while True:
    data, addr = sock.recvfrom(1024)
    msg = json.loads(data.decode("utf-8"))
    print(f"[RECV] From {addr}: {msg}")

    if msg.get("type") == "HELLO":
        reply = json.dumps({
            "type": "ACK",
            "device_id": "controller_1",
            "status": "connected"
        }).encode("utf-8")
        sock.sendto(reply, addr)
        print(f"[SENT] ACK sent to {addr}")
