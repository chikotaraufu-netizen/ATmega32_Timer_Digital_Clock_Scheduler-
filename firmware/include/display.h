/**
 * @file display.h
 * @brief USART display driver – outputs HH:MM:SS clock via serial
 *
 * Uses the ATmega32 USART peripheral at 9600 baud, 8N1 to transmit
 * the current clock time in human-readable format.
 */

#ifndef DISPLAY_H
#define DISPLAY_H

#include "timer.h"  /* for clock_time_t */

/**
 * @brief  Initialise the USART peripheral (9600 baud, 8N1, TX only).
 */
void usart_init(void);

/**
 * @brief  Transmit a single character (blocking).
 * @param  c  Character to send.
 */
void usart_putchar(char c);

/**
 * @brief  Transmit a null-terminated string.
 * @param  s  Pointer to the string.
 */
void usart_puts(const char *s);

/**
 * @brief  Display the clock time as "HH:MM:SS\r\n" on the USART.
 * @param  t  The time to display.
 *
 * Uses carriage-return + newline so serial terminals overwrite the
 * same line or scroll as appropriate.
 */
void display_time(clock_time_t t);

/**
 * @brief  Display a status message string on the USART.
 * @param  msg  Null-terminated message string.
 */
void display_message(const char *msg);

#endif /* DISPLAY_H */
