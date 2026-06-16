# 🔄 Program Flowcharts

> Detailed flowcharts illustrating the program logic, interrupt service routine, clock update algorithm, button handling state machine, and task scheduler for the ATmega32 Digital Clock & Task Scheduler.

---

## Table of Contents

- [Main Program Flowchart](#main-program-flowchart)
- [System Initialization Flowchart](#system-initialization-flowchart)
- [Timer1 ISR Flowchart](#timer1-isr-flowchart)
- [Clock Update Algorithm](#clock-update-algorithm)
- [Time-Set Mode State Machine](#time-set-mode-state-machine)
- [Task Scheduler Flowchart](#task-scheduler-flowchart)
- [USART Transmission Flowchart](#usart-transmission-flowchart)
- [Button Read and Debounce Flowchart](#button-read-and-debounce-flowchart)

---

## Main Program Flowchart

The top-level program flow from power-on through the infinite main loop:

```mermaid
flowchart TD
    START(["🔌 Power On / Reset"]) --> INIT["System Initialization<br/>• ports_init()<br/>• timer1_init()<br/>• usart_init()<br/>• Print startup banner"]
    INIT --> SEI["Enable Global Interrupts<br/>sei()"]
    SEI --> LOOP_START{{"♻️ Main Loop Start"}}

    LOOP_START --> CHECK_TICK{"tick_flag<br/>== 1?"}

    CHECK_TICK -->|Yes| CLEAR_TICK["tick_flag = 0"]
    CLEAR_TICK --> UPDATE_CLOCK["Update Clock<br/>seconds++<br/>Handle rollovers"]
    UPDATE_CLOCK --> SEND_TIME["Send HH:MM:SS<br/>via USART"]
    SEND_TIME --> CHECK_STATUS

    CHECK_TICK -->|No| CHECK_STATUS{"led_status_flag<br/>== 1?"}

    CHECK_STATUS -->|Yes| CLEAR_STATUS["led_status_flag = 0"]
    CLEAR_STATUS --> TOGGLE_LED["Toggle Status LED<br/>PB0 ^= 1"]
    TOGGLE_LED --> CHECK_TASK

    CHECK_STATUS -->|No| CHECK_TASK{"led_task_flag<br/>== 1?"}

    CHECK_TASK -->|Yes| CLEAR_TASK["led_task_flag = 0"]
    CLEAR_TASK --> FLASH_LED["Flash Task LED<br/>PB1 ON → delay → OFF"]
    FLASH_LED --> CHECK_BUTTONS

    CHECK_TASK -->|No| CHECK_BUTTONS["Read Buttons<br/>buttons_read()"]

    CHECK_BUTTONS --> BTN_SET{"SET button<br/>pressed?"}
    BTN_SET -->|Yes| HANDLE_SET["Handle SET:<br/>Cycle time-set field"]
    BTN_SET -->|No| BTN_INC{"INC button<br/>pressed?"}

    HANDLE_SET --> LOOP_START

    BTN_INC -->|Yes| HANDLE_INC["Handle INC:<br/>Increment selected field"]
    BTN_INC -->|No| BTN_RST{"RESET button<br/>pressed?"}

    HANDLE_INC --> LOOP_START

    BTN_RST -->|Yes| HANDLE_RST["Handle RESET:<br/>Clock → 00:00:00"]
    BTN_RST -->|No| LOOP_START

    HANDLE_RST --> LOOP_START

    style START fill:#4caf50,color:#fff,stroke:#2e7d32
    style LOOP_START fill:#2196f3,color:#fff,stroke:#1565c0
    style CHECK_TICK fill:#fff3e0,stroke:#e65100
    style CHECK_STATUS fill:#fff3e0,stroke:#e65100
    style CHECK_TASK fill:#fff3e0,stroke:#e65100
```

---

## System Initialization Flowchart

Detailed initialization sequence executed once at startup:

```mermaid
flowchart TD
    START(["System Init"]) --> PORT_INIT["Port Initialization"]

    PORT_INIT --> PORTA_CFG["Configure Port A<br/>DDRA = 0x00 (inputs)<br/>PORTA = 0x07 (pull-ups PA0-PA2)"]
    PORTA_CFG --> PORTB_CFG["Configure Port B<br/>DDRB = 0x03 (PB0,PB1 outputs)<br/>PORTB = 0x00 (LEDs off)"]
    PORTB_CFG --> TIMER_INIT["Timer1 Initialization"]

    TIMER_INIT --> T1_CTC["Set CTC Mode<br/>TCCR1A = 0x00<br/>TCCR1B = (1<<WGM12)|(1<<CS12)|(1<<CS10)"]
    T1_CTC --> T1_OCR["Set Compare Value<br/>OCR1A = 1249"]
    T1_OCR --> T1_CNT["Reset Counter<br/>TCNT1 = 0"]
    T1_CNT --> T1_INT["Enable Interrupt<br/>TIMSK |= (1<<OCIE1A)"]
    T1_INT --> USART_INIT["USART Initialization"]

    USART_INIT --> U_BAUD["Set Baud Rate<br/>UBRRL = 51 (9600 @ 8MHz)<br/>UBRRH = 0"]
    U_BAUD --> U_CTRL["Enable TX/RX<br/>UCSRB = (1<<TXEN)|(1<<RXEN)"]
    U_CTRL --> U_FMT["Set Frame Format<br/>UCSRC = 8-bit, 1 stop, no parity"]
    U_FMT --> VARS_INIT["Initialize Variables<br/>hours = 0, minutes = 0<br/>seconds = 0, mode = NORMAL"]
    VARS_INIT --> BANNER["Print Startup Banner<br/>via USART"]
    BANNER --> DONE(["Init Complete<br/>→ Enable sei()"])

    style START fill:#ff9800,color:#fff
    style DONE fill:#4caf50,color:#fff
```

---

## Timer1 ISR Flowchart

The interrupt service routine that fires every ~1 second:

```mermaid
flowchart TD
    ENTRY(["⚡ TIMER1_COMPA_vect<br/>ISR Entry"]) --> SAVE["Hardware auto-saves<br/>SREG, PC"]
    SAVE --> INC_CTR["isr_counter++"]
    INC_CTR --> SET_TICK["tick_flag = 1"]

    SET_TICK --> CHECK_2S{"isr_counter<br/>% 2 == 0?"}
    CHECK_2S -->|Yes| SET_LED_S["led_status_flag = 1"]
    CHECK_2S -->|No| CHECK_5S

    SET_LED_S --> CHECK_5S{"isr_counter<br/>% 5 == 0?"}
    CHECK_5S -->|Yes| SET_LED_T["led_task_flag = 1"]
    CHECK_5S -->|No| CHECK_WRAP

    SET_LED_T --> CHECK_WRAP{"isr_counter<br/>>= 10?"}
    CHECK_WRAP -->|Yes| RESET_CTR["isr_counter = 0"]
    CHECK_WRAP -->|No| EXIT

    RESET_CTR --> EXIT(["ISR Exit<br/>Restore SREG, RETI"])

    style ENTRY fill:#f44336,color:#fff,stroke:#b71c1c
    style EXIT fill:#f44336,color:#fff,stroke:#b71c1c
    style SET_TICK fill:#e8f5e9,stroke:#2e7d32
    style SET_LED_S fill:#e8f5e9,stroke:#2e7d32
    style SET_LED_T fill:#e8f5e9,stroke:#2e7d32
```

### ISR Execution Timeline

```mermaid
gantt
    title ISR Flag Setting Over 10 Seconds
    dateFormat X
    axisFormat %s

    section tick_flag
    t=1s  :a1, 1, 2
    t=2s  :a2, 2, 3
    t=3s  :a3, 3, 4
    t=4s  :a4, 4, 5
    t=5s  :a5, 5, 6
    t=6s  :a6, 6, 7
    t=7s  :a7, 7, 8
    t=8s  :a8, 8, 9
    t=9s  :a9, 9, 10
    t=10s :a10, 10, 11

    section led_status_flag
    t=2s  :crit, b1, 2, 3
    t=4s  :crit, b2, 4, 5
    t=6s  :crit, b3, 6, 7
    t=8s  :crit, b4, 8, 9
    t=10s :crit, b5, 10, 11

    section led_task_flag
    t=5s  :active, c1, 5, 6
    t=10s :active, c2, 10, 11
```

---

## Clock Update Algorithm

The step-by-step process for updating the HH:MM:SS clock:

```mermaid
flowchart TD
    START(["Clock Update<br/>Called when tick_flag = 1"]) --> INC_SEC["seconds++"]

    INC_SEC --> CHECK_SEC{"seconds<br/>>= 60?"}
    CHECK_SEC -->|No| FORMAT["Format output string<br/>sprintf: HH:MM:SS"]
    CHECK_SEC -->|Yes| RESET_SEC["seconds = 0"]

    RESET_SEC --> INC_MIN["minutes++"]
    INC_MIN --> CHECK_MIN{"minutes<br/>>= 60?"}
    CHECK_MIN -->|No| FORMAT
    CHECK_MIN -->|Yes| RESET_MIN["minutes = 0"]

    RESET_MIN --> INC_HR["hours++"]
    INC_HR --> CHECK_HR{"hours<br/>>= 24?"}
    CHECK_HR -->|No| FORMAT
    CHECK_HR -->|Yes| RESET_HR["hours = 0<br/>(midnight rollover)"]

    RESET_HR --> FORMAT
    FORMAT --> SEND["Send via USART<br/>'[CLOCK] HH:MM:SS\\r\\n'"]
    SEND --> DONE(["Return"])

    style START fill:#2196f3,color:#fff
    style DONE fill:#2196f3,color:#fff
    style RESET_HR fill:#ffcdd2,stroke:#c62828
```

### Clock Value Ranges

```mermaid
graph LR
    subgraph HOURS["Hours"]
        H["0 → 1 → 2 → ... → 22 → 23 → 0"]
    end
    subgraph MINUTES["Minutes"]
        M["0 → 1 → 2 → ... → 58 → 59 → 0"]
    end
    subgraph SECONDS["Seconds"]
        S["0 → 1 → 2 → ... → 58 → 59 → 0"]
    end

    S -->|"carry"| M
    M -->|"carry"| H
```

---

## Time-Set Mode State Machine

The SET button cycles through a state machine for setting the time:

```mermaid
stateDiagram-v2
    [*] --> NORMAL

    NORMAL --> SET_HOURS : SET Button Press
    SET_HOURS --> SET_MINUTES : SET Button Press
    SET_MINUTES --> SET_SECONDS : SET Button Press
    SET_SECONDS --> NORMAL : SET Button Press

    state NORMAL {
        [*] --> Running
        Running : Clock counting normally
        Running : INC button: no effect
        Running : Display: HH:MM:SS
    }

    state SET_HOURS {
        [*] --> HoursSelected
        HoursSelected : Hours field highlighted
        HoursSelected : INC button: hours++
        HoursSelected : Wraps: 23 → 0
    }

    state SET_MINUTES {
        [*] --> MinutesSelected
        MinutesSelected : Minutes field highlighted
        MinutesSelected : INC button: minutes++
        MinutesSelected : Wraps: 59 → 0
    }

    state SET_SECONDS {
        [*] --> SecondsSelected
        SecondsSelected : Seconds field highlighted
        SecondsSelected : INC button: seconds++
        SecondsSelected : Wraps: 59 → 0
    }

    note right of NORMAL
        RESET button returns
        to NORMAL from any
        state and sets
        time to 00:00:00
    end note
```

### State Transition Table

| Current State | SET Pressed | INC Pressed | RESET Pressed |
|--------------|-------------|-------------|---------------|
| **NORMAL** | → SET_HOURS | No effect | Reset to 00:00:00 |
| **SET_HOURS** | → SET_MINUTES | hours++ (wrap 23→0) | Reset to 00:00:00, → NORMAL |
| **SET_MINUTES** | → SET_SECONDS | minutes++ (wrap 59→0) | Reset to 00:00:00, → NORMAL |
| **SET_SECONDS** | → NORMAL | seconds++ (wrap 59→0) | Reset to 00:00:00, → NORMAL |

### State Implementation

```mermaid
flowchart TD
    READ["Read SET button<br/>(PA0 LOW = pressed)"] --> PRESSED{"SET pressed<br/>(with debounce)?"}
    PRESSED -->|No| EXIT(["Return<br/>No state change"])
    PRESSED -->|Yes| GET_STATE{"Current<br/>mode?"}

    GET_STATE -->|NORMAL| TO_HOURS["mode = SET_HOURS<br/>Display: >HH<:MM:SS"]
    GET_STATE -->|SET_HOURS| TO_MINUTES["mode = SET_MINUTES<br/>Display: HH:>MM<:SS"]
    GET_STATE -->|SET_MINUTES| TO_SECONDS["mode = SET_SECONDS<br/>Display: HH:MM:>SS<"]
    GET_STATE -->|SET_SECONDS| TO_NORMAL["mode = NORMAL<br/>Display: HH:MM:SS<br/>Resume counting"]

    TO_HOURS --> EXIT
    TO_MINUTES --> EXIT
    TO_SECONDS --> EXIT
    TO_NORMAL --> EXIT
```

---

## Task Scheduler Flowchart

The cooperative task scheduler main loop logic:

```mermaid
flowchart TD
    ENTRY(["Scheduler<br/>Main Loop Iteration"]) --> T1{"tick_flag?"}

    T1 -->|"1"| T1_HANDLE["Task 1: Clock Tick<br/>• Clear flag<br/>• Increment time<br/>• Format HH:MM:SS<br/>• Send via USART"]
    T1 -->|"0"| T2

    T1_HANDLE --> T2{"led_status_flag?"}

    T2 -->|"1"| T2_HANDLE["Task 2: Status LED<br/>• Clear flag<br/>• Toggle PB0<br/>• Log to USART"]
    T2 -->|"0"| T3

    T2_HANDLE --> T3{"led_task_flag?"}

    T3 -->|"1"| T3_HANDLE["Task 3: Task LED<br/>• Clear flag<br/>• Flash PB1<br/>  (ON → 100ms → OFF)<br/>• Log to USART"]
    T3 -->|"0"| T4

    T3_HANDLE --> T4["Task 4: Button Scan<br/>• Read PA0, PA1, PA2<br/>• Debounce check<br/>• Execute command"]

    T4 --> ENTRY

    style T1_HANDLE fill:#bbdefb,stroke:#1565c0
    style T2_HANDLE fill:#c8e6c9,stroke:#2e7d32
    style T3_HANDLE fill:#fff9c4,stroke:#f9a825
    style T4 fill:#e1bee7,stroke:#6a1b9a
```

### Task Priority and Timing

```mermaid
graph TB
    subgraph PRIORITY["Task Priority (Highest to Lowest)"]
        direction TB
        P1["🔴 Priority 1: Clock Tick<br/>Period: 1s | Critical for timekeeping"]
        P2["🟡 Priority 2: Status LED<br/>Period: 2s | Visual heartbeat"]
        P3["🟢 Priority 3: Task LED<br/>Period: 5s | Activity indicator"]
        P4["🔵 Priority 4: Button Scan<br/>Period: Every loop | User responsiveness"]
    end

    P1 --> P2 --> P3 --> P4
```

---

## USART Transmission Flowchart

The process for transmitting a single character and a formatted time string:

```mermaid
flowchart TD
    subgraph CHAR_TX["Single Character Transmission"]
        C_START(["usart_putchar(c)"]) --> C_WAIT{"UDRE flag<br/>set in UCSRA?"}
        C_WAIT -->|No| C_WAIT
        C_WAIT -->|Yes| C_WRITE["Write c to UDR"]
        C_WRITE --> C_DONE(["Return"])
    end

    subgraph STRING_TX["String Transmission"]
        S_START(["usart_puts(str)"]) --> S_CHECK{"*str != '\\0'?"}
        S_CHECK -->|Yes| S_SEND["usart_putchar(*str)"]
        S_SEND --> S_INC["str++"]
        S_INC --> S_CHECK
        S_CHECK -->|No| S_DONE(["Return"])
    end

    subgraph TIME_TX["Time Display Transmission"]
        T_START(["send_time(h, m, s)"]) --> T_FMT["Format string:<br/>'[CLOCK] HH:MM:SS\\r\\n'"]
        T_FMT --> T_SEND["usart_puts(formatted)"]
        T_SEND --> T_DONE(["Return"])
    end

    style CHAR_TX fill:#e3f2fd,stroke:#1565c0
    style STRING_TX fill:#f1f8e9,stroke:#33691e
    style TIME_TX fill:#fce4ec,stroke:#880e4f
```

### USART Configuration Summary

```mermaid
graph LR
    subgraph USART_CFG["USART Configuration"]
        BAUD["Baud Rate<br/>9600"]
        BITS["Data Bits<br/>8"]
        PARITY["Parity<br/>None"]
        STOP["Stop Bits<br/>1"]
        UBRR["UBRR Value<br/>51"]
    end

    BAUD --- BITS --- PARITY --- STOP
```

**UBRR Calculation:**
```
UBRR = (F_CPU / (16 × BAUD)) - 1
UBRR = (8,000,000 / (16 × 9600)) - 1
UBRR = (8,000,000 / 153,600) - 1
UBRR = 52.08 - 1
UBRR = 51
```

---

## Button Read and Debounce Flowchart

```mermaid
flowchart TD
    START(["Button Scan (Non-blocking)"]) --> READ_PIN["Read raw state from PINA"]
    READ_PIN --> CHECK_STABLE{"raw ==<br/>g_last_stable?"}

    CHECK_STABLE -->|Yes| INC_CNT["g_debounce_cnt++"]
    CHECK_STABLE -->|No| RESET_CNT["g_debounce_cnt = 0<br/>g_last_stable = raw"]

    INC_CNT --> CHECK_THRESH{"g_debounce_cnt<br/>== 5?"}
    CHECK_THRESH -->|Yes| EDGE_DETECT["Detect falling edges<br/>(pressed events)"]
    CHECK_THRESH -->|No| DONE
    
    RESET_CNT --> DONE
    
    EDGE_DETECT --> SET_EVENT_SET{"SET pressed?"}
    SET_EVENT_SET -->|Yes| QUEUE_SET["Queue BTN_SET event"]
    SET_EVENT_SET -->|No| SET_EVENT_INC
    
    QUEUE_SET --> SET_EVENT_INC
    
    SET_EVENT_INC{"INC pressed?"}
    SET_EVENT_INC -->|Yes| QUEUE_INC["Queue BTN_INC event"]
    SET_EVENT_INC -->|No| SET_EVENT_RST
    
    QUEUE_INC --> SET_EVENT_RST
    
    SET_EVENT_RST{"RESET pressed?"}
    SET_EVENT_RST -->|Yes| QUEUE_RST["Queue BTN_RESET event"]
    SET_EVENT_RST -->|No| UPDATE_STATE
    
    QUEUE_RST --> UPDATE_STATE
    
    UPDATE_STATE["g_debounced_state = raw"] --> DONE

    DONE(["Return to Main Loop"])

    style START fill:#9c27b0,color:#fff
    style DONE fill:#9c27b0,color:#fff
    style QUEUE_SET fill:#e8f5e9,stroke:#2e7d32
    style QUEUE_INC fill:#e8f5e9,stroke:#2e7d32
    style QUEUE_RST fill:#ffcdd2,stroke:#c62828
```

---

## Complete System Timing Diagram

A combined view of all system events over a 10-second window:

```
Time (s):  0    1    2    3    4    5    6    7    8    9   10
           |    |    |    |    |    |    |    |    |    |    |
Clock:     00   01   02   03   04   05   06   07   08   09   10
           ├────┤────┤────┤────┤────┤────┤────┤────┤────┤────┤

Status     OFF  OFF  ON   ON   OFF  OFF  ON   ON   OFF  OFF  ON
LED(PB0):  ─────┘    └────┘    └────┘    └────┘    └────┘    └──
                ↑         ↑         ↑         ↑         ↑
              toggle    toggle    toggle    toggle    toggle
              (t=2)     (t=4)     (t=6)     (t=8)     (t=10)

Task       OFF  OFF  OFF  OFF  OFF  ██   OFF  OFF  OFF  OFF  ██
LED(PB1):  ──────────────────────┘  └──────────────────────┘  └─
                                ↑                          ↑
                              flash                      flash
                              (t=5)                      (t=10)

ISR_CTR:   1    2    3    4    5    6    7    8    9   10→0  1
```

---

*← Back to [Block Diagram](block_diagram.md) | Return to [README](../README.md) →*
