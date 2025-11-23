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
print("BIG TEXT USB Text Editor")

# ---------------------------
# TEXT CONFIG
# ---------------------------
scale = 3
char_width = 6 * scale
max_chars = DISPLAY_WIDTH // char_width

lines = []             # wrapped lines
logical = [""]         # original lines
max_visible = DISPLAY_HEIGHT // (8 * scale)

# ---------------------------
# HELPERS
# ---------------------------
def wrap_line(text):
    return [text[i:i+max_chars] for i in range(0, len(text), max_chars)]

def rebuild_wrapped():
    global lines
    out = []
    for ln in logical:
        out.extend(wrap_line(ln))
    lines = out

def draw_screen():
    print("\n" * 20)
    start = max(0, len(lines) - max_visible)
    for ln in lines[start:]:
        print(ln)

# <<< SAVE ADDED >>>
def handle_save(cmd):
    parts = cmd.split()
    if len(parts) == 2:
        filename = parts[1]
        # send file to host as a block of text
        print("<<BEGIN_SAVE " + filename + ">>")
        for ln in logical:
            print(ln)
        print("<<END_SAVE>>")
        print(f"[Saved to host: {filename}]")
    else:
        print("[Usage: :save filename.txt]")

# ---------------------------
# MAIN LOOP
# ---------------------------
while True:
    if supervisor.runtime.serial_bytes_available:
        ch = sys.stdin.read(1)

        # detect SAVE command live
        if logical[-1].startswith(":save") and ch in ("\n", "\r"):
            cmd = logical[-1]
            logical[-1] = ""
            handle_save(cmd)
            rebuild_wrapped()
            draw_screen()
            continue

        # NEWLINE
        if ch in ("\n", "\r"):
            logical.append("")
            rebuild_wrapped()
            draw_screen()
            continue

        # BACKSPACE
        if ch in ("\x7f", "\b"):
            if len(logical[-1]) > 0:
                logical[-1] = logical[-1][:-1]
                rebuild_wrapped()
                draw_screen()
            continue

        # NORMAL CHARACTER
        logical[-1] += ch
        rebuild_wrapped()
        draw_screen()

    time.sleep(0.01)
