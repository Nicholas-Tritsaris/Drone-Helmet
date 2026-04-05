# Prompt for ChatGPT to Generate Project Files (Neutral Version)

Please generate the following files for the **Secure Industrial Wearable v2.1.0** project. This is a wearable, offline device with a hardware-enforced dual-interlock system built on an ESP32-WROOM-32.

### Project Context for File Content:
- **Technical Features**: Dual-switch safety interlock (requires two inputs to be active for release), Torque-activated solenoid engagement (threshold ≥ 2.2 N·m), Battery voltage monitoring with fail-safe cutoff (3.4 V), Fail-open solenoid design.
- **Hardware**: ESP32-WROOM-32, 1.3" OLED, Pull-type solenoid driver (GPIO23), HX711 Load Cell Interface (GPIO32/33), Vibration motor driver (GPIO27).
- **Communication**: Local-only BLE-UART communication (no cloud/telemetry).

### Files to Generate:

1. **Excel Sheet (`bom_v2.1.0.xlsx`)**:
   - Create a Bill of Materials for a secure industrial wearable.
   - Include columns: Component, Quantity, Part Number, Estimated Cost, and Purpose.
   - Include: ESP32-WROOM-32, 12V Solenoid, HX711 Load Cell, 1.3" OLED, TP4056 Charger, 18650 Battery, and medical-grade silicone components.

2. **Word Document (`manual_v2.1.0.docx`)**:
   - Technical user manual for the Secure Industrial Wearable.
   - Sections: System Overview, Assembly Instructions, Safety Interlock Precautions, Load Cell Calibration Protocol, and Operating Procedures.

3. **PowerPoint Presentation (`presentation_v2.1.0.pptx`)**:
   - Technical design overview presentation.
   - Slides: Project Goals (Secure Wearable Interface), Safety-Critical Architecture (Dual-Interlock, Torque Sensing, Voltage Cutoff), Hardware Subsystems, MicroPython Firmware Structure, and Future Technical Roadmap.

4. **PDF Document (`safety_v2.1.0.pdf`)**:
   - Engineering Safety Verification Report.
   - Detail the safety-critical requirements for the dual-interlock mechanism and the battery-health fail-safe.

5. **Placeholder STL Files**:
   - Provide four files with the following names:
     - `shell_base_v2.1.0.stl`
     - `oled_mount_v2.1.0.stl`
     - `lock_icon_v2.1.0.stl`
     - `label_backplate_v2.1.0.stl`
   - These should be valid ASCII STL files (e.g., `solid [name] \n endsolid [name]`).

Please provide these files for download.
