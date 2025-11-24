import sys, tty, termios

import serial
import serial.tools.list_ports
ports= serial.tools.list_ports.comports()
pykit_port = None

for port in ports:
    if 'USB' in port.description or 'CircuitPython' in port.description:
        pykit_port = port.device
        break

if not pykit_port:
    print("PyKit not found!")
    exit ()

print(f"Connected to Pykit on {pykit_port}")
ser = serial.Serial(pykit_port, 115200, timeout=1)

fd = sys.stdin.fileno()
old_settings = termios.tcgetattr(fd)

try:
    tty.setraw(sys.stdin.fileno())
    while True:
        ch = sys.stdin.read (1) # reads instantly
        if ch == '\x1b': # ESC key
            break
        print("Pressed:" , repr(ch))
        ser.write(ch.encode ())
finally:
    termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
