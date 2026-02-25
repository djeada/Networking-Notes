# Data Link Layer

The Data Link Layer (Layer 2) is responsible for node-to-node data transfer between
directly connected devices. It handles framing, error detection/correction, flow control,
and media access control. This layer sits between the Physical Layer (Layer 1) and the
Network Layer (Layer 3) in the OSI model.

---

## Sublayers

The Data Link Layer is divided into two sublayers:

- **LLC (Logical Link Control)** — defined by IEEE 802.2, handles flow control and
  error checking. It provides a uniform interface to the Network Layer regardless of
  the underlying physical medium.
- **MAC (Media Access Control)** — handles addressing (MAC addresses) and controls
  how devices on the network gain access to the medium.

```text
+--------------------------------------------------+
|              Network Layer (Layer 3)              |
+--------------------------------------------------+
|   Logical Link Control (LLC) sublayer             |
|   - Flow control                                  |
|   - Error detection                               |
|   - Multiplexing of protocols                     |
+--------------------------------------------------+
|   Media Access Control (MAC) sublayer             |
|   - MAC addressing                                |
|   - Frame delimiting                              |
|   - Media access (CSMA/CD, Token Ring, etc.)      |
+--------------------------------------------------+
|              Physical Layer (Layer 1)              |
+--------------------------------------------------+
```

---

## Flow Control

Flow control ensures a fast sender does not overwhelm a slow receiver. The key
parameter is:

- **a = Tp / Tt** (propagation delay divided by transmission delay)
- **Sender's Window Size = N**
- **Sequence Number requirement**: Seq No >= Sender Window + Receiver Window

### Stop-and-Wait

The sender transmits one frame, then waits for an acknowledgement (ACK) before
sending the next frame.

- **Efficiency = 1 / (1 + 2a)**
- Sender window size = 1, Receiver window size = 1

```text
Sender                          Receiver
  |                                |
  |---- Frame 0 ------------------>|
  |                                |
  |<-------------- ACK 0 ---------|
  |                                |
  |---- Frame 1 ------------------>|
  |                                |
  |<-------------- ACK 1 ---------|
  |                                |

  Time -->
  |<-- Tt -->|<----- 2 * Tp ----->|
  [  Frame   ][   Wait for ACK    ]
```

### Go-Back-N (GBN)

The sender can transmit up to N frames without waiting for an ACK. If a frame is
lost, the sender retransmits that frame and ALL subsequent frames.

- **Efficiency = N / (1 + 2a)** when N < (1 + 2a), otherwise 1
- Sender window size = N, Receiver window size = 1
- Sequence numbers needed >= N + 1

```text
Sender                              Receiver
  |                                    |
  |---- Frame 0 ---------------------->|  ACK 0
  |---- Frame 1 ---------------------->|  ACK 1
  |---- Frame 2 ---X  (lost)          |
  |---- Frame 3 ---------------------->|  Discarded (expects 2)
  |---- Frame 4 ---------------------->|  Discarded (expects 2)
  |                                    |
  |<------------ NAK 2 ---------------|
  |                                    |
  |---- Frame 2 ---------------------->|  ACK 2  (retransmit from 2)
  |---- Frame 3 ---------------------->|  ACK 3
  |---- Frame 4 ---------------------->|  ACK 4
  |                                    |
```

### Selective Repeat (SR)

The sender can transmit up to N frames. Only the specific lost or errored frames
are retransmitted, not the entire window.

- **Efficiency = N / (1 + 2a)** when N < (1 + 2a), otherwise 1
- Sender window size = N, Receiver window size = N
- Sequence numbers needed >= 2N

```text
Sender                              Receiver
  |                                    |
  |---- Frame 0 ---------------------->|  ACK 0
  |---- Frame 1 ---------------------->|  ACK 1
  |---- Frame 2 ---X  (lost)          |
  |---- Frame 3 ---------------------->|  Buffered, ACK 3
  |---- Frame 4 ---------------------->|  Buffered, ACK 4
  |                                    |
  |<------------ NAK 2 ---------------|
  |                                    |
  |---- Frame 2 ---------------------->|  ACK 2 (only frame 2 resent)
  |                                    |  Delivers 2, 3, 4 in order
```

