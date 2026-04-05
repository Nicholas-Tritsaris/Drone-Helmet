import machine

class LockControl:
    def __init__(self, solenoid_pin):
        self.solenoid = machine.Pin(solenoid_pin, machine.Pin.OUT)
        self.solenoid.value(0) # Fail-open by default
        self.locked = False

    def engage(self):
        self.solenoid.value(1)
        self.locked = True

    def release(self):
        self.solenoid.value(0)
        self.locked = False

    def status(self):
        return self.locked
