# HEX Firmware Output
#
# The compiled HEX file is generated from the firmware source.
# To build and generate main.hex:
#
# 1. Install AVR toolchain:
#    sudo apt-get install gcc-avr avr-libc binutils-avr avrdude
#
# 2. Build the firmware:
#    cd /path/to/firmware/
#    make all
#
# 3. The HEX file will be generated at:
#    firmware/hex/main.hex
#
# 4. To flash to ATmega32 via USBasp:
#    make flash
#    (or: avrdude -c usbasp -p atmega32 -U flash:w:hex/main.hex:i)
#
# 5. Fuse bits for 8MHz external crystal:
#    Low fuse:  0xFF  (external crystal, no clock division)
#    High fuse: 0xD9  (JTAG disabled, SPI enabled, watchdog off)
#
# SimulIDE: Load main.hex into the ATmega32 component
#           by right-clicking → Properties → Load firmware
