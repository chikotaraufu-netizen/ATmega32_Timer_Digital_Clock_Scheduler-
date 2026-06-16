# Compare-Match Calculation

## Task 3: Calculate Timer Prescaler and Compare Value

### Formula Used

```
OCR1A = (F_CPU / (Prescaler x f_interrupt)) - 1
```

### Known Values
- F_CPU = 8,000,000 Hz (8 MHz)
- f_interrupt = 1 Hz (target: one interrupt per second)
- Timer1 is 16-bit, so OCR1A must satisfy 0 <= OCR1A <= 65535

---

## Step 1: Evaluate All Available Prescaler Options

Timer1 prescaler options on the ATmega32: 1, 8, 64, 256, 1024

| Prescaler | OCR1A = (8,000,000 / (Prescaler x 1)) - 1 | Fits in 16-bit (<= 65535)? |
|---|---|---|
| 1    | 7,999,999 | No |
| 8    | 999,999   | No |
| 64   | 124,999   | No |
| 256  | 31,249    | Yes |
| 1024 | 7,811.5 -> 7812 | Yes |

---

## Step 2: Prescaler Selection Justification

Prescaler = **1024** was selected because:

1. It matches the worked example given in the project specification,
   keeping firmware and documentation consistent.
2. It produces a smaller OCR1A value (7812) relative to the 16-bit
   ceiling (65535), leaving more headroom for future changes
   (e.g., if F_CPU is increased to 16 MHz, OCR1A would become ~15624,
   still well within range -- whereas with prescaler 256 it would
   become ~62499, very close to overflow).
3. Prescaler 256 is also valid but offers a much tighter margin to
   the 16-bit limit and was not used in the reference example.

---

## Step 3: Final Calculation

```
OCR1A = (8,000,000 / (1024 x 1)) - 1
OCR1A = 7812.5 - 1
OCR1A = 7811.5  ->  rounds to 7812
```

**Final value: OCR1A = 7812**

---

## Step 4: Verify Actual Resulting Frequency (Rounding Error)

```
Actual f_interrupt = F_CPU / (Prescaler x (OCR1A + 1))
                    = 8,000,000 / (1024 x 7813)
                    = 8,000,000 / 7,999,312
                    ~= 1.0000086 Hz
```

- Error: approximately 0.00086%
- Equivalent drift: approximately 1 second every ~13 days
- This level of drift is acceptable for this project and should be
  noted in test_results.md as expected clock behavior.

---

## Final Register Configuration

```c
TCCR1B |= (1 << WGM12);              // CTC mode (WGM12=1, WGM13=0)
OCR1A = 7812;                        // Compare value for 1 Hz interrupt
TIMSK |= (1 << OCIE1A);              // Enable Timer1 Compare Match A interrupt
TCCR1B |= (1 << CS12) | (1 << CS10); // Prescaler = 1024 (CS12:CS11:CS10 = 1:0:1)
sei();                                // Enable global interrupts
```

---

## Summary

| Parameter | Value |
|---|---|
| F_CPU | 8 MHz |
| Prescaler | 1024 |
| OCR1A | 7812 |
| Target frequency | 1 Hz |
| Actual frequency | ~1.0000086 Hz |
| Drift | ~1 sec every 13 days |
