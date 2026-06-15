# Gerber Files
#
# These Gerber manufacturing files are generated from KiCad PCB Editor.
# To generate:
#   1. Open ATmega32_Clock.kicad_pcb in KiCad PCB Editor
#   2. Go to File → Plot
#   3. Set output format: Gerber
#   4. Set output directory: ../gerber/
#   5. Select layers: F.Cu, B.Cu, F.SilkS, B.SilkS, F.Mask, B.Mask, Edge.Cuts
#   6. Click Plot
#   7. Click Generate Drill Files
#
# Or use kicad-cli (once installed):
#   kicad-cli pcb export gerbers --output ./gerber/ ATmega32_Clock.kicad_pcb
#
# Expected output files:
#   ATmega32_Clock-F_Cu.gbr         Front copper layer
#   ATmega32_Clock-B_Cu.gbr         Back copper layer
#   ATmega32_Clock-F_SilkS.gbr      Front silkscreen
#   ATmega32_Clock-B_SilkS.gbr      Back silkscreen
#   ATmega32_Clock-F_Mask.gbr       Front solder mask
#   ATmega32_Clock-B_Mask.gbr       Back solder mask
#   ATmega32_Clock-Edge_Cuts.gbr    Board outline
#   ATmega32_Clock.drl              Drill file