---

## Efficiency in Polling (TDM)

In a polling-based Time Division Multiplexing system:

- **Efficiency = Tt / (T_poll + Tt)**

Where T_poll is the time the controller spends polling each station.

---

## CSMA/CD (Carrier Sense Multiple Access with Collision Detection)

Used in traditional Ethernet (IEEE 802.3). Stations listen to the medium before
transmitting. If two stations transmit simultaneously, a collision occurs.

### Key Rules

- A station must be able to detect a collision while still transmitting.
- **Tt >= 2 * Tp** (transmission time must be at least twice the propagation delay)
- **Minimum frame length = 2 * Tp * Bandwidth**
- **Efficiency = 1 / (1 + 6.44a)**

### Collision Detection Process

```text
Station A                                        Station B
  |                                                 |
  |===== Transmitting frame ========================>
  |                                                 |
  |                    <==== Station B starts transmitting
  |                          (doesn't yet see A's signal)
  |                                                 |
  |              COLLISION DETECTED!                |
  |           <~~~~~~ Jam Signal ~~~~~~>             |
  |                                                 |
  |  Both stations stop, wait random backoff time   |
  |                                                 |
  |===== A retransmits (won backoff) =============>  |
  |                                                 |

  Timeline:
  |<--- Tp --->|  propagation delay one way
  |<------ 2*Tp ------>|  worst-case detection time
```

### Back-off Algorithm

After a collision, each station waits a random time before retransmitting:

1. Let n = collision number (retransmission attempt number)
2. Choose K randomly from the range [0, 2^n - 1]
3. Wait time = K * T_slot
4. After 10 collisions, the range is capped at [0, 1023]
5. After 16 collisions, the transmission is aborted

