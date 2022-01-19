# SPDX-FileCopyrightText: 2021 ladyada for Adafruit Industries
# SPDX-License-Identifier: MIT
"""
Simple button example.
STMPE610 touch controller with TFT FeatherWing
"""

import board
import displayio
import terminalio
import time
import adafruit_touchscreen
from adafruit_button import Button

# Instantiate display
from adafruit_ili9341 import ILI9341  # 2.4" 320x240 TFT FeatherWing (#3315)

# from adafruit_hx8357 import HX8357  # 3.5" 480x320 TFT FeatherWing (#3651)

# Release any resources currently in use for the displays
displayio.release_displays()
spi = board.SPI()  # SCK to display SCK, MO to display SI, MI to display SO (SD card)
tft_cs = board.D9  # to display TCS
tft_dc = board.D10  # to display D/C
tft_reset = None  # to display RST (for Feather, board.D6 for breakout)

display_bus = displayio.FourWire(
    board.SPI(), command=tft_dc, chip_select=tft_cs, reset=tft_reset
)

# 320 x 240
display = ILI9341(display_bus, width=320, height=240)
# 480 x 320
# display = HX8357(display_bus, width=480, height=320)

display.rotation = 0
# Always set display width and height after rotation
WIDTH = display.width
HEIGHT = display.height

# --| Button Config |-------------------------------------------------
BUTTON_X = 50
BUTTON_Y = 50
BUTTON_WIDTH = 100
BUTTON_HEIGHT = 50
BUTTON_STYLE = Button.ROUNDRECT
BUTTON_FILL_COLOR = 0x00FFFF
BUTTON_OUTLINE_COLOR = 0xFF00FF
BUTTON_LABEL = "HELLO WORLD"
BUTTON_LABEL_COLOR = 0x000000
# --| Button Config |-------------------------------------------------

# Instantiate touch screen without calibration or display size parameters
import digitalio
import cg_stmpe610

# Display rotation must be established before instantiation
ts_cs_pin = digitalio.DigitalInOut(board.D6)

ts = cg_stmpe610.Adafruit_STMPE610_SPI(
    spi,
    ts_cs_pin,
    calibration=((357, 3812), (390, 3555)),
    size=(WIDTH, HEIGHT),
    display_rotation=display.rotation,
)

# Create the displayio group and show it
splash = displayio.Group()
display.show(splash)

# Defiine the button
button = Button(
    x=BUTTON_X,
    y=BUTTON_Y,
    width=BUTTON_WIDTH,
    height=BUTTON_HEIGHT,
    style=BUTTON_STYLE,
    fill_color=BUTTON_FILL_COLOR,
    outline_color=BUTTON_OUTLINE_COLOR,
    label=BUTTON_LABEL,
    label_font=terminalio.FONT,
    label_color=BUTTON_LABEL_COLOR,
)

# Add button to the displayio group
splash.append(button)

# Loop and look for touches
while True:
    p = ts.touch_point
    if p:
        if button.contains(p):
            button.selected = True
            # Perform a task related to the button press
            time.sleep(0.25)  # Wait a bit so we can see the button color change
        else:
            button.selected = False  # When touch moves outside of button
    else:
        button.selected = False  # When button is released
