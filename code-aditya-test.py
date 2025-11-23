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
print("USB Editor (type :w to output full text)")

# -------------------------
# Display text (single line, big)
# -------------------------
splash = displayio.Group()
display.root_group = splash

TEXT_SCALE = 2  # increase for bigger text
CHAR_WIDTH = 6 * TEXT_SCALE  # approximate pixel width of one terminalio char
CHARS_ON_SCREEN = DISPLAY_WIDTH // CHAR_WIDTH

text_area = label.Label(
    terminalio.FONT,
    text="",
    color=0xFFFFFF,
    x=0,
    y=20,
    scale=TEXT_SCALE
)
splash.append(text_area)

# -------------------------
# Editor buffer
# -------------------------
buffer = ""

def output_to_host(text):
    """Print text back to host instead of saving to CIRCUITPY."""
    print("\n---BEGIN SAVE---")
    print(text)
    print("---END SAVE---\n")

# -------------------------
# Main loop
# -------------------------
while True:

    if supervisor.runtime.serial_bytes_available:
        ch = sys.stdin.read(1)

        # SAVE COMMAND (:w)
        if ch == ":":
            nxt = sys.stdin.read(1)
            if nxt == "w":
                output_to_host(buffer)
                continue
            buffer += ch + nxt
            print(ch + nxt, end="")  # console echo
        # BACKSPACE
        elif ch in ("\x7f", "\b"):
            if len(buffer) > 0:
                buffer = buffer[:-1]
                print("\b \b", end="")  # erase on host console
        # NEWLINE (ignored for horizontal-only editor)
        elif ch in ("\n", "\r"):
            print()  # console newline only
        else:
            # NORMAL CHARACTER
            buffer += ch
            print(ch, end="")

        # --------------------------------------------------
        # Horizontal scrolling for TFT display:
        # show only the rightmost section of the current line
        # --------------------------------------------------
        visible = buffer[-CHARS_ON_SCREEN:]
        text_area.text = visible

    time.sleep(0.01)
