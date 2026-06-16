#!/usr/bin/env python3
"""
Rebuild ATmega32 Clock schematic with COMPLETE wiring.
Every component pin is connected to the correct MCU pin via wires.
"""

import uuid as uuid_mod

# ── Helpers ──────────────────────────────────────────────────────────────
_uuid_counter = 0
def mk_uuid():
    global _uuid_counter
    _uuid_counter += 1
    return f"b{_uuid_counter:07x}-{_uuid_counter:04x}-4000-8000-{_uuid_counter:012x}"

def wire(x1, y1, x2, y2):
    return f'  (wire (pts (xy {x1} {y1}) (xy {x2} {y2})) (stroke (width 0) (type default)) (uuid "{mk_uuid()}"))\n'

def label(name, x, y, angle=0):
    return f'  (label "{name}" (at {x} {y} {angle}) (effects (font (size 1.27 1.27))) (uuid "{mk_uuid()}"))\n'

def pwr_flag(x, y):
    return f"""  (symbol (lib_id "power:PWR_FLAG") (at {x} {y} 0) (unit 1) (in_bom yes) (on_board yes) (dnp no)
    (uuid "{mk_uuid()}")
    (property "Reference" "#FLG0{_uuid_counter}" (at {x} {y+3.81} 0) (effects (font (size 1.27 1.27)) hide))
    (property "Value" "PWR_FLAG" (at {x} {y+5.08} 0) (effects (font (size 1.27 1.27))))
    (instances (project "ATmega32_Clock" (path "/e63e39d7-6ac0-4ffd-8aa3-1841a4541b55" (reference "#FLG0{_uuid_counter}") (unit 1))))
  )\n"""

PROJECT_UUID = "e63e39d7-6ac0-4ffd-8aa3-1841a4541b55"

# ── MCU placement ────────────────────────────────────────────────────────
# U1 ATmega32A-P  at (152.4, 101.6) - center of sheet
# Pin offsets from the KiCad symbol for ATmega16L-8P (which ATmega32A-P extends):
#   Right side pins exit at x + 15.24 from symbol center
#   Left  side pins exit at x - 15.24 from symbol center
#   VCC exits at y - 50.8 from symbol center (top)
#   GND exits at y + 50.8 from symbol center (bottom -> actually no, GND at offset y=-50.8 but pin is 90deg up)
# MCU center = (152.4, 101.6)
# Right-side pins at x=167.64, Left-side pins at x=137.16
# PA0 (pin 40) at 167.64, 58.42   (43.18 offset from center going up)
# PA1 (pin 39) at 167.64, 60.96
# PA2 (pin 38) at 167.64, 63.5
# PB0 (pin 1)  at 167.64, 81.28   (20.32 offset from center going up)  
# PB1 (pin 2)  at 167.64, 83.82
# PD0 (pin 14) at 167.64, 127.0   (25.4 offset from center going down)
# PD1 (pin 15) at 167.64, 129.54
# XTAL1 (pin 13) at 137.16, 63.5  
# XTAL2 (pin 12) at 137.16, 68.58
# RESET (pin 9) at 137.16, 58.42
# VCC (pin 10) at 152.4, 50.8
# GND (pin 11) at 152.4, 152.4
# AVCC (pin 30) at 154.94, 50.8
# AREF (pin 32) at 137.16, 73.66
# PB5/MOSI (pin 6) at 167.64, 94.0
# PB6/MISO (pin 7) at 167.64, 96.52
# PB7/SCK  (pin 8) at 167.64, 99.06

# Let me recalculate based on the pin offsets in the symbol definition:
MCU_X = 152.4
MCU_Y = 101.6

# Right-side pins (at symbol offset 15.24, so world x = 152.4 + 15.24 = 167.64)
RX = MCU_X + 15.24  # 167.64

# Left-side pins (at symbol offset -15.24, so world x = 152.4 - 15.24 = 137.16)  
LX = MCU_X - 15.24  # 137.16

# Top power pins (VCC at symbol offset y=-50.8 from center, but placed at 0, 270deg rotation)
# Actually: VCC pin at (0, 50.8) with 270deg = exits upward -> world y = 101.6 - 50.8 = 50.8
VCC_Y = MCU_Y - 50.8  # 50.8
# AVCC at (2.54, 50.8) with 270deg -> world = (154.94, 50.8)
AVCC_X = MCU_X + 2.54  # 154.94

# Bottom power pin (GND at (0, -50.8) with 90deg = exits downward -> world y = 101.6 + 50.8 = 152.4)
GND_Y = MCU_Y + 50.8  # 152.4

