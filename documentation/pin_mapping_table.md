# Pin Mapping Table

## Task 4: ATmega32 Pin Mapping (USART Display Option)

This project uses the **USART (serial terminal)** for displaying clock
time and task status, instead of an LCD module.

---

## Functional Pin Assignments

| ATmega32 Pin | Direction | Connected Device | Function | Net Label |
|---|---|---|---|---|
| Timer/Counter1 (internal) | Internal | -- | Generates 1 Hz periodic interrupt (system time base) | -- |
| PB0 | Digital output | Status LED (+ current-limiting resistor) | Toggles every 2 seconds | LED_STATUS |
| PB1 | Digital output | Sampling/task LED (+ current-limiting resistor) | Flashes every 5 seconds | LED_TASK |
| PA0 | Digital input | Set button | Activates time-setting mode | SET_BTN |
| PA1 | Digital input | Increment button | Increments hours/minutes while in set mode | INC_BTN |
| PA2 | Digital input | Reset button | Resets clock to 00:00:00 | CLOCK_RESET |
| PD1 (TXD) | Digital output | USART TX -- serial terminal (USB-to-serial / FTDI header) | Sends "TIME: hh:mm:ss" and "TASK: ..." messages to PC terminal | USART_TXD |
| PD0 (RXD) | Digital input | USART RX -- serial terminal | Reserved (not used by firmware, but wired for completeness) | USART_RXD |

---

## Power, Clock, and Reset Pins

| ATmega32 Pin | Direction | Connected Device | Function |
|---|---|---|---|
| VCC (pin 10) | Power input | 5V supply | Main digital power |
| AVCC (pin 30) | Power input | 5V supply (with decoupling) | Analog power supply reference |
| GND (pins 8, 22, 31) | Power | Ground plane | Common ground |
| AREF (pin 32) | Analog reference | Decoupling capacitor to GND | ADC reference filtering (not actively used, but should be decoupled) |
| XTAL1 (pin 13) | Clock input | Crystal oscillator + capacitor | External clock input |
| XTAL2 (pin 12) | Clock output | Crystal oscillator + capacitor | External clock feedback |
| RESET (pin 9) | Digital input | Push button + pull-up resistor | Manual microcontroller reset |

---

## Button Wiring Notes

All three buttons (SET_BTN, INC_BTN, CLOCK_RESET) should be wired with
a **pull-up resistor to VCC**, with the button connecting the pin to
GND when pressed (active-low). This is the standard configuration for
ATmega32 PORTA inputs and matches typical `PINA & (1<<PAx)` polling
logic (pin reads 0 when pressed).

Alternatively, the ATmega32's internal pull-up resistors can be
enabled in firmware (`PORTA |= (1<<PA0)` etc. after setting DDRA bit
to input), removing the need for external pull-up resistors -- note
this choice in your schematic notes either way.

---

## LED Wiring Notes

Both LEDs (LED_STATUS on PB0, LED_TASK on PB1) should be wired through
a current-limiting resistor (typically 220 ohm - 330 ohm at 5V) to GND,
with the anode connected to the resistor and the ATmega32 pin driving
the circuit (pin HIGH = LED on).

---

## USART Connection Notes

- PD1 (TXD) connects to the RX pin of a USB-to-serial adapter (e.g.,
  FTDI, CP2102) or a serial header (USART_TXD net label).
- PD0 (RXD) is wired for completeness per the schematic requirement
  but is not actively read by the firmware in the base project.
- Recommended baud rate: 9600 bps (set in `initialize_display()` /
  USART init function).
- The terminal should display lines in the format specified by the
  project:
  ```
  TIME: 00:05:27
  TASK: SENSOR SAMPLE
  ```

---

## Summary Table (Quick Reference)

| Pin | Net Label | Role |
|---|---|---|
| PB0 | LED_STATUS | Output -- status LED (2 sec toggle) |
| PB1 | LED_TASK | Output -- sampling LED (5 sec flash) |
| PA0 | SET_BTN | Input -- enter time-set mode |
| PA1 | INC_BTN | Input -- increment time value |
| PA2 | CLOCK_RESET | Input -- reset clock to 00:00:00 |
| PD1 | USART_TXD | Output -- serial display (clock + task status) |
| PD0 | USART_RXD | Input -- reserved/unused |
| Timer1 | -- | Internal -- 1 Hz interrupt source |
