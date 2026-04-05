# Calibration Protocol v2.1.0

This document outlines the step-by-step calibration procedure for the Kink Drone v2.1.0.

## 1. Battery Monitoring Calibration
The ESP32 uses a voltage divider (e.g., 100k/47k) to read the 3.7V LiPo battery on GPIO33.

1.  Connect a variable DC power supply to the battery input.
2.  Set the power supply to 3.7V and measure the voltage at GPIO33 with a multimeter.
3.  Calculate the scaling factor: `3.7V / ADC_Value`.
4.  Verify that the firmware correctly reads 3.7V.
5.  Lower the power supply to 3.4V.
6.  Ensure the firmware sets `LOCK_DISABLED` and shows a "LOW BATTERY" warning on the OLED.

## 2. Torque Sensor (HX711) Calibration
The torque sensor (strain gauge) must be calibrated using a known torque wrench.

1.  Secure the Kink Drone frame in a stable jig.
2.  Apply known torque values using a calibrated torque wrench: 1.0, 2.0, and 3.0 N·m.
3.  Record the raw ADC values from the HX711 for each point.
4.  Calculate the linear regression to map ADC values to N·m.
5.  Update the `TORQUE_THRESHOLD` constant in `firmware/src/lock_control.c` to 2.2 N·m.
6.  Verify that `TORQUE_LOCK_READY` only activates when force is ≥ 2.2 N·m.

## 3. Dual-Release Mechanical Test
1.  Verify the solenoid fails-open without power.
2.  Confirm that the strap buckle and mouth cap must BOTH be released to disengage the restraint.
3.  Test that no single-point release is possible.