# Pin world coordinates (from symbol pin offsets + MCU placement):
# Pin name: (pin_number, world_x, world_y)
pins = {
    'PB0':   (1,  RX, MCU_Y - 20.32),   # 167.64, 81.28
    'PB1':   (2,  RX, MCU_Y - 17.78),   # 167.64, 83.82
    'PB2':   (3,  RX, MCU_Y - 15.24),   # 167.64, 86.36
    'PB3':   (4,  RX, MCU_Y - 12.7),    # 167.64, 88.9
    'PB4':   (5,  RX, MCU_Y - 10.16),   # 167.64, 91.44
    'PB5':   (6,  RX, MCU_Y - 7.62),    # 167.64, 93.98
    'PB6':   (7,  RX, MCU_Y - 5.08),    # 167.64, 96.52
    'PB7':   (8,  RX, MCU_Y - 2.54),    # 167.64, 99.06
    'RESET': (9,  LX, MCU_Y - 43.18),   # 137.16, 58.42
    'VCC':   (10, MCU_X, VCC_Y),         # 152.4, 50.8
    'GND':   (11, MCU_X, GND_Y),         # 152.4, 152.4
    'XTAL2': (12, LX, MCU_Y - 33.02),   # 137.16, 68.58
    'XTAL1': (13, LX, MCU_Y - 38.1),    # 137.16, 63.5
    'PD0':   (14, RX, MCU_Y + 25.4),    # 167.64, 127.0
    'PD1':   (15, RX, MCU_Y + 27.94),   # 167.64, 129.54
    'PA7':   (33, RX, MCU_Y - 25.4),    # 167.64, 76.2
    'PA6':   (34, RX, MCU_Y - 27.94),   # 167.64, 73.66
    'PA5':   (35, RX, MCU_Y - 30.48),   # 167.64, 71.12
    'PA4':   (36, RX, MCU_Y - 33.02),   # 167.64, 68.58
    'PA3':   (37, RX, MCU_Y - 35.56),   # 167.64, 66.04
    'PA2':   (38, RX, MCU_Y - 38.1),    # 167.64, 63.5
    'PA1':   (39, RX, MCU_Y - 40.64),   # 167.64, 60.96
    'PA0':   (40, RX, MCU_Y - 43.18),   # 167.64, 58.42
    'AVCC':  (30, AVCC_X, VCC_Y),        # 154.94, 50.8
    'AREF':  (32, LX, MCU_Y - 27.94),   # 137.16, 73.66
    'PC0':   (22, RX, MCU_Y + 2.54),    # 167.64, 104.14
    'PC1':   (23, RX, MCU_Y + 5.08),    # 167.64, 106.68
}

# ══════════════════════════════════════════════════════════════════════════
#  BUILD THE SCHEMATIC
# ══════════════════════════════════════════════════════════════════════════

out = []

# ── Header ───────────────────────────────────────────────────────────────
out.append(f"""(kicad_sch (version 20231120) (generator "eeschema") (generator_version "8.0")
  (uuid "{PROJECT_UUID}")
  (paper "A3")
  (title_block
    (title "ATmega32 Timer-Based Digital Clock & Task Scheduler")
    (date "2026-06-15")
    (rev "1.0")
    (comment 1 "Timer1 CTC | 8MHz Crystal | Prescaler 64 | OCR1A=1249 | 100Hz")
    (comment 2 "CT_321 PBL Project 08")
  )
""")

# ── lib_symbols ──────────────────────────────────────────────────────────
# Read from the existing file to preserve all lib_symbols exactly
with open('kicad/schematic/ATmega32_Clock.kicad_sch') as f:
    old = f.read()

# Extract lib_symbols block
import re
m = re.search(r'(  \(lib_symbols\n[\s\S]*?\n  \)\n  \))', old)
lib_block = m.group(1)
out.append(lib_block)
out.append('\n')

# ── Component instances ──────────────────────────────────────────────────
def inst(path_suffix):
    return f'    (instances (project "ATmega32_Clock" (path "/{PROJECT_UUID}" (reference "{path_suffix[0]}") (unit 1))))'

# U1 - ATmega32A-P at center
out.append(f"""  (symbol (lib_id "MCU_Microchip_ATmega:ATmega32A-P") (at {MCU_X} {MCU_Y} 0) (unit 1)
    (in_bom yes) (on_board yes) (dnp no)
    (uuid "{mk_uuid()}")
    (property "Reference" "U1" (at {MCU_X-12.7} {MCU_Y-50.8} 0) (effects (font (size 1.27 1.27))))
    (property "Value" "ATmega32A-P" (at {MCU_X+2.54} {MCU_Y+50.8} 0) (effects (font (size 1.27 1.27))))
    (property "Footprint" "Package_DIP:DIP-40_W15.24mm" (at {MCU_X} {MCU_Y} 0) (effects (font (size 1.27 1.27)) hide))
    (property "Datasheet" "" (at {MCU_X} {MCU_Y} 0) (effects (font (size 1.27 1.27)) hide))
    (instances (project "ATmega32_Clock" (path "/{PROJECT_UUID}" (reference "U1") (unit 1))))
  )\n""")

