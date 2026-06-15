/**
 * @file timer.c
 * @brief Timer1 CTC mode driver – 1 Hz timekeeping for the digital clock
 *
 * Timer1 is configured in Clear Timer on Compare (CTC) mode.  When the
 * counter reaches OCR1A it resets to 0 and fires the TIMER1_COMPA_vect
 * interrupt.  With F_CPU = 8 MHz, prescaler = 1024, and OCR1A = 7812
 * the interrupt fires at almost exactly 1 Hz.
 *
 *   Period = (1 + OCR1A) * prescaler / F_CPU
 *          = (1 + 7812) * 1024 / 8 000 000
 *          = 7813 * 1024 / 8 000 000
 *          = 0.999 424 s   (~0.06 % fast – acceptable for a demo clock)
 */

#include <avr/io.h>
#include <avr/interrupt.h>
#include <stdbool.h>
#include <util/atomic.h>

#include "config.h"
#include "timer.h"

/* ---- Module-level state (accessed from ISR and main) ---- */

/** Flag set by ISR, cleared by main loop via timer1_tick_pending(). */
static volatile bool g_tick_flag = false;

/** Current clock time – modified only from main-loop context. */
static clock_time_t g_clock = {0, 0, 0};

/* ================================================================== */
/*  Timer1 Interrupt Service Routine                                  */
/* ================================================================== */

/**
 * TIMER1_COMPA_vect – fires every ~1 second.
 *
 * The ISR does minimal work: it just sets a flag.  All heavy processing
 * (clock increment, display, scheduling) happens in the main loop,
 * keeping interrupt latency low.
 */
ISR(TIMER1_COMPA_vect)
{
    g_tick_flag = true;
}

/* ================================================================== */
/*  Public API                                                        */
/* ================================================================== */

void timer1_init(void)
{
    /*
     * 1. Set Timer1 to CTC mode (WGM12 = 1, others = 0).
     *    CTC mode: timer counts up, resets to 0 on compare match.
     *
     *    TCCR1A = 0x00  (WGM11:10 = 00)
     *    TCCR1B: WGM13:12 = 01  →  bit WGM12 set
     */
    TCCR1A = 0x00;
    TCCR1B = (1 << WGM12);

    /*
     * 2. Load the compare value for a 1 Hz period.
     *    OCR1A = 7812 (see header comment for calculation).
     */
    OCR1A = TIMER1_TOP;

    /*
     * 3. Reset the counter so we start from a known state.
     */
    TCNT1 = 0;

    /*
     * 4. Enable Output Compare A Match interrupt.
     *    OCIE1A in TIMSK register.
     */
    TIMSK |= (1 << OCIE1A);

    /*
     * 5. Start the timer by setting the prescaler bits (clk/1024).
     *    CS12=1, CS11=0, CS10=1  → TCCR1B |= 0x05
     */
    TCCR1B |= TIMER1_PRESCALER_BITS;
}

bool timer1_tick_pending(void)
{
    bool pending = false;

    /*
     * Atomic read-and-clear of the volatile flag.
     * ATOMIC_BLOCK ensures the flag cannot be set between the read
     * and the clear.
     */
    ATOMIC_BLOCK(ATOMIC_RESTORESTATE)
    {
        if (g_tick_flag) {
            g_tick_flag = false;
            pending = true;
        }
    }

    return pending;
}

void clock_tick(void)
{
    g_clock.seconds++;
    if (g_clock.seconds >= 60) {
        g_clock.seconds = 0;
        g_clock.minutes++;
        if (g_clock.minutes >= 60) {
            g_clock.minutes = 0;
            g_clock.hours++;
            if (g_clock.hours >= 24) {
                g_clock.hours = 0;  /* Midnight rollover */
            }
        }
    }
}

clock_time_t clock_get_time(void)
{
    return g_clock;
}

void clock_set_time(clock_time_t t)
{
    /* Clamp to valid ranges for safety */
    if (t.hours   > 23) t.hours   = 23;
    if (t.minutes > 59) t.minutes = 59;
    if (t.seconds > 59) t.seconds = 59;

    g_clock = t;
}

void clock_reset(void)
{
    g_clock.hours   = 0;
    g_clock.minutes = 0;
    g_clock.seconds = 0;
}
