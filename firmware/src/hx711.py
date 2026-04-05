import machine
import time

class HX711:
    def __init__(self, pd_sck, dout, gain=128):
        self.pd_sck = machine.Pin(pd_sck, machine.Pin.OUT)
        self.dout = machine.Pin(dout, machine.Pin.IN)
        self.gain = gain
        self.offset = 0
        self.scale = 1.0

        self.pd_sck.value(0)
        self.set_gain(gain)

    def set_gain(self, gain):
        if gain == 128:
            self.gain_pulses = 1
        elif gain == 64:
            self.gain_pulses = 3
        elif gain == 32:
            self.gain_pulses = 2
        else:
            self.gain_pulses = 1

    def is_ready(self, timeout_ms=100):
        """Check if the HX711 is ready with a safety timeout."""
        start = time.ticks_ms()
        while self.dout.value() == 1:
            if time.ticks_diff(time.ticks_ms(), start) > timeout_ms:
                return False
        return True

    def read(self):
        """Read 24-bit raw value from the HX711 with safety check."""
        if not self.is_ready():
            return 0 # Return 0 or handle sensor error in main loop

        value = 0
        for _ in range(24):
            self.pd_sck.value(1)
            time.sleep_us(1)
            value = (value << 1) | self.dout.value()
            self.pd_sck.value(0)
            time.sleep_us(1)

        # Pulse for gain
        for _ in range(self.gain_pulses):
            self.pd_sck.value(1)
            time.sleep_us(1)
            self.pd_sck.value(0)
            time.sleep_us(1)

        # 2's complement
        if value & 0x800000:
            value -= 0x1000000

        return value

    def get_units(self, count=5):
        """Read and average multiple readings, or return last value if sensor fails."""
        total = 0
        readings = 0
        for _ in range(count):
            val = self.read()
            if val != 0:
                total += val
                readings += 1

        if readings == 0:
            return -1.0 # Error indicator

        average = total / readings
        return (average - self.offset) / self.scale

    def tare(self, count=10):
        total = 0
        readings = 0
        for _ in range(count):
            val = self.read()
            if val != 0:
                total += val
                readings += 1
        if readings > 0:
            self.offset = total / readings

    def set_scale(self, scale):
        self.scale = scale
