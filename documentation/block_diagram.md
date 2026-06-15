# 📊 System Block Diagram

> Visual representation of the ATmega32 Digital Clock & Task Scheduler system architecture, including hardware blocks, firmware modules, and signal flow.

---

## Table of Contents

- [High-Level System Block Diagram](#high-level-system-block-diagram)
- [Hardware Block Diagram](#hardware-block-diagram)
- [Firmware Architecture Diagram](#firmware-architecture-diagram)
- [Data Flow Diagram](#data-flow-diagram)
- [Interrupt and Scheduler Flow](#interrupt-and-scheduler-flow)
- [Signal Path Descriptions](#signal-path-descriptions)

---

## High-Level System Block Diagram

This diagram shows the complete system at the highest level of abstraction:

```mermaid
graph TB
    subgraph POWER["⚡ Power Supply"]
        PS["5V Regulated<br/>DC Supply"]
    end

    subgraph CLOCK_SRC["🔮 Clock Source"]
        XTAL["8 MHz Crystal<br/>+ 2×22pF Caps"]
    end

    subgraph INPUT["🔘 User Input"]
        BTN1["SET Button<br/>(PA0)"]
        BTN2["INC Button<br/>(PA1)"]
        BTN3["RESET Button<br/>(PA2)"]
    end

    subgraph MCU["🖥️ ATmega32 Microcontroller"]
        direction TB
        CORE["AVR CPU Core"]
        T1["Timer1<br/>CTC Mode"]
        USART["USART<br/>9600 Baud"]
        GPIO["GPIO Ports<br/>A, B, C, D"]
    end

    subgraph OUTPUT_VISUAL["💡 Visual Output"]
        LED1["Status LED<br/>(PB0)"]
        LED2["Task LED<br/>(PB1)"]
    end

    subgraph OUTPUT_SERIAL["📟 Serial Output"]
        UART_ADAPTER["USB-to-UART<br/>Adapter"]
        PC["PC / Terminal<br/>HH:MM:SS Display"]
    end

    subgraph PROGRAMMING["🔧 Programming"]
        ISP["ISP Programmer<br/>(USBasp)"]
    end

    PS --> MCU
    XTAL --> MCU
    BTN1 --> GPIO
    BTN2 --> GPIO
    BTN3 --> GPIO
    GPIO --> LED1
    GPIO --> LED2
    USART --> UART_ADAPTER
    UART_ADAPTER --> PC
    ISP -.->|"MOSI/MISO/SCK<br/>(PB5-PB7)"| MCU

    style MCU fill:#e1f5fe,stroke:#01579b,stroke-width:3px
    style POWER fill:#fff3e0,stroke:#e65100
    style CLOCK_SRC fill:#f3e5f5,stroke:#4a148c
    style INPUT fill:#e8f5e9,stroke:#1b5e20
    style OUTPUT_VISUAL fill:#fff9c4,stroke:#f57f17
    style OUTPUT_SERIAL fill:#fce4ec,stroke:#880e4f
    style PROGRAMMING fill:#efebe9,stroke:#3e2723
```

---

## Hardware Block Diagram

This diagram details the physical hardware connections and electrical interfaces:

```mermaid
graph LR
    subgraph POWER_SECTION["Power Section"]
        VCC["VCC (Pin 10)<br/>+5V"]
        GND["GND (Pin 11)<br/>0V"]
        AVCC["AVCC (Pin 30)<br/>+5V"]
        AGND["AGND (Pin 31)<br/>0V"]
        DECAP["100nF<br/>Decoupling Cap"]
    end

    subgraph RESET_SECTION["Reset Circuit"]
        RPULLUP["10kΩ<br/>Pull-up"]
        RCAP["100nF<br/>Filter Cap"]
        RSTPIN["RESET (Pin 9)"]
    end

    subgraph OSCILLATOR["Oscillator Circuit"]
        CRYSTAL["8 MHz<br/>Crystal"]
        C1["22pF<br/>C1"]
        C2["22pF<br/>C2"]
        XTAL1["XTAL1 (Pin 13)"]
        XTAL2["XTAL2 (Pin 12)"]
    end

    subgraph BUTTONS["Button Inputs (Active Low)"]
        SET["SET<br/>Push Button"]
        INC["INC<br/>Push Button"]
        RST["RESET<br/>Push Button"]
        PA0["PA0 (Pin 40)"]
        PA1["PA1 (Pin 39)"]
        PA2["PA2 (Pin 38)"]
    end

    subgraph LEDS["LED Outputs"]
        R1["330Ω"]
        R2["330Ω"]
        SLED["Status<br/>LED"]
        TLED["Task<br/>LED"]
        PB0["PB0 (Pin 1)"]
        PB1["PB1 (Pin 2)"]
    end

    subgraph SERIAL["USART Interface"]
        PD0["PD0/RXD (Pin 14)"]
        PD1["PD1/TXD (Pin 15)"]
        FTDI["USB-UART<br/>Adapter"]
    end

    VCC --- DECAP --- GND
    VCC --- RPULLUP --- RSTPIN
    RSTPIN --- RCAP --- GND

    CRYSTAL --- XTAL1
    CRYSTAL --- XTAL2
    XTAL1 --- C1 --- GND
    XTAL2 --- C2 --- GND

    SET --- PA0
    INC --- PA1
    RST --- PA2

    PB0 --- R1 --- SLED
    PB1 --- R2 --- TLED

    PD0 --- FTDI
    PD1 --- FTDI
```

---

## Firmware Architecture Diagram

This diagram shows the software module hierarchy and dependencies:

```mermaid
graph TB
    subgraph APP["Application Layer"]
        MAIN["main.c<br/>Main Loop &<br/>Initialization"]
    end

    subgraph SCHED_LAYER["Scheduler Layer"]
        SCHED["scheduler.c/.h<br/>Task Flag Polling<br/>& Dispatch"]
    end

    subgraph MODULE_LAYER["Module Layer"]
        CLOCK["clock.c/.h<br/>HH:MM:SS Logic<br/>Inc/Set/Reset"]
        BTNMOD["buttons.c/.h<br/>Read & Debounce<br/>Active-Low Logic"]
        LEDMOD["leds.c/.h<br/>Toggle & Flash<br/>Control"]
        UARTMOD["usart.c/.h<br/>9600 8N1<br/>TX String/Char"]
    end

    subgraph DRIVER_LAYER["Hardware Abstraction"]
        TIMER["timer.c/.h<br/>Timer1 CTC Init<br/>ISR Flags"]
        CONFIG["config.h<br/>Pin Definitions<br/>F_CPU, Constants"]
    end

    subgraph AVR_LAYER["AVR Libraries"]
        AVRIO["avr/io.h"]
        AVRINT["avr/interrupt.h"]
        UTIL["util/delay.h"]
    end

    MAIN --> SCHED
    MAIN --> CLOCK
    MAIN --> BTNMOD
    MAIN --> LEDMOD
    MAIN --> UARTMOD
    MAIN --> TIMER

    SCHED --> CLOCK
    SCHED --> LEDMOD
    SCHED --> TIMER

    CLOCK --> UARTMOD
    BTNMOD --> CLOCK
    LEDMOD --> CONFIG
    UARTMOD --> CONFIG

    TIMER --> CONFIG
    TIMER --> AVRINT
    CONFIG --> AVRIO
    UARTMOD --> AVRIO
    BTNMOD --> UTIL

    style APP fill:#bbdefb,stroke:#1565c0,stroke-width:2px
    style SCHED_LAYER fill:#c8e6c9,stroke:#2e7d32,stroke-width:2px
    style MODULE_LAYER fill:#fff9c4,stroke:#f9a825,stroke-width:2px
    style DRIVER_LAYER fill:#ffccbc,stroke:#bf360c,stroke-width:2px
    style AVR_LAYER fill:#e0e0e0,stroke:#424242,stroke-width:2px
```

---

## Data Flow Diagram

This diagram traces the flow of data through the system:

```mermaid
graph LR
    subgraph ISR_CONTEXT["ISR Context (Timer1)"]
        TICK["Timer1<br/>Compare Match"]
        FLAGS["Scheduler Flags<br/>tick_flag<br/>led_status_flag<br/>led_task_flag"]
    end

    subgraph MAIN_CONTEXT["Main Loop Context"]
        POLL["Flag<br/>Polling"]
        CLK_UPDATE["Clock<br/>Update"]
        LED_CTRL["LED<br/>Control"]
        BTN_READ["Button<br/>Read"]
        FORMAT["Format<br/>HH:MM:SS"]
        TX["USART<br/>Transmit"]
    end

    subgraph HW_OUTPUT["Hardware Output"]
        LEDS_HW["LEDs<br/>PB0, PB1"]
        UART_HW["USART<br/>TXD Pin"]
        TERMINAL["Serial<br/>Terminal"]
    end

    subgraph HW_INPUT["Hardware Input"]
        BTNS_HW["Buttons<br/>PA0-PA2"]
    end

    TICK -->|"Set flags"| FLAGS
    FLAGS -->|"Read & clear"| POLL
    POLL -->|"tick_flag"| CLK_UPDATE
    POLL -->|"led_*_flag"| LED_CTRL
    CLK_UPDATE --> FORMAT
    FORMAT --> TX
    TX --> UART_HW --> TERMINAL
    LED_CTRL --> LEDS_HW
    BTNS_HW --> BTN_READ
    BTN_READ -->|"SET/INC/RESET<br/>commands"| CLK_UPDATE

    style ISR_CONTEXT fill:#ffcdd2,stroke:#c62828,stroke-width:2px
    style MAIN_CONTEXT fill:#dcedc8,stroke:#33691e,stroke-width:2px
```

---

## Interrupt and Scheduler Flow

This diagram details how the ISR and main-loop scheduler interact:

```mermaid
sequenceDiagram
    participant T1 as Timer1 Hardware
    participant ISR as TIMER1_COMPA ISR
    participant FLAGS as Volatile Flags
    participant MAIN as Main Loop
    participant CLK as Clock Module
    participant LED as LED Module
    participant UART as USART Module

    Note over T1: TCNT1 counts 0→7812

    T1->>ISR: Compare Match Interrupt
    activate ISR
    ISR->>FLAGS: tick_flag = 1
    ISR->>FLAGS: isr_counter++
    alt isr_counter % 2 == 0
        ISR->>FLAGS: led_status_flag = 1
    end
    alt isr_counter % 5 == 0
        ISR->>FLAGS: led_task_flag = 1
    end
    deactivate ISR

    Note over MAIN: Continuous polling loop

    MAIN->>FLAGS: Check tick_flag
    alt tick_flag == 1
        MAIN->>FLAGS: tick_flag = 0
        MAIN->>CLK: Increment seconds
        CLK->>CLK: Handle rollover (s→m→h)
        CLK->>UART: Send formatted "HH:MM:SS"
        UART->>UART: Transmit via TXD
    end

    MAIN->>FLAGS: Check led_status_flag
    alt led_status_flag == 1
        MAIN->>FLAGS: led_status_flag = 0
        MAIN->>LED: Toggle PB0
    end

    MAIN->>FLAGS: Check led_task_flag
    alt led_task_flag == 1
        MAIN->>FLAGS: led_task_flag = 0
        MAIN->>LED: Flash PB1
    end

    Note over T1: Cycle repeats every ~1s
```

---

## Signal Path Descriptions

### Clock Signal Path

```
8 MHz Crystal → XTAL1/XTAL2 → System Clock (clk_IO)
    → Prescaler (/1024) → Timer1 Clock (7812.5 Hz)
    → TCNT1 counts 0→7812 → Compare Match
    → OCF1A Flag → ISR → tick_flag
    → Main Loop → Clock Module → USART TX → Terminal
```

### Button Signal Path

```
User Press → Button closes to GND → PA0/PA1/PA2 reads LOW
    → Software polls PINx register → Debounce delay
    → Command decoded (SET/INC/RESET)
    → Clock Module updates time fields
    → Updated time sent to USART
```

### LED Signal Path

```
Timer1 ISR → Scheduler flag (led_status_flag / led_task_flag)
    → Main Loop detects flag → LED Module called
    → PORTx bit toggled/set → GPIO pin drives HIGH
    → 330Ω resistor → LED → GND (current flows, LED lights)
```

### ISP Programming Path

```
PC (avrdude) → USB → USBasp Programmer
    → SPI Bus: MOSI (PB5), MISO (PB6), SCK (PB7), RESET
    → ATmega32 Flash memory programmed
```

---

## Legend

| Symbol | Meaning |
|--------|---------|
| Solid arrow (→) | Data/signal flow |
| Dashed arrow (-.->)| Programming/debug connection |
| Blue block | Core/application layer |
| Green block | Scheduler/logic layer |
| Yellow block | Functional modules |
| Red/orange block | Hardware drivers |
| Gray block | External libraries |

---

*← Back to [Test Results](test_results.md) | Next: [Flowchart](flowchart.md) →*
