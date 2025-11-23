import time
import board
import displayio
import digitalio
import microcontroller
import supervisor
import sys
from fourwire import FourWire
from adafruit_st7789 import ST7789
from adafruit_display_text import label
import terminalio

# -------------------------
# Display initialization
# -------------------------
backlight = digitalio.DigitalInOut(microcontroller.pin.PA06)
backlight.direction = digitalio.Direction.OUTPUT
displayio.release_displays()

spi = board.LCD_SPI()
tft_cs = board.LCD_CS
tft_dc = board.D4
backlight.value = False  # Active LOW

DISPLAY_WIDTH = 240
DISPLAY_HEIGHT = 135

display_bus = FourWire(spi, command=tft_dc, chip_select=tft_cs)
display = ST7789(
    display_bus,
    rotation=90,
    width=DISPLAY_WIDTH,
    height=DISPLAY_HEIGHT,
    rowstart=40,
    colstart=53
)

print("PyKit Display Ready")
print("USB Editor Ready (:w to save)")

# -------------------------
# Text area setup (BIG TEXT)
# -------------------------
splash = displayio.Group()
display.root_group = splash

text_area = label.Label(
    terminalio.FONT,
    text="",
    color=0xFFFFFF,
    x=0,
    y=20,
    scale=2     # << change this (1–4) to adjust text size
)

splash.append(text_area)

# -------------------------
# Editor buffer
# -------------------------
buffer = ""

def save_text(text):
    """Save editor buffer to CIRCUITPY filesystem."""
    try:
        with open("/code_output.txt", "w") as f:
            f.write(text)
        print("\n[SAVED] to code_output.txt")
    except Exception as e:
        print("\nSave error:", e)

# -------------------------
# Main USB text editor loop
# -------------------------
while True:

    if supervisor.runtime.serial_bytes_available:
        ch = sys.stdin.read(1)

        # SAVE COMMAND (:w)
        if ch == ":":
            nxt = sys.stdin.read(1)
            if nxt == "w":
                save_text(buffer)
                continue
            # Not a save command → treat normally
            buffer += ch + nxt
            print(ch + nxt, end="")
            text_area.text = buffer[-500:]  # prevent overflow
            continue

        # BACKSPACE
        if ch in ("\x7f", "\b"):
            if len(buffer) > 0:
                buffer = buffer[:-1]
                print("\b \b", end="")
                text_area.text = buffer[-500:]
            continue

        # NEWLINE
        if ch in ("\n", "\r"):
            buffer += "\n"
            print()
            text_area.text = buffer[-500:]
            continue

        # NORMAL CHARACTER
        buffer += ch
        print(ch, end="")
        text_area.text = buffer[-500:]

    time.sleep(0.01)
