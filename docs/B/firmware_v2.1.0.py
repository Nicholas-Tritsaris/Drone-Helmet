
# Secure Industrial Wearable v2.1.0 Firmware (MicroPython)

from machine import Pin, ADC
import time

# GPIO setup
solenoid = Pin(23, Pin.OUT)
vibration = Pin(27, Pin.OUT)

interlock1 = Pin(18, Pin.IN, Pin.PULL_UP)
interlock2 = Pin(19, Pin.IN, Pin.PULL_UP)

battery_adc = ADC(Pin(34))
battery_adc.atten(ADC.ATTN_11DB)

SAFE_VOLTAGE = 3.4

def read_battery():
    raw = battery_adc.read()
    voltage = (raw / 4095) * 4.2
    return voltage

def check_interlock():
    return interlock1.value() == 0 and interlock2.value() == 0

def engage_lock():
    solenoid.value(1)

def release_lock():
    solenoid.value(0)

while True:
    voltage = read_battery()
    
    if voltage < SAFE_VOLTAGE:
        release_lock()
        vibration.value(1)
        time.sleep(0.2)
        vibration.value(0)
        continue
    
    if check_interlock():
        engage_lock()
    else:
        release_lock()
    
    time.sleep(0.1)