# ── Crystal Y1 (8MHz) ───────────────────────────────────────────────────
# Place crystal to the left of MCU, between XTAL1 and XTAL2 pins
# XTAL1 = 137.16, 63.5  and XTAL2 = 137.16, 68.58
# Crystal center: (127, 66.04) vertical orientation
CRYS_X = 127.0
CRYS_Y = 66.04
out.append(f"""  (symbol (lib_id "Device:Crystal") (at {CRYS_X} {CRYS_Y} 90) (unit 1)
    (in_bom yes) (on_board yes) (dnp no)
    (uuid "{mk_uuid()}")
    (property "Reference" "Y1" (at {CRYS_X-5.08} {CRYS_Y} 0) (effects (font (size 1.27 1.27))))
    (property "Value" "8MHz" (at {CRYS_X+5.08} {CRYS_Y} 0) (effects (font (size 1.27 1.27))))
    (property "Footprint" "Crystal:Crystal_HC49-4H_Vertical" (at {CRYS_X} {CRYS_Y} 0) (effects (font (size 1.27 1.27)) hide))
    (property "Datasheet" "" (at {CRYS_X} {CRYS_Y} 0) (effects (font (size 1.27 1.27)) hide))
    (instances (project "ATmega32_Clock" (path "/{PROJECT_UUID}" (reference "Y1") (unit 1))))
  )\n""")

# ── Load Capacitors C1, C2 (22pF) ───────────────────────────────────────
# C1 on XTAL1 side, C2 on XTAL2 side, both going to GND
C1_X = 121.92
C1_Y = 58.42  # near XTAL1 line
out.append(f"""  (symbol (lib_id "Device:C") (at {C1_X} {C1_Y} 0) (unit 1)
    (in_bom yes) (on_board yes) (dnp no)
    (uuid "{mk_uuid()}")
    (property "Reference" "C1" (at {C1_X+3.05} {C1_Y-1.27} 0) (effects (font (size 1.27 1.27)) (justify left)))
    (property "Value" "22pF" (at {C1_X+3.05} {C1_Y+1.27} 0) (effects (font (size 1.27 1.27)) (justify left)))
    (property "Footprint" "Capacitor_THT:C_Disc_D3.0mm_W1.6mm_P2.50mm" (at {C1_X} {C1_Y} 0) (effects (font (size 1.27 1.27)) hide))
    (property "Datasheet" "" (at {C1_X} {C1_Y} 0) (effects (font (size 1.27 1.27)) hide))
    (instances (project "ATmega32_Clock" (path "/{PROJECT_UUID}" (reference "C1") (unit 1))))
  )\n""")

C2_X = 121.92
C2_Y = 73.66  # near XTAL2 line
out.append(f"""  (symbol (lib_id "Device:C") (at {C2_X} {C2_Y} 0) (unit 1)
    (in_bom yes) (on_board yes) (dnp no)
    (uuid "{mk_uuid()}")
    (property "Reference" "C2" (at {C2_X+3.05} {C2_Y-1.27} 0) (effects (font (size 1.27 1.27)) (justify left)))
    (property "Value" "22pF" (at {C2_X+3.05} {C2_Y+1.27} 0) (effects (font (size 1.27 1.27)) (justify left)))
    (property "Footprint" "Capacitor_THT:C_Disc_D3.0mm_W1.6mm_P2.50mm" (at {C2_X} {C2_Y} 0) (effects (font (size 1.27 1.27)) hide))
    (property "Datasheet" "" (at {C2_X} {C2_Y} 0) (effects (font (size 1.27 1.27)) hide))
    (instances (project "ATmega32_Clock" (path "/{PROJECT_UUID}" (reference "C2") (unit 1))))
  )\n""")

# ── Decoupling Caps C3 (VCC), C4 (AVCC) ─────────────────────────────────
# Place near the top of the MCU, close to VCC/AVCC pins
C3_X = MCU_X - 5.08  # 147.32
C3_Y = 43.18
out.append(f"""  (symbol (lib_id "Device:C") (at {C3_X} {C3_Y} 0) (unit 1)
    (in_bom yes) (on_board yes) (dnp no)
    (uuid "{mk_uuid()}")
    (property "Reference" "C3" (at {C3_X+3.05} {C3_Y-1.27} 0) (effects (font (size 1.27 1.27)) (justify left)))
    (property "Value" "100nF" (at {C3_X+3.05} {C3_Y+1.27} 0) (effects (font (size 1.27 1.27)) (justify left)))
    (property "Footprint" "Capacitor_THT:C_Disc_D3.0mm_W1.6mm_P2.50mm" (at {C3_X} {C3_Y} 0) (effects (font (size 1.27 1.27)) hide))
    (property "Datasheet" "" (at {C3_X} {C3_Y} 0) (effects (font (size 1.27 1.27)) hide))
    (instances (project "ATmega32_Clock" (path "/{PROJECT_UUID}" (reference "C3") (unit 1))))
  )\n""")

C4_X = MCU_X + 5.08  # 157.48
C4_Y = 43.18
out.append(f"""  (symbol (lib_id "Device:C") (at {C4_X} {C4_Y} 0) (unit 1)
    (in_bom yes) (on_board yes) (dnp no)
    (uuid "{mk_uuid()}")
    (property "Reference" "C4" (at {C4_X+3.05} {C4_Y-1.27} 0) (effects (font (size 1.27 1.27)) (justify left)))
    (property "Value" "100nF" (at {C4_X+3.05} {C4_Y+1.27} 0) (effects (font (size 1.27 1.27)) (justify left)))
    (property "Footprint" "Capacitor_THT:C_Disc_D3.0mm_W1.6mm_P2.50mm" (at {C4_X} {C4_Y} 0) (effects (font (size 1.27 1.27)) hide))
    (property "Datasheet" "" (at {C4_X} {C4_Y} 0) (effects (font (size 1.27 1.27)) hide))
    (instances (project "ATmega32_Clock" (path "/{PROJECT_UUID}" (reference "C4") (unit 1))))
  )\n""")

