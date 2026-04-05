# Prompt for ChatGPT to Generate Project Files

Please generate the following files for the **Kink Drone v2.1.0** project. This is a wearable, offline restraint interface built on an ESP32-WROOM-32 with hardware-enforced safety.

### Project Context for File Content:
- **Safety Features**: Dual-release (strap buckle + mouth cap), Torque engagement threshold (≥ 2.2 N·m), Battery cutoff (3.4 V), Fail-open solenoid.
- **Hardware**: ESP32, 1.3" OLED, Pull-type solenoid (GPIO23), HX711 Load Cell (GPIO32/33), Vibration motor (GPIO27).
- **Communication**: Local BLE-UART only (no cloud).

### Files to Generate:

1. **Excel Sheet (`bom_v2.1.0.xlsx`)**:
   - Create a Bill of Materials.
   - Include columns: Component, Quantity, Part Number, Estimated Cost, and Purpose.
   - Include items like ESP32-WROOM-32, 12V Solenoid, HX711 Board, 1.3" OLED Display, TP4056 Charger, 18650 Battery, etc.

2. **Word Document (`manual_v2.1.0.docx`)**:
   - A comprehensive user manual.
   - Sections: Overview, Assembly Instructions, Safety Precautions (very important), Calibration Protocol, and Operation Guide.

3. **PowerPoint Presentation (`presentation_v2.1.0.pptx`)**:
   - A technical overview presentation.
   - Slides: Project Goals, Safety Architecture (Dual-Release, Torque, Battery), Hardware Components, Firmware Logic (MicroPython/C), and Future Roadmap.

4. **PDF Document (`safety_v2.1.0.pdf`)**:
   - A formal safety verification report.
   - Detail the non-negotiable safety rules and how they are implemented in hardware/firmware.

5. **Placeholder STL Files**:
   - Provide four files with the following names:
     - `shell_base_v2.1.0.stl`
     - `oled_mount_v2.1.0.stl`
     - `lock_icon_v2.1.0.stl`
     - `label_backplate_v2.1.0.stl`
   - These can be empty ASCII STL files (e.g., `solid [name] \n endsolid [name]`).

Please provide these files for download.
