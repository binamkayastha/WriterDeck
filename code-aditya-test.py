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
print("USB Editor with Auto-Wrap + Scrolling (:w to save)")

# -------------------------
# Display group
# -------------------------
splash = displayio.Group()
display.root_group = splash

TEXT_SCALE = 2
CHAR_WIDTH = 6 * TEXT_SCALE
CHARS_PER_LINE = DISPLAY_WIDTH // CHAR_WIDTH  # ≈ 20

LINE_HEIGHT = 8 * TEXT_SCALE
MAX_LINES = DISPLAY_HEIGHT // LINE_HEIGHT     # ≈ 8 lines

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
# Editor buffer (list of lines)
# -------------------------
lines = [""]

def save_to_host(text):
    print("\n---BEGIN SAVE---")
    print(text)
    print("---END SAVE---\n")

def wrap_line_to_list(line):
    """Split a long line into multiple wrapped lines."""
    return [line[i:i+CHARS_PER_LINE] for i in range(0, len(line), CHARS_PER_LINE)]

# -------------------------
# Main loop
# -------------------------
while True:

    if supervisor.runtime.serial_bytes_available:
        ch = sys.stdin.read(1)

        # SAVE (:w)
        if ch == ":":
            nxt = sys.stdin.read(1)
            if nxt == "w":
                save_to_host("\n".join(lines))
                continue
            # add literal characters
            ch = ":" + nxt
            print(ch, end="")

            # append normally
            for c in ch:
                lines[-1] += c

        # BACKSPACE
        elif ch in ("\x7f", "\b"):
            if len(lines[-1]) > 0:
                lines[-1] = lines[-1][:-1]
                print("\b \b", end="")
            else:
                if len(lines) > 1:
                    lines.pop()
                    print("\b \b", end="")

        # NEWLINE (ENTER)
        elif ch in ("\n", "\r"):
            lines.append("")
            print()

        # NORMAL CHAR
        else:
            lines[-1] += ch
            print(ch, end="")

        # -------------------------------------
        # AUTO WRAP + VERTICAL SCROLLING
        # -------------------------------------
        wrapped = []
        for ln in lines:
            wrapped.extend(wrap_line_to_list(ln))

        visible_lines = wrapped[-MAX_LINES:]
        text_area.text = "\n".join(visible_lines)

    time.sleep(0.01)
