/**
 * @file buttons.c
 * @brief Non-blocking debounced button driver for SET, INCREMENT, and RESET
 *
 * At 1 Hz tick rate each tick is 1 second apart, which is far longer than
 * any mechanical contact bounce (~5-20 ms).  A single stable reading per
 * tick is therefore sufficient for reliable edge detection.
 */

#include <avr/io.h>
#include <stdbool.h>

#include "config.h"
#include "buttons.h"

/* State for non-blocking debounce */
static uint8_t g_debounced_state = 0xFF;  /* All high = all released */
static uint8_t g_events = 0;

void buttons_init(void)
{
    BTN_DDR &= ~((1 << SET_BTN) | (1 << INC_BTN) | (1 << RESET_BTN));
    BTN_PORT |= (1 << SET_BTN) | (1 << INC_BTN) | (1 << RESET_BTN);
}

void buttons_tick(void)
{
    /*
     * At 1 Hz, each tick is 1 second apart – well beyond any mechanical
     * bounce window.  Detect falling edges (active-low press) directly
     * by comparing current state against the previous debounced state.
     */
    uint8_t raw = BTN_PIN & ((1 << SET_BTN) | (1 << INC_BTN) | (1 << RESET_BTN));

    uint8_t changed = g_debounced_state ^ raw;
    /* Active-low: a press is a bit that was high (released) and is now low */
    uint8_t pressed = changed & g_debounced_state;

    if (pressed & (1 << SET_BTN))   g_events |= (1 << SET_BTN);
    if (pressed & (1 << INC_BTN))   g_events |= (1 << INC_BTN);
    if (pressed & (1 << RESET_BTN)) g_events |= (1 << RESET_BTN);

    g_debounced_state = raw;
}

button_event_t buttons_read(void)
{
    if (g_events & (1 << SET_BTN)) {
        g_events &= ~(1 << SET_BTN);
        return BTN_SET;
    }
    if (g_events & (1 << INC_BTN)) {
        g_events &= ~(1 << INC_BTN);
        return BTN_INC;
    }
    if (g_events & (1 << RESET_BTN)) {
        g_events &= ~(1 << RESET_BTN);
        return BTN_RESET;
    }
    return BTN_NONE;
}
