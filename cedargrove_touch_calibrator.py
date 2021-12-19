# SPDX-FileCopyrightText: 2021, 2022 Cedar Grove Maker Studios
# SPDX-License-Identifier: MIT

# cedargrove_touch_calibrator.py
# 2021-12-18 v1.0

import board
import time
import displayio
import vectorio
from adafruit_bitmap_font import bitmap_font
from adafruit_display_text.label import Label
import adafruit_touchscreen

class Colors:
    BLUE_DK = 0x000060
    RED = 0xFF0000
    WHITE = 0xFFFFFF


def touch_calibrator(rotation=None):
    """On-screen touchscreen calibrator function for built-in displays. To use,
    include the following lines in the calling module:

    from cedargrove_touch_calibrator import touch_calibrator
    touch_calibrator()

    When the test screen appears, use a stylus to swipe outwards from just
    inside each of the four display edges towards the outside of the visible
    display area. The minimum and maximum calibration values will display on
    the screen and in the REPL. The REPL values can be copied and pasted into
    the calling code's touchscreen instantiation statement.

    To override the display's previous rotation value, specify a rotation value
    (in degrees: 0, 90, 180, 270) when calling the calibrator function:

    touch_calibrator(rotation=90)

    Note: During calibration, avoid touching the touchscreen contacts on the
    edge of the display. Finger resistance may alter the measurements. """

    display_group = displayio.Group()

    display = board.DISPLAY
    if rotation:  # Override display rotation
        display.rotation = rotation
    else:
        rotation = display.rotation
    WIDTH = board.DISPLAY.width
    HEIGHT = board.DISPLAY.height

    display.show(display_group)

    # Instantiate touch screen without calibration or display size parameters
    if rotation == 0:
        ts = adafruit_touchscreen.Touchscreen(
            board.TOUCH_XL,
            board.TOUCH_XR,
            board.TOUCH_YD,
            board.TOUCH_YU,
            #calibration=((5200, 59000), (5200, 59500)),
            #size=(WIDTH, HEIGHT),
        )

    if rotation == 90:
        ts = adafruit_touchscreen.Touchscreen(
            board.TOUCH_YU,
            board.TOUCH_YD,
            board.TOUCH_XL,
            board.TOUCH_XR,
            #calibration=((5200, 59000), (5200, 59500)),
            #size=(WIDTH, HEIGHT),
        )

    if rotation == 180:
        ts = adafruit_touchscreen.Touchscreen(
            board.TOUCH_XR,
            board.TOUCH_XL,
            board.TOUCH_YU,
            board.TOUCH_YD,
            #calibration=((5200, 59000), (5200, 59500)),
            #size=(WIDTH, HEIGHT),
        )

    if rotation == 270:
        ts = adafruit_touchscreen.Touchscreen(
            board.TOUCH_YD,
            board.TOUCH_YU,
            board.TOUCH_XR,
            board.TOUCH_XL,
            #calibration=((5200, 59000), (5200, 59500)),
            #size=(WIDTH, HEIGHT),
        )

    FONT_0 = bitmap_font.load_font("/fonts/OpenSans-9.bdf")

    coordinates = Label(
        font=FONT_0,
        text="calib: ((x_min, x_max), (y_min, y_max))",
        color=Colors.WHITE,
    )
    coordinates.anchor_point = (0.5, 0.5)
    coordinates.anchored_position = (WIDTH//2, HEIGHT//4)

    display_rotation = Label(
        font=FONT_0,
        text="rotation: " + str(rotation),
        color=Colors.WHITE,
    )
    display_rotation.anchor_point = (0.5, 0.5)
    display_rotation.anchored_position = (WIDTH//2, HEIGHT//4 - 30)

    target_palette = displayio.Palette(1)
    target_palette[0] = Colors.BLUE_DK
    boundary1 = vectorio.Rectangle(
        pixel_shader=target_palette,
        x=2,
        y=2,
        width=WIDTH-4,
        height=HEIGHT-4,
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

    display_group.append(boundary2)
    display_group.append(boundary1)
    display_group.append(coordinates)
    display_group.append(display_rotation)

    # Reset x and y values to scale center
    x_min = x_max = y_min = y_max = 65535//2

    while True:
        time.sleep(0.100)
        touch = ts.touch_point
        if touch and touch[0] > 3000:
            x_min = min(x_min, touch[0])
            x_max = max(x_max, touch[0])
            y_min = min(y_min, touch[1])
            y_max = max(y_max, touch[1])

            print(f"rot: {rotation}  calib: (({x_min}, {x_max}), ({y_min}, {y_max}))")
            coordinates.text = (f"calib: (({x_min}, {x_max}), ({y_min}, {y_max}))")
    return
