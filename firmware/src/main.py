import machine
import time
import hx711
import ble_uart
import display
from media_engine import MediaEngine
from lock_control import LockControl

# GPIO Pins - Updated v2.1.1
BATTERY_ADC_PIN = 34 # Input-only
SOLENOID_PIN = 23
VIBRATION_PWM_PIN = 27
STRAP_BUCKLE_PIN = 14
MOUTH_CAP_PIN = 15
HX711_SCK_PIN = 32
HX711_DOUT_PIN = 33
I2C_SDA_PIN = 21
I2C_SCL_PIN = 22

# Global status
status = {
    "battery_v": 0.0,
    "torque_nm": 0.0,
    "consent_given": False,
    "lock_state": "UNLOCKED",
    "locked": False,
    "last_packet_time": 0
}

# Pre-initialize ADC to avoid memory fragmentation
battery_adc = machine.ADC(machine.Pin(BATTERY_ADC_PIN))
battery_adc.atten(machine.ADC.ATTN_11DB)

def read_battery_voltage():
    val = battery_adc.read()
    # Assuming a 100k/47k voltage divider (scale accordingly)
    # Voltage = ADC * (Vref/4095) * (Divider_Factor)
    voltage = (val / 4095.0) * 3.3 * (147.0 / 47.0)
    return voltage

def setup():
    print("Kink Drone v2.1.0 Initializing...")
    # Initialize Watchdog Timer (WDT) - 5 second timeout
    wdt = machine.WDT(timeout=5000)

    # Setup pins
    solenoid_pin = machine.Pin(SOLENOID_PIN, machine.Pin.OUT)
    solenoid_pin.value(0) # Fail-open by default

    strap_buckle = machine.Pin(STRAP_BUCKLE_PIN, machine.Pin.IN, machine.Pin.PULL_UP)
    mouth_cap = machine.Pin(MOUTH_CAP_PIN, machine.Pin.IN, machine.Pin.PULL_UP)

    # Initialize components
    i2c = machine.I2C(0, sda=machine.Pin(I2C_SDA_PIN), scl=machine.Pin(I2C_SCL_PIN))
    oled = display.Display(i2c)

    hx = hx711.HX711(pd_sck=HX711_SCK_PIN, dout=HX711_DOUT_PIN)
    hx.set_scale(100.0) # To be calibrated with torque wrench
    hx.tare()

    ble = ble_uart.BLEUART()
    media = MediaEngine(vibe_pin=VIBRATION_PWM_PIN)
    lock = LockControl(solenoid_pin=SOLENOID_PIN)

    return wdt, oled, hx, ble, media, lock, strap_buckle, mouth_cap

def main_loop():
    wdt, oled, hx, ble, media, lock, strap_buckle, mouth_cap = setup()
    status["last_packet_time"] = time.time()

    while True:
        # 1. Feed the Watchdog Timer
        wdt.feed()

        # 2. Health check
        battery_v = read_battery_voltage()
        status["battery_v"] = battery_v

        # 3. Dual-release check (active high if released)
        buckle_unlatched = (strap_buckle.value() == 1)
        mouth_removed = (mouth_cap.value() == 1)

        # 4. Torque sensor read
        torque_nm = hx.get_units(3) # Fewer counts for faster loop
        status["torque_nm"] = torque_nm

        # 5. BLE commands
        cmd = ble.read()
        if "CONSENT_ACK" in cmd:
            status["consent_given"] = True
            status["last_packet_time"] = time.time()
        elif "STOP" in cmd:
            status["consent_given"] = False
            lock.release()
            media.stop_tone()
            media.vibrate(0)

        # 6. State Update & Solenoid Control
        lock_ready = (battery_v >= 3.4 and torque_nm >= 2.2 and status["consent_given"])

        # Check safety overrides first
        if buckle_unlatched or mouth_removed or battery_v < 3.4:
            lock.release()
            media.stop_tone()
            status["lock_state"] = "UNLOCKED"
            status["locked"] = False
        elif lock_ready:
            lock.engage()
            status["lock_state"] = "LOCKED"
            status["locked"] = True
        elif torque_nm >= 2.2:
            lock.release() # Ensure solenoid is off if torque is high but consent/battery is missing
            status["lock_state"] = "PRE_LOCKED"
            status["locked"] = False
        else:
            lock.release() # Default to off
            status["lock_state"] = "UNLOCKED"
            status["locked"] = False

        # 7. Watchdog/Timeout check (5s timeout for control packets)
        if time.time() - status["last_packet_time"] > 5.0 and status["locked"]:
            lock.release()
            media.stop_tone()
            status["lock_state"] = "TIMEOUT_RELEASE"
            status["locked"] = False

        # 8. Display update
        oled.clear()
        oled.text(f"BAT: {battery_v:.2f}V", 0, 0)
        oled.text(f"TRQ: {torque_nm:.2f}Nm", 0, 10)
        oled.text(f"STATE: {status['lock_state']}", 0, 20)
        if not status["consent_given"]:
            oled.text("WAIT CONSENT", 0, 30)
        oled.show()

        # 9. Media control (if locked)
        if status["locked"]:
            media.decode_frame(None) # Placeholder for visual loop

        # 10. Send Telemetry to BLE app
        ble.write(f"ST: {status['lock_state']} | B: {battery_v:.2f}V | T: {torque_nm:.2f}Nm\n")

        time.sleep(0.05) # Loop at ~20Hz for responsiveness

if __name__ == "__main__":
    main_loop()
