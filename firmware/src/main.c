/**
 * @file main.c
 * @brief ATmega32 Digital Clock & Task Scheduler – Main program
 *
 * This is the top-level firmware entry point.  It initialises all
 * peripherals and modules, then enters an infinite non-blocking
 * super-loop that:
 *
 *   1. Checks for a 1 s (1 Hz) tick from Timer1 (ISR-set flag).
 *   2. On each 1 s tick: advances the clock, scheduler, and buttons.
 *   3. Updates the display every second.
 *   4. Runs any pending scheduled tasks (LED toggling/flashing).
 *   5. Polls buttons and handles time-set mode.
 *
 * Design notes:
 *   - The ISR (timer.c) only sets a flag – all work happens here.
 *   - The main loop never blocks (except the brief debounce delay
 *     inside buttons_read when a press is detected).
 *   - Time-set mode cycles through fields: HOURS → MINUTES → SECONDS
 *     → NORMAL.  Each press of SET advances the mode; INC increments
 *     the selected field.
 *
 * Target: ATmega32, 8 MHz, AVR-GCC
 */

#include <avr/io.h>
#include <avr/interrupt.h>

#include "config.h"
#include "timer.h"
#include "display.h"
#include "buttons.h"
#include "scheduler.h"

/* ========================== Time-Set Mode ============================== */

/**
 * @brief  Enumeration of time-setting states.
 *
 * The user presses SET to cycle:
 *   NORMAL → SET_HOURS → SET_MINUTES → SET_SECONDS → NORMAL
 * While in a SET_* state, INC increments that field.
 */
typedef enum {
    MODE_NORMAL = 0,
    MODE_SET_HOURS,
    MODE_SET_MINUTES,
    MODE_SET_SECONDS
} set_mode_t;

/* ========================== Main ======================================= */

int main(void)
{
    /* ---- Initialise all modules ---- */
    buttons_init();     /* GPIO inputs with pull-ups   */
    usart_init();       /* 9600 baud 8N1               */
    scheduler_init();   /* LED outputs, counters reset  */
    timer1_init();      /* Timer1 CTC → 1 Hz tick       */

    /* Enable global interrupts – Timer1 ISR can now fire */
    sei();

    /* Send a startup banner */
    display_message("=== ATmega32 Digital Clock ===");
    display_message("Timer1 CTC @ 1 Hz | USART 9600");
    display_message("Buttons: SET / INC / RESET");
    display_message("------------------------------");

    /* Display initial time */
    display_time(clock_get_time());

    /* Current time-set mode */
    set_mode_t mode = MODE_NORMAL;

    /* ================================================================ */
    /*  Super-loop – runs forever, non-blocking                        */
    /* ================================================================ */
    for (;;) {

        /* ---- 1. Check for 1 s (1 Hz) tick ---- */
        if (timer1_tick_pending()) {

            /* Advance the task scheduler and buttons every 1 s */
            scheduler_tick();
            buttons_tick();

            if (mode == MODE_NORMAL) {
                /* Advance clock only in normal mode */
                clock_tick();
            }

            /* Display the current time every second */
            display_time(clock_get_time());
        }

        /* ---- 2. Execute any pending scheduled tasks ---- */
        scheduler_run();

        /* ---- 3. Poll buttons ---- */
        button_event_t btn = buttons_read();

        switch (btn) {

            case BTN_SET:
                /*
                 * Cycle through time-set modes.
                 * Each press advances to the next field or back to NORMAL.
                 */
                switch (mode) {
                    case MODE_NORMAL:
                        mode = MODE_SET_HOURS;
                        display_message("[SET] Mode: HOURS");
                        break;
                    case MODE_SET_HOURS:
                        mode = MODE_SET_MINUTES;
                        display_message("[SET] Mode: MINUTES");
                        break;
                    case MODE_SET_MINUTES:
                        mode = MODE_SET_SECONDS;
                        display_message("[SET] Mode: SECONDS");
                        break;
                    case MODE_SET_SECONDS:
                        mode = MODE_NORMAL;
                        display_message("[SET] Mode: NORMAL (running)");
                        break;
                }
                break;

            case BTN_INC:
                /*
                 * Increment the currently selected time field.
                 * Only active when in a SET_* mode.
                 */
                if (mode != MODE_NORMAL) {
                    clock_time_t t = clock_get_time();

                    switch (mode) {
                        case MODE_SET_HOURS:
                            t.hours = (t.hours + 1) % 24;
                            break;
                        case MODE_SET_MINUTES:
                            t.minutes = (t.minutes + 1) % 60;
                            break;
                        case MODE_SET_SECONDS:
                            t.seconds = (t.seconds + 1) % 60;
                            break;
                        default:
                            break;
                    }

                    clock_set_time(t);
                    display_time(t);
                    display_message("[INC] Field incremented");
                }
                break;

            case BTN_RESET:
                /*
                 * Reset the clock to 00:00:00 regardless of mode.
                 * Also return to normal running mode.
                 */
                clock_reset();
                mode = MODE_NORMAL;
                display_time(clock_get_time());
                display_message("[RESET] Clock reset to 00:00:00");
                break;

            case BTN_NONE:
            default:
                /* No button pressed – nothing to do */
                break;
        }
    }

    /* Never reached */
    return 0;
}
