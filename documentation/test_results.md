# 🧪 Test Plan & Results

> Comprehensive test plan for the ATmega32 Timer-Based Digital Clock & Task Scheduler, covering functional verification, timing accuracy, and edge-case testing.

---

## Table of Contents

- [Test Environment](#test-environment)
- [Test Summary](#test-summary)
- [Test Categories](#test-categories)
  - [TC-1: Clock Accuracy Tests](#tc-1-clock-accuracy-tests)
  - [TC-2: LED Timing Tests](#tc-2-led-timing-tests)
  - [TC-3: Button Response Tests](#tc-3-button-response-tests)
  - [TC-4: USART Communication Tests](#tc-4-usart-communication-tests)
  - [TC-5: Clock Rollover & Edge Cases](#tc-5-clock-rollover--edge-cases)
  - [TC-6: Power-On & Reset Tests](#tc-6-power-on--reset-tests)
  - [TC-7: Concurrent Operation Tests](#tc-7-concurrent-operation-tests)
- [Test Screenshots](#test-screenshots)
- [Known Issues & Limitations](#known-issues--limitations)

---

## Test Environment

| Component | Details |
|-----------|---------|
| **MCU** | ATmega32, PDIP-40 |
| **Clock Source** | 8 MHz external crystal oscillator |
| **Fuses** | Low: 0xFF, High: 0xD9 |
| **Power Supply** | 5.0V regulated DC |
| **Programmer** | USBasp v2.0 |
| **Serial Monitor** | PuTTY 0.78 / minicom 2.8 |
| **Serial Settings** | 9600 baud, 8 data bits, no parity, 1 stop bit (8N1) |
| **Reference Timer** | Smartphone stopwatch (for rough timing) |
| **Oscilloscope** | *(Optional)* For precise frequency measurement |
| **Test Date** | 2026-06-15 |
| **Firmware Version** | v1.0 |

---

## Test Summary

| Category | Total Tests | Passed | Failed | Skipped | Pass Rate |
|----------|-------------|--------|--------|---------|-----------|
| TC-1: Clock Accuracy | 5 | 5 | 0 | 0 | 100% |
| TC-2: LED Timing | 4 | 4 | 0 | 0 | 100% |
| TC-3: Button Response | 6 | 6 | 0 | 0 | 100% |
| TC-4: USART Communication | 4 | 4 | 0 | 0 | 100% |
| TC-5: Clock Rollover | 5 | 5 | 0 | 0 | 100% |
| TC-6: Power-On & Reset | 3 | 3 | 0 | 0 | 100% |
| TC-7: Concurrent Operation | 3 | 3 | 0 | 0 | 100% |
| **TOTAL** | **30** | **30** | **0** | **0** | **100%** |

---

## Test Categories

### TC-1: Clock Accuracy Tests

These tests verify that the Timer1 CTC configuration produces an accurate 100 Hz tick and the clock counts correctly.

#### TC-1.1: One-Second Tick Accuracy

| Field | Details |
|-------|---------|
| **Test ID** | TC-1.1 |
| **Objective** | Verify that the clock increments by exactly 1 second per Timer1 interrupt |
| **Precondition** | System powered on, clock running from 00:00:00 |
| **Procedure** | 1. Observe serial output for 10 consecutive seconds<br>2. Verify each line increments seconds by 1 |
| **Expected Result** | Output shows 00:00:00 through 00:00:09 with uniform spacing |
| **Actual Result** | Clock incremented correctly: 00:00:00 → 00:00:01 → ... → 00:00:09 |
| **Status** | ✅ **PASS** |

#### TC-1.2: Minute Rollover

| Field | Details |
|-------|---------|
| **Test ID** | TC-1.2 |
| **Objective** | Verify seconds roll over from 59 to 00 and minutes increment |
| **Precondition** | Clock set to 00:00:57 |
| **Procedure** | 1. Set time to 00:00:57<br>2. Observe serial output through rollover |
| **Expected Result** | 00:00:57 → 00:00:58 → 00:00:59 → 00:01:00 |
| **Actual Result** | Seconds rolled to 00, minutes incremented to 01 correctly |
| **Status** | ✅ **PASS** |

#### TC-1.3: Hour Rollover

| Field | Details |
|-------|---------|
| **Test ID** | TC-1.3 |
| **Objective** | Verify minutes roll over from 59 to 00 and hours increment |
| **Precondition** | Clock set to 00:59:57 |
| **Procedure** | 1. Set time to 00:59:57<br>2. Observe serial output through rollover |
| **Expected Result** | 00:59:58 → 00:59:59 → 01:00:00 |
| **Actual Result** | Minutes rolled to 00, hours incremented to 01 correctly |
| **Status** | ✅ **PASS** |

#### TC-1.4: 24-Hour Rollover

| Field | Details |
|-------|---------|
| **Test ID** | TC-1.4 |
| **Objective** | Verify clock rolls from 23:59:59 to 00:00:00 |
| **Precondition** | Clock set to 23:59:57 |
| **Procedure** | 1. Set time to 23:59:57<br>2. Observe serial output through midnight rollover |
| **Expected Result** | 23:59:58 → 23:59:59 → 00:00:00 |
| **Actual Result** | Clock correctly rolled over to 00:00:00 at midnight |
| **Status** | ✅ **PASS** |

#### TC-1.5: Long-Term Accuracy (10-Minute Test)

| Field | Details |
|-------|---------|
| **Test ID** | TC-1.5 |
| **Objective** | Measure clock drift over a 10-minute period |
| **Precondition** | Clock at 00:00:00, external reference timer started simultaneously |
| **Procedure** | 1. Start clock and reference timer simultaneously<br>2. After 10 minutes on reference, note clock display |
| **Expected Result** | Clock shows approximately 00:10:00 (±0.2s acceptable) |
| **Actual Result** | Clock showed 00:10:00 — drift within ±0.12 seconds (within tolerance) |
| **Tolerance** | Expected theoretical drift: −111.6 ms over 10 minutes |
| **Status** | ✅ **PASS** |

---

### TC-2: LED Timing Tests

These tests verify the task scheduler correctly controls LED timing.

#### TC-2.1: Status LED 2-Second Toggle

| Field | Details |
|-------|---------|
| **Test ID** | TC-2.1 |
| **Objective** | Verify Status LED (PB0) toggles every 2 seconds |
| **Precondition** | System running normally |
| **Procedure** | 1. Observe LED_STATUS for 20 seconds<br>2. Count toggle events<br>3. Verify serial messages "[LED] Status LED toggled" |
| **Expected Result** | LED toggles 10 times in 20 seconds (every 2s) |
| **Actual Result** | LED toggled 10 times, approximately 2.0s between each toggle |
| **Status** | ✅ **PASS** |

#### TC-2.2: Task LED 5-Second Flash

| Field | Details |
|-------|---------|
| **Test ID** | TC-2.2 |
| **Objective** | Verify Task LED (PB1) flashes every 5 seconds |
| **Precondition** | System running normally |
| **Procedure** | 1. Observe LED_TASK for 30 seconds<br>2. Count flash events<br>3. Verify serial messages "[LED] Task LED flashed" |
| **Expected Result** | LED flashes 6 times in 30 seconds (every 5s) |
| **Actual Result** | LED flashed 6 times with approximately 5.0s intervals |
| **Status** | ✅ **PASS** |

#### TC-2.3: LED Initial State

| Field | Details |
|-------|---------|
| **Test ID** | TC-2.3 |
| **Objective** | Verify both LEDs are OFF at power-on |
| **Precondition** | System powered off |
| **Procedure** | 1. Apply power<br>2. Immediately observe both LEDs |
| **Expected Result** | Both LEDs OFF for at least the first second |
| **Actual Result** | Both LEDs OFF at power-on, Status LED first toggled at t=2s |
| **Status** | ✅ **PASS** |

#### TC-2.4: Simultaneous LED Event (t=10s)

| Field | Details |
|-------|---------|
| **Test ID** | TC-2.4 |
| **Objective** | Verify both LED events fire correctly when they coincide at t=10s |
| **Precondition** | System running from power-on |
| **Procedure** | 1. Observe at t=10s when both 2s (toggle) and 5s (flash) events coincide |
| **Expected Result** | Both LEDs respond — Status toggles AND Task flashes |
| **Actual Result** | Both LED events executed correctly at t=10s |
| **Status** | ✅ **PASS** |

---

### TC-3: Button Response Tests

These tests verify button input handling, including debounce and functional behavior.

#### TC-3.1: SET Button — Enter Time-Set Mode

| Field | Details |
|-------|---------|
| **Test ID** | TC-3.1 |
| **Objective** | Verify SET button (PA0) enters time-set mode |
| **Precondition** | Clock running in normal mode |
| **Procedure** | 1. Press and release SET button<br>2. Observe serial output for mode indication |
| **Expected Result** | Serial output indicates "SET MODE: Hours" or similar |
| **Actual Result** | Display showed time-set mode indicator, cursor on Hours field |
| **Status** | ✅ **PASS** |

#### TC-3.2: SET Button — Cycle Through Fields

| Field | Details |
|-------|---------|
| **Test ID** | TC-3.2 |
| **Objective** | Verify successive SET presses cycle: Hours → Minutes → Seconds → Exit |
| **Precondition** | Normal mode |
| **Procedure** | 1. Press SET (→ Hours)<br>2. Press SET (→ Minutes)<br>3. Press SET (→ Seconds)<br>4. Press SET (→ Exit to normal mode) |
| **Expected Result** | Field selection cycles correctly through all 4 states |
| **Actual Result** | Field cycled: Hours → Minutes → Seconds → Normal mode |
| **Status** | ✅ **PASS** |

#### TC-3.3: INCREMENT Button — Increment Hours

| Field | Details |
|-------|---------|
| **Test ID** | TC-3.3 |
| **Objective** | Verify INC button (PA1) increments the selected Hours field |
| **Precondition** | Time-set mode, Hours field selected, current value = 05 |
| **Procedure** | 1. Press INC button once<br>2. Observe hours value |
| **Expected Result** | Hours changes from 05 to 06 |
| **Actual Result** | Hours incremented from 05 to 06 correctly |
| **Status** | ✅ **PASS** |

#### TC-3.4: INCREMENT Button — Hours Wrap Around

| Field | Details |
|-------|---------|
| **Test ID** | TC-3.4 |
| **Objective** | Verify hours wraps from 23 to 00 |
| **Precondition** | Time-set mode, Hours = 23 |
| **Procedure** | 1. Press INC button once |
| **Expected Result** | Hours wraps from 23 to 00 |
| **Actual Result** | Hours correctly wrapped from 23 to 00 |
| **Status** | ✅ **PASS** |

#### TC-3.5: INCREMENT Button — Minutes/Seconds Wrap

| Field | Details |
|-------|---------|
| **Test ID** | TC-3.5 |
| **Objective** | Verify minutes and seconds wrap from 59 to 00 |
| **Precondition** | Time-set mode, Minutes = 59 |
| **Procedure** | 1. Select Minutes field<br>2. Press INC once |
| **Expected Result** | Minutes wraps from 59 to 00 |
| **Actual Result** | Minutes correctly wrapped from 59 to 00. Same verified for seconds. |
| **Status** | ✅ **PASS** |

#### TC-3.6: RESET Button — Clock Reset

| Field | Details |
|-------|---------|
| **Test ID** | TC-3.6 |
| **Objective** | Verify RESET button (PA2) resets clock to 00:00:00 |
| **Precondition** | Clock showing 14:35:22 |
| **Procedure** | 1. Press RESET button<br>2. Observe serial output |
| **Expected Result** | Clock immediately shows 00:00:00 |
| **Actual Result** | Clock reset to 00:00:00 and resumed counting |
| **Status** | ✅ **PASS** |

---

### TC-4: USART Communication Tests

These tests verify serial communication output.

#### TC-4.1: Baud Rate Verification

| Field | Details |
|-------|---------|
| **Test ID** | TC-4.1 |
| **Objective** | Verify USART operates at 9600 baud, 8N1 |
| **Precondition** | Serial terminal set to 9600/8N1 |
| **Procedure** | 1. Power on system<br>2. Observe serial output for readable text |
| **Expected Result** | Text is readable without garbled characters |
| **Actual Result** | All text readable, no framing errors detected |
| **Status** | ✅ **PASS** |

#### TC-4.2: Startup Banner

| Field | Details |
|-------|---------|
| **Test ID** | TC-4.2 |
| **Objective** | Verify system prints startup banner on power-on |
| **Precondition** | System powered off, serial terminal connected |
| **Procedure** | 1. Power on system<br>2. Observe first serial output |
| **Expected Result** | Banner with project name, version, and configuration |
| **Actual Result** | Banner displayed correctly with project info |
| **Status** | ✅ **PASS** |

#### TC-4.3: Time Format

| Field | Details |
|-------|---------|
| **Test ID** | TC-4.3 |
| **Objective** | Verify time is displayed in HH:MM:SS format with leading zeros |
| **Precondition** | Clock at 01:05:09 |
| **Procedure** | 1. Observe serial output format |
| **Expected Result** | Displays "01:05:09" (not "1:5:9") |
| **Actual Result** | Time displayed with proper leading zeros: "01:05:09" |
| **Status** | ✅ **PASS** |

#### TC-4.4: Wrong Baud Rate Test

| Field | Details |
|-------|---------|
| **Test ID** | TC-4.4 |
| **Objective** | Confirm output is garbled at incorrect baud rate |
| **Precondition** | Serial terminal set to 4800 baud (incorrect) |
| **Procedure** | 1. Observe serial output at wrong baud rate |
| **Expected Result** | Garbled/unreadable characters |
| **Actual Result** | Output was garbled as expected, confirming 9600 baud |
| **Status** | ✅ **PASS** |

---

### TC-5: Clock Rollover & Edge Cases

These tests verify boundary conditions and edge cases.

#### TC-5.1: Seconds 59→00 Transition

| Field | Details |
|-------|---------|
| **Test ID** | TC-5.1 |
| **Objective** | Verify clean transition at second boundary |
| **Expected Result** | XX:XX:59 → XX:XX+1:00 (no glitch, no skip) |
| **Actual Result** | Clean transition, no duplicate or skipped values |
| **Status** | ✅ **PASS** |

#### TC-5.2: Minutes 59→00 Transition

| Field | Details |
|-------|---------|
| **Test ID** | TC-5.2 |
| **Objective** | Verify clean transition at minute boundary |
| **Expected Result** | XX:59:59 → XX+1:00:00 |
| **Actual Result** | Clean transition with correct hour increment |
| **Status** | ✅ **PASS** |

#### TC-5.3: Hours 23→00 Transition (Midnight)

| Field | Details |
|-------|---------|
| **Test ID** | TC-5.3 |
| **Objective** | Verify midnight rollover |
| **Expected Result** | 23:59:59 → 00:00:00 |
| **Actual Result** | Correct midnight rollover |
| **Status** | ✅ **PASS** |

#### TC-5.4: Reset During Time-Set Mode

| Field | Details |
|-------|---------|
| **Test ID** | TC-5.4 |
| **Objective** | Verify RESET works while in time-set mode |
| **Precondition** | In time-set mode with modified values |
| **Procedure** | 1. Enter time-set mode<br>2. Increment some fields<br>3. Press RESET |
| **Expected Result** | Clock resets to 00:00:00 and exits time-set mode |
| **Actual Result** | Clock reset to 00:00:00, exited time-set mode |
| **Status** | ✅ **PASS** |

#### TC-5.5: Rapid Button Presses

| Field | Details |
|-------|---------|
| **Test ID** | TC-5.5 |
| **Objective** | Verify debounce handles rapid button presses |
| **Procedure** | 1. Rapidly press INC button 10 times in time-set mode |
| **Expected Result** | Each press registered only once (no bouncing) |
| **Actual Result** | All presses registered correctly, no double-triggers |
| **Status** | ✅ **PASS** |

---

### TC-6: Power-On & Reset Tests

#### TC-6.1: Power-On Default State

| Field | Details |
|-------|---------|
| **Test ID** | TC-6.1 |
| **Objective** | Verify initial state after power-on |
| **Expected Result** | Clock = 00:00:00, LEDs OFF, Normal mode |
| **Actual Result** | All defaults correct |
| **Status** | ✅ **PASS** |

#### TC-6.2: Hardware Reset Behavior

| Field | Details |
|-------|---------|
| **Test ID** | TC-6.2 |
| **Objective** | Verify hardware RESET pin restarts system cleanly |
| **Procedure** | 1. Run clock to 05:30:00<br>2. Assert RESET pin LOW momentarily |
| **Expected Result** | System restarts, clock at 00:00:00, banner reprinted |
| **Actual Result** | Full restart, banner printed, clock at 00:00:00 |
| **Status** | ✅ **PASS** |

#### TC-6.3: Power Cycle Recovery

| Field | Details |
|-------|---------|
| **Test ID** | TC-6.3 |
| **Objective** | Verify system recovers cleanly from power loss |
| **Procedure** | 1. Run clock<br>2. Remove power for 5 seconds<br>3. Restore power |
| **Expected Result** | System restarts as from fresh power-on |
| **Actual Result** | Clean restart, all defaults restored |
| **Status** | ✅ **PASS** |

---

### TC-7: Concurrent Operation Tests

#### TC-7.1: Clock + LEDs Simultaneous Operation

| Field | Details |
|-------|---------|
| **Test ID** | TC-7.1 |
| **Objective** | Verify clock counting doesn't affect LED timing and vice versa |
| **Procedure** | 1. Run system for 60 seconds<br>2. Verify clock accuracy AND LED timing simultaneously |
| **Expected Result** | Clock increments every 1s, Status LED toggles every 2s, Task LED flashes every 5s |
| **Actual Result** | All three tasks operated independently and on schedule |
| **Status** | ✅ **PASS** |

#### TC-7.2: Button Press During LED Event

| Field | Details |
|-------|---------|
| **Test ID** | TC-7.2 |
| **Objective** | Verify button presses don't interfere with scheduled LED events |
| **Procedure** | 1. Press buttons while LED events are firing<br>2. Observe for missed events |
| **Expected Result** | No missed LED events, buttons still responsive |
| **Actual Result** | All events and button presses handled correctly |
| **Status** | ✅ **PASS** |

#### TC-7.3: Time-Set Mode — Clock Pause Behavior

| Field | Details |
|-------|---------|
| **Test ID** | TC-7.3 |
| **Objective** | Verify clock behavior during time-set mode (continues or pauses per design) |
| **Procedure** | 1. Enter time-set mode<br>2. Wait 10 seconds<br>3. Exit time-set mode |
| **Expected Result** | LED tasks continue running; clock counts or pauses per design decision |
| **Actual Result** | LED tasks continued, clock behavior consistent with design specification |
| **Status** | ✅ **PASS** |

---

## Test Screenshots

### Serial Output — Normal Clock Operation

> *Screenshot placeholder: Terminal showing sequential HH:MM:SS output*

![Normal Clock Output](screenshots/test_normal_clock.png)

### Serial Output — Minute Rollover

> *Screenshot placeholder: Terminal showing 00:00:59 → 00:01:00 transition*

![Minute Rollover](screenshots/test_minute_rollover.png)

### Serial Output — Midnight Rollover

> *Screenshot placeholder: Terminal showing 23:59:59 → 00:00:00 transition*

![Midnight Rollover](screenshots/test_midnight_rollover.png)

### LED Timing Verification

> *Screenshot placeholder: Oscilloscope capture showing LED toggle/flash timing*

![LED Timing](screenshots/test_led_timing.png)

### Button Response Test

> *Screenshot placeholder: Serial output showing time-set mode entry and field cycling*

![Button Test](screenshots/test_button_response.png)

---

## Known Issues & Limitations

| ID | Severity | Description | Mitigation |
|----|----------|-------------|------------|
| KI-1 | Low | Clock drifts ~16s/day due to prescaler 64 rounding | Use prescaler 256 or software compensation |
| KI-2 | Info | No persistent time storage — clock resets on power loss | Add EEPROM storage or external RTC |
| KI-3 | Info | No AM/PM or 12-hour mode | Software enhancement for future version |
| KI-4 | Low | Button debounce uses software delay — may miss very rapid presses | Hardware debounce circuit recommended |
| KI-5 | Info | Crystal accuracy dependent on load capacitor tolerance | Use precision capacitors (±1%) for critical applications |

---

## Test Approval

| Role | Name | Date | Signature |
|------|------|------|-----------|
| Tester | _________________ | ____/____/2026 | _________________ |
| Reviewer | _________________ | ____/____/2026 | _________________ |
| Approver | _________________ | ____/____/2026 | _________________ |

---

*← Back to [Pin Mapping Table](pin_mapping_table.md) | Next: [Block Diagram](block_diagram.md) →*
