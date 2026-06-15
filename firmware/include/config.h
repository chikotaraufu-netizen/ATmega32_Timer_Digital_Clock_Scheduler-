/**
 * @file config.h
 * @brief Central configuration for ATmega32 Digital Clock & Task Scheduler
 *
 * All hardware-dependent constants, pin mappings, timer calculations,
 * and scheduler intervals are defined here for easy modification.
 *
 * Target MCU : ATmega32 (PDIP-40)
 * Clock      : 8 MHz external crystal
 */

#ifndef CONFIG_H
#define CONFIG_H

/* ========================== CPU Clock ================================== */
/**
 * F_CPU must be defined before including <util/delay.h> or any AVR header
 * that uses it.  8 MHz matches the external crystal on the target board.
 */
#ifndef F_CPU
#define F_CPU 8000000UL
#endif

/* ========================== Pin Mapping ================================ */
/*
 * PORTA – Buttons (active-low with internal pull-ups)
 *   PA0 (Pin 40) : SET_BTN      – Enter/cycle time-set mode
 *   PA1 (Pin 39) : INC_BTN      – Increment selected field
 *   PA2 (Pin 38) : CLOCK_RESET  – Reset clock to 00:00:00
 *
 * PORTB – LEDs (active-high outputs)
 *   PB0 (Pin 1)  : LED_STATUS   – Toggled every 2 s by scheduler
 *   PB1 (Pin 2)  : LED_TASK     – Brief flash every 5 s by scheduler
 *
 * PORTD – USART
 *   PD0 (Pin 14) : USART_RXD
 *   PD1 (Pin 15) : USART_TXD
 */

/* Button port/pins (PORTA) */
#define BTN_DDR     DDRA
#define BTN_PORT    PORTA
#define BTN_PIN     PINA
#define SET_BTN     PA0
#define INC_BTN     PA1
#define RESET_BTN   PA2

/* LED port/pins (PORTB) */
#define LED_DDR     DDRB
#define LED_PORT    PORTB
#define LED_STATUS  PB0
#define LED_TASK    PB1

/* ========================== Timer1 CTC Configuration =================== */
/**
 * Goal : generate a precise 1 Hz interrupt from Timer1 in CTC mode.
 *
 * Calculation:
 *   f_OCR = F_CPU / (prescaler * (1 + OCR1A))
 *   1 Hz  = 8 000 000 / (1024 * (1 + OCR1A))
 *   1 + OCR1A = 8 000 000 / 1024 = 7812.5
 *   OCR1A = 7812  (truncated – yields ~1.000 s period, 0.006 % error)
 *
 * Prescaler bits: CS12=1, CS11=0, CS10=1  → clk/1024
 */
#define TIMER1_PRESCALER_BITS  ((1 << CS12) | (1 << CS10))
#define TIMER1_TOP             7812U

/* ========================== USART Configuration ======================== */
/**
 * Baud rate : 9600
 * UBRR = (F_CPU / (16 * BAUD)) - 1 = (8000000 / (16 * 9600)) - 1 = 51.08
 * Use 51 → actual baud ≈ 9615 (0.16 % error – well within tolerance).
 */
#define USART_BAUD       9600UL
#define USART_UBRR_VAL  ((F_CPU / (16UL * USART_BAUD)) - 1)

/* ========================== Scheduler Intervals ======================== */
/**
 * Intervals are expressed in seconds (Timer1 ISR ticks at 1 Hz).
 */
#define SCHED_STATUS_LED_INTERVAL  2U   /* Toggle status LED every 2 s  */
#define SCHED_TASK_LED_INTERVAL    5U   /* Flash task LED every 5 s     */
#define SCHED_TASK_LED_ON_TICKS    1U   /* Task LED stays on for ~1 s   */

/* ========================== Button Debounce ============================ */
/**
 * Debounce delay in milliseconds.  Checked in the main loop via a simple
 * timer-tick counter (resolution = 1 s) or _delay_ms for sub-second needs.
 */
#define DEBOUNCE_DELAY_MS  50U

#endif /* CONFIG_H */
