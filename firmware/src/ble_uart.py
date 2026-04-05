import bluetooth
import time

class BLEUART:
    def __init__(self, name="KinkDrone-v2.1.0"):
        self.ble = bluetooth.BLE()
        self.ble.active(True)
        self.ble.irq(self._irq)
        self.name = name
        self.conn_handle = None

        # Simple BLE-UART profile (NRF51822 format)
        self.uuid_service = bluetooth.UUID("6E400001-B5A3-F393-E0A9-E50E24DCCA9E")
        self.uuid_rx = bluetooth.UUID("6E400002-B5A3-F393-E0A9-E50E24DCCA9E")
        self.uuid_tx = bluetooth.UUID("6E400003-B5A3-F393-E0A9-E50E24DCCA9E")

        services = (
            (self.uuid_service, ((self.uuid_rx, bluetooth.FLAG_WRITE), (self.uuid_tx, bluetooth.FLAG_NOTIFY))),
        )
        ((self.handle_rx, self.handle_tx),) = self.ble.gatts_register_services(services)

        self.advertising_payload = bytearray(b"\x02\x01\x06") + bytearray([len(name) + 1, 0x09]) + bytearray(name, "utf-8")
        self.advertise()
        self.rx_buffer = ""

    def _irq(self, event, data):
        if event == 1: # _IRQ_CENTRAL_CONNECT
            self.conn_handle, _, _ = data
            print(f"Connected: {self.conn_handle}")
        elif event == 2: # _IRQ_CENTRAL_DISCONNECT
            print(f"Disconnected: {self.conn_handle}")
            self.conn_handle = None
            self.advertise()
        elif event == 3: # _IRQ_GATTS_WRITE
            conn_handle, value_handle = data
            if conn_handle == self.conn_handle and value_handle == self.handle_rx:
                self.rx_buffer += self.ble.gatts_read(self.handle_rx).decode("utf-8")

    def advertise(self, interval_us=500000):
        self.ble.gap_advertise(interval_us, self.advertising_payload)

    def write(self, data):
        if self.conn_handle is not None:
            self.ble.gatts_notify(self.conn_handle, self.handle_tx, data)

    def read(self):
        result = self.rx_buffer
        self.rx_buffer = ""
        return result

    def is_connected(self):
        return self.conn_handle is not None
