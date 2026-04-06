# BlueBoopYT Drone Helmet v0.1 Alpha

A wearable, fully offline "drone" interface with hardware-enforced safety.

## Overview
This device is designed as a secure, consent-focused wearable restraint interface. It features a local OLED display, a 3.5mm audio interface, a solenoid-driven physical lock, a torque sensor for engagement, and a battery-health monitoring system.

## Key Safety Features
- **Dual-Release Mechanism**: Requires both strap buckle unlatching and mouth-cap removal for device removal.
- **Torque Threshold**: Lock only engages when torque ≥ 2.2 N·m is detected.
- **Battery Safety**: Lock is disabled if battery voltage drops below 3.4 V.
- **Fail-Open Design**: Solenoid fails open if power is lost or the controller hangs.
- **Offline Only**: No cloud, no telemetry, local BLE-only communication.

## Quickstart
1.  **Calibration**: Follow `docs/calibration_protocol_v2.1.0.md` to calibrate the torque sensor and battery monitoring.
2.  **Firmware**: Flash the firmware from `firmware/src/` to an ESP32-WROOM-32.
3.  **Hardware**: Print components from `hardware/stls/` and assemble according to the BOM in `hardware/bom.csv`.
4.  **App**: Use the local-only companion app in `app/` to provide consent and trigger media patterns.

## Safety Warning
**ALWAYS** ensure the dual-release mechanism is tested and functional before use. **NEVER** bypass the torque sensor or battery safety checks.
