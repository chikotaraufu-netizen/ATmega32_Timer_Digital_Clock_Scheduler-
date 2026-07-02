/**
 * @file scheduler.h
 * @brief Cooperative periodic task scheduler driven by 1 Hz (1 s) ticks
 *
 * The scheduler maintains 1-second-resolution counters for each periodic
 * task.  On each 1 Hz tick the counters are advanced and corresponding
 * flags are set.  The main loop checks the flags and executes the tasks.
 *
 * Tasks:
 *  - Status LED  : toggled every SCHED_STATUS_LED_TICKS seconds
 *  - Task LED    : turned on every SCHED_TASK_LED_TICKS seconds,
 *                  then turned off after SCHED_TASK_LED_ON_TICKS seconds
 */

#ifndef SCHEDULER_H
#define SCHEDULER_H

#include <stdbool.h>

/**
 * @brief  Initialise scheduler counters and LED GPIO.
 */
void scheduler_init(void);

/**
 * @brief  Advance scheduler counters by 1 second.
 *
 * Call this exactly once per 1 Hz tick (inside the main loop after
 * detecting timer1_tick_pending()).  Sets internal flags when tasks
 * are due.
 */
void scheduler_tick(void);

/**
 * @brief  Execute any pending scheduled tasks (LED toggling / flashing).
 *
 * Call this in the main loop after scheduler_tick().  It checks the
 * internal flags, performs the actions, and clears the flags.
 * Non-blocking.
 */
void scheduler_run(void);

#endif /* SCHEDULER_H */
