/**
 * @file buttons.c
 * @brief Non-blocking debounced button driver for SET, INCREMENT, and RESET
 */

#include <avr/io.h>
#include <stdbool.h>

#include "config.h"
#include "buttons.h"

/* State for non-blocking debounce */
static uint8_t g_debounced_state = 0xFF;  /* All high = all released */
static uint8_t g_last_stable = 0xFF;
static uint8_t g_debounce_cnt = 0;
static uint8_t g_events = 0;

void buttons_init(void)
{
    BTN_DDR &= ~((1 << SET_BTN) | (1 << INC_BTN) | (1 << RESET_BTN));
    BTN_PORT |= (1 << SET_BTN) | (1 << INC_BTN) | (1 << RESET_BTN);
}

void buttons_tick(void)
{
    uint8_t raw = BTN_PIN & ((1 << SET_BTN) | (1 << INC_BTN) | (1 << RESET_BTN));
    
    if (raw == g_last_stable) {
        if (g_debounce_cnt < 5) {
            g_debounce_cnt++;
            if (g_debounce_cnt == 5) {
                uint8_t changed = g_debounced_state ^ raw;
                uint8_t pressed = changed & g_debounced_state;
                if (pressed & (1 << SET_BTN)) g_events |= (1 << SET_BTN);
                if (pressed & (1 << INC_BTN)) g_events |= (1 << INC_BTN);
                if (pressed & (1 << RESET_BTN)) g_events |= (1 << RESET_BTN);
                g_debounced_state = raw;
            }
        }
    } else {
        g_debounce_cnt = 0;
        g_last_stable = raw;
    }
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
