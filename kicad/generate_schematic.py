#!/usr/bin/env python3
"""
Generate a valid KiCad 7 schematic for ATmega32 Digital Clock project.
Extracts real symbol definitions from installed KiCad libraries to ensure
the schematic is parseable by kicad-cli.
"""
import os, sys

PROJ = "/home/devagent/Desktop/microproj2"
SYM_DIR = "/usr/share/kicad/symbols"
OUT = os.path.join(PROJ, "kicad/schematic/ATmega32_Clock.kicad_sch")

def extract_symbol(filepath, name):
    """Extract a top-level symbol block from a .kicad_sym file."""
    with open(filepath, 'r') as f:
        content = f.read()
    target = f'  (symbol "{name}"'
    start = content.find(target)
    if start == -1:
        return None
    depth = 0
    for i in range(start, len(content)):
        if content[i] == '(':
            depth += 1
        elif content[i] == ')':
            depth -= 1
            if depth == 0:
                return content[start:i+1]
    return None

# Extract all needed symbols from installed KiCad 7 libraries
symbols = {}

# ATmega32A-P extends ATmega16L-8P - need both
base = extract_symbol(f"{SYM_DIR}/MCU_Microchip_ATmega.kicad_sym", "ATmega16L-8P")
ext = extract_symbol(f"{SYM_DIR}/MCU_Microchip_ATmega.kicad_sym", "ATmega32A-P")
if base and ext:
    # Prefix with library name for schematic lib_symbols
    symbols["MCU"] = base.replace('(symbol "ATmega16L-8P"', 
                                   '(symbol "MCU_Microchip_ATmega:ATmega16L-8P"', 1)
    symbols["MCU_EXT"] = ext.replace('(symbol "ATmega32A-P"',
                                      '(symbol "MCU_Microchip_ATmega:ATmega32A-P"', 1)
    # Fix the extends reference too
    symbols["MCU_EXT"] = symbols["MCU_EXT"].replace(
        '(extends "ATmega16L-8P")',
        '(extends "MCU_Microchip_ATmega:ATmega16L-8P")')
    print(f"  ATmega32A-P: OK ({len(base)+len(ext)} chars)")
else:
    print("ERROR: Could not extract ATmega symbols"); sys.exit(1)

# Simple components from Device library
for name in ["R", "C", "LED", "Crystal"]:
    s = extract_symbol(f"{SYM_DIR}/Device.kicad_sym", name)
    if s:
        symbols[name] = s.replace(f'(symbol "{name}"', f'(symbol "Device:{name}"', 1)
        # Fix sub-symbol references
        symbols[name] = symbols[name].replace(f'(symbol "{name}_', f'(symbol "Device:{name}_')
        print(f"  Device:{name}: OK")
    else:
        print(f"WARNING: Could not extract Device:{name}")

# SW_Push from Switch library
s = extract_symbol(f"{SYM_DIR}/Switch.kicad_sym", "SW_Push")
if s:
    symbols["SW"] = s.replace('(symbol "SW_Push"', '(symbol "Switch:SW_Push"', 1)
    symbols["SW"] = symbols["SW"].replace('(symbol "SW_Push_', '(symbol "Switch:SW_Push_')
    print(f"  Switch:SW_Push: OK")

# Connectors
for name in ["Conn_01x02", "Conn_02x03_Odd_Even"]:
    s = extract_symbol(f"{SYM_DIR}/Connector_Generic.kicad_sym", name)
    if s:
        symbols[name] = s.replace(f'(symbol "{name}"', f'(symbol "Connector_Generic:{name}"', 1)
        symbols[name] = symbols[name].replace(f'(symbol "{name}_', f'(symbol "Connector_Generic:{name}_')
        print(f"  Connector_Generic:{name}: OK")

# Power symbols
for name in ["VCC", "GND"]:
    s = extract_symbol(f"{SYM_DIR}/power.kicad_sym", name)
    if s:
        symbols[name] = s.replace(f'(symbol "{name}"', f'(symbol "power:{name}"', 1)
        symbols[name] = symbols[name].replace(f'(symbol "{name}_', f'(symbol "power:{name}_')
        print(f"  power:{name}: OK")

# Build the schematic
lib_syms = "\n".join(["    " + symbols[k] for k in symbols])

