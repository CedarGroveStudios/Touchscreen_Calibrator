# Touchscreen Calibrator
A simple CircuitPython DisplayIO touchscreen calibrator for built-in displays.

On-screen touchscreen calibrator function for built-in displays. To use, include the following lines in the calling module:

   ```python
   from cedargrove_calculator.touch_calibrator import touch_calibrator
   touch_calibrator()
   ```

   When the test screen appears, use a stylus to swipe outwards from just inside each of the four display edges towards the outside of the visible display area. The minimum and maximum calibration values will display on the screen and in the REPL. The REPL values can be copied and pasted into the calling code's touchscreen instantiation statement.

   To override the display's previous rotation value, specify a rotation value (in degrees: 0, 90, 180, 270) when calling the calibrator function:

   ```python
   touch_calibrator(rotation=90)
   ```

   Note: During calibration, avoid touching the touchscreen contacts on the edge of the display. Finger resistance may alter the measurements.
   
   Touchscreen Instantiation Example code. The order of the calibration tuples is determined by the display rotation value.
   
   ![Touchscreen Instantiation Example](https://github.com/CedarGroveStudios/Touchscreen_Calibrator/blob/main/docs/Touch_Rot_Calib_example)
   
