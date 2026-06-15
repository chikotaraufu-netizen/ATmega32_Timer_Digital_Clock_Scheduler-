/**
 * @file scheduler.c
 * @brief Cooperative periodic task scheduler driven by 10 ms ticks
 *
 * Periodic tasks managed:
 *
 *   1. STATUS LED (PB0) – toggled every 2 seconds.
 *   2. TASK LED   (PB1) – turned ON every 5 seconds for a 1-second flash,
 *                          then turned OFF.
 *   3. EXTENSION TASK   – 500 ms heartbeat task over USART.
 *
 * Architecture:
 *   scheduler_tick()  is called once per 10 ms interrupt-flag from the
 *                     main loop.  It increments per-task counters and
 *                     sets boolean flags when an action is due.
 *
 *   scheduler_run()   checks the flags, performs the action (GPIO write),
 *                     and clears the flags.  This two-phase design keeps
 *                     the timing logic separate from the I/O logic and
 *                     makes unit testing easier.
 */

#include <avr/io.h>
#include <stdbool.h>

#include "config.h"
#include "scheduler.h"
#include "display.h"

/* ---- Internal state ---- */

/** 10ms-resolution counter for the status LED task. */
static uint16_t g_status_counter = 0;

/** 10ms-resolution counter for the task LED task. */
static uint16_t g_task_counter = 0;

/** Counter tracking how long the task LED has been ON (0 = OFF). */
static uint16_t g_task_led_on_counter = 0;

/** 10ms-resolution counter for the extension task (500 ms). */
static uint16_t g_ext_counter = 0;

/** Flag: set when it is time to toggle the status LED. */
static volatile bool g_flag_status_led = false;

/** Flag: set when it is time to flash the task LED ON. */
static volatile bool g_flag_task_led_on = false;

/** Flag: set when the task LED flash duration has elapsed. */
static volatile bool g_flag_task_led_off = false;

/** Flag: set when the 500ms extension task should run. */
static volatile bool g_flag_ext_task = false;

/* ================================================================== */
/*  Public API                                                        */
/* ================================================================== */

void scheduler_init(void)
{
    /*
     * Configure PB0 (LED_STATUS) and PB1 (LED_TASK) as outputs.
     * Start with both LEDs off (low).
     */
    LED_DDR  |= (1 << LED_STATUS) | (1 << LED_TASK);
    LED_PORT &= ~((1 << LED_STATUS) | (1 << LED_TASK));

    /* Reset counters */
    g_status_counter    = 0;
    g_task_counter      = 0;
    g_task_led_on_counter = 0;
    g_ext_counter       = 0;

    /* Reset flags */
    g_flag_status_led  = false;
    g_flag_task_led_on = false;
    g_flag_task_led_off = false;
    g_flag_ext_task    = false;
}

void scheduler_tick(void)
{
    /* ---- Status LED counter ---- */
    g_status_counter++;
    if (g_status_counter >= SCHED_STATUS_LED_TICKS) {
        g_status_counter = 0;
        g_flag_status_led = true;
    }

    /* ---- Task LED counter ---- */
    g_task_counter++;
    if (g_task_counter >= SCHED_TASK_LED_TICKS) {
        g_task_counter = 0;
        g_flag_task_led_on = true;
        g_task_led_on_counter = 0;  /* Reset on-duration counter */
    }

    /* ---- Extension Task counter (500 ms) ---- */
    g_ext_counter++;
    if (g_ext_counter >= SCHED_EXT_TASK_TICKS) {
        g_ext_counter = 0;
        g_flag_ext_task = true;
    }

    /*
     * If the task LED is currently ON, count how long it's been on.
     * After SCHED_TASK_LED_ON_TICKS ticks, flag it to be turned off.
     */
    if (g_task_led_on_counter < SCHED_TASK_LED_ON_TICKS &&
        (LED_PORT & (1 << LED_TASK))) {
        g_task_led_on_counter++;
        if (g_task_led_on_counter >= SCHED_TASK_LED_ON_TICKS) {
            g_flag_task_led_off = true;
        }
    }
}

void scheduler_run(void)
{
    /* ---- Status LED: toggle ---- */
    if (g_flag_status_led) {
        g_flag_status_led = false;
        LED_PORT ^= (1 << LED_STATUS);  /* XOR toggles the pin */
    }

    /* ---- Task LED: flash ON ---- */
    if (g_flag_task_led_on) {
        g_flag_task_led_on = false;
        LED_PORT |= (1 << LED_TASK);    /* Turn ON */
        display_message("TASK: SENSOR SAMPLE");
    }

    /* ---- Task LED: flash OFF ---- */
    if (g_flag_task_led_off) {
        g_flag_task_led_off = false;
        LED_PORT &= ~(1 << LED_TASK);   /* Turn OFF */
    }

    /* ---- Extension Task: 500ms heartbeat ---- */
    if (g_flag_ext_task) {
        g_flag_ext_task = false;
        display_message("[500ms Tick] Ext Task");
    }
}
