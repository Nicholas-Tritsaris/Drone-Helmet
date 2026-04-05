# Makefile for Kink Drone v2.1.0 (ESP32 C Components)

CC = xtensa-esp32-elf-gcc
CFLAGS = -Wall -Werror -I.
TARGET = lock_control.o

all: $(TARGET)

$(TARGET): lock_control.c
	$(CC) $(CFLAGS) -c $< -o $@

clean:
	rm -f $(TARGET)

.PHONY: all clean

# Note: This C component is intended to be integrated as a MicroPython User Module.
# Refer to MicroPython documentation (Adding C modules) for full ESP-IDF integration.
# The current Python implementation (lock_control.py) provides a direct equivalent
# for standard MicroPython environments.
