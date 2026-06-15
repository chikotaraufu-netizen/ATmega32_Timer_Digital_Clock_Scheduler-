# 📌 ATmega32 Pin Mapping Table

> Complete PDIP-40 pin mapping for the ATmega32 Timer-Based Digital Clock & Task Scheduler project, including electrical characteristics and port configuration.

---

## Table of Contents

- [Project Pin Assignment Summary](#project-pin-assignment-summary)
- [Complete PDIP-40 Pin Table](#complete-pdip-40-pin-table)
- [Port-by-Port Configuration](#port-by-port-configuration)
- [Electrical Characteristics](#electrical-characteristics)
- [Pin Configuration Code](#pin-configuration-code)
- [Physical Pinout Diagram](#physical-pinout-diagram)

---

## Project Pin Assignment Summary

### Used Pins

| Pin # | Port.Bit | Signal Name | Direction | Type | Description |
|-------|----------|-------------|-----------|------|-------------|
| 40 | PA0 | SET_BTN | Input | Digital, Active Low | Time-set mode button |
| 39 | PA1 | INC_BTN | Input | Digital, Active Low | Increment field button |
| 38 | PA2 | CLOCK_RESET | Input | Digital, Active Low | Clock reset button |
| 1 | PB0 | LED_STATUS | Output | Digital, Active High | Status heartbeat LED |
| 2 | PB1 | LED_TASK | Output | Digital, Active High | Task indicator LED |
| 6 | PB5 | MOSI | — | ISP | SPI Master Out / Slave In |
| 7 | PB6 | MISO | — | ISP | SPI Master In / Slave Out |
| 8 | PB7 | SCK | — | ISP | SPI Serial Clock |
| 9 | — | RESET | Input | Active Low | MCU hardware reset |
| 10 | — | VCC | Power | +5V | Digital supply |
| 11 | — | GND | Power | 0V | Digital ground |
| 12 | — | XTAL2 | Oscillator | — | Crystal output |
| 13 | — | XTAL1 | Oscillator | — | Crystal input |
| 14 | PD0 | USART_RXD | Input | Digital | USART receive data |
| 15 | PD1 | USART_TXD | Output | Digital | USART transmit data |
| 30 | — | AVCC | Power | +5V | Analog supply |
| 31 | — | AGND | Power | 0V | Analog ground |

### Pin Usage Statistics

| Category | Count | Percentage |
|----------|-------|------------|
| GPIO (Inputs) | 3 | 7.5% |
| GPIO (Outputs) | 2 | 5.0% |
| Communication (USART) | 2 | 5.0% |
| Programming (ISP) | 3 | 7.5% |
| Power/Ground | 4 | 10.0% |
| Oscillator | 2 | 5.0% |
| Reset | 1 | 2.5% |
| **Unused/Available** | **23** | **57.5%** |

---

## Complete PDIP-40 Pin Table

The following table lists all 40 pins of the ATmega32 in PDIP-40 package format:

| Pin # | Port | Default Function | Alternate Functions | **Project Assignment** | Direction | Notes |
|-------|------|-----------------|--------------------|-----------------------|-----------|-------|
| 1 | PB0 | GPIO | T0, XCK | **LED_STATUS** | Output | 330Ω to LED to GND |
| 2 | PB1 | GPIO | T1 | **LED_TASK** | Output | 330Ω to LED to GND |
| 3 | PB2 | GPIO | INT2, AIN0 | *Unused* | — | Available |
| 4 | PB3 | GPIO | OC0, AIN1 | *Unused* | — | Available |
| 5 | PB4 | GPIO | SS | *Unused* | — | Available |
| 6 | PB5 | GPIO | MOSI | **ISP_MOSI** | — | ISP header |
| 7 | PB6 | GPIO | MISO | **ISP_MISO** | — | ISP header |
| 8 | PB7 | GPIO | SCK | **ISP_SCK** | — | ISP header |
| 9 | — | **RESET** | — | **RESET** | Input | 10kΩ pull-up + 100nF cap |
| 10 | — | **VCC** | — | **+5V Supply** | Power | 100nF decoupling to GND |
| 11 | — | **GND** | — | **Ground** | Power | Main digital ground |
| 12 | — | **XTAL2** | — | **8 MHz Crystal** | Osc | 22pF cap to GND |
| 13 | — | **XTAL1** | — | **8 MHz Crystal** | Osc | 22pF cap to GND |
| 14 | PD0 | GPIO | RXD | **USART_RXD** | Input | From USB-UART adapter TX |
| 15 | PD1 | GPIO | TXD | **USART_TXD** | Output | To USB-UART adapter RX |
| 16 | PD2 | GPIO | INT0 | *Unused* | — | Available (ext interrupt) |
| 17 | PD3 | GPIO | INT1 | *Unused* | — | Available (ext interrupt) |
| 18 | PD4 | GPIO | OC1B | *Unused* | — | Available (Timer1 OC) |
| 19 | PD5 | GPIO | OC1A | *Unused* | — | Available (Timer1 OC) |
| 20 | PD6 | GPIO | ICP1 | *Unused* | — | Available (input capture) |
| 21 | PD7 | GPIO | OC2 | *Unused* | — | Available (Timer2 OC) |
| 22 | PC0 | GPIO | SCL | *Unused* | — | Available (I2C clock) |
| 23 | PC1 | GPIO | SDA | *Unused* | — | Available (I2C data) |
| 24 | PC2 | GPIO | TCK | *Unused* | — | JTAG (disabled by fuse) |
| 25 | PC3 | GPIO | TMS | *Unused* | — | JTAG (disabled by fuse) |
| 26 | PC4 | GPIO | TDO | *Unused* | — | JTAG (disabled by fuse) |
| 27 | PC5 | GPIO | TDI | *Unused* | — | JTAG (disabled by fuse) |
| 28 | PC6 | GPIO | TOSC1 | *Unused* | — | Available (Timer2 osc) |
| 29 | PC7 | GPIO | TOSC2 | *Unused* | — | Available (Timer2 osc) |
| 30 | — | **AVCC** | — | **+5V Analog** | Power | Connect to VCC |
| 31 | — | **AGND** | — | **Analog GND** | Power | Connect to GND |
| 32 | — | **AREF** | — | *Unused* | — | ADC reference (N/C) |
| 33 | PA7 | GPIO | ADC7 | *Unused* | — | Available (ADC ch7) |
| 34 | PA6 | GPIO | ADC6 | *Unused* | — | Available (ADC ch6) |
| 35 | PA5 | GPIO | ADC5 | *Unused* | — | Available (ADC ch5) |
| 36 | PA4 | GPIO | ADC4 | *Unused* | — | Available (ADC ch4) |
| 37 | PA3 | GPIO | ADC3 | *Unused* | — | Available (ADC ch3) |
| 38 | PA2 | GPIO | ADC2 | **CLOCK_RESET** | Input | Active low, internal pull-up |
| 39 | PA1 | GPIO | ADC1 | **INC_BTN** | Input | Active low, internal pull-up |
| 40 | PA0 | GPIO | ADC0 | **SET_BTN** | Input | Active low, internal pull-up |

---

## Port-by-Port Configuration

### Port A — Button Inputs

```
Port A Direction Register (DDRA):
Bit:    7    6    5    4    3    2    1    0
Value:  0    0    0    0    0    0    0    0    = 0x00 (all inputs)

Port A Data Register (PORTA) — Pull-ups:
Bit:    7    6    5    4    3    2    1    0
Value:  0    0    0    0    0    1    1    1    = 0x07 (pull-ups on PA0-PA2)
```

| Bit | Pin # | Function | DDR | PORT | Configuration |
|-----|-------|----------|-----|------|---------------|
| PA0 | 40 | SET_BTN | 0 (Input) | 1 (Pull-up ON) | Button to GND |
| PA1 | 39 | INC_BTN | 0 (Input) | 1 (Pull-up ON) | Button to GND |
| PA2 | 38 | CLOCK_RESET | 0 (Input) | 1 (Pull-up ON) | Button to GND |
| PA3 | 37 | Unused | 0 | 0 | Tri-state |
| PA4 | 36 | Unused | 0 | 0 | Tri-state |
| PA5 | 35 | Unused | 0 | 0 | Tri-state |
| PA6 | 34 | Unused | 0 | 0 | Tri-state |
| PA7 | 33 | Unused | 0 | 0 | Tri-state |

### Port B — LED Outputs and ISP

```
Port B Direction Register (DDRB):
Bit:    7    6    5    4    3    2    1    0
Value:  0    0    0    0    0    0    1    1    = 0x03 (PB0-PB1 outputs)

Port B Data Register (PORTB) — Initial state:
Bit:    7    6    5    4    3    2    1    0
Value:  0    0    0    0    0    0    0    0    = 0x00 (LEDs off)
```

| Bit | Pin # | Function | DDR | PORT | Configuration |
|-----|-------|----------|-----|------|---------------|
| PB0 | 1 | LED_STATUS | 1 (Output) | 0 (Low/OFF) | Active high, 330Ω series |
| PB1 | 2 | LED_TASK | 1 (Output) | 0 (Low/OFF) | Active high, 330Ω series |
| PB2 | 3 | Unused | 0 | 0 | Tri-state |
| PB3 | 4 | Unused | 0 | 0 | Tri-state |
| PB4 | 5 | Unused | 0 | 0 | Tri-state |
| PB5 | 6 | MOSI (ISP) | — | — | Controlled by programmer |
| PB6 | 7 | MISO (ISP) | — | — | Controlled by programmer |
| PB7 | 8 | SCK (ISP) | — | — | Controlled by programmer |

### Port C — Unused (JTAG Disabled)

```
Port C Direction Register (DDRC):
Bit:    7    6    5    4    3    2    1    0
Value:  0    0    0    0    0    0    0    0    = 0x00 (all inputs/tri-state)

Port C Data Register (PORTC):
Bit:    7    6    5    4    3    2    1    0
Value:  0    0    0    0    0    0    0    0    = 0x00 (no pull-ups)
```

> **Note**: PC2–PC5 are JTAG pins. JTAG is disabled via the JTAGEN fuse bit (HFUSE bit 6 = 1) to free these pins for GPIO use if needed.

### Port D — USART Communication

```
Port D Direction Register (DDRD):
Bit:    7    6    5    4    3    2    1    0
Value:  0    0    0    0    0    0    1    0    = 0x02 (PD1 output for TXD)

Note: USART hardware automatically configures PD0 (RXD) and PD1 (TXD)
when the USART is enabled. Manual DDR configuration is optional.
```

| Bit | Pin # | Function | DDR | PORT | Configuration |
|-----|-------|----------|-----|------|---------------|
| PD0 | 14 | USART_RXD | 0 (Input) | — | USART controlled |
| PD1 | 15 | USART_TXD | 1 (Output) | — | USART controlled |
| PD2 | 16 | Unused | 0 | 0 | Available (INT0) |
| PD3 | 17 | Unused | 0 | 0 | Available (INT1) |
| PD4 | 18 | Unused | 0 | 0 | Available (OC1B) |
| PD5 | 19 | Unused | 0 | 0 | Available (OC1A) |
| PD6 | 20 | Unused | 0 | 0 | Available (ICP1) |
| PD7 | 21 | Unused | 0 | 0 | Available (OC2) |

---

## Electrical Characteristics

### ATmega32 DC Characteristics (VCC = 5V)

| Parameter | Symbol | Min | Typical | Max | Unit |
|-----------|--------|-----|---------|-----|------|
| Supply Voltage | VCC | 4.5 | 5.0 | 5.5 | V |
| Input Low Voltage | VIL | — | — | 0.3×VCC (1.5) | V |
| Input High Voltage | VIH | 0.6×VCC (3.0) | — | — | V |
| Output Low Voltage (IOL = 20mA) | VOL | — | — | 0.7 | V |
| Output High Voltage (IOH = −20mA) | VOH | 4.2 | — | — | V |
| Input Pull-up Resistance | Rpu | 20 | 35 | 50 | kΩ |
| DC Current per I/O Pin | — | — | — | 40 | mA |
| DC Current (VCC/GND pins) | — | — | — | 200 | mA |
| Total Package DC Current | — | — | — | 400 | mA |

### LED Circuit Calculations

```
VCC = 5.0V
V_LED (typical red) = 2.0V
I_LED (desired) = 10mA

R = (VCC - V_LED) / I_LED
R = (5.0 - 2.0) / 0.010
R = 300Ω

Selected: R = 330Ω (nearest standard value)

Actual I_LED = (5.0 - 2.0) / 330 = 9.1 mA ✅
Power dissipated in resistor: P = I² × R = 0.0091² × 330 = 27.3 mW
```

### Button Input Characteristics

```
Internal Pull-up: R_pullup ≈ 35 kΩ (typical)

Button pressed (LOW):    V_pin ≈ 0V (below VIL = 1.5V) ✅
Button released (HIGH):  V_pin ≈ 5V (above VIH = 3.0V) ✅

Pull-up current when pressed: I = VCC / R_pullup = 5V / 35kΩ ≈ 143 µA
```

### Crystal Oscillator Circuit

| Component | Value | Purpose |
|-----------|-------|---------|
| Crystal | 8 MHz, HC49 | Frequency-determining element |
| C1 (XTAL1 to GND) | 22 pF | Load capacitor |
| C2 (XTAL2 to GND) | 22 pF | Load capacitor |

> Load capacitance formula: `C_load = (C1 × C2) / (C1 + C2) + C_stray`
> With C1 = C2 = 22 pF and C_stray ≈ 5 pF: `C_load ≈ 16 pF` — suitable for most 8 MHz crystals.

---

## Pin Configuration Code

```c
#include <avr/io.h>

/* =============================================
 * Pin Definitions (config.h)
 * ============================================= */

// Port A — Button Inputs
#define SET_BTN_PIN     PA0
#define SET_BTN_PORT    PORTA
#define SET_BTN_DDR     DDRA
#define SET_BTN_PINR    PINA

#define INC_BTN_PIN     PA1
#define INC_BTN_PORT    PORTA
#define INC_BTN_DDR     DDRA
#define INC_BTN_PINR    PINA

#define RESET_BTN_PIN   PA2
#define RESET_BTN_PORT  PORTA
#define RESET_BTN_DDR   DDRA
#define RESET_BTN_PINR  PINA

// Port B — LED Outputs
#define LED_STATUS_PIN  PB0
#define LED_STATUS_PORT PORTB
#define LED_STATUS_DDR  DDRB

#define LED_TASK_PIN    PB1
#define LED_TASK_PORT   PORTB
#define LED_TASK_DDR    DDRB

/* =============================================
 * Port Initialization Function
 * ============================================= */

void ports_init(void) {
    // --- Port A: Button Inputs with Pull-ups ---
    DDRA  &= ~((1 << PA0) | (1 << PA1) | (1 << PA2));  // Inputs
    PORTA |=  ((1 << PA0) | (1 << PA1) | (1 << PA2));   // Pull-ups ON

    // --- Port B: LED Outputs ---
    DDRB  |=  ((1 << PB0) | (1 << PB1));   // Outputs
    PORTB &= ~((1 << PB0) | (1 << PB1));   // Initially OFF

    // --- Port D: USART (configured by USART init) ---
    // PD0 (RXD) and PD1 (TXD) configured automatically
}

/* =============================================
 * Button Read Macros
 * ============================================= */

// Active LOW: button pressed returns 0, so invert
#define IS_SET_PRESSED()   (!(PINA & (1 << PA0)))
#define IS_INC_PRESSED()   (!(PINA & (1 << PA1)))
#define IS_RESET_PRESSED() (!(PINA & (1 << PA2)))

/* =============================================
 * LED Control Macros
 * ============================================= */

#define LED_STATUS_ON()     (PORTB |=  (1 << PB0))
#define LED_STATUS_OFF()    (PORTB &= ~(1 << PB0))
#define LED_STATUS_TOGGLE() (PORTB ^=  (1 << PB0))

#define LED_TASK_ON()       (PORTB |=  (1 << PB1))
#define LED_TASK_OFF()      (PORTB &= ~(1 << PB1))
#define LED_TASK_TOGGLE()   (PORTB ^=  (1 << PB1))
```

---

## Physical Pinout Diagram

```
                    ATmega32 PDIP-40
                   ┌────────┐  ┌────────┐
     LED_STATUS ──→│ PB0  1 │──│ 40 PA0 │←── SET_BTN
      LED_TASK ──→│ PB1  2 │──│ 39 PA1 │←── INC_BTN
        (free) ───│ PB2  3 │──│ 38 PA2 │←── CLOCK_RESET
        (free) ───│ PB3  4 │──│ 37 PA3 │─── (free)
        (free) ───│ PB4  5 │──│ 36 PA4 │─── (free)
     ISP_MOSI ───│ PB5  6 │──│ 35 PA5 │─── (free)
     ISP_MISO ───│ PB6  7 │──│ 34 PA6 │─── (free)
      ISP_SCK ───│ PB7  8 │──│ 33 PA7 │─── (free)
        RESET ───│ RST  9 │──│ 32 AREF│─── (N/C)
          +5V ───│ VCC 10 │──│ 31 AGND│─── GND
          GND ───│ GND 11 │──│ 30 AVCC│─── +5V
    8MHz XTAL ───│ XT2 12 │──│ 29 PC7 │─── (free)
    8MHz XTAL ───│ XT1 13 │──│ 28 PC6 │─── (free)
    USART_RXD ───│ PD0 14 │──│ 27 PC5 │─── (free/JTAG)
    USART_TXD ───│ PD1 15 │──│ 26 PC4 │─── (free/JTAG)
        (free) ───│ PD2 16 │──│ 25 PC3 │─── (free/JTAG)
        (free) ───│ PD3 17 │──│ 24 PC2 │─── (free/JTAG)
        (free) ───│ PD4 18 │──│ 23 PC1 │─── (free/I2C)
        (free) ───│ PD5 19 │──│ 22 PC0 │─── (free/I2C)
        (free) ───│ PD6 20 │──│ 21 PD7 │─── (free)
                   └─────────┘──└────────┘
```

---

## Expansion Possibilities

The following pins are available for future expansion:

| Available Port | Free Pins | Potential Use |
|---------------|-----------|---------------|
| Port A (PA3–PA7) | 5 pins | Additional buttons, ADC sensors |
| Port B (PB2–PB4) | 3 pins | More LEDs, PWM buzzer |
| Port C (PC0–PC7) | 8 pins | LCD display (HD44780), I2C peripherals, 7-segment display |
| Port D (PD2–PD7) | 6 pins | External interrupts, rotary encoder, additional tasks |
| **Total Available** | **22 pins** | — |

---

## References

- ATmega32 Datasheet — Section 4: "I/O Ports"
- ATmega32 Datasheet — Table 27-1: "DC Characteristics"
- ATmega32 Datasheet — Figure 1-1: "Pin Configuration (PDIP)"

---

*← Back to [Compare Match Calculation](compare_match_calculation.md) | Next: [Test Results](test_results.md) →*
