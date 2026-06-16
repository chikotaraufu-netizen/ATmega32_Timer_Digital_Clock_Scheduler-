# Timer Configuration

## Task 2: Select Timer Resource and Time Base

### Timer Resource Selected
**Timer/Counter1 (16-bit)**

Timer1 was selected because its 16-bit resolution allows a direct
compare-match value for a 1-second interrupt at 8 MHz with a 1024
prescaler, without overflow or extra software-divider tricks. The
8-bit timers (Timer0, Timer2) cannot reach a 1-second period at
reasonable prescaler values without additional counting layers.

### Mode of Operation Selected
**CTC (Clear Timer on Compare Match) — Mode 4 (WGM13:0 = 0100)**

Reasons for choosing CTC mode over alternatives:

| Mode | Suitability |
|---|---|
| Normal mode | Requires manually reloading the counter inside the ISR, which is less accurate and accumulates timing drift over long periods. |
| PWM modes (Fast PWM, Phase Correct) | Designed for generating output waveforms on OC1A/OC1B pins, not for generating periodic interrupts for timekeeping. |
| **CTC mode (selected)** | On reaching `OCR1A`, the timer automatically resets to 0 and triggers `TIMER1_COMPA_vect`. No manual reload needed — accurate, repeatable, and simple to use as a system time base. |

### Time Base Selected
**1 Hz (one interrupt every 1 second)**

This was chosen over the 1 ms or 10 ms options because:
- It maps directly onto the "seconds value increases every 1 second"
  requirement with no extra software division.
- It keeps the ISR simple — each interrupt = exactly one second elapsed.
- The 2-second and 5-second scheduled tasks (status LED, sampling LED)
  can be derived with simple tick counters (`tick_count % 2`,
  `tick_count % 5`).

> **Note (Extension Task):** If implementing the extension (500 ms,
> 2 s, and 10 s tasks), a faster base such as 1 ms or 10 ms would be
> selected instead, with all longer intervals derived from a
> millisecond tick counter using modulo arithmetic.

### Clock Source
**F_CPU = 8 MHz**

### Prescaler Selected
**1024**

Chosen because it keeps the resulting compare value (`OCR1A` ≈ 7812)
small enough to fit comfortably within Timer1's 16-bit range
(0–65535) while still producing exactly 1 Hz. (Full calculation
verification is covered in Task 3 / `compare_match_calculation.md`.)

---

## Summary Table

| Parameter | Selected Value | Justification |
|---|---|---|
| Timer | Timer1 (16-bit) | Sufficient range for 1 Hz compare value at 8 MHz / 1024 |
| Mode | CTC (Mode 4) | Auto-reset on compare match; no manual reload; accurate |
| Time base | 1 Hz (1 second) | Matches "seconds" requirement directly |
| Prescaler | 1024 | Keeps OCR1A small (~7812), fits in 16-bit register |
| Clock source (F_CPU) | 8 MHz | Standard ATmega32 operating clock |
