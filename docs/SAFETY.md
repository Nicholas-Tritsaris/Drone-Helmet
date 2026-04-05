# Kink Drone v2.1.0 Safety Verification

This document outlines how each of the non-negotiable safety rules is implemented in the Kink Drone v2.1.0 design.

## 1. Dual-Release Mechanism
**Rule**: Device must be removable ONLY by simultaneously: (1) Unbuckling the strap AND (2) Removing the mouth cap.
- **Implementation (Hardware)**: Two separate physical switches (GPIO14, GPIO15) are integrated into the strap buckle and mouth cap.
- **Implementation (Firmware)**: `firmware/src/main.py` checks both switches. If EITHER is triggered (value == 1), the lock is released immediately.
- **Fail-Open**: The solenoid is a pull-type with a physical spring. Without power, it remains in the UNLOCKED state.

## 2. Torque Sensor Threshold
**Rule**: Lock engages only when torque ≥ 2.2 N·m.
- **Implementation (Hardware)**: 5kg load cell with HX711 24-bit ADC on GPIO32/33.
- **Implementation (Firmware)**: `TORQUE_THRESHOLD_NM = 2.2` check in `main.py`. The firmware monitors the `hx711.py` driver, which includes a non-blocking safety timeout to prevent system hangs if the sensor fails.
- **Calibration**: See `docs/calibration_protocol_v2.1.0.md` for the torque wrench calibration steps.

## 3. Battery Health Check
**Rule**: If voltage < 3.4 V, disable lock mode and show warning.
- **Implementation (Hardware)**: Voltage divider (100k/47k) on GPIO34 (Input-only).
- **Implementation (Firmware)**: `BATTERY_MIN_V = 3.4` in `main.py`. The `main_loop()` reads the battery voltage every cycle. If it drops below 3.4V, the solenoid is released and a "LOW BATTERY" warning is shown on the OLED.

## 4. Materials Safety
**Rule**: All silicone/foam parts must be ISO 10993-5 certified.
- **Implementation (BOM)**: `hardware/bom.csv` specifies "Dragon Skin 10 NV" medical-grade silicone from Smooth-On. No substitutions are allowed.

## 5. Fail-Safe / Watchdog
**Rule**: If the ESP32 hangs, the lock must fail-open.
- **Implementation (Hardware)**: A 10k pull-down resistor on the solenoid MOSFET gate (GPIO23) ensures it releases if the ESP32 pin goes high-impedance.
- **Implementation (Firmware)**: A software Watchdog Timer (`machine.WDT`) is enabled with a 5-second timeout in `main.py`. If the main loop hangs due to blocking calls or errors, the ESP32 resets, forcing the solenoid into the fail-open state.
- **Non-Blocking Logic**: All drivers (HX711, MediaEngine) are implemented using timeouts or background timers (Timer 1) to ensure the safety-critical loop remains responsive.
