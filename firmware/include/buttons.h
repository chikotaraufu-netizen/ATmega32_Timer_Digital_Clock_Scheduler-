/**
 * @file buttons.h
 * @brief Debounced button driver for SET, INCREMENT, and RESET
 *
 * Three buttons on PORTA with internal pull-ups.  Buttons are active-low
 * (pressed = logic 0).  Debouncing uses a fully non-blocking, tick-based
 * approach with edge detection (reports press only on falling edge).
 */

#ifndef BUTTONS_H
#define BUTTONS_H

#include <stdbool.h>

/**
 * @brief  Button event identifiers returned by buttons_read().
 */
typedef enum {
    BTN_NONE = 0,   /**< No button pressed                       */
    BTN_SET,        /**< SET button – enter/cycle time-set mode   */
    BTN_INC,        /**< INCREMENT – increment selected field     */
    BTN_RESET       /**< RESET – reset clock to 00:00:00          */
} button_event_t;

/**
 * @brief  Initialise button GPIO pins (enable internal pull-ups).
 */
void buttons_init(void);

/**
 * @brief  Periodic tick for non-blocking debounce (call every 10ms).
 */
void buttons_tick(void);

/**
 * @brief  Poll the buttons with debounce and edge detection.
 * @return The button event if a valid press was detected, BTN_NONE otherwise.
 *
 * Call this once per main-loop iteration.  The function handles its own
 * debounce timing so it is non-blocking from the caller's perspective
 * (returns immediately if debounce period has not elapsed).
 */
button_event_t buttons_read(void);

#endif /* BUTTONS_H */
