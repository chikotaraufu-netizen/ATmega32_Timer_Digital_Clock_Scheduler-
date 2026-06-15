# 🔢 Compare Match (OCR1A) Calculation

> Step-by-step derivation of the Output Compare Register value for generating a precise 100 Hz (10 ms) interrupt on the ATmega32 Timer1.

---

## Table of Contents

- [The Fundamental Formula](#the-fundamental-formula)
- [Parameter Definitions](#parameter-definitions)
- [Step-by-Step Calculation](#step-by-step-calculation)
- [Verification](#verification)
- [Prescaler Options](#prescaler-options)

---

## The Fundamental Formula

The compare match value for CTC mode is calculated using:

```
┌─────────────────────────────────────────────────────┐
│                                                     │
│              F_CPU                                  │
│   OCR1A = ─────────────────────── − 1               │
│           Prescaler × f_interrupt                   │
│                                                     │
└─────────────────────────────────────────────────────┘
```

### Why "− 1"?

The timer counts from **0 to OCR1A** inclusive, which means the timer goes through **(OCR1A + 1)** states before resetting. Therefore:

```
Total counts per cycle = OCR1A + 1

Interrupt period = (OCR1A + 1) × Prescaler / F_CPU

Solving for OCR1A:
    OCR1A + 1 = F_CPU / (Prescaler × f_interrupt)
    OCR1A     = F_CPU / (Prescaler × f_interrupt) - 1
```

---

## Parameter Definitions

| Symbol | Parameter | Value | Unit |
|--------|-----------|-------|------|
| F_CPU | System clock frequency | 8,000,000 | Hz |
| Prescaler | Timer clock divider | 64 | — |
| f_interrupt | Desired interrupt frequency | 100 | Hz |
| f_timer | Timer clock frequency (F_CPU / Prescaler) | 125,000 | Hz |
| T_tick | Timer tick period (1 / f_timer) | 8.0 | µs |
| OCR1A | Output Compare Register value | 1,249 | — |

---

## Step-by-Step Calculation

### Step 1: Determine the Timer Clock Frequency

The prescaler divides the system clock to produce the timer's input clock:

```
f_timer = F_CPU / Prescaler
f_timer = 8,000,000 Hz / 64
f_timer = 125,000 Hz
```

> This means the timer counter (TCNT1) increments **125,000 times per second**.

### Step 2: Calculate the Required Number of Counts

For a 100 Hz interrupt (one interrupt every 10 milliseconds), the timer must count through a specific number of ticks:

```
Required counts = f_timer / f_interrupt
Required counts = 125,000 / 100
Required counts = 1,250 ticks
```

### Step 3: Apply the OCR1A Formula

Since the timer counts from 0, we subtract 1:

```
OCR1A = Required counts - 1
OCR1A = 1,250 - 1
OCR1A = 1,249
```

### Step 4: Verify the Range

The ATmega32 Timer1 is a 16-bit timer:

```
Minimum OCR1A value: 0
Maximum OCR1A value: 65,535 (0xFFFF)

Our value: 1,249 ✅ (well within the 16-bit range)
```

### Final Result

```
┌─────────────────────────────┐
│                             │
│     OCR1A = 1249            │
│     (Hex: 0x04E1)           │
│     (Binary: 0000 0100      │
│              1110 0001)     │
│                             │
└─────────────────────────────┘
```

---

## Verification

### Forward Calculation: OCR1A → Frequency

Starting from our chosen OCR1A value, verify the resulting interrupt frequency:

```
Step 1: Total counts per cycle
    counts = OCR1A + 1 = 1249 + 1 = 1250

Step 2: Time per cycle (interrupt period)
    T_interrupt = counts × Prescaler / F_CPU
    T_interrupt = 1250 × 64 / 8,000,000
    T_interrupt = 80,000 / 8,000,000
    T_interrupt = 0.010000 seconds (Exactly 10 ms)

Step 3: Actual interrupt frequency
    f_actual = 1 / T_interrupt
    f_actual = 1 / 0.010000
    f_actual = 100.000000 Hz
```

### Verification Summary

| Parameter | Ideal | Actual | Difference |
|-----------|-------|--------|------------|
| OCR1A | 1249 | 1249 | 0 |
| Interrupt period | 10.000000 ms | 10.000000 ms | 0.0 µs |
| Interrupt frequency | 100.000000 Hz | 100.000000 Hz | 0.0000% |

> **Conclusion**: By using Prescaler 64 and OCR1A = 1249, we achieve **0.000% error**. The timer is mathematically perfect relative to the external 8 MHz crystal oscillator.

---

## Prescaler Options

### Full Prescaler Analysis for 100 Hz @ 8 MHz

| Prescaler | f_timer (Hz) | Exact OCR1A | Rounded OCR1A | Fits 16-bit | Error |
|-----------|-------------|-------------|---------------|-------------|-------|
| 1 | 8,000,000 | 79,999 | 79,999 | ❌ No* | — |
| 8 | 1,000,000 | 9,999 | 9,999 | ✅ Yes | **0%** |
| **64** | **125,000** | **1,249** | **1,249** | **✅ Yes** | **0%** |
| 256 | 31,250 | 311.5 | 312 | ✅ Yes | ~0.16% |
| 1024 | 7,812.5 | 77.125 | 77 | ✅ Yes | ~0.16% |

*\* Value exceeds 65,535 (16-bit maximum)*

> **Why Prescaler 64?** We chose 64 because it provides a perfectly exact 100 Hz frequency while keeping the OCR1A value (1249) comfortably small but large enough to provide excellent sub-millisecond precision if needed elsewhere in the program.
