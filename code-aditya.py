import board
import busio
import displayio
import terminalio
import digitalio
from adafruit_display_text import label
#import adafruit_st7789
import time

print("Start")

# ----------------------------------------
# DEFINITIVE TFT PINOUT FROM SCHEMATIC
# ----------------------------------------
TFT_CS = board.D10 # NLTFT0CS
TFT_DC = board.D4 # NLTFT0RS
TFT_RST = board.D11 # NLTFT0RESET
TFT_BL = board.D8 # NLTFT0LEDA (backlight)

TFT_SCK = board.D6 # NLTFT0SCK
TFT_MOSI = board.D5 # NLTFT0MOSI

# Display parameters
DISPLAY_WIDTH = 240
DISPLAY_HEIGHT = 135
DISPLAY_ROTATION = 90 # horizontal along the ruler


# ----------------------------------------
# BLE UART SETUP
# ----------------------------------------
BLE_TX = board.BLE_TX # SAME51 TX → RNBD451 RX
BLE_RX = board.BLE_RX # RNBD451 TX → SAME51 RX
BLE_BAUD = 115200

uart = busio.UART(
    BLE_TX,
    BLE_RX,
    baudrate=BLE_BAUD,
    timeout=0.01,
)


# ----------------------------------------
# INITIALIZE DISPLAY
# ----------------------------------------
displayio.release_displays()

# Software SPI (because TFT SCK/MOSI are on D6/D5 per schematic)
spi = busio.SPI(clock=TFT_SCK, MOSI=TFT_MOSI)

# Chip select pin
cs = digitalio.DigitalInOut(TFT_CS)
cs.direction = digitalio.Direction.OUTPUT
cs.value = True

# Data/Command pin
dc = digitalio.DigitalInOut(TFT_DC)
dc.direction = digitalio.Direction.OUTPUT

# Reset pin
reset_pin = digitalio.DigitalInOut(TFT_RST)
reset_pin.direction = digitalio.Direction.OUTPUT

# Backlight pin
bl = digitalio.DigitalInOut(TFT_BL)
bl.direction = digitalio.Direction.OUTPUT
bl.value = True # turn on backlight


# 4-wire SPI bus for display
display_bus = displayio.FourWire(
    spi,
    command=dc,
    chip_select=cs,
    reset=reset_pin,
    baudrate=24_000_000,
)


# display = adafruit_st7789.ST7789(
#     display_bus,
#     width=DISPLAY_WIDTH,
#     height=DISPLAY_HEIGHT,
#     rotation=DISPLAY_ROTATION,
# )


# ----------------------------------------
# TEXT BUFFER SETUP
# ----------------------------------------
main_group = displayio.Group()
# display.root_group = main_group

bg_bitmap = displayio.Bitmap(DISPLAY_WIDTH, DISPLAY_HEIGHT, 1)
bg_palette = displayio.Palette(1)
bg_palette[0] = 0x000000
bg_sprite = displayio.TileGrid(bg_bitmap, pixel_shader=bg_palette)
main_group.append(bg_sprite)

text_area = label.Label(
    terminalio.FONT,
    text="Waiting for BLE...\n",
    color=0xFFFFFF,
    x=0, y=0,
    line_spacing=1.0,
)
main_group.append(text_area)

lines = ["Waiting for BLE..."]
MAX_CHARS_PER_LINE = 26
MAX_LINES = 7


def append_text(s):
    global lines

    for ch in s:
        if ch == "\r":
            continue
        if ch == "\n":
            lines.append("")
            continue

        if len(lines[-1]) >= MAX_CHARS_PER_LINE:
            lines.append(ch)
        else:
            lines[-1] += ch

    if len(lines) > MAX_LINES:
        lines = lines[-MAX_LINES:]

    text_area.text = "\n".join(lines)



# ----------------------------------------
# MAIN LOOP
# ----------------------------------------
append_text("\nReady.\nConnect from tablet BLE UART.\n")
print("Before Loop")

while True:

    print("Loop")
    data = uart.read(32)
    if data:
        try:
            txt = data.decode("utf-8", errors="ignore")
        except:
            txt = "".join(chr(b) for b in data if 32 <= b <= 126)

        append_text(txt)

    time.sleep(0.01)

# # SPDX-FileCopyrightText: 2018 Kattni Rembor for Adafruit Industries
# #
# # SPDX-License-Identifier: MIT

# """CircuitPython Essentials Internal RGB LED red, green, blue example"""
# import time
# import board
# import busio
# import digitalio


# if hasattr(board, "APA102_SCK"):
#     import adafruit_dotstar

#     led = adafruit_dotstar.DotStar(board.APA102_SCK, board.APA102_MOSI, 1)
# else:
#     import neopixel

#     led = neopixel.NeoPixel(board.NEOPIXEL, 1)

# led.brightness = 0.3


# while True:
#     led[0] = (255, 0, 0)
#     print("helllo")
#     time.sleep(0.5)
#     led[0] = (0, 255, 0)
#     time.sleep(0.5)
#     led[0] = (0, 0, 255)
#     time.sleep(0.5)

    

#     # SPDX-FileCopyrightText: 2018 Kattni Rembor for Adafruit Industries
# #
# # SPDX-License-Identifier: MIT

# """CircuitPython Essentials UART Serial example"""
# # For most CircuitPython boards:
# led = digitalio.DigitalInOut(board.D13)
# # For QT Py M0:
# # led = digitalio.DigitalInOut(board.SCK)
# led.direction = digitalio.Direction.OUTPUT

# uart = busio.UART(board.BLE_TX, board.BLE_RX, baudrate=115200)

# UPDATE_INTERVAL = 0.5
# last_time_sent = 0

# value = 0

# while True:
    
#     now = time.monotonic()
#     if now - last_time_sent >= UPDATE_INTERVAL:
#         uart.write(bytes(f"Value:{value}\n", "ascii"))
#         last_time_sent = now
#         value += 1
    
#     data = uart.read(32)  # read up to 32 bytes
#     print(data)  # this is a bytearray type
