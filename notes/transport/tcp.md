# TCP (Transmission Control Protocol)

## Introduction

TCP is a **connection-oriented**, **reliable** transport layer protocol defined in RFC 793. It provides ordered, error-checked delivery of a stream of bytes between applications running on hosts communicating over an IP network. TCP is the backbone of most internet traffic — it powers HTTP, HTTPS, FTP, SMTP, SSH, and many other protocols.

Before any data is exchanged, TCP establishes a connection using a **three-way handshake**. It guarantees that data arrives in order, without duplication, and retransmits lost segments automatically.

---

## TCP Segment Header

Every TCP segment begins with a header containing control information. The minimum header size is **20 bytes** (without options).

```text
 0                   1                   2                   3
 0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
|          Source Port          |       Destination Port        |
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
|                        Sequence Number                        |
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
|                    Acknowledgment Number                      |
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
|  Data |       |U|A|P|R|S|F|                                   |
| Offset| Rsrvd |R|C|S|S|Y|I|            Window Size            |
|       |       |G|K|H|T|N|N|                                   |
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
|           Checksum            |         Urgent Pointer        |
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
|                    Options (variable length)                   |
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
|                                                               |
|                         Data / Payload                        |
|                                                               |
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
```

### Header Fields

| Field | Size | Description |
|---|---|---|
| Source Port | 16 bits | Port opened by the sender. Chosen randomly from available ports (0–65535). |
| Destination Port | 16 bits | Port the receiving application listens on (e.g., 80 for HTTP, 443 for HTTPS). |
| Sequence Number | 32 bits | Byte-stream position of the first data byte in this segment. Set to the ISN during SYN. |
| Acknowledgment Number | 32 bits | Next sequence number the sender expects to receive. Valid when ACK flag is set. |
| Data Offset | 4 bits | Size of the TCP header in 32-bit words (minimum 5 = 20 bytes). |
| Reserved | 3 bits | Reserved for future use; must be zero. |
| Flags (URG, ACK, PSH, RST, SYN, FIN) | 6 bits | Control bits that manage connection state and data flow. |
| Window Size | 16 bits | Number of bytes the sender is willing to receive (flow control). |
| Checksum | 16 bits | Error-detection value computed over header and data for integrity. |
| Urgent Pointer | 16 bits | Points to urgent data in the segment (valid when URG flag is set). |
| Options | Variable | Optional fields such as Maximum Segment Size (MSS), window scaling, timestamps. |

---

## TCP Three-Way Handshake

TCP uses a three-way handshake to establish a reliable connection before data transfer begins.

```text
     Client                                   Server
       |                                         |
       |  1. SYN (seq=x)                         |
       |----------------------------------------->|
       |                                         |
       |  2. SYN/ACK (seq=y, ack=x+1)            |
       |<-----------------------------------------|
       |                                         |
       |  3. ACK (seq=x+1, ack=y+1)              |
       |----------------------------------------->|
       |                                         |
       |        Connection ESTABLISHED            |
       |                                         |
```

| Step | Message | Description |
|---|---|---|
| 1 | **SYN** | Client sends a SYN packet with its Initial Sequence Number (ISN) to initiate a connection. |
| 2 | **SYN/ACK** | Server acknowledges the client's SYN and sends its own ISN. `ack = client ISN + 1`. |
| 3 | **ACK** | Client acknowledges the server's ISN. `ack = server ISN + 1`. Connection is now established. |
| — | **DATA** | Once established, data is exchanged in both directions. |
| — | **FIN** | Used to cleanly close the connection after transfer is complete. |
| — | **RST** | Abruptly terminates all communication (last resort — indicates an error or resource problem). |

---

## Sequence Numbers and Acknowledgments

Any sent data is given a random initial sequence number (ISN) and is reconstructed using this number, incrementing by 1 for each byte. Both computers must agree on the same starting number during the handshake.

### ISN Exchange Example

1. **SYN** — Client: "Here's my ISN to SYNchronise with **(0)**"
2. **SYN/ACK** — Server: "Here's my ISN **(5000)**, and I ACKnowledge your ISN (0)"
3. **ACK** — Client: "I ACKnowledge your ISN (5000), here is data starting at ISN+1 **(1)**"

```text
     Client (ISN=0)                        Server (ISN=5000)
       |                                         |
       |  SYN  seq=0                              |
       |----------------------------------------->|
       |                                         |
       |  SYN/ACK  seq=5000, ack=1                |
       |<-----------------------------------------|
       |                                         |
       |  ACK  seq=1, ack=5001                    |
       |  DATA: "Hello" (5 bytes)                 |
       |----------------------------------------->|
       |                                         |
       |  ACK  seq=5001, ack=6                    |
       |<-----------------------------------------|
       |                                         |
```

| Device | Initial Sequence Number (ISN) | After Sending | Next Sequence Number |
|---|---|---|---|
| Client | 0 | Sends 5 bytes ("Hello") | 0 + 1 (SYN) + 5 = **6** |
| Server | 5000 | Sends ACK | 5000 + 1 (SYN) = **5001** |

---

## TCP Connection Teardown

TCP closes a connection gracefully using a **four-way handshake**. Either side can initiate the close. TCP reserves system resources, so connections should be closed as soon as they are no longer needed.

