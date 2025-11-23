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
print("USB Editor (:w to save)")

# -------------------------
# Display group
# -------------------------
splash = displayio.Group()
display.root_group = splash

TEXT_SCALE = 2
LINE_HEIGHT = 8 * TEXT_SCALE
MAX_LINES = DISPLAY_HEIGHT // LINE_HEIGHT   # ≈ 8 lines

# text Label
text_area = label.Label(
    terminalio.FONT,
    text="",
    color=0xFFFFFF,
    x=0,
    y=LINE_HEIGHT,
    scale=TEXT_SCALE
)
splash.append(text_area)

# -------------------------
# Editor buffer
# -------------------------
buffer = ""
lines = [""]  # Start with one empty line

def output_to_host(text):
    print("\n---BEGIN SAVE---")
    print(text)
    print("---END SAVE---\n")

# -------------------------
# Main loop
# -------------------------
while True:

    if supervisor.runtime.serial_bytes_available:
        ch = sys.stdin.read(1)

        # SAVE COMMAND :w
        if ch == ":":
            nxt = sys.stdin.read(1)
            if nxt == "w":
                output_to_host(buffer)
                continue
            buffer += ch + nxt
            print(ch + nxt, end="")
        # BACKSPACE
        elif ch in ("\x7f", "\b"):
            if len(buffer) > 0:
                buffer = buffer[:-1]
            if len(lines[-1]) > 0:
                lines[-1] = lines[-1][:-1]
                print("\b \b", end="")
            else:
                # remove empty line
                if len(lines) > 1:
                    lines.pop()
                    print("\b \b", end="")
        # NEWLINE (ENTER)
        elif ch in ("\n", "\r"):
            buffer += "\n"
            lines.append("")   # start new empty line
            print()            # new line in USB console
        # NORMAL CHAR
        else:
            buffer += ch
            lines[-1] += ch
            print(ch, end="")

        # -------------------------
        #   Vertical scrolling on TFT
        # -------------------------
        visible_lines = lines[-MAX_LINES:]
        text_area.text = "\n".join(visible_lines)

    time.sleep(0.01)
