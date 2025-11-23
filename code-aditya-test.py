import time
import board
import displayio
import digitalio
import microcontroller
import supervisor
import sys
from fourwire import FourWire
from adafruit_st7789 import ST7789
from adafruit_display_text.label import Label
import terminalio

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

# ---------------------------
# TEXT GROUP + LABEL
# ---------------------------
splash = displayio.Group()
display.root_group = splash

text_label = Label(terminalio.FONT, text="", color=0xFFFFFF, scale=2)  
text_label.x = 0
text_label.y = 20
splash.append(text_label)

# ---------------------------
# EDITOR STATE
# ---------------------------
buffer = ""
lines = []
max_visible = 6    # because font is bigger (scale=2)

def redraw():
    start = max(0, len(lines) - max_visible)
    visible = lines[start:]
    text_label.text = "\n".join(visible)

# ---------------------------
# MAIN LOOP
# ---------------------------
current = ""

while True:
    if supervisor.runtime.serial_bytes_available:
        ch = sys.stdin.read(1)

        # NEWLINE
        if ch in ("\n", "\r"):
            lines.append(current)
            current = ""
            redraw()
            print()
            continue

        # BACKSPACE
        if ch in ("\x7f", "\b"):
            if len(current) > 0:
                current = current[:-1]
                print("\b \b", end="")
                redraw()
            continue

        # NORMAL CHAR
        current += ch
        print(ch, end="")

        temp = lines[-max_visible:] + [current]
        text_label.text = "\n".join(temp)

    time.sleep(0.01)
