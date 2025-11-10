import socket
import json
import time
import cryptography.fernet

BROADCAST_IP = "172.16.3.255"
# BROADCAST_IP = "localhost"
PORT = 5000
# PORT = 5050
SHARED_KEY = b"ZzLmrPJ8Sh2tFrjXOGV024YbR97nmCp-50GZhUF_4s8="
SHARED_KEY = b"AWXEIG9bte7vvCx9kGqzQHktstqkoK3IWQpSXiTUE6M="

cipher = cryptography.fernet.Fernet(SHARED_KEY)
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEPORT, 1)
sock.settimeout(3)
sock.bind(("", 0))

hello_msg = json.dumps({
    "type": "HELLO",
    "device_id": "sensor_1",
    "role": "sensor",
    "status": "online"
}).encode("utf-8")

while True:

    encrypted = cipher.encrypt(hello_msg)
    # Broadcast encrypted HELLO
    sock.sendto(encrypted, (BROADCAST_IP, PORT))
    print(f"[SENT] Encrypted HELLO broadcasted")

    # Wait for replies
    try:
        data, addr = sock.recvfrom(1024)
        decrypted = cipher.decrypt(data)
        msg = json.loads(decrypted.decode('utf-8'))
        print(f"[RECV] From {addr}: {msg}")
    except socket.timeout:
        print("[INFO] No reply yet...")
    except Exception as e:
        print(f"[WARN] Failed to decrypt: {e}")
    time.sleep(5)
