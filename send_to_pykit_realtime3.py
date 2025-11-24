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

def on_key_press(key):
    if hasattr(key, "char"):
        print(f"Sending {key}")
        ser.write(str(key).encode())

keyboard_listener = keyboard.Listener(
    on_press=on_key_press
)

while True:
    pass

