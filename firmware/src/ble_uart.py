import bluetooth
import struct
import time

class BLEUART:
    def __init__(self, name="BlueBoopYT-Drone-v0.1a"):
        self.ble = bluetooth.BLE()
        self.ble.active(True)
        self.ble.irq(self._irq)
        self.name = name
        self.conn_handle = None

        # --- GATT Service/Characteristic UUIDs (BlueBoopYT v0.1a spec) ---
        # 1. Lock Control Service
        self.svc_lock = bluetooth.UUID("BBBB1111-AAAA-BBBB-CCCC-DDDDEEEEFFFF")
        self.char_lock_state = (bluetooth.UUID("BBBB1112-AAAA-BBBB-CCCC-DDDDEEEEFFFF"), bluetooth.FLAG_READ | bluetooth.FLAG_NOTIFY)
        self.char_lock_threshold = (bluetooth.UUID("BBBB1113-AAAA-BBBB-CCCC-DDDDEEEEFFFF"), bluetooth.FLAG_READ | bluetooth.FLAG_WRITE)
        self.char_lock_emergency = (bluetooth.UUID("BBBB1114-AAAA-BBBB-CCCC-DDDDEEEEFFFF"), bluetooth.FLAG_WRITE)

        # 2. Media Stream Service
        self.svc_media = bluetooth.UUID("BBBB2222-AAAA-BBBB-CCCC-DDDDEEEEFFFF")
        self.char_media_frame = (bluetooth.UUID("BBBB2223-AAAA-BBBB-CCCC-DDDDEEEEFFFF"), bluetooth.FLAG_WRITE)
        self.char_media_fps = (bluetooth.UUID("BBBB2224-AAAA-BBBB-CCCC-DDDDEEEEFFFF"), bluetooth.FLAG_READ | bluetooth.FLAG_WRITE)

        # 3. Telemetry Service
        self.svc_telemetry = bluetooth.UUID("BBBB3333-AAAA-BBBB-CCCC-DDDDEEEEFFFF")
        self.char_tele_battery = (bluetooth.UUID("BBBB3334-AAAA-BBBB-CCCC-DDDDEEEEFFFF"), bluetooth.FLAG_READ | bluetooth.FLAG_NOTIFY)
        self.char_tele_temp = (bluetooth.UUID("BBBB3335-AAAA-BBBB-CCCC-DDDDEEEEFFFF"), bluetooth.FLAG_READ | bluetooth.FLAG_NOTIFY)
        self.char_tele_torque = (bluetooth.UUID("BBBB3336-AAAA-BBBB-CCCC-DDDDEEEEFFFF"), bluetooth.FLAG_READ | bluetooth.FLAG_NOTIFY)

        services = (
            (self.svc_lock, (self.char_lock_state, self.char_lock_threshold, self.char_lock_emergency)),
            (self.svc_media, (self.char_media_frame, self.char_media_fps)),
            (self.svc_telemetry, (self.char_tele_battery, self.char_tele_temp, self.char_tele_torque)),
        )

        ((self.h_lock_state, self.h_lock_thresh, self.h_lock_emerg),
         (self.h_media_frame, self.h_media_fps),
         (self.h_tele_batt, self.h_tele_temp, self.h_tele_torque)) = self.ble.gatts_register_services(services)

        self.advertising_payload = bytearray(b"\x02\x01\x06") + bytearray([len(name) + 1, 0x09]) + bytearray(name, "utf-8")
        self.advertise()

        # State
        self.lock_threshold = 2.20
        self.media_fps = 1
        self.new_frame = None
        self.emergency_cmd = False
        self.consent_given = False # Derived from threshold/state interaction

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
            if conn_handle == self.conn_handle:
                raw_val = self.ble.gatts_read(value_handle)
                if value_handle == self.h_lock_thresh:
                    self.lock_threshold = struct.unpack("<f", raw_val)[0]
                    self.consent_given = True # Writing to threshold confirms engagement intent
                elif value_handle == self.h_lock_emerg:
                    if struct.unpack("<H", raw_val)[0] == 0xDEAD:
                        self.emergency_cmd = True
                elif value_handle == self.h_media_frame:
                    self.new_frame = raw_val
                elif value_handle == self.h_media_fps:
                    self.media_fps = raw_val[0]

    def advertise(self, interval_us=500000):
        self.ble.gap_advertise(interval_us, self.advertising_payload)

    def update_telemetry(self, battery, temp, torque):
        if self.conn_handle is not None:
            self.ble.gatts_write(self.h_tele_batt, struct.pack("<f", battery))
            self.ble.gatts_notify(self.conn_handle, self.h_tele_batt)
            self.ble.gatts_write(self.h_tele_temp, struct.pack("<f", temp))
            self.ble.gatts_notify(self.conn_handle, self.h_tele_temp)
            self.ble.gatts_write(self.h_tele_torque, struct.pack("<f", torque))
            self.ble.gatts_notify(self.conn_handle, self.h_tele_torque)

    def update_lock_state(self, state):
        # uint8: 0x00=unlocked, 0x01=locked, 0x02=engaged, 0x03=emergency
        if self.conn_handle is not None:
            self.ble.gatts_write(self.h_lock_state, bytes([state]))
            self.ble.gatts_notify(self.conn_handle, self.h_lock_state)

    def is_connected(self):
        return self.conn_handle is not None
