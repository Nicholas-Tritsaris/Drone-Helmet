# Hardware Design v2.1.0

This directory contains the mechanical and electrical design for the Kink Drone v2.1.0.

## 1. Mechanical (STLs)
The shell is designed for 3D printing in PETG. The STLs are located in `hardware/stls/`.
- `shell_base_v2.1.0.stl`: Main housing for ESP32, battery, and solenoid.
- `oled_mount_v2.1.0.stl`: Press-fit frame for the 1.3" OLED.
- `lock_icon_v2.1.0.stl`: Indicator for lock state status.
- `label_backplate_v2.1.0.stl`: Mounting point for regulatory and safety labels.

**Filament Choice**: Use PETG (Prusa PETG or equivalent) for its toughness and low-shrink properties.
**Silicone/Foam**: All skin-contacting parts MUST be ISO 10993-5 certified medical-grade silicone. Use Dragon Skin 10 NV or equivalent for custom-molded parts.

## 2. Electrical (PCB)
The electronics are based on an ESP32-WROOM-32. The KiCad project is located in `hardware/pcb/`.
- `kink_drone_sch_v2.1.0.kicad_sch`: Schematic with safety isolation for the solenoid.
- `kink_drone_pcb_v2.1.0.kicad_pcb`: 2-layer PCB layout with optimized thermal dissipation for the solenoid driver.

### Pinout (ESP32) - Updated v2.1.1
- **I2C SDA**: GPIO21 (OLED)
- **I2C SCL**: GPIO22 (OLED)
- **Solenoid Driver (PWM/OUT)**: GPIO23
- **Battery Monitoring (ADC)**: GPIO34 (Input-only pin)
- **Torque Sensor (HX711 SCK)**: GPIO32
- **Torque Sensor (HX711 DOUT)**: GPIO33
- **Vibration Motor (PWM)**: GPIO27
- **Audio Jack (DAC L/R)**: GPIO25 and GPIO26 (Dedicated DAC pins)
- **Strap Buckle Switch**: GPIO14
- **Mouth Cap Switch**: GPIO15

## 3. Bill of Materials
Refer to `hardware/bom.csv` for the full component list and estimated costs.