Reference: [Back-off Algorithm for CSMA/CD](https://www.geeksforgeeks.org/back-off-algorithm-csmacd/)

---

## Aloha Protocols

Aloha is one of the earliest random-access protocols, developed at the University
of Hawaii.

### Pure Aloha

- Stations transmit whenever they have data.
- If a collision occurs, wait a random time and retransmit.
- **Vulnerable period = 2 * T_frame**
- **Maximum efficiency = 1 / (2e) = 18.4%**

```text
  Station A: |====Frame====|
  Station B:          |====Frame====|
                      ^             ^
                      |-- Overlap --|  = COLLISION

  Vulnerable period for A's frame:
  |<-------- 2 * Tf -------->|
  [  Any frame starting here causes collision  ]
         |====A's Frame====|
```

### Slotted Aloha

- Time is divided into equal slots matching the frame transmission time.
- Stations may only begin transmitting at the start of a slot.
- **Vulnerable period = 1 * T_frame**
- **Maximum efficiency = 1 / e = 36.8%**

```text
  Slots:  |  Slot 1  |  Slot 2  |  Slot 3  |  Slot 4  |
          |          |          |          |          |
  Stn A:  |==Frame===|          |          |          |
  Stn B:  |==Frame===|          |          |          |
           ^ collision          |          |          |
  Stn A:  |          |          |==Frame===|          |  Success
  Stn B:  |          |==Frame===|          |          |  Success
```

---

## Error Detection and Correction

### Hamming Code

Hamming code can detect up to 2-bit errors and correct 1-bit errors.

**Redundant bits formula**: 2^r >= m + r + 1
- r = number of redundant (parity) bits
- m = number of data bits

**Example**: Encode data word `1011` using Hamming code.

1. m = 4 data bits. Find r such that 2^r >= 4 + r + 1.
   - r = 3 works: 2^3 = 8 >= 4 + 3 + 1 = 8. Yes.
2. Total bits = m + r = 7. Positions 1, 2, 4 are parity bits (P1, P2, P4).

```text
  Bit position:   1    2    3    4    5    6    7
  Bit type:       P1   P2   D1   P4   D2   D3   D4
  Data 1011:      ?    ?    1    ?    0    1    1

  P1 covers positions with bit 0 set in binary (1,3,5,7):
     P1 XOR D1 XOR D2 XOR D4 = P1 XOR 1 XOR 0 XOR 1 = 0  =>  P1 = 0

  P2 covers positions with bit 1 set in binary (2,3,6,7):
     P2 XOR D1 XOR D3 XOR D4 = P2 XOR 1 XOR 1 XOR 1 = 0  =>  P2 = 1

  P4 covers positions with bit 2 set in binary (4,5,6,7):
     P4 XOR D2 XOR D3 XOR D4 = P4 XOR 0 XOR 1 XOR 1 = 0  =>  P4 = 0

  Encoded word:   0    1    1    0    0    1    1
```

Reference: [Hamming Code](https://www.geeksforgeeks.org/computer-network-hamming-code/)

### Other Error Detection Methods

- **Parity Check**: Single bit added to make total number of 1s even (even parity) or odd (odd parity). Detects single-bit errors only.
- **Checksum**: Sum of data segments. Receiver re-computes and compares.
- **CRC (Cyclic Redundancy Check)**: Polynomial division-based method. Very effective at detecting burst errors. Widely used in Ethernet and Wi-Fi.

---

## Framing

Framing defines how a stream of bits from the Physical Layer is grouped into
meaningful units (frames). The receiver needs to identify the start and end of
each frame.

Reference: [Framing in DLL](https://www.geeksforgeeks.org/computer-network-framing-data-link-layer/)

### Character (Byte) Stuffing

Used when frames are made of characters. Special flag characters mark the start
and end. If the flag appears in the data, an escape (ESC) character is inserted.

```text
  Flag = F, Escape = E

  Original data:    [A] [B] [F] [C] [E] [D]
  After stuffing:   [F] [A] [B] [E][F] [C] [E][E] [D] [F]
                     ^                                    ^
                   Start                                End
                   flag                                 flag

  Rule: F in data -> E F
        E in data -> E E
```

### Bit Stuffing

Used in protocols like HDLC. The flag pattern is `01111110`. To prevent the flag
from appearing in the data, a `0` is inserted after every five consecutive `1`s.

```text
  Flag pattern: 01111110

  Original data:   011111011111101
  After stuffing:  0111110 1 0111110 1 01
                         ^          ^
                     inserted 0   inserted 0

  Transmitted frame:
  [01111110] [0111110101111101001] [01111110]
     Flag           Data              Flag
```

---

## Channel Capacity (Maximum Data Rate)

Reference: [Maximum Data Rate](https://www.geeksforgeeks.org/computer-network-maximum-data-rate-channel-capacity-noiseless-noisy-channels/)

### Noiseless Channel — Nyquist Bit Rate

  BitRate = 2 * Bandwidth * log2(L)

- Bandwidth: channel bandwidth in Hz
- L: number of signal levels

Example: Bandwidth = 3000 Hz, L = 2 levels
  BitRate = 2 * 3000 * log2(2) = 2 * 3000 * 1 = 6000 bps

### Noisy Channel — Shannon Capacity

  Capacity = Bandwidth * log2(1 + SNR)

- SNR: signal-to-noise ratio (linear, not in dB)
- To convert from dB: SNR = 10^(SNR_dB / 10)

Example: Bandwidth = 3000 Hz, SNR_dB = 30 dB
  SNR = 10^(30/10) = 1000
  Capacity = 3000 * log2(1 + 1000) = 3000 * ~9.97 = ~29,910 bps

---

## Token Ring

In a Token Ring network (IEEE 802.5), stations are connected in a logical ring.
A special frame called a **token** circulates around the ring. A station may only
transmit when it holds the token.

```text
        Station A
        /       \
       /         \
  Station D     Station B
       \         /
        \       /
        Station C

  Token circulation: A -> B -> C -> D -> A -> ...

  Transmission:
  1. Station A captures the token
  2. Station A transmits its data frame
  3. Frame travels:  A -> B -> C -> D -> A (back to sender)
  4. Station A removes the frame and releases the token
```

### Efficiency

Let a = Tp / Tt and N = number of stations.

- **Early Token Reinsertion** (sender releases token immediately after transmitting):

  Efficiency = 1 / (1 + a/N)

- **Delayed Token Reinsertion** (sender waits for frame to return before releasing token):

  Efficiency = 1 / (1 + (N+1)*a / N)