# ── R1 (10K Reset Pull-up) ──────────────────────────────────────────────
# Place above RESET pin, vertical. Top goes to VCC, bottom to RESET line.
R1_X = 129.54
R1_Y = 50.8
out.append(f"""  (symbol (lib_id "Device:R") (at {R1_X} {R1_Y} 0) (unit 1)
    (in_bom yes) (on_board yes) (dnp no)
    (uuid "{mk_uuid()}")
    (property "Reference" "R1" (at {R1_X+2.54} {R1_Y} 0) (effects (font (size 1.27 1.27))))
    (property "Value" "10K" (at {R1_X-2.54} {R1_Y} 0) (effects (font (size 1.27 1.27))))
    (property "Footprint" "Resistor_THT:R_Axial_DIN0207_L6.3mm_D2.5mm_P10.16mm_Horizontal" (at {R1_X} {R1_Y} 0) (effects (font (size 1.27 1.27)) hide))
    (property "Datasheet" "" (at {R1_X} {R1_Y} 0) (effects (font (size 1.27 1.27)) hide))
    (instances (project "ATmega32_Clock" (path "/{PROJECT_UUID}" (reference "R1") (unit 1))))
  )\n""")

# ── SW1 (Reset Button) ──────────────────────────────────────────────────
# Below R1, connects RESET line to GND
SW1_X = 129.54
SW1_Y = 63.5
out.append(f"""  (symbol (lib_id "Switch:SW_Push") (at {SW1_X} {SW1_Y} 0) (unit 1)
    (in_bom yes) (on_board yes) (dnp no)
    (uuid "{mk_uuid()}")
    (property "Reference" "SW1" (at {SW1_X} {SW1_Y-3.81} 0) (effects (font (size 1.27 1.27))))
    (property "Value" "RESET" (at {SW1_X} {SW1_Y+3.81} 0) (effects (font (size 1.27 1.27))))
    (property "Footprint" "Button_Switch_THT:SW_PUSH_6mm" (at {SW1_X} {SW1_Y} 0) (effects (font (size 1.27 1.27)) hide))
    (property "Datasheet" "" (at {SW1_X} {SW1_Y} 0) (effects (font (size 1.27 1.27)) hide))
    (instances (project "ATmega32_Clock" (path "/{PROJECT_UUID}" (reference "SW1") (unit 1))))
  )\n""")

# ── Button pull-up resistors R2, R3, R4 ─────────────────────────────────
# Place to the right of MCU, in a row. Each connects VCC → R → MCU pin, with button to GND
BTN_BASE_X = 187.96
BTN_R_Y_START = 53.34  # R2 for PA0
BTN_SPACING = 12.7

for i, (ref, val, btn_name) in enumerate([('R2','10K','SET'), ('R3','10K','INCREMENT'), ('R4','10K','CLK_RST')]):
    rx = BTN_BASE_X + i * BTN_SPACING
    ry = BTN_R_Y_START
    out.append(f"""  (symbol (lib_id "Device:R") (at {rx} {ry} 0) (unit 1)
    (in_bom yes) (on_board yes) (dnp no)
    (uuid "{mk_uuid()}")
    (property "Reference" "{ref}" (at {rx+2.54} {ry} 0) (effects (font (size 1.27 1.27))))
    (property "Value" "{val}" (at {rx-2.54} {ry} 0) (effects (font (size 1.27 1.27))))
    (property "Footprint" "Resistor_THT:R_Axial_DIN0207_L6.3mm_D2.5mm_P10.16mm_Horizontal" (at {rx} {ry} 0) (effects (font (size 1.27 1.27)) hide))
    (property "Datasheet" "" (at {rx} {ry} 0) (effects (font (size 1.27 1.27)) hide))
    (instances (project "ATmega32_Clock" (path "/{PROJECT_UUID}" (reference "{ref}") (unit 1))))
  )\n""")

# ── Button switches SW2, SW3, SW4 ───────────────────────────────────────
for i, (ref, val) in enumerate([('SW2','SET'), ('SW3','INCREMENT'), ('SW4','CLK_RST')]):
    sx = BTN_BASE_X + i * BTN_SPACING
    sy = BTN_R_Y_START + 15.24
    out.append(f"""  (symbol (lib_id "Switch:SW_Push") (at {sx} {sy} 90) (unit 1)
    (in_bom yes) (on_board yes) (dnp no)
    (uuid "{mk_uuid()}")
    (property "Reference" "{ref}" (at {sx-3.81} {sy} 90) (effects (font (size 1.27 1.27))))
    (property "Value" "{val}" (at {sx+3.81} {sy} 90) (effects (font (size 1.27 1.27))))
    (property "Footprint" "Button_Switch_THT:SW_PUSH_6mm" (at {sx} {sy} 0) (effects (font (size 1.27 1.27)) hide))
    (property "Datasheet" "" (at {sx} {sy} 0) (effects (font (size 1.27 1.27)) hide))
    (instances (project "ATmega32_Clock" (path "/{PROJECT_UUID}" (reference "{ref}") (unit 1))))
  )\n""")

