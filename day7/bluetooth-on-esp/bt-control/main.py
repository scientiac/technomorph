# send.py
import sys
import serial
import time

if len(sys.argv) != 2 or sys.argv[1] not in ['on', 'off']:
    print("Usage: python send.py [on|off]")
    sys.exit(1)

msg = sys.argv[1] + "\n"

PORT = "/dev/rfcomm0"
BAUD = 115200

try:
    with serial.Serial(PORT, BAUD, timeout=2) as bt:
        time.sleep(1)
        bt.write(msg.encode())
        print(f"Sent: {msg.strip()}")
except serial.SerialException as e:
    print("Failed to open port:", e)
