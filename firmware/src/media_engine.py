import machine
import math
import time

class MediaEngine:
    def __init__(self, vibe_pin=27):
        # PWM for vibration motor (GPIO27 by default)
        self.vibe = machine.PWM(machine.Pin(vibe_pin))
        self.vibe.freq(1000)
        self.vibe.duty(0)

        # Audio DAC for binaural tones (GPIO25/26 on ESP32)
        self.dac = machine.DAC(machine.Pin(25))
        self.tone_timer = machine.Timer(1)
        self.phase = 0
        self.frequency = 0

    def _tone_callback(self, timer):
        """Timer callback for background sine wave generation."""
        if self.frequency > 0:
            val = int(128 + 127 * math.sin(self.phase))
            self.dac.write(val)
            # Sample rate is 1/period (e.g. 1/2ms = 500Hz)
            # Phase increment = 2 * pi * f / fs
            self.phase += 2 * math.pi * self.frequency / 500.0
            if self.phase > 2 * math.pi:
                self.phase -= 2 * math.pi
        else:
            self.dac.write(128)

    def play_tone(self, frequency):
        """Start playing a tone in the background without blocking."""
        self.frequency = frequency
        if frequency > 0:
            # 2ms period = 500Hz sample rate
            self.tone_timer.init(period=2, mode=machine.Timer.PERIODIC, callback=self._tone_callback)
        else:
            self.tone_timer.deinit()
            self.dac.write(128)

    def stop_tone(self):
        """Halt background tone generation."""
        self.play_tone(0)

    def vibrate(self, intensity):
        """Set vibration intensity (0-1023)."""
        self.vibe.duty(intensity)

    def decode_frame(self, frame_data):
        """
        Processes 16384-bit (2048-byte) monochrome frame data received via BLE.
        Pushes a single frame to the OLED display buffer.
        """
        if frame_data is not None and len(frame_data) == 2048:
            # Transfer frame data to internal storage (assumes display.buffer availability)
            # Placeholder for PSRAM-optimized mapping or direct DMA transfer
            # print(f"[MEDIA] Decoded {len(frame_data)} byte frame.")
            pass
        elif frame_data is not None:
            # print(f"[MEDIA] Invalid frame size: {len(frame_data)}")
            pass
