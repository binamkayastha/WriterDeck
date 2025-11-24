from pynput import keyboard
import serial
import serial.tools.list_ports
ports = serial.tools.list_ports.comports()
pykit_port = None

for port in ports:
    if 'USB' in port.description or 'CircuitPython' in port.description:
        pykit_port = port.device
        break

if not pykit_port:
    print("PyKit not found!")
    exit()

print(f"Connected to PyKit on {pykit_port}")
ser = serial.Serial(pykit_port, 115200, timeout=1)

print("Display connected.")

with keyboard.Events() as events:
    while True:
        # Block for as much as possible
        event = events.get(1e6)
        letter = str(event.key)
        print(letter)
        print(f"sending letter: {letter}")

        ser.write(letter.encode())


