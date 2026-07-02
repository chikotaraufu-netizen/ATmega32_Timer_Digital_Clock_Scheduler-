/**
 * @file timer.h
 * @brief Timer1 CTC mode driver – 1 Hz timekeeping for the digital clock
 *
 * Provides:
 *  - Timer1 initialisation in CTC mode (prescaler 1024, OCR1A=7812)
 *  - A volatile tick flag set by the ISR every 1 s
 *  - Clock time structure and accessor/mutator functions
 */

#ifndef TIMER_H
#define TIMER_H

#include <stdint.h>
#include <stdbool.h>

/* ---- Clock time representation ---- */
typedef struct {
    uint8_t hours;    /* 0–23 */
    uint8_t minutes;  /* 0–59 */
    uint8_t seconds;  /* 0–59 */
} clock_time_t;

/**
 * @brief  Initialise Timer1 in CTC mode for a 1 Hz interrupt.
 *
 * Configures OCR1A, enables the Output Compare A Match interrupt,
 * and starts the timer with prescaler 1024.  Global interrupts must
 * be enabled separately via sei().
 */
void timer1_init(void);

/**
 * @brief  Check whether a 1 s tick has occurred.
 * @return true  if the ISR has signalled a new tick (flag is cleared).
 * @return false if no tick has occurred since the last check.
 *
 * This is the main loop's non-blocking way of detecting elapsed 1 s ticks.
 */
bool timer1_tick_pending(void);

/**
 * @brief  Advance the clock by one second (handles rollover).
 */
void clock_tick(void);

/**
 * @brief  Get a snapshot of the current clock time.
 * @return clock_time_t with hours, minutes, seconds.
 */
clock_time_t clock_get_time(void);

/**
 * @brief  Overwrite the current clock time (used by time-set mode).
 * @param  t  New time to set.
 */
void clock_set_time(clock_time_t t);

/**
 * @brief  Reset the clock to 00:00:00.
 */
void clock_reset(void);

#endif /* TIMER_H */