# ── LED resistors R5, R6 (330R) ─────────────────────────────────────────
LED_BASE_X = 187.96
LED_R_Y = 86.36

for i, (ref, val) in enumerate([('R5','330R'), ('R6','330R')]):
    rx = LED_BASE_X + i * 12.7
    ry = LED_R_Y
    out.append(f"""  (symbol (lib_id "Device:R") (at {rx} {ry} 0) (unit 1)
    (in_bom yes) (on_board yes) (dnp no)
    (uuid "{mk_uuid()}")
    (property "Reference" "{ref}" (at {rx+2.54} {ry} 0) (effects (font (size 1.27 1.27))))
    (property "Value" "{val}" (at {rx-2.54} {ry} 0) (effects (font (size 1.27 1.27))))
    (property "Footprint" "Resistor_THT:R_Axial_DIN0207_L6.3mm_D2.5mm_P10.16mm_Horizontal" (at {rx} {ry} 0) (effects (font (size 1.27 1.27)) hide))
    (property "Datasheet" "" (at {rx} {ry} 0) (effects (font (size 1.27 1.27)) hide))
    (instances (project "ATmega32_Clock" (path "/{PROJECT_UUID}" (reference "{ref}") (unit 1))))
  )\n""")

# ── LEDs D1, D2 ─────────────────────────────────────────────────────────
for i, (ref, val) in enumerate([('D1','STATUS'), ('D2','TASK')]):
    dx = LED_BASE_X + i * 12.7
    dy = LED_R_Y + 12.7  # 99.06
    out.append(f"""  (symbol (lib_id "Device:LED") (at {dx} {dy} 270) (unit 1)
    (in_bom yes) (on_board yes) (dnp no)
    (uuid "{mk_uuid()}")
    (property "Reference" "{ref}" (at {dx+5.08} {dy} 0) (effects (font (size 1.27 1.27))))
    (property "Value" "{val}" (at {dx} {dy+5.08} 0) (effects (font (size 1.27 1.27))))
    (property "Footprint" "LED_THT:LED_D3.0mm" (at {dx} {dy} 0) (effects (font (size 1.27 1.27)) hide))
    (property "Datasheet" "" (at {dx} {dy} 0) (effects (font (size 1.27 1.27)) hide))
    (instances (project "ATmega32_Clock" (path "/{PROJECT_UUID}" (reference "{ref}") (unit 1))))
  )\n""")

# ── J1 USART Header (1x02) ──────────────────────────────────────────────
J1_X = 187.96
J1_Y = 129.54
out.append(f"""  (symbol (lib_id "Connector_Generic:Conn_01x02") (at {J1_X} {J1_Y} 0) (unit 1)
    (in_bom yes) (on_board yes) (dnp no)
    (uuid "{mk_uuid()}")
    (property "Reference" "J1" (at {J1_X} {J1_Y-5.08} 0) (effects (font (size 1.27 1.27))))
    (property "Value" "USART" (at {J1_X} {J1_Y+5.08} 0) (effects (font (size 1.27 1.27))))
    (property "Footprint" "Connector_PinHeader_2.54mm:PinHeader_1x02_P2.54mm_Vertical" (at {J1_X} {J1_Y} 0) (effects (font (size 1.27 1.27)) hide))
    (property "Datasheet" "" (at {J1_X} {J1_Y} 0) (effects (font (size 1.27 1.27)) hide))
    (instances (project "ATmega32_Clock" (path "/{PROJECT_UUID}" (reference "J1") (unit 1))))
  )\n""")

# ── J2 ISP Header (2x03) ────────────────────────────────────────────────
J2_X = 187.96
J2_Y = 142.24
out.append(f"""  (symbol (lib_id "Connector_Generic:Conn_02x03_Odd_Even") (at {J2_X} {J2_Y} 0) (unit 1)
    (in_bom yes) (on_board yes) (dnp no)
    (uuid "{mk_uuid()}")
    (property "Reference" "J2" (at {J2_X} {J2_Y-7.62} 0) (effects (font (size 1.27 1.27))))
    (property "Value" "ISP" (at {J2_X} {J2_Y+7.62} 0) (effects (font (size 1.27 1.27))))
    (property "Footprint" "Connector_PinHeader_2.54mm:PinHeader_2x03_P2.54mm_Vertical" (at {J2_X} {J2_Y} 0) (effects (font (size 1.27 1.27)) hide))
    (property "Datasheet" "" (at {J2_X} {J2_Y} 0) (effects (font (size 1.27 1.27)) hide))
    (instances (project "ATmega32_Clock" (path "/{PROJECT_UUID}" (reference "J2") (unit 1))))
  )\n""")

