import machine

# A minimal SHARP LS013B4DN02 driver for 1.3" 128x128 OLED via I2C
# This driver handles the 1bpp monochrome buffer and VCOM bit toggling
class Display:
    def __init__(self, i2c, addr=0x3C, width=128, height=128):
        self.i2c = i2c
        self.addr = addr
        self.width = width
        self.height = height
        # 128x128 monochrome = 16384 bits = 2048 bytes
        self.buffer = bytearray(self.width * self.height // 8)
        self.vcom = 0x40 # VCOM bit for SHARP memory LCDs
        self.init_display()

    def init_display(self):
        # Initialization for SHARP Memory LCD equivalent
        # Standard SSD1306-style command sequence for compatibility
        init_cmds = [
            0xAE, # DISPLAYOFF
            0xD5, 0x80, # SETDISPLAYCLOCKDIV
            0xA8, 0x7F, # SETMULTIPLEX
            0xD3, 0x00, # SETDISPLAYOFFSET
            0x40, # SETSTARTLINE
            0x8D, 0x14, # CHARGEPUMP
            0x20, 0x00, # MEMORYMODE
            0xA1, # SEGREMAP
            0xC8, # COMSCANDEC
            0xDA, 0x12, # SETCOMPINS
            0x81, 0xCF, # SETCONTRAST
            0xD9, 0xF1, # SETPRECHARGE
            0xDB, 0x40, # SETVCOMDETECT
            0xA4, # DISPLAYALLON_RESUME
            0xA6, # NORMALDISPLAY
            0xAF # DISPLAYON
        ]
        for cmd in init_cmds:
            self.i2c.writeto(self.addr, bytes([0x00, cmd]))

    def clear(self):
        # Zero out the monochrome buffer
        for i in range(len(self.buffer)):
            self.buffer[i] = 0x00

    def text(self, msg, x, y):
        # Basic character-to-buffer renderer for 8x8 font
        # Placeholder for real glyph logic; prints to console for serial debug
        print(f"[BLUEBOOP-OLED] {x},{y}: {msg}")

    def show(self):
        # Toggle VCOM to prevent DC bias buildup (SHARP spec)
        self.vcom ^= 0x40
        # Transmit 2048 byte buffer in 16 pages of 128 bytes (I2C block limits)
        for page in range(self.height // 8):
            # Set page/column addresses for SSD1306/SHARP controller
            self.i2c.writeto(self.addr, bytes([0x00, 0xB0 + page, 0x00, 0x10]))
            start = page * self.width
            self.i2c.writeto(self.addr, b'\x40' + self.buffer[start:start + self.width])
