/**
 * @file display.c
 * @brief USART display driver – outputs HH:MM:SS clock via serial
 *
 * Configures the ATmega32 USART for 9600 baud, 8-N-1 transmission.
 * Provides helper functions for character, string, and formatted
 * clock-time output.
 *
 * UBRR calculation (from config.h):
 *   UBRR = F_CPU / (16 * BAUD) - 1
 *        = 8 000 000 / (16 * 9600) - 1
 *        = 51.08  →  51
 *   Actual baud = 8 000 000 / (16 * 52) = 9615  (0.16 % error)
 */

#include <avr/io.h>
#include <stdio.h>

#include "config.h"
#include "display.h"

/* ================================================================== */
/*  Public API                                                        */
/* ================================================================== */

void usart_init(void)
{
    /*
     * 1. Set baud rate – load UBRRH:UBRRL with the computed value.
     *    ATmega32 shares UBRRH with UCSRC; bit URSEL selects which
     *    register is written.  Writing UBRRH requires URSEL = 0.
     */
    UBRRH = (uint8_t)(USART_UBRR_VAL >> 8);
    UBRRL = (uint8_t)(USART_UBRR_VAL);

    /*
     * 2. Enable transmitter (and receiver for possible future use).
     *    TXEN  – enable transmitter
     *    RXEN  – enable receiver
     */
    UCSRB = (1 << TXEN) | (1 << RXEN);

    /*
     * 3. Set frame format: 8 data bits, no parity, 1 stop bit (8N1).
     *    URSEL must be 1 to write to UCSRC (shared address with UBRRH).
     *    UCSZ1:UCSZ0 = 11  →  8-bit character size
     */
    UCSRC = (1 << URSEL) | (1 << UCSZ1) | (1 << UCSZ0);
}

void usart_putchar(char c)
{
    /* Wait until the transmit buffer is empty (UDRE flag set) */
    while (!(UCSRA & (1 << UDRE)))
        ;
    UDR = c;
}

void usart_puts(const char *s)
{
    while (*s) {
        usart_putchar(*s++);
    }
}

/**
 * @brief  Helper – output a two-digit decimal number (00–99).
 * @param  val  Value to print (clamped to 0–99).
 */
static void usart_put_two_digits(uint8_t val)
{
    usart_putchar('0' + (val / 10));
    usart_putchar('0' + (val % 10));
}

void display_time(clock_time_t t)
{
    /*
     * Format: "HH:MM:SS\r\n"
     *
     * Carriage return (\r) allows terminals that support it to
     * overwrite the current line; newline (\n) provides scrolling
     * on terminals that don't.
     */
    usart_puts("TIME: ");
    usart_put_two_digits(t.hours);
    usart_putchar(':');
    usart_put_two_digits(t.minutes);
    usart_putchar(':');
    usart_put_two_digits(t.seconds);
    usart_puts("\r\n");
}

void display_message(const char *msg)
{
    usart_puts(msg);
    usart_puts("\r\n");
}
