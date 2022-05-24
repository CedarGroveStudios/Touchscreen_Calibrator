# Touchscreen Calibrator
A simple CircuitPython DisplayIO resistive touchscreen calibrator for Adafruit built-in and TFT FeatherWing displays.

On-screen touchscreen calibrator for built-in and TFT FeatherWing displays. To use, run as a standalone module, include the following line in the calling module, or type into the REPL:

   ```python
   import touch_calibrator_built_in
   ```
   for built-in displays or
   ```python
   import touch_calibrator_stmpe610
   ```
   for TFT FeatherWing displays.
   
   Operational paramaters such as screen rotation and REPL-only measurement display can be set in the `operational paramaters` portion of the module.

   When the test screen appears, use a stylus to swipe to the four edges of the visible display area. As the screen is calibrated, the small red square tracks the stylus tip (REPL_ONLY=False). Minimum and maximum calibration values will display on the screen and in the REPL. The REPL values can be copied and pasted into the calling code's touchscreen instantiation statement.
   
   Touchscreen Instantiation example code for built-in displays. The order of the calibration tuples is determined by the display rotation value.
   
   ![Touchscreen Instantiation Example Code](https://github.com/CedarGroveStudios/Touchscreen_Calibrator/blob/main/docs/Touch_Calib_example.png)
   
![example screen shot](https://github.com/CedarGroveStudios/Touchscreen_Calibrator/blob/main/docs/touchscreen_calibrator_screen.jpg)
