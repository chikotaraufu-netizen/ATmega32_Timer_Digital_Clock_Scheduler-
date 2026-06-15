/**
 * @file buttons.c
 * @brief Debounced button driver for SET, INCREMENT, and RESET
 *
 * Reads three active-low buttons on PORTA with internal pull-ups.
 * Implements a simple delay-based debounce with edge detection so
 * that a single press produces exactly one event.
 *
 * Debounce strategy:
 *   On each call to buttons_read(), the raw pin state is sampled.
 *   If a button is detected as pressed (low) and was not pressed on
 *   the previous sample, a _delay_ms debounce wait is performed and
 *   the pin is re-sampled.  If still low the press is accepted.
 *   The previous-state variable prevents auto-repeat.
 *
 *   This approach works well in a polling super-loop where the main
 *   loop already runs fast enough that the short blocking delay is
 *   acceptable.  For harder real-time requirements the debounce
 *   could be integrated into a timer tick instead.
 */

#include <avr/io.h>
#include <util/delay.h>
#include <stdbool.h>

#include "config.h"
#include "buttons.h"

/* ---- Previous (debounced) state – one bit per button ---- */
static uint8_t g_prev_state = 0xFF;  /* All high = all released (pull-ups) */

/* ================================================================== */
/*  Public API                                                        */
/* ================================================================== */

void buttons_init(void)
{
    /*
     * Configure PA0, PA1, PA2 as inputs.
     *   DDRx = 0  →  input  (default after reset, but explicit is safer)
     */
    BTN_DDR &= ~((1 << SET_BTN) | (1 << INC_BTN) | (1 << RESET_BTN));

    /*
     * Enable internal pull-ups on the three button pins.
     *   Writing 1 to PORTx when DDRx = 0 activates the pull-up.
     *   External buttons short the pin to GND when pressed → active-low.
     */
    BTN_PORT |= (1 << SET_BTN) | (1 << INC_BTN) | (1 << RESET_BTN);
}

button_event_t buttons_read(void)
{
    /* Read the current raw pin state (only the three button bits) */
    uint8_t raw = BTN_PIN & ((1 << SET_BTN) | (1 << INC_BTN) | (1 << RESET_BTN));

    /*
     * Detect falling edges: a bit was 1 (released) last time and is
     * 0 (pressed) now.  XOR finds changed bits; AND with previous
     * state isolates newly-pressed ones.
     */
    uint8_t changed  = raw ^ g_prev_state;    /* bits that changed          */
    uint8_t pressed  = changed & g_prev_state; /* bits that went high→low   */

    /* Update stored state for next call's edge detection */
    g_prev_state = raw;

    if (pressed == 0) {
        return BTN_NONE;  /* No new press detected */
    }

    /*
     * A potential press was detected – perform a debounce delay and
     * re-read to confirm the press is stable.
     */
    _delay_ms(DEBOUNCE_DELAY_MS);

    uint8_t confirmed = BTN_PIN & ((1 << SET_BTN) | (1 << INC_BTN) | (1 << RESET_BTN));

    /*
     * Update the stored state again after the debounce delay so that
     * the next call sees the debounced level (prevents double-fire).
     */
    g_prev_state = confirmed;

    /*
     * Check each button: the bit must still be low (pressed) after
     * debounce AND it must have been in the original 'pressed' mask.
     * Priority: SET > INC > RESET (only one event per call).
     */
    if ((pressed & (1 << SET_BTN)) && !(confirmed & (1 << SET_BTN))) {
        return BTN_SET;
    }
    if ((pressed & (1 << INC_BTN)) && !(confirmed & (1 << INC_BTN))) {
        return BTN_INC;
    }
    if ((pressed & (1 << RESET_BTN)) && !(confirmed & (1 << RESET_BTN))) {
        return BTN_RESET;
    }

    return BTN_NONE;  /* Press was not confirmed after debounce (noise) */
}