```text
     Client                                   Server
       |                                         |
       |  1. FIN (seq=u)                          |
       |----------------------------------------->|
       |                                         |
       |  2. ACK (ack=u+1)                        |
       |<-----------------------------------------|
       |                                         |
       |  3. FIN (seq=v)                          |
       |<-----------------------------------------|
       |                                         |
       |  4. ACK (ack=v+1)                        |
       |----------------------------------------->|
       |                                         |
       |        Connection CLOSED                 |
       |                                         |
```

1. **FIN** — The initiator (e.g., client) sends a FIN segment to signal it has finished sending data.
2. **ACK** — The receiver acknowledges the FIN.
3. **FIN** — The receiver sends its own FIN when it is also done sending data.
4. **ACK** — The initiator acknowledges the receiver's FIN. The connection is now fully closed.

---

## TCP Flow Control — Sliding Window

TCP uses a **sliding window** mechanism to prevent a fast sender from overwhelming a slow receiver. The receiver advertises a **window size** indicating how many bytes it can accept.

```text
  Sender's View of the Byte Stream:
  
  |<--- sent & acked --->|<--- sent, not acked --->|<--- can send --->|<--- cannot send --->|
  |                       |                         |                  |                     |
  +---+---+---+---+---+--+---+---+---+---+---+---+-+---+---+---+---+--+---+---+---+---+---+
  | 1 | 2 | 3 | 4 | 5 |  | 6 | 7 | 8 | 9 |10 |11 | 12|13 |14 |15 |  |16 |17 |18 |19 |20 |
  +---+---+---+---+---+--+---+---+---+---+---+---+-+---+---+---+---+--+---+---+---+---+---+
                          |<-------- Window Size (receiver advertised) -------->|
                          |                                                     |
                    Left Edge                                            Right Edge
```

- The **window slides right** as acknowledgments arrive.
- If the receiver's buffer fills up, it advertises a **window size of 0**, pausing the sender.
- The sender can only have (window size) bytes of unacknowledged data in flight at any time.

---

## TCP Congestion Control

TCP also manages **network congestion** to avoid overwhelming routers and links (separate from flow control, which protects the receiver).

### Key Algorithms

| Algorithm | Description |
|---|---|
| **Slow Start** | Start with a small congestion window (cwnd = 1 MSS). Double cwnd each RTT until a threshold is reached. |
| **Congestion Avoidance** | After the threshold, increase cwnd linearly (by 1 MSS per RTT) to probe for available bandwidth carefully. |
| **Fast Retransmit** | If 3 duplicate ACKs are received, retransmit the missing segment immediately without waiting for a timeout. |
| **Fast Recovery** | After fast retransmit, halve the threshold and enter congestion avoidance (skip slow start). |

```text
  cwnd
  (segments)
    ^
    |                          * Timeout: cwnd reset to 1
    |                  *      /
    |              *       * /
    |          *              
    |       *    <-- Congestion Avoidance (linear)
    |     *
    |   *
    |  *   <-- Slow Start (exponential)
    | *
    |*
    +-------------------------------------------> Time (RTTs)
          ^
          |
     Threshold (ssthresh)
```

---

## TCP State Diagram

A TCP connection transitions through multiple states during its lifetime.

```text
                         +------------+
                         |   CLOSED   |
                         +-----+------+
                    passive    |    active open
                    open       |    send SYN
                         +-----v------+
               +---------+   LISTEN   |
               |         +-----+------+
          recv SYN             |  recv SYN
          send SYN/ACK         |  send SYN/ACK
               |         +-----v------+
               +-------->| SYN_RCVD   |
                         +-----+------+
                               |  recv ACK
                               |
                         +-----v------+
                    +--->| ESTABLISHED|<---+
                    |    +-----+------+    |
                    |          |           |
               recv FIN   close /     recv FIN
               send ACK   send FIN    send ACK
                    |          |           |
              +-----v----+ +--v--------+ +v-----------+
              |CLOSE_WAIT | |FIN_WAIT_1 | |            |
              +-----+-----+ +--+--------+ +------------+
                    |           |
               close /     recv ACK
               send FIN        |
                    |     +----v-------+
              +-----v---+ |FIN_WAIT_2  |
              |LAST_ACK | +----+-------+
              +-----+---+      |
                    |      recv FIN
               recv ACK   send ACK
                    |           |
              +-----v---+ +----v-------+
              | CLOSED  | |TIME_WAIT   |
              +---------+ +----+-------+
                               |
                          2MSL timeout
                               |
                         +-----v------+
                         |   CLOSED   |
                         +------------+
```

| State | Description |
|---|---|
| CLOSED | No connection exists. |
| LISTEN | Server is waiting for incoming SYN requests. |
| SYN_SENT | Client has sent a SYN and is awaiting SYN/ACK. |
| SYN_RCVD | Server received a SYN, sent SYN/ACK, waiting for final ACK. |
| ESTABLISHED | Connection is open; data transfer can occur. |
| FIN_WAIT_1 | Initiator has sent FIN, waiting for ACK. |
| FIN_WAIT_2 | Initiator received ACK for its FIN, waiting for peer's FIN. |
| CLOSE_WAIT | Received FIN from peer; application has not yet closed. |
| LAST_ACK | Sent FIN after receiving peer's FIN, waiting for final ACK. |
| TIME_WAIT | Waiting for 2× Maximum Segment Lifetime before fully closing. |
