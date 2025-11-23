print("Hello World!")
# SPDX-FileCopyrightText: 2018 Kattni Rembor for Adafruit Industries
#
# SPDX-License-Identifier: MIT

# """CircuitPython Essentials UART Serial example"""
# import board
# import busio
# import digitalio
# import time

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
