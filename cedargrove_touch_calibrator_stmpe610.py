# SPDX-FileCopyrightText: 2021 Cedar Grove Maker Studios
# SPDX-License-Identifier: MIT

# cedargrove_touch_calibrator_stmpe610.py
# 2022-01-18 v1.9

import board
import time
import digitalio
import displayio
import vectorio
from adafruit_bitmap_font import bitmap_font
from adafruit_display_text.label import Label
import cg_stmpe610
from simpleio import map_range


class Colors:
    BLUE_DK = 0x000060
    RED = 0xFF0000
    WHITE = 0xFFFFFF


def touch_calibrator(rotation=None, repl_only=False, raw_data=True):
    """On-screen touchscreen calibrator function for TFT FeatherWings. To use,
    include the following two lines in the calling module or type into the REPL:

    from cedargrove_touch_calibrator_SMTPE610 import touch_calibrator
    touch_calibrator()

    To override the display's previous rotation value, specify a rotation value
    (in degrees: 0, 90, 180, 270) when calling the calibrator function:

    touch_calibrator(rotation=90)

    When the test screen appears, use a stylus to swipe to the four sides
    of the visible display area. As the screen is calibrated, the small red
    square tracks the stylus tip (repl_only=False). Minimum and maximum
    calibration values will display on the screen and in the REPL. The REPL
    values can be copied and pasted into the calling code's touchscreen
    instantiation statement.

    :param int rotation: Display rotation value in degrees. Only values of
    None, 0, 90, 180, and 270 degrees are accepted. Defaults to None, the
    previous orientation of the display.
    :param bool repl_only: If False, calibration values are shown on the screen
    and printed to the REPL. If True, the values are only printed to the REPL.
    Default value is False.
    """

    from adafruit_ili9341 import ILI9341  # 2.4" 320x240 TFT FeatherWing (#3315)

    # from adafruit_hx8357 import HX8357  # 3.5" 480x320 TFT FeatherWing (#3651)

    # Release any resources currently in use for the displays
    displayio.release_displays()

    spi = (
        board.SPI()
    )  # SCK to display SCK, MO to display SI, MI to display SO (SD card)
    tft_cs = board.D9  # to display TCS
    tft_dc = board.D10  # to display D/C
    tft_reset = None  # to display RST (for Feather, board.D6 for breakout)

    display_bus = displayio.FourWire(
        spi, command=tft_dc, chip_select=tft_cs, reset=tft_reset
    )

    # 320 x 240
    display = ILI9341(display_bus, width=320, height=240)
    # 480 x 320
    # display = HX8357(display_bus, width=480, height=320)

    if not rotation:
        _rotation = 0
    else:
        _rotation = rotation

    display.rotation = _rotation

    WIDTH, HEIGHT = (display.width, display.height)

    if not repl_only:
        display_group = displayio.Group()
        display.show(display_group)

    # Instantiate touch screen without calibration or display size parameters
    ts_cs_pin = digitalio.DigitalInOut(board.D6)

    # Measure and display raw touch data or
    #  scaled screen size data with a previously measured raw calibration range
    if raw_data:
        ts = cg_stmpe610.Adafruit_STMPE610_SPI(spi, ts_cs_pin)
    else:
        ts = cg_stmpe610.Adafruit_STMPE610_SPI(
            spi, ts_cs_pin, calibration=((357, 3812), (390, 3555)), size=(WIDTH, HEIGHT)
        )

    if not repl_only:
        FONT_0 = bitmap_font.load_font("/fonts/OpenSans-9.bdf")

        coordinates = Label(
            font=FONT_0,
            text="calib: ((x_min, x_max), (y_min, y_max))",
            color=Colors.WHITE,
        )
        coordinates.anchor_point = (0.5, 0.5)
        coordinates.anchored_position = (WIDTH // 2, HEIGHT // 4)

        display_rotation = Label(
            font=FONT_0,
            text="rotation: " + str(rotation),
            color=Colors.WHITE,
        )
        display_rotation.anchor_point = (0.5, 0.5)
        display_rotation.anchored_position = (WIDTH // 2, HEIGHT // 4 - 30)

        target_palette = displayio.Palette(1)
        target_palette[0] = Colors.BLUE_DK
        boundary1 = vectorio.Rectangle(
            pixel_shader=target_palette,
            x=2,
            y=2,
            width=WIDTH - 4,
            height=HEIGHT - 4,
        )

        target_palette = displayio.Palette(1)
        target_palette[0] = Colors.RED
        boundary2 = vectorio.Rectangle(
            pixel_shader=target_palette,
            x=0,
            y=0,
            width=WIDTH,
            height=HEIGHT,
        )

        pen = vectorio.Rectangle(
            pixel_shader=target_palette,
            x=WIDTH // 2,
            y=HEIGHT // 2,
            width=10,
            height=10,
        )

        display_group.append(boundary2)
        display_group.append(boundary1)
        display_group.append(pen)
        display_group.append(coordinates)
        display_group.append(display_rotation)

    # Reset x and y values to raw value mid-point
    x = y = 0
    if raw_data:
        x_min = y_min = x_max = y_max = 4096 // 2
    else:
        x_min = y_min = x_max = y_max = min(WIDTH, HEIGHT) // 2  # Display mid-point

    print("Touchscreen Calibrator")
    print("  Use a stylus to swipe to the four sides")
    print("  of the visible display area.")
    print(" ")
    print(f"  rotation: {rotation}")
    print("  Calibration values follow:")
    print(" ")

    while True:
        time.sleep(0.100)
        touch = ts.touch_point
        if touch:
            x = touch[0]
            y = touch[1]

            if not repl_only:
                pen.x = int(round(map_range(x, x_min, x_max, 0, WIDTH), 0)) - 5
                pen.y = int(round(map_range(y, y_min, y_max, 0, HEIGHT), 0)) - 5

            x_min = min(x_min, touch[0])
            x_max = max(x_max, touch[0])
            y_min = min(y_min, touch[1])
            y_max = max(y_max, touch[1])

            print(f"(({x_min}, {x_max}), ({y_min}, {y_max}))")
            if not repl_only:
                coordinates.text = f"calib: (({x_min}, {x_max}), ({y_min}, {y_max}))"
    return
