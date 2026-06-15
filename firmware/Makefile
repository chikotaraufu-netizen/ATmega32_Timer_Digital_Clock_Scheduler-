###############################################################################
#  Makefile – ATmega32 Digital Clock & Task Scheduler
#
#  Build system for AVR-GCC.  Compiles all .c sources in src/ with headers
#  from include/, links them into an ELF, then generates Intel HEX for
#  flashing with avrdude.
#
#  Usage:
#    make            – build the HEX file
#    make flash      – build and flash via avrdude (USBasp programmer)
#    make clean      – remove all build artefacts
#    make size       – show memory usage (text/data/bss)
#
#  Adjust PROGRAMMER and PORT below to match your hardware programmer.
###############################################################################

# ---- Target MCU and clock ----
MCU        = atmega32
F_CPU      = 8000000UL

# ---- Toolchain ----
CC         = avr-gcc
OBJCOPY    = avr-objcopy
OBJDUMP    = avr-objdump
SIZE       = avr-size
AVRDUDE    = avrdude

# ---- Programmer (change to match your setup) ----
PROGRAMMER = usbasp
PORT       = usb

# ---- Project directories ----
SRCDIR     = src
INCDIR     = include
BUILDDIR   = build

# ---- Source and object files ----
SOURCES    = $(wildcard $(SRCDIR)/*.c)
OBJECTS    = $(patsubst $(SRCDIR)/%.c, $(BUILDDIR)/%.o, $(SOURCES))

# ---- Output files ----
TARGET     = $(BUILDDIR)/clock
ELF        = $(TARGET).elf
HEX        = $(TARGET).hex
MAP        = $(TARGET).map
LSS        = $(TARGET).lss

# ---- Compiler flags ----
#   -mmcu          : target MCU
#   -DF_CPU        : pass clock frequency to preprocessor
#   -Os            : optimise for size (important on 32 KB flash)
#   -std=gnu99     : use C99 with GNU extensions (for ATOMIC_BLOCK etc.)
#   -Wall -Wextra  : enable most warnings
#   -Wstrict-prototypes : enforce C prototype style
#   -funsigned-char     : default char is unsigned (AVR convention)
#   -funsigned-bitfields: default bitfield is unsigned
#   -fpack-struct       : pack structs tightly
#   -fshort-enums       : use smallest type for enums
CFLAGS     = -mmcu=$(MCU) \
             -DF_CPU=$(F_CPU) \
             -Os \
             -std=gnu99 \
             -Wall -Wextra -Wstrict-prototypes \
             -funsigned-char \
             -funsigned-bitfields \
             -fpack-struct \
             -fshort-enums \
             -I$(INCDIR) \
             -Wl,-Map,$(MAP)

# ---- Linker flags (passed through CFLAGS since we link with gcc) ----
LDFLAGS    = -mmcu=$(MCU)

###############################################################################
#  Build rules
###############################################################################

.PHONY: all flash clean size disasm

## Default target: build the HEX file
all: $(HEX) size

## Create the build directory if it doesn't exist
$(BUILDDIR):
	mkdir -p $(BUILDDIR)

## Compile .c → .o
$(BUILDDIR)/%.o: $(SRCDIR)/%.c | $(BUILDDIR)
	@echo "  CC    $<"
	$(CC) $(CFLAGS) -c $< -o $@

## Link .o → .elf
$(ELF): $(OBJECTS)
	@echo "  LINK  $@"
	$(CC) $(CFLAGS) $(OBJECTS) -o $@

## Convert .elf → .hex (Intel HEX format, flash section only)
$(HEX): $(ELF)
	@echo "  HEX   $@"
	$(OBJCOPY) -O ihex -R .eeprom $< $@

## Show memory usage
size: $(ELF)
	@echo ""
	@echo "  ---- Memory Usage ----"
	$(SIZE) --mcu=$(MCU) --format=avr $(ELF)

## Generate disassembly listing
disasm: $(ELF)
	$(OBJDUMP) -h -S $(ELF) > $(LSS)

## Flash the HEX to the MCU via avrdude
flash: $(HEX)
	$(AVRDUDE) -c $(PROGRAMMER) -p $(MCU) -P $(PORT) -U flash:w:$(HEX):i

## Clean all build artefacts
clean:
	rm -rf $(BUILDDIR)