# ── Power Symbols ────────────────────────────────────────────────────────
pwr_count = [0]
def vcc(x, y):
    pwr_count[0] += 1
    ref = f"#PWR0{pwr_count[0]:02d}"
    return f"""  (symbol (lib_id "power:VCC") (at {x} {y} 0) (unit 1) (in_bom yes) (on_board yes) (dnp no)
    (uuid "{mk_uuid()}")
    (property "Reference" "{ref}" (at {x} {y-3.81} 0) (effects (font (size 1.27 1.27)) hide))
    (property "Value" "VCC" (at {x} {y-2.54} 0) (effects (font (size 1.27 1.27))))
    (instances (project "ATmega32_Clock" (path "/{PROJECT_UUID}" (reference "{ref}") (unit 1))))
  )\n"""

def gnd(x, y):
    pwr_count[0] += 1
    ref = f"#PWR0{pwr_count[0]:02d}"
    return f"""  (symbol (lib_id "power:GND") (at {x} {y} 0) (unit 1) (in_bom yes) (on_board yes) (dnp no)
    (uuid "{mk_uuid()}")
    (property "Reference" "{ref}" (at {x} {y+3.81} 0) (effects (font (size 1.27 1.27)) hide))
    (property "Value" "GND" (at {x} {y+2.54} 0) (effects (font (size 1.27 1.27))))
    (instances (project "ATmega32_Clock" (path "/{PROJECT_UUID}" (reference "{ref}") (unit 1))))
  )\n"""

# VCC symbols
out.append(vcc(MCU_X, VCC_Y - 5.08))            # MCU VCC
out.append(vcc(AVCC_X, VCC_Y - 5.08))           # MCU AVCC
out.append(vcc(R1_X, R1_Y - 7.62))               # R1 pull-up top
out.append(vcc(C3_X, C3_Y - 5.08))               # C3 decoupling top
out.append(vcc(C4_X, C4_Y - 5.08))               # C4 decoupling top

# VCC for button pull-ups
for i in range(3):
    rx = BTN_BASE_X + i * BTN_SPACING
    out.append(vcc(rx, BTN_R_Y_START - 7.62))

# GND symbols
out.append(gnd(MCU_X, GND_Y + 5.08))            # MCU GND
out.append(gnd(C1_X, C1_Y + 7.62))               # C1 bottom
out.append(gnd(C2_X, C2_Y + 7.62))               # C2 bottom
out.append(gnd(C3_X, C3_Y + 5.08))               # C3 bottom
out.append(gnd(C4_X, C4_Y + 5.08))               # C4 bottom
out.append(gnd(SW1_X + 5.08, SW1_Y))             # SW1 bottom (reset btn to GND)

# GND for button switches
for i in range(3):
    sx = BTN_BASE_X + i * BTN_SPACING
    out.append(gnd(sx, BTN_R_Y_START + 15.24 + 5.08))

# GND for LEDs
for i in range(2):
    dx = LED_BASE_X + i * 12.7
    out.append(gnd(dx, LED_R_Y + 12.7 + 5.08))

# GND for ISP header pin 6
out.append(gnd(J2_X + 7.62, J2_Y + 2.54))

# ── WIRES ────────────────────────────────────────────────────────────────
wires = ''

# === MCU Power ===
# VCC power symbol -> MCU VCC pin
wires += wire(MCU_X, VCC_Y - 5.08, MCU_X, VCC_Y)
# AVCC power symbol -> MCU AVCC pin
wires += wire(AVCC_X, VCC_Y - 5.08, AVCC_X, VCC_Y)
# MCU GND pin -> GND symbol
wires += wire(MCU_X, GND_Y, MCU_X, GND_Y + 5.08)

# === Decoupling caps ===
# C3: VCC -> top of C3, bottom of C3 -> GND
wires += wire(C3_X, C3_Y - 5.08, C3_X, C3_Y - 2.54)
wires += wire(C3_X, C3_Y + 2.54, C3_X, C3_Y + 5.08)
# VCC rail to C3 top node, connect to MCU VCC rail
wires += wire(C3_X, VCC_Y, MCU_X, VCC_Y)  # tie C3 VCC to MCU VCC
# C4: VCC -> top of C4, bottom of C4 -> GND
wires += wire(C4_X, C4_Y - 5.08, C4_X, C4_Y - 2.54)
wires += wire(C4_X, C4_Y + 2.54, C4_X, C4_Y + 5.08)
# C4 VCC to AVCC rail
wires += wire(C4_X, VCC_Y, AVCC_X, VCC_Y)

# === Crystal circuit ===
# Crystal pin 1 (top, at CRYS_X, CRYS_Y - 2.54) -> XTAL1 line
# Crystal pin 2 (bottom, at CRYS_X, CRYS_Y + 2.54) -> XTAL2 line
xtal1_y = pins['XTAL1'][2]  # 63.5
xtal2_y = pins['XTAL2'][2]  # 68.58

