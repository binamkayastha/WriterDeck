import time
import board
import displayio
import digitalio
import microcontroller
import supervisor
import sys
from fourwire import FourWire
from adafruit_st7789 import ST7789

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
display = ST7789(
    display_bus, rotation=90, width=DISPLAY_WIDTH, height=DISPLAY_HEIGHT, rowstart=40, colstart=53
)

print("PyKit Display Ready: ")
print("USB Text Editor: type text, backspace works")

buffer = ""  # editor buffer

while True:
    if supervisor.runtime.serial_bytes_available:
        ch = sys.stdin.read(1)

        # BACKSPACE
        if ch == "\x7f" or ch == "\b":
            if len(buffer) > 0:
                buffer = buffer[:-1]
                print("\b \b", end="")   # erase on console
            continue

        # NEWLINE
        if ch == "\n" or ch == "\r":
            buffer += "\n"
            print()  # go to next line on TFT + console
            continue

        # NORMAL CHAR
        buffer += ch
        print(ch, end="")  # print char to console + TFT

    time.sleep(0.01)
