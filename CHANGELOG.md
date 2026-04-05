# CHANGELOG v2.1.0

## [2.1.0] - 2024-10-24
### Added
- New **Dual-Release** mechanism for strap buckle + mouth-cap.
- Improved **Torque Sensor** calibration (≥2.2 N·m threshold).
- Enhanced **Battery Health** check (3.4 V minimum at GPIO33).
- **OLED UI** (1.3" I2C) for status monitoring (lock, consent, torque, battery).
- **BLE-UART** local-only communication for media control.
- **Fail-Open** solenoid latch design.
- **MicroPython + C** dual-source firmware architecture.

### Changed
- Updated housing to **PETG-optimized** shell (v2.1.0).
- Refined **HX711** load cell integration for higher precision.
- Standardized **ISO 10993-5** certified silicone parts.

### Fixed
- Fixed bug where lock state could be bypassed on power-on reset.
- Improved solenoid thermal dissipation for extended lock durations.
- Corrected I2C address conflict for the SHARP LS013B4DN02 equivalent OLED.
