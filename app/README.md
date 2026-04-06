# BlueBoopYT Drone Helmet Companion App (v0.1 Alpha)

The BlueBoopYT Drone Helmet v0.1 Alpha uses a local-only mobile app for status monitoring and consent management.

## 1. Local-Only Design
- **No Cloud**: No internet permissions are required or used.
- **BLE-only**: All communication is via Bluetooth Low Energy (BLE) using a custom GATT profile.
- **Media Streaming**: Visual patterns (128x128 monochrome) are sent to the device via the Media Stream Service.

## 2. Core Functions
- **Lock Status**: Real-time display of the device's current lock state (unlocked, locked, engaged, or emergency).
- **Consent Confirmation**: Writing to the Torque Threshold characteristic confirms the user's intent to engage the lock.
- **Torque/Battery Readings**: Real-time telemetry via the Telemetry Service.
- **Media Control**: Uploading frames and setting frame rates for the visual spiral.

## 3. GATT Profile (BlueBoopYT v0.1a)

### Lock Control Service (0xBBBB1111-AAAA-BBBB-CCCC-DDDDEEEEFFFF)
- **Lock State (0xBBBB1112)**: [Read/Notify] uint8 (0: unlocked, 1: locked, 2: engaged, 3: emergency)
- **Torque Threshold (0xBBBB1113)**: [Read/Write] float32 (N·m). Writing here confirms consent.
- **Emergency Release (0xBBBB1114)**: [Write] uint16. Write `0xDEAD` to trigger release.

### Media Stream Service (0xBBBB2222-AAAA-BBBB-CCCC-DDDDEEEEFFFF)
- **Spiral Frame (0xBBBB2223)**: [Write] uint8[2048] (128x128 monochrome bitmap).
- **Frame Rate (0xBBBB2224)**: [Read/Write] uint8 (1–12 fps).

### Telemetry Service (0xBBBB3333-AAAA-BBBB-CCCC-DDDDEEEEFFFF)
- **Battery Voltage (0xBBBB3334)**: [Read/Notify] float32 (V).
- **Ambient Temp (0xBBBB3335)**: [Read/Notify] float32 (°C).
- **Torque Reading (0xBBBB3336)**: [Read/Notify] float32 (N·m).

## 4. Mobile Platforms
- **Android**: Kotlin / Jetpack Compose, see `/app/android/`.
- **iOS**: Swift / SwiftUI, see `/app/ios/`.
- **Windows Phone 10**: C# / UWP, see `/app/wp10/`.

**Key Rule**: The app NEVER enforces the lock state; the device's hardware and firmware always have the final say on safety.