sch = f'''(kicad_sch (version 20230121) (generator eeschema)

  (uuid "e63e39d7-6ac0-4ffd-8aa3-1841a4541b55")

  (paper "A3")
  (title_block
    (title "ATmega32 Timer-Based Digital Clock & Task Scheduler")
    (date "2026-06-15")
    (rev "1.0")
    (company "CT_321 PBL Project 08")
    (comment 1 "Timer1 CTC | 8MHz Crystal | Prescaler 1024 | OCR1A=7812 | 1Hz Interrupt")
    (comment 2 "Status LED: PB0 toggles 2s | Task LED: PB1 flashes 5s | USART 9600")
  )

  (lib_symbols
{lib_syms}
  )

  ;; ============= ATmega32 MCU (U1) - Center =============
  (symbol (lib_id "MCU_Microchip_ATmega:ATmega32A-P") (at 152.4 101.6 0) (unit 1)
    (in_bom yes) (on_board yes) (dnp no)
    (uuid "a0000001-0001-4000-8000-000000000001")
    (property "Reference" "U1" (at 139.7 50.8 0) (effects (font (size 1.27 1.27))))
    (property "Value" "ATmega32A-P" (at 154.94 152.4 0) (effects (font (size 1.27 1.27))))
    (property "Footprint" "Package_DIP:DIP-40_W15.24mm" (at 152.4 101.6 0) (effects (font (size 1.27 1.27)) hide))
    (property "Datasheet" "" (at 152.4 101.6 0) (effects (font (size 1.27 1.27)) hide))
    (instances (project "ATmega32_Clock" (path "/e63e39d7-6ac0-4ffd-8aa3-1841a4541b55" (reference "U1") (unit 1))))
  )

  ;; ============= Crystal Y1 (8MHz) =============
  (symbol (lib_id "Device:Crystal") (at 115.57 78.74 90) (unit 1)
    (in_bom yes) (on_board yes) (dnp no)
    (uuid "a0000002-0002-4000-8000-000000000002")
    (property "Reference" "Y1" (at 110.49 78.74 0) (effects (font (size 1.27 1.27))))
    (property "Value" "8MHz" (at 120.65 78.74 0) (effects (font (size 1.27 1.27))))
    (property "Footprint" "Crystal:Crystal_HC49-4H_Vertical" (at 115.57 78.74 0) (effects (font (size 1.27 1.27)) hide))
    (property "Datasheet" "" (at 115.57 78.74 0) (effects (font (size 1.27 1.27)) hide))
    (instances (project "ATmega32_Clock" (path "/e63e39d7-6ac0-4ffd-8aa3-1841a4541b55" (reference "Y1") (unit 1))))
  )

  ;; ============= C1 22pF (XTAL1 load cap) =============
  (symbol (lib_id "Device:C") (at 107.95 88.9 0) (unit 1)
    (in_bom yes) (on_board yes) (dnp no)
    (uuid "a0000003-0003-4000-8000-000000000003")
    (property "Reference" "C1" (at 111 88.9 0) (effects (font (size 1.27 1.27)) (justify left)))
    (property "Value" "22pF" (at 111 91.44 0) (effects (font (size 1.27 1.27)) (justify left)))
    (property "Footprint" "Capacitor_THT:C_Disc_D3.0mm_W1.6mm_P2.50mm" (at 107.95 88.9 0) (effects (font (size 1.27 1.27)) hide))
    (property "Datasheet" "" (at 107.95 88.9 0) (effects (font (size 1.27 1.27)) hide))
    (instances (project "ATmega32_Clock" (path "/e63e39d7-6ac0-4ffd-8aa3-1841a4541b55" (reference "C1") (unit 1))))
  )

  ;; ============= C2 22pF (XTAL2 load cap) =============
  (symbol (lib_id "Device:C") (at 123.19 88.9 0) (unit 1)
    (in_bom yes) (on_board yes) (dnp no)
    (uuid "a0000004-0004-4000-8000-000000000004")
    (property "Reference" "C2" (at 126.24 88.9 0) (effects (font (size 1.27 1.27)) (justify left)))
    (property "Value" "22pF" (at 126.24 91.44 0) (effects (font (size 1.27 1.27)) (justify left)))
    (property "Footprint" "Capacitor_THT:C_Disc_D3.0mm_W1.6mm_P2.50mm" (at 123.19 88.9 0) (effects (font (size 1.27 1.27)) hide))
    (property "Datasheet" "" (at 123.19 88.9 0) (effects (font (size 1.27 1.27)) hide))
    (instances (project "ATmega32_Clock" (path "/e63e39d7-6ac0-4ffd-8aa3-1841a4541b55" (reference "C2") (unit 1))))
  )

  ;; ============= C3 100nF (VCC decoupling) =============
  (symbol (lib_id "Device:C") (at 157.48 48.26 0) (unit 1)
    (in_bom yes) (on_board yes) (dnp no)
    (uuid "a0000005-0005-4000-8000-000000000005")
    (property "Reference" "C3" (at 160.53 48.26 0) (effects (font (size 1.27 1.27)) (justify left)))
    (property "Value" "100nF" (at 160.53 50.8 0) (effects (font (size 1.27 1.27)) (justify left)))
    (property "Footprint" "Capacitor_THT:C_Disc_D3.0mm_W1.6mm_P2.50mm" (at 157.48 48.26 0) (effects (font (size 1.27 1.27)) hide))
    (property "Datasheet" "" (at 157.48 48.26 0) (effects (font (size 1.27 1.27)) hide))
    (instances (project "ATmega32_Clock" (path "/e63e39d7-6ac0-4ffd-8aa3-1841a4541b55" (reference "C3") (unit 1))))
  )

  ;; ============= C4 100nF (AVCC decoupling) =============
  (symbol (lib_id "Device:C") (at 165.1 48.26 0) (unit 1)
    (in_bom yes) (on_board yes) (dnp no)
    (uuid "a0000006-0006-4000-8000-000000000006")
    (property "Reference" "C4" (at 168.15 48.26 0) (effects (font (size 1.27 1.27)) (justify left)))
    (property "Value" "100nF" (at 168.15 50.8 0) (effects (font (size 1.27 1.27)) (justify left)))
    (property "Footprint" "Capacitor_THT:C_Disc_D3.0mm_W1.6mm_P2.50mm" (at 165.1 48.26 0) (effects (font (size 1.27 1.27)) hide))
    (property "Datasheet" "" (at 165.1 48.26 0) (effects (font (size 1.27 1.27)) hide))
    (instances (project "ATmega32_Clock" (path "/e63e39d7-6ac0-4ffd-8aa3-1841a4541b55" (reference "C4") (unit 1))))
  )

  ;; ============= R1 10K (RESET pull-up) =============
  (symbol (lib_id "Device:R") (at 121.92 55.88 0) (unit 1)
    (in_bom yes) (on_board yes) (dnp no)
    (uuid "a0000007-0007-4000-8000-000000000007")
    (property "Reference" "R1" (at 123.95 55.88 0) (effects (font (size 1.27 1.27))))
    (property "Value" "10K" (at 119.89 55.88 0) (effects (font (size 1.27 1.27))))
    (property "Footprint" "Resistor_THT:R_Axial_DIN0207_L6.3mm_D2.5mm_P10.16mm_Horizontal" (at 121.92 55.88 0) (effects (font (size 1.27 1.27)) hide))
    (property "Datasheet" "" (at 121.92 55.88 0) (effects (font (size 1.27 1.27)) hide))
    (instances (project "ATmega32_Clock" (path "/e63e39d7-6ac0-4ffd-8aa3-1841a4541b55" (reference "R1") (unit 1))))
  )

  ;; ============= SW1 RESET button =============
  (symbol (lib_id "Switch:SW_Push") (at 121.92 68.58 90) (unit 1)
    (in_bom yes) (on_board yes) (dnp no)
    (uuid "a0000008-0008-4000-8000-000000000008")
    (property "Reference" "SW1" (at 118.11 68.58 90) (effects (font (size 1.27 1.27))))
    (property "Value" "RESET" (at 125.73 68.58 90) (effects (font (size 1.27 1.27))))
    (property "Footprint" "Button_Switch_THT:SW_PUSH_6mm" (at 121.92 68.58 0) (effects (font (size 1.27 1.27)) hide))
    (property "Datasheet" "" (at 121.92 68.58 0) (effects (font (size 1.27 1.27)) hide))
    (instances (project "ATmega32_Clock" (path "/e63e39d7-6ac0-4ffd-8aa3-1841a4541b55" (reference "SW1") (unit 1))))
  )

  ;; ============= R2-R4 Button pull-ups =============
  (symbol (lib_id "Device:R") (at 195.58 121.92 0) (unit 1)
    (in_bom yes) (on_board yes) (dnp no)
    (uuid "a0000009-0009-4000-8000-000000000009")
    (property "Reference" "R2" (at 197.61 121.92 0) (effects (font (size 1.27 1.27))))
    (property "Value" "10K" (at 193.55 121.92 0) (effects (font (size 1.27 1.27))))
    (property "Footprint" "Resistor_THT:R_Axial_DIN0207_L6.3mm_D2.5mm_P10.16mm_Horizontal" (at 195.58 121.92 0) (effects (font (size 1.27 1.27)) hide))
    (property "Datasheet" "" (at 195.58 121.92 0) (effects (font (size 1.27 1.27)) hide))
    (instances (project "ATmega32_Clock" (path "/e63e39d7-6ac0-4ffd-8aa3-1841a4541b55" (reference "R2") (unit 1))))
  )
  (symbol (lib_id "Device:R") (at 208.28 121.92 0) (unit 1)
    (in_bom yes) (on_board yes) (dnp no)
    (uuid "a000000a-000a-4000-8000-00000000000a")
    (property "Reference" "R3" (at 210.31 121.92 0) (effects (font (size 1.27 1.27))))
    (property "Value" "10K" (at 206.25 121.92 0) (effects (font (size 1.27 1.27))))
    (property "Footprint" "Resistor_THT:R_Axial_DIN0207_L6.3mm_D2.5mm_P10.16mm_Horizontal" (at 208.28 121.92 0) (effects (font (size 1.27 1.27)) hide))
    (property "Datasheet" "" (at 208.28 121.92 0) (effects (font (size 1.27 1.27)) hide))
    (instances (project "ATmega32_Clock" (path "/e63e39d7-6ac0-4ffd-8aa3-1841a4541b55" (reference "R3") (unit 1))))
  )
  (symbol (lib_id "Device:R") (at 220.98 121.92 0) (unit 1)
    (in_bom yes) (on_board yes) (dnp no)
    (uuid "a000000b-000b-4000-8000-00000000000b")
    (property "Reference" "R4" (at 223.01 121.92 0) (effects (font (size 1.27 1.27))))
    (property "Value" "10K" (at 218.95 121.92 0) (effects (font (size 1.27 1.27))))
    (property "Footprint" "Resistor_THT:R_Axial_DIN0207_L6.3mm_D2.5mm_P10.16mm_Horizontal" (at 220.98 121.92 0) (effects (font (size 1.27 1.27)) hide))
    (property "Datasheet" "" (at 220.98 121.92 0) (effects (font (size 1.27 1.27)) hide))
    (instances (project "ATmega32_Clock" (path "/e63e39d7-6ac0-4ffd-8aa3-1841a4541b55" (reference "R4") (unit 1))))
  )

  ;; ============= SW2-SW4 User buttons =============
  (symbol (lib_id "Switch:SW_Push") (at 195.58 134.62 90) (unit 1)
    (in_bom yes) (on_board yes) (dnp no)
    (uuid "a000000c-000c-4000-8000-00000000000c")
    (property "Reference" "SW2" (at 191.77 134.62 90) (effects (font (size 1.27 1.27))))
    (property "Value" "SET" (at 199.39 134.62 90) (effects (font (size 1.27 1.27))))
    (property "Footprint" "Button_Switch_THT:SW_PUSH_6mm" (at 195.58 134.62 0) (effects (font (size 1.27 1.27)) hide))
    (property "Datasheet" "" (at 195.58 134.62 0) (effects (font (size 1.27 1.27)) hide))
    (instances (project "ATmega32_Clock" (path "/e63e39d7-6ac0-4ffd-8aa3-1841a4541b55" (reference "SW2") (unit 1))))
  )
  (symbol (lib_id "Switch:SW_Push") (at 208.28 134.62 90) (unit 1)
    (in_bom yes) (on_board yes) (dnp no)
    (uuid "a000000d-000d-4000-8000-00000000000d")
    (property "Reference" "SW3" (at 204.47 134.62 90) (effects (font (size 1.27 1.27))))
    (property "Value" "INCREMENT" (at 212.09 134.62 90) (effects (font (size 1.27 1.27))))
    (property "Footprint" "Button_Switch_THT:SW_PUSH_6mm" (at 208.28 134.62 0) (effects (font (size 1.27 1.27)) hide))
    (property "Datasheet" "" (at 208.28 134.62 0) (effects (font (size 1.27 1.27)) hide))
    (instances (project "ATmega32_Clock" (path "/e63e39d7-6ac0-4ffd-8aa3-1841a4541b55" (reference "SW3") (unit 1))))
  )
  (symbol (lib_id "Switch:SW_Push") (at 220.98 134.62 90) (unit 1)
    (in_bom yes) (on_board yes) (dnp no)
    (uuid "a000000e-000e-4000-8000-00000000000e")
    (property "Reference" "SW4" (at 217.17 134.62 90) (effects (font (size 1.27 1.27))))
    (property "Value" "CLK_RST" (at 224.79 134.62 90) (effects (font (size 1.27 1.27))))
    (property "Footprint" "Button_Switch_THT:SW_PUSH_6mm" (at 220.98 134.62 0) (effects (font (size 1.27 1.27)) hide))
    (property "Datasheet" "" (at 220.98 134.62 0) (effects (font (size 1.27 1.27)) hide))
    (instances (project "ATmega32_Clock" (path "/e63e39d7-6ac0-4ffd-8aa3-1841a4541b55" (reference "SW4") (unit 1))))
  )

  ;; ============= R5-R6 LED resistors =============
  (symbol (lib_id "Device:R") (at 195.58 76.2 0) (unit 1)
    (in_bom yes) (on_board yes) (dnp no)
    (uuid "a000000f-000f-4000-8000-00000000000f")
    (property "Reference" "R5" (at 197.61 76.2 0) (effects (font (size 1.27 1.27))))
    (property "Value" "330R" (at 193.55 76.2 0) (effects (font (size 1.27 1.27))))
    (property "Footprint" "Resistor_THT:R_Axial_DIN0207_L6.3mm_D2.5mm_P10.16mm_Horizontal" (at 195.58 76.2 0) (effects (font (size 1.27 1.27)) hide))
    (property "Datasheet" "" (at 195.58 76.2 0) (effects (font (size 1.27 1.27)) hide))
    (instances (project "ATmega32_Clock" (path "/e63e39d7-6ac0-4ffd-8aa3-1841a4541b55" (reference "R5") (unit 1))))
  )
  (symbol (lib_id "Device:R") (at 208.28 76.2 0) (unit 1)
    (in_bom yes) (on_board yes) (dnp no)
    (uuid "a0000010-0010-4000-8000-000000000010")
    (property "Reference" "R6" (at 210.31 76.2 0) (effects (font (size 1.27 1.27))))
    (property "Value" "330R" (at 206.25 76.2 0) (effects (font (size 1.27 1.27))))
    (property "Footprint" "Resistor_THT:R_Axial_DIN0207_L6.3mm_D2.5mm_P10.16mm_Horizontal" (at 208.28 76.2 0) (effects (font (size 1.27 1.27)) hide))
    (property "Datasheet" "" (at 208.28 76.2 0) (effects (font (size 1.27 1.27)) hide))
    (instances (project "ATmega32_Clock" (path "/e63e39d7-6ac0-4ffd-8aa3-1841a4541b55" (reference "R6") (unit 1))))
  )

  ;; ============= D1-D2 LEDs =============
  (symbol (lib_id "Device:LED") (at 195.58 88.9 270) (unit 1)
    (in_bom yes) (on_board yes) (dnp no)
    (uuid "a0000011-0011-4000-8000-000000000011")
    (property "Reference" "D1" (at 200.66 88.9 0) (effects (font (size 1.27 1.27))))
    (property "Value" "STATUS" (at 195.58 93.98 0) (effects (font (size 1.27 1.27))))
    (property "Footprint" "LED_THT:LED_D3.0mm" (at 195.58 88.9 0) (effects (font (size 1.27 1.27)) hide))
    (property "Datasheet" "" (at 195.58 88.9 0) (effects (font (size 1.27 1.27)) hide))
    (instances (project "ATmega32_Clock" (path "/e63e39d7-6ac0-4ffd-8aa3-1841a4541b55" (reference "D1") (unit 1))))
  )
  (symbol (lib_id "Device:LED") (at 208.28 88.9 270) (unit 1)
    (in_bom yes) (on_board yes) (dnp no)
    (uuid "a0000012-0012-4000-8000-000000000012")
    (property "Reference" "D2" (at 213.36 88.9 0) (effects (font (size 1.27 1.27))))
    (property "Value" "TASK" (at 208.28 93.98 0) (effects (font (size 1.27 1.27))))
    (property "Footprint" "LED_THT:LED_D3.0mm" (at 208.28 88.9 0) (effects (font (size 1.27 1.27)) hide))
    (property "Datasheet" "" (at 208.28 88.9 0) (effects (font (size 1.27 1.27)) hide))
    (instances (project "ATmega32_Clock" (path "/e63e39d7-6ac0-4ffd-8aa3-1841a4541b55" (reference "D2") (unit 1))))
  )

  ;; ============= J1 USART Header =============
  (symbol (lib_id "Connector_Generic:Conn_01x02") (at 107.95 114.3 180) (unit 1)
    (in_bom yes) (on_board yes) (dnp no)
    (uuid "a0000013-0013-4000-8000-000000000013")
    (property "Reference" "J1" (at 107.95 107.95 0) (effects (font (size 1.27 1.27))))
    (property "Value" "USART" (at 107.95 119.38 0) (effects (font (size 1.27 1.27))))
    (property "Footprint" "Connector_PinHeader_2.54mm:PinHeader_1x02_P2.54mm_Vertical" (at 107.95 114.3 0) (effects (font (size 1.27 1.27)) hide))
    (property "Datasheet" "" (at 107.95 114.3 0) (effects (font (size 1.27 1.27)) hide))
    (instances (project "ATmega32_Clock" (path "/e63e39d7-6ac0-4ffd-8aa3-1841a4541b55" (reference "J1") (unit 1))))
  )

  ;; ============= J2 ISP Header =============
  (symbol (lib_id "Connector_Generic:Conn_02x03_Odd_Even") (at 88.9 82.55 0) (unit 1)
    (in_bom yes) (on_board yes) (dnp no)
    (uuid "a0000014-0014-4000-8000-000000000014")
    (property "Reference" "J2" (at 88.9 74.93 0) (effects (font (size 1.27 1.27))))
    (property "Value" "ISP" (at 88.9 90.17 0) (effects (font (size 1.27 1.27))))
    (property "Footprint" "Connector_PinHeader_2.54mm:PinHeader_2x03_P2.54mm_Vertical" (at 88.9 82.55 0) (effects (font (size 1.27 1.27)) hide))
    (property "Datasheet" "" (at 88.9 82.55 0) (effects (font (size 1.27 1.27)) hide))
    (instances (project "ATmega32_Clock" (path "/e63e39d7-6ac0-4ffd-8aa3-1841a4541b55" (reference "J2") (unit 1))))
  )

  ;; ============= Power Symbols =============
  (symbol (lib_id "power:VCC") (at 152.4 38.1 0) (unit 1) (in_bom yes) (on_board yes) (dnp no)
    (uuid "a0000020-0020-4000-8000-000000000020")
    (property "Reference" "#PWR01" (at 152.4 41.91 0) (effects (font (size 1.27 1.27)) hide))
    (property "Value" "VCC" (at 152.4 34.29 0) (effects (font (size 1.27 1.27))))
    (instances (project "ATmega32_Clock" (path "/e63e39d7-6ac0-4ffd-8aa3-1841a4541b55" (reference "#PWR01") (unit 1))))
  )
  (symbol (lib_id "power:VCC") (at 121.92 48.26 0) (unit 1) (in_bom yes) (on_board yes) (dnp no)
    (uuid "a0000021-0021-4000-8000-000000000021")
    (property "Reference" "#PWR02" (at 121.92 52.07 0) (effects (font (size 1.27 1.27)) hide))
    (property "Value" "VCC" (at 121.92 44.45 0) (effects (font (size 1.27 1.27))))
    (instances (project "ATmega32_Clock" (path "/e63e39d7-6ac0-4ffd-8aa3-1841a4541b55" (reference "#PWR02") (unit 1))))
  )
  (symbol (lib_id "power:VCC") (at 195.58 114.3 0) (unit 1) (in_bom yes) (on_board yes) (dnp no)
    (uuid "a0000022-0022-4000-8000-000000000022")
    (property "Reference" "#PWR03" (at 195.58 118.11 0) (effects (font (size 1.27 1.27)) hide))
    (property "Value" "VCC" (at 195.58 110.49 0) (effects (font (size 1.27 1.27))))
    (instances (project "ATmega32_Clock" (path "/e63e39d7-6ac0-4ffd-8aa3-1841a4541b55" (reference "#PWR03") (unit 1))))
  )
  (symbol (lib_id "power:VCC") (at 208.28 114.3 0) (unit 1) (in_bom yes) (on_board yes) (dnp no)
    (uuid "a0000023-0023-4000-8000-000000000023")
    (property "Reference" "#PWR04" (at 208.28 118.11 0) (effects (font (size 1.27 1.27)) hide))
    (property "Value" "VCC" (at 208.28 110.49 0) (effects (font (size 1.27 1.27))))
    (instances (project "ATmega32_Clock" (path "/e63e39d7-6ac0-4ffd-8aa3-1841a4541b55" (reference "#PWR04") (unit 1))))
  )
  (symbol (lib_id "power:VCC") (at 220.98 114.3 0) (unit 1) (in_bom yes) (on_board yes) (dnp no)
    (uuid "a0000024-0024-4000-8000-000000000024")
    (property "Reference" "#PWR05" (at 220.98 118.11 0) (effects (font (size 1.27 1.27)) hide))
    (property "Value" "VCC" (at 220.98 110.49 0) (effects (font (size 1.27 1.27))))
    (instances (project "ATmega32_Clock" (path "/e63e39d7-6ac0-4ffd-8aa3-1841a4541b55" (reference "#PWR05") (unit 1))))
  )

  (symbol (lib_id "power:GND") (at 152.4 157.48 0) (unit 1) (in_bom yes) (on_board yes) (dnp no)
    (uuid "a0000030-0030-4000-8000-000000000030")
    (property "Reference" "#PWR06" (at 152.4 163.83 0) (effects (font (size 1.27 1.27)) hide))
    (property "Value" "GND" (at 152.4 161.29 0) (effects (font (size 1.27 1.27))))
    (instances (project "ATmega32_Clock" (path "/e63e39d7-6ac0-4ffd-8aa3-1841a4541b55" (reference "#PWR06") (unit 1))))
  )
  (symbol (lib_id "power:GND") (at 107.95 96.52 0) (unit 1) (in_bom yes) (on_board yes) (dnp no)
    (uuid "a0000031-0031-4000-8000-000000000031")
    (property "Reference" "#PWR07" (at 107.95 102.87 0) (effects (font (size 1.27 1.27)) hide))
    (property "Value" "GND" (at 107.95 100.33 0) (effects (font (size 1.27 1.27))))
    (instances (project "ATmega32_Clock" (path "/e63e39d7-6ac0-4ffd-8aa3-1841a4541b55" (reference "#PWR07") (unit 1))))
  )
  (symbol (lib_id "power:GND") (at 123.19 96.52 0) (unit 1) (in_bom yes) (on_board yes) (dnp no)
    (uuid "a0000032-0032-4000-8000-000000000032")
    (property "Reference" "#PWR08" (at 123.19 102.87 0) (effects (font (size 1.27 1.27)) hide))
    (property "Value" "GND" (at 123.19 100.33 0) (effects (font (size 1.27 1.27))))
    (instances (project "ATmega32_Clock" (path "/e63e39d7-6ac0-4ffd-8aa3-1841a4541b55" (reference "#PWR08") (unit 1))))
  )
  (symbol (lib_id "power:GND") (at 121.92 76.2 0) (unit 1) (in_bom yes) (on_board yes) (dnp no)
    (uuid "a0000033-0033-4000-8000-000000000033")
    (property "Reference" "#PWR09" (at 121.92 82.55 0) (effects (font (size 1.27 1.27)) hide))
    (property "Value" "GND" (at 121.92 80.01 0) (effects (font (size 1.27 1.27))))
    (instances (project "ATmega32_Clock" (path "/e63e39d7-6ac0-4ffd-8aa3-1841a4541b55" (reference "#PWR09") (unit 1))))
  )
  (symbol (lib_id "power:GND") (at 195.58 96.52 0) (unit 1) (in_bom yes) (on_board yes) (dnp no)
    (uuid "a0000034-0034-4000-8000-000000000034")
    (property "Reference" "#PWR010" (at 195.58 102.87 0) (effects (font (size 1.27 1.27)) hide))
    (property "Value" "GND" (at 195.58 100.33 0) (effects (font (size 1.27 1.27))))
    (instances (project "ATmega32_Clock" (path "/e63e39d7-6ac0-4ffd-8aa3-1841a4541b55" (reference "#PWR010") (unit 1))))
  )
  (symbol (lib_id "power:GND") (at 208.28 96.52 0) (unit 1) (in_bom yes) (on_board yes) (dnp no)
    (uuid "a0000035-0035-4000-8000-000000000035")
    (property "Reference" "#PWR011" (at 208.28 102.87 0) (effects (font (size 1.27 1.27)) hide))
    (property "Value" "GND" (at 208.28 100.33 0) (effects (font (size 1.27 1.27))))
    (instances (project "ATmega32_Clock" (path "/e63e39d7-6ac0-4ffd-8aa3-1841a4541b55" (reference "#PWR011") (unit 1))))
  )
  (symbol (lib_id "power:GND") (at 195.58 144.78 0) (unit 1) (in_bom yes) (on_board yes) (dnp no)
    (uuid "a0000036-0036-4000-8000-000000000036")
    (property "Reference" "#PWR012" (at 195.58 151.13 0) (effects (font (size 1.27 1.27)) hide))
    (property "Value" "GND" (at 195.58 148.59 0) (effects (font (size 1.27 1.27))))
    (instances (project "ATmega32_Clock" (path "/e63e39d7-6ac0-4ffd-8aa3-1841a4541b55" (reference "#PWR012") (unit 1))))
  )
  (symbol (lib_id "power:GND") (at 208.28 144.78 0) (unit 1) (in_bom yes) (on_board yes) (dnp no)
    (uuid "a0000037-0037-4000-8000-000000000037")
    (property "Reference" "#PWR013" (at 208.28 151.13 0) (effects (font (size 1.27 1.27)) hide))
    (property "Value" "GND" (at 208.28 148.59 0) (effects (font (size 1.27 1.27))))
    (instances (project "ATmega32_Clock" (path "/e63e39d7-6ac0-4ffd-8aa3-1841a4541b55" (reference "#PWR013") (unit 1))))
  )
  (symbol (lib_id "power:GND") (at 220.98 144.78 0) (unit 1) (in_bom yes) (on_board yes) (dnp no)
    (uuid "a0000038-0038-4000-8000-000000000038")
    (property "Reference" "#PWR014" (at 220.98 151.13 0) (effects (font (size 1.27 1.27)) hide))
    (property "Value" "GND" (at 220.98 148.59 0) (effects (font (size 1.27 1.27))))
    (instances (project "ATmega32_Clock" (path "/e63e39d7-6ac0-4ffd-8aa3-1841a4541b55" (reference "#PWR014") (unit 1))))
  )

  ;; ============= Net Labels =============
  (label "SET_BTN" (at 177.8 139.7 0) (effects (font (size 1.27 1.27))) (uuid "a0000040-0040-4000-8000-000000000040"))
  (label "INC_BTN" (at 177.8 137.16 0) (effects (font (size 1.27 1.27))) (uuid "a0000041-0041-4000-8000-000000000041"))
  (label "CLOCK_RESET" (at 177.8 134.62 0) (effects (font (size 1.27 1.27))) (uuid "a0000042-0042-4000-8000-000000000042"))
  (label "LED_STATUS" (at 177.8 78.74 0) (effects (font (size 1.27 1.27))) (uuid "a0000043-0043-4000-8000-000000000043"))
  (label "LED_TASK" (at 177.8 81.28 0) (effects (font (size 1.27 1.27))) (uuid "a0000044-0044-4000-8000-000000000044"))
  (label "USART_TXD" (at 119.38 113.03 0) (effects (font (size 1.27 1.27))) (uuid "a0000045-0045-4000-8000-000000000045"))
  (label "USART_RXD" (at 119.38 115.57 0) (effects (font (size 1.27 1.27))) (uuid "a0000046-0046-4000-8000-000000000046"))
  (label "MOSI" (at 81.28 85.09 0) (effects (font (size 1.27 1.27))) (uuid "a0000047-0047-4000-8000-000000000047"))
  (label "MISO" (at 97.79 82.55 0) (effects (font (size 1.27 1.27))) (uuid "a0000048-0048-4000-8000-000000000048"))
  (label "SCK" (at 81.28 82.55 0) (effects (font (size 1.27 1.27))) (uuid "a0000049-0049-4000-8000-000000000049"))

  ;; ============= Wires =============
  (wire (pts (xy 152.4 38.1) (xy 152.4 52.07)) (stroke (width 0) (type default)) (uuid "a0000050-0050-4000-8000-000000000050"))
  (wire (pts (xy 152.4 149.86) (xy 152.4 157.48)) (stroke (width 0) (type default)) (uuid "a0000051-0051-4000-8000-000000000051"))
  (wire (pts (xy 121.92 48.26) (xy 121.92 52.07)) (stroke (width 0) (type default)) (uuid "a0000052-0052-4000-8000-000000000052"))
  (wire (pts (xy 121.92 59.69) (xy 121.92 63.5)) (stroke (width 0) (type default)) (uuid "a0000053-0053-4000-8000-000000000053"))
  (wire (pts (xy 107.95 85.09) (xy 107.95 82.55)) (stroke (width 0) (type default)) (uuid "a0000054-0054-4000-8000-000000000054"))
  (wire (pts (xy 107.95 92.71) (xy 107.95 96.52)) (stroke (width 0) (type default)) (uuid "a0000055-0055-4000-8000-000000000055"))
  (wire (pts (xy 123.19 85.09) (xy 123.19 82.55)) (stroke (width 0) (type default)) (uuid "a0000056-0056-4000-8000-000000000056"))
  (wire (pts (xy 123.19 92.71) (xy 123.19 96.52)) (stroke (width 0) (type default)) (uuid "a0000057-0057-4000-8000-000000000057"))
  (wire (pts (xy 195.58 114.3) (xy 195.58 118.11)) (stroke (width 0) (type default)) (uuid "a0000058-0058-4000-8000-000000000058"))
  (wire (pts (xy 208.28 114.3) (xy 208.28 118.11)) (stroke (width 0) (type default)) (uuid "a0000059-0059-4000-8000-000000000059"))
  (wire (pts (xy 220.98 114.3) (xy 220.98 118.11)) (stroke (width 0) (type default)) (uuid "a000005a-005a-4000-8000-00000000005a"))
  (wire (pts (xy 195.58 125.73) (xy 195.58 129.54)) (stroke (width 0) (type default)) (uuid "a000005b-005b-4000-8000-00000000005b"))
  (wire (pts (xy 208.28 125.73) (xy 208.28 129.54)) (stroke (width 0) (type default)) (uuid "a000005c-005c-4000-8000-00000000005c"))
  (wire (pts (xy 220.98 125.73) (xy 220.98 129.54)) (stroke (width 0) (type default)) (uuid "a000005d-005d-4000-8000-00000000005d"))
  (wire (pts (xy 195.58 139.7) (xy 195.58 144.78)) (stroke (width 0) (type default)) (uuid "a000005e-005e-4000-8000-00000000005e"))
  (wire (pts (xy 208.28 139.7) (xy 208.28 144.78)) (stroke (width 0) (type default)) (uuid "a000005f-005f-4000-8000-00000000005f"))
  (wire (pts (xy 220.98 139.7) (xy 220.98 144.78)) (stroke (width 0) (type default)) (uuid "a0000060-0060-4000-8000-000000000060"))
  (wire (pts (xy 195.58 72.39) (xy 195.58 68.58)) (stroke (width 0) (type default)) (uuid "a0000061-0061-4000-8000-000000000061"))
  (wire (pts (xy 195.58 80.01) (xy 195.58 85.09)) (stroke (width 0) (type default)) (uuid "a0000062-0062-4000-8000-000000000062"))
  (wire (pts (xy 195.58 92.71) (xy 195.58 96.52)) (stroke (width 0) (type default)) (uuid "a0000063-0063-4000-8000-000000000063"))
  (wire (pts (xy 208.28 72.39) (xy 208.28 68.58)) (stroke (width 0) (type default)) (uuid "a0000064-0064-4000-8000-000000000064"))
  (wire (pts (xy 208.28 80.01) (xy 208.28 85.09)) (stroke (width 0) (type default)) (uuid "a0000065-0065-4000-8000-000000000065"))
  (wire (pts (xy 208.28 92.71) (xy 208.28 96.52)) (stroke (width 0) (type default)) (uuid "a0000066-0066-4000-8000-000000000066"))
  (wire (pts (xy 121.92 63.5) (xy 121.92 68.58)) (stroke (width 0) (type default)) (uuid "a0000067-0067-4000-8000-000000000067"))
  (wire (pts (xy 121.92 73.66) (xy 121.92 76.2)) (stroke (width 0) (type default)) (uuid "a0000068-0068-4000-8000-000000000068"))

  ;; ============= Text annotations =============
  (text "TIMER1 CTC: OCR1A = 8000000/(1024*1) - 1 = 7812\\nInterrupt Rate: 1 Hz (1 second)\\nPrescaler: 1024 | F_CPU: 8 MHz"
    (at 30.48 44.45 0) (effects (font (size 1.524 1.524)))
    (uuid "a0000070-0070-4000-8000-000000000070")
  )
  (text "CLOCK: 8MHz Crystal\\n22pF load caps"
    (at 99.06 68.58 0) (effects (font (size 1.27 1.27)))
    (uuid "a0000071-0071-4000-8000-000000000071")
  )
  (text "BUTTONS: SET(PA0) INC(PA1) RST(PA2)\\nActive-low, 10K pull-ups"
    (at 182.88 107.95 0) (effects (font (size 1.27 1.27)))
    (uuid "a0000072-0072-4000-8000-000000000072")
  )
  (text "LEDs: STATUS(PB0) TASK(PB1)\\n330R current limiters"
    (at 182.88 63.5 0) (effects (font (size 1.27 1.27)))
    (uuid "a0000073-0073-4000-8000-000000000073")
  )

  (sheet_instances
    (path "/" (page "1"))
  )
)
'''

with open(OUT, 'w') as f:
    f.write(sch)

print(f"\nSchematic written: {OUT}")
print(f"File size: {os.path.getsize(OUT)} bytes")
