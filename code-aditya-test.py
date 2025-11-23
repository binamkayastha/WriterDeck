import time
import board
import displayio
import digitalio
import microcontroller
import supervisor
import sys
from fourwire import FourWire
from adafruit_st7789 import ST7789

# ---------------------------
# DISPLAY SETUP
# ---------------------------
backlight = digitalio.DigitalInOut(microcontroller.pin.PA06)
backlight.direction = digitalio.Direction.OUTPUT
displayio.release_displays()

spi = board.LCD_SPI()
tft_cs = board.LCD_CS
tft_dc = board.D4
backlight.value = False

DISPLAY_WIDTH = 240
DISPLAY_HEIGHT = 135

display_bus = FourWire(spi, command=tft_dc, chip_select=tft_cs)
display = ST7789(display_bus, rotation=90,
                 width=DISPLAY_WIDTH, height=DISPLAY_HEIGHT,
                 rowstart=40, colstart=53)

print("PyKit Display Ready")
print("Minimal USB Text Editor")

# ---------------------------
# TEXT BUFFER + SCROLL
# ---------------------------
lines = []                   # store each line as a string
max_visible = 8              # fits nicely with 2× scaled text
scale = 2                    # bigger text (2×)

# Simple screen clear helper
def draw_screen():
    print("\n" * 20)   # this clears the TFT because it mirrors console output
    start = max(0, len(lines) - max_visible)
    for ln in lines[start:]:
        print(ln)

# ---------------------------
# EDITOR LOOP
# ---------------------------
current = ""      # current line being typed

while True:
    if supervisor.runtime.serial_bytes_available:
        ch = sys.stdin.read(1)

        # NEWLINE
        if ch in ("\n", "\r"):
            lines.append(current)
            current = ""
            draw_screen()
            continue

        # BACKSPACE
        if ch in ("\x7f", "\b"):
            if len(current) > 0:
                current = current[:-1]
                print("\b \b", end="")
            continue

        # NORMAL CHARACTER
        current += ch
        print(ch, end="")

        # update display live
        temp = lines[-max_visible:] + [current]
        print("\n" * 20)
        for ln in temp:
            print(ln)

    time.sleep(0.01)