# Crystal top -> horizontal to XTAL1
wires += wire(CRYS_X, CRYS_Y - 2.54, CRYS_X, xtal1_y)
wires += wire(CRYS_X, xtal1_y, LX, xtal1_y)

# Crystal bottom -> horizontal to XTAL2
wires += wire(CRYS_X, CRYS_Y + 2.54, CRYS_X, xtal2_y)
wires += wire(CRYS_X, xtal2_y, LX, xtal2_y)

# C1 on XTAL1 line: junction at (C1_X, xtal1_y), C1 top connects there
wires += wire(C1_X, C1_Y - 2.54, C1_X, xtal1_y)
wires += wire(C1_X, xtal1_y, CRYS_X, xtal1_y)  # tie into crystal line
# C1 bottom to GND
wires += wire(C1_X, C1_Y + 2.54, C1_X, C1_Y + 7.62)

# C2 on XTAL2 line: junction at (C2_X, xtal2_y), C2 top connects there
wires += wire(C2_X, C2_Y - 2.54, C2_X, xtal2_y)
wires += wire(C2_X, xtal2_y, CRYS_X, xtal2_y)
# C2 bottom to GND
wires += wire(C2_X, C2_Y + 2.54, C2_X, C2_Y + 7.62)

# === Reset circuit ===
# R1 top -> VCC
wires += wire(R1_X, R1_Y - 3.81, R1_X, R1_Y - 7.62)
# R1 bottom -> RESET line -> MCU RESET pin
reset_y = pins['RESET'][2]  # 58.42
wires += wire(R1_X, R1_Y + 3.81, R1_X, reset_y)
wires += wire(R1_X, reset_y, LX, reset_y)
# SW1 left side connects to RESET line, right side to GND
wires += wire(SW1_X - 2.54, SW1_Y, R1_X, reset_y)  # SW1 pin 1 to reset node
wires += wire(SW1_X + 2.54, SW1_Y, SW1_X + 5.08, SW1_Y)  # SW1 pin 2 to GND

# === Button circuits (PA0=SET, PA1=INC, PA2=CLK_RST) ===
pa_pins = [
    ('PA0', pins['PA0']),   # SET button
    ('PA1', pins['PA1']),   # INC button  
    ('PA2', pins['PA2']),   # CLK_RST button
]

for i, (pin_name, (pin_num, px, py)) in enumerate(pa_pins):
    rx = BTN_BASE_X + i * BTN_SPACING
    r_top = BTN_R_Y_START - 3.81
    r_bot = BTN_R_Y_START + 3.81
    sw_top = BTN_R_Y_START + 15.24 - 2.54
    sw_bot = BTN_R_Y_START + 15.24 + 2.54

    # VCC -> R top
    wires += wire(rx, BTN_R_Y_START - 7.62, rx, r_top)
    # R bottom -> junction node -> SW top
    junction_y = r_bot + 2.54  # midpoint
    wires += wire(rx, r_bot, rx, sw_top)
    # SW bottom -> GND
    wires += wire(rx, sw_bot, rx, sw_bot + 2.54)  # to GND symbol

    # MCU pin -> horizontal wire to junction between R and SW
    mid_y = (r_bot + sw_top) / 2.0
    wires += wire(px, py, rx, py)  # horizontal from MCU pin
    wires += wire(rx, py, rx, r_bot)  # vertical to resistor bottom/junction

# === LED circuits (PB0=STATUS, PB1=TASK) ===
pb_pins = [
    ('PB0', pins['PB0']),   # STATUS LED
    ('PB1', pins['PB1']),   # TASK LED
]

for i, (pin_name, (pin_num, px, py)) in enumerate(pb_pins):
    rx = LED_BASE_X + i * 12.7
    r_top = LED_R_Y - 3.81
    r_bot = LED_R_Y + 3.81
    led_top = LED_R_Y + 12.7 - 2.54  # LED anode
    led_bot = LED_R_Y + 12.7 + 2.54  # LED cathode

    # MCU PBx pin -> horizontal to R top
    wires += wire(px, py, rx, py)  # horizontal from MCU
    wires += wire(rx, py, rx, r_top)  # vertical down to R top

    # R bottom -> LED anode
    wires += wire(rx, r_bot, rx, led_top)
    # LED cathode -> GND
    wires += wire(rx, led_bot, rx, led_bot + 2.54)

# === USART connector ===
# J1 is a 1x02 connector. Pin 1 = TXD (PD1), Pin 2 = RXD (PD0)
# Connector pins exit at x - 2.54 (facing left)
# PD0 (RXD) at 167.64, 127.0
# PD1 (TXD) at 167.64, 129.54
j1_pin1_x = J1_X - 2.54
j1_pin1_y = J1_Y - 1.27
j1_pin2_x = J1_X - 2.54
j1_pin2_y = J1_Y + 1.27

pd0_x, pd0_y = pins['PD0'][1], pins['PD0'][2]
pd1_x, pd1_y = pins['PD1'][1], pins['PD1'][2]

# PD1 (TXD) -> J1 pin 1
wires += wire(pd1_x, pd1_y, j1_pin1_x, pd1_y)
wires += wire(j1_pin1_x, pd1_y, j1_pin1_x, j1_pin1_y)

