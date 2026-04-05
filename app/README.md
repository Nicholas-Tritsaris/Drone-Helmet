# Kink Drone Companion App (Local-only)

The Kink Drone v2.1.0 uses a local-only mobile app for status monitoring and consent management.

## 1. Local-Only Design
- **No Cloud**: No internet permissions are required or used.
- **BLE-only**: All communication is via Bluetooth Low Energy (BLE) using a custom UART profile.
- **Media Streaming**: Audio and visual patterns are stored on the phone and sent to the device via BLE.

## 2. Core Functions
- **Lock Status**: Real-time display of the device's current lock state (locked, unlocked, or pre-locked).
- **Consent Confirmation**: A "Confirm Override" or "Acknowledge" button for providing the necessary consent for locking.
- **Torque/Battery Readings**: Real-time readout of the N·m sensor and battery voltage from the device.
- **Media Control**: Triggering pre-loaded audio/vibration patterns or custom patterns from the app.

## 3. Protocol (BLE-UART)
The app communicates with the ESP32 using simple JSON-like command strings:
- `CONSENT_ACK`: User has provided consent for locking.
- `PLAY_PATTERN <ID>`: Trigger a specific vibration/media pattern.
- `STOP_MEDIA`: Immediately halt all media and audio playback.
- `GET_STATUS`: Request battery and sensor telemetry.

## 4. Mobile Platforms
- **Android**: Flutter-based app (v2.1.0), see `android/` for APK.
- **iOS**: Xcode project (v2.1.0), see `ios/` for IPA.

**Key Rule**: The app NEVER enforces the lock state; the device's hardware and firmware always have the final say on safety.
