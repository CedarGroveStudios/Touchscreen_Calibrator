# Touchscreen Calibrator
A simple CircuitPython DisplayIO touchscreen calibrator for built-in displays.

On-screen touchscreen calibrator function for built-in displays. To use, include the following two lines in the calling module or type into the REPL:

   ```python
   from cedargrove_touch_calibrator import touch_calibrator
   touch_calibrator()
   ```
   
   To override the display's previous rotation value, specify a rotation value (in degrees: 0, 90, 180, 270) when calling the calibrator function:

   ```python
   touch_calibrator(rotation=90)
   ```

   To disable the graphics display and use only the REPL, specify `True` for the `repl_only` argument:

   ```python
   touch_calibrator(repl_only=True)
   ```

   When the test screen appears, use a stylus to swipe to the four sides of the visible display area. As the screen is calibrated, the small red square tracks the stylus tip (repl_only=False). Minimum and maximum calibration values will display on the screen and in the REPL. The REPL values can be copied and pasted into the calling code's touchscreen instantiation statement.
   
   Touchscreen Instantiation example code. The order of the calibration tuples is determined by the display rotation value.
   
   ![Touchscreen Instantiation Example Code](https://github.com/CedarGroveStudios/Touchscreen_Calibrator/blob/main/docs/Touch_Calib_example.png)
   
![example screen shot](https://github.com/CedarGroveStudios/Touchscreen_Calibrator/blob/main/docs/Touch_Calib_example.png)