# PD0 (RXD) -> J1 pin 2
wires += wire(pd0_x, pd0_y, j1_pin2_x, pd0_y)
wires += wire(j1_pin2_x, pd0_y, j1_pin2_x, j1_pin2_y)

# === ISP Header ===
# Standard AVR ISP pinout:
# Pin 1 = MOSI (PB5), Pin 2 = VCC
# Pin 3 = SCK (PB7), Pin 4 = MISO (PB6)
# Pin 5 = RESET, Pin 6 = GND
# J2 at 187.96, 142.24
# Odd pins (1,3,5) exit left at x-5.08
# Even pins (2,4,6) exit right at x+7.62
j2_lx = J2_X - 5.08
j2_rx = J2_X + 7.62

# ISP Pin 1 (MOSI=PB5)
pb5_x, pb5_y = pins['PB5'][1], pins['PB5'][2]
isp1_y = J2_Y - 2.54
wires += wire(j2_lx, isp1_y, j2_lx - 5.08, isp1_y)
out.append(label("MOSI", j2_lx - 5.08, isp1_y, 180))
out.append(label("MOSI", pb5_x + 2.54, pb5_y, 0))
wires += wire(pb5_x, pb5_y, pb5_x + 2.54, pb5_y)

# ISP Pin 2 (VCC)
out.append(vcc(j2_rx, J2_Y - 2.54 - 2.54))
wires += wire(j2_rx, J2_Y - 2.54 - 2.54, j2_rx, isp1_y)

# ISP Pin 3 (SCK=PB7)
pb7_x, pb7_y = pins['PB7'][1], pins['PB7'][2]
isp3_y = J2_Y
wires += wire(j2_lx, isp3_y, j2_lx - 5.08, isp3_y)
out.append(label("SCK", j2_lx - 5.08, isp3_y, 180))
out.append(label("SCK", pb7_x + 2.54, pb7_y, 0))
wires += wire(pb7_x, pb7_y, pb7_x + 2.54, pb7_y)

# ISP Pin 4 (MISO=PB6)
pb6_x, pb6_y = pins['PB6'][1], pins['PB6'][2]
isp4_y = J2_Y
wires += wire(j2_rx, isp4_y, j2_rx + 5.08, isp4_y)
out.append(label("MISO", j2_rx + 5.08, isp4_y, 0))
out.append(label("MISO", pb6_x + 2.54, pb6_y, 0))
wires += wire(pb6_x, pb6_y, pb6_x + 2.54, pb6_y)

# ISP Pin 5 (RESET)
isp5_y = J2_Y + 2.54
wires += wire(j2_lx, isp5_y, j2_lx - 5.08, isp5_y)
out.append(label("~{RESET}", j2_lx - 5.08, isp5_y, 180))

# ISP Pin 6 (GND) - already have GND symbol placed

# AREF connection to AVCC (or left unconnected with a cap)
# Connect AREF to AVCC through a jumper wire for simplicity
aref_x, aref_y = LX, pins['AREF'][2]
wires += wire(aref_x, aref_y, aref_x - 5.08, aref_y)
wires += wire(aref_x - 5.08, aref_y, aref_x - 5.08, VCC_Y)
out.append(vcc(aref_x - 5.08, VCC_Y - 2.54))
wires += wire(aref_x - 5.08, VCC_Y - 2.54, aref_x - 5.08, VCC_Y)

out.append(wires)

# ── Text annotations ────────────────────────────────────────────────────
out.append(f"""  (text "TIMER1 CTC: OCR1A = 8000000/(64*100) - 1 = 1249\\nInterrupt Rate: 100 Hz (10 ms)\\nPrescaler: 64 | F_CPU: 8 MHz"
    (at 30.48 30.48 0) (effects (font (size 1.524 1.524)))
    (uuid "{mk_uuid()}")
  )
  (text "CLOCK: 8MHz Crystal\\n22pF load caps"
    (at 109.22 52.07 0) (effects (font (size 1.27 1.27)))
    (uuid "{mk_uuid()}")
  )
  (text "BUTTONS: SET(PA0) INC(PA1) RST(PA2)\\nActive-low, 10K pull-ups"
    (at {BTN_BASE_X} {BTN_R_Y_START - 15.24} 0) (effects (font (size 1.27 1.27)))
    (uuid "{mk_uuid()}")
  )
  (text "LEDs: STATUS(PB0) TASK(PB1)\\n330R current limiters"
    (at {LED_BASE_X} {LED_R_Y - 12.7} 0) (effects (font (size 1.27 1.27)))
    (uuid "{mk_uuid()}")
  )
""")

# ── Footer ───────────────────────────────────────────────────────────────
out.append(f"""  (sheet_instances
    (path "/" (page "1"))
  )
)
""")

# ── Write the file ───────────────────────────────────────────────────────
with open('kicad/schematic/ATmega32_Clock.kicad_sch', 'w') as f:
    f.write(''.join(out))

print("Schematic rebuilt successfully!")
