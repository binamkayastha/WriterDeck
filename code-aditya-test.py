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

display_bus = FourWire(
    spi,
    command=tft_dc,
    chip_select=tft_cs
)
display = ST7789(
    display_bus,
    rotation=90,
    width=DISPLAY_WIDTH,
    height=DISPLAY_HEIGHT,
    rowstart=40,
    colstart=53
)

print("PyKit Display Ready: ")
print("USB Text Editor: big text + scroll")

# ---------------------------
# LABEL FOR BIG TEXT
# ---------------------------
splash = displayio.Group()
display.root_group = splash

TEXT_SCALE = 2           # make this 3 or 4 for even bigger
CHAR_W = 6 * TEXT_SCALE  # terminalio font is ~6 px wide
CHAR_H = 8 * TEXT_SCALE

CHARS_PER_LINE = DISPLAY_WIDTH // CHAR_W
MAX_LINES = DISPLAY_HEIGHT // CHAR_H

text_label = Label(
    terminalio.FONT,
    text="",
    color=0xFFFFFF,
    scale=TEXT_SCALE,
)
text_label.x = 0
text_label.y = CHAR_H      # first baseline
splash.append(text_label)

# ---------------------------
# EDITOR STATE
# ---------------------------
buffer = ""   # whole text, including '\n'


def recompute_visible_text():
    """Wrap buffer to screen width and keep only last MAX_LINES."""
    # split into logical lines first
    logical_lines = buffer.split("\n")

    wrapped = []
    for ln in logical_lines:
        # wrap long lines at CHARS_PER_LINE
        if ln == "":
            wrapped.append("")  # preserve blank lines
        else:
            for i in range(0, len(ln), CHARS_PER_LINE):
                wrapped.append(ln[i:i + CHARS_PER_LINE])

    # keep last MAX_LINES for display
    visible = wrapped[-MAX_LINES:] if len(wrapped) > MAX_LINES else wrapped
    text_label.text = "\n".join(visible)


# ---------------------------
# MAIN LOOP
# ---------------------------
while True:
    if supervisor.runtime.serial_bytes_available:
        ch = sys.stdin.read(1)

        # BACKSPACE
        if ch == "\x7f" or ch == "\b":
            if len(buffer) > 0:
                buffer = buffer[:-1]
                print("\b \b", end="")   # USB console
                recompute_visible_text()
            continue

        # NEWLINE
        if ch == "\n" or ch == "\r":
            buffer += "\n"
            print()                      # USB console newline
            recompute_visible_text()
            continue

        # NORMAL CHAR
        buffer += ch
        print(ch, end="")                # USB console echo
        recompute_visible_text()

    time.sleep(0.01)
