This project simulates a garden irrigation network using a peer-to-peer architecture. Each IoT device (sensor or controller) communicates directly over UDP broadcast messages without a central server.

Part A implements basic discovery and message exchange.
Part B extends this with encrypted communication using the Python cryptography.fernet library.

Requirements
------------
Python 3.10 or later
`cryptography` library

Directories
-----------
/basic_connectivity/  → unencrypted version (HELLO ↔ ACK)
/secure_connectivity/ → encrypted version (Fernet AES + HMAC)
LOGS.ODT              → implementation and testing logs
FEATURE_CHECKLIST.TXT → summary of features implemented
REPORT.ODT            → 500-word design and testing report
README.TXT            → me

Running the basic version
-------------------------
Open two terminals or IDE tabs.

In the first terminal, start the controller.

In the second terminal, start the sensor.

The sensor will broadcast "HELLO" JSON messages.
The controller will receive and reply with "ACK".
Both sides will print their logs to the console.

Running the secure version
--------------------------
Generate a Fernet key (if not already provided). Use Python in the terminal:
   `import cryptography.fernet`
   `print(cryptography.fernet.Fernet.generate_key().decode())`

Paste the same key into both secure scripts (sensor and controller).

Open two terminals or IDE tabs.

In the first terminal, start the controller.

In the second terminal, start the sensor.

Encrypted messages will be exchanged where only peers with matching keys can communicate.
