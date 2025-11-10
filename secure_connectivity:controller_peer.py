import socket
import json
import cryptography.fernet

PORT = 5000
# PORT = 5050
SHARED_KEY = b"ZzLmrPJ8Sh2tFrjXOGV024YbR97nmCp-50GZhUF_4s8="

cipher = cryptography.fernet.Fernet(SHARED_KEY)
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEPORT, 1)
sock.bind(("", PORT))
print(f"[INFO] Secure controller listening on UDP {PORT}...")

while True:
    data, addr = sock.recvfrom(1024)
    try:
        decrypted = cipher.decrypt(data)
        msg = json.loads(decrypted.decode("utf-8"))
        print(f"[RECV] From {addr}: {msg}")
    except Exception as e:
        print(f"[WARN] Could not decrypt packet from {addr}: {e}")
        continue

    if msg.get("type") == "HELLO":
        reply = json.dumps({
            "type": "ACK",
            "device_id": "controller_1",
            "status": "connected"
        }).encode("utf-8")
        encrypted = cipher.encrypt(reply)
        sock.sendto(encrypted, addr)
        print(f"[SENT] Encrypted ACK sent to {addr}")
