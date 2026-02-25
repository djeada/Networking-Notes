# Protocols

## Introduction

Network protocols are formal sets of rules and conventions that govern how devices communicate over a network. They define the syntax, semantics, and synchronization of data exchange, ensuring that devices from different manufacturers and running different software can interoperate seamlessly.

Without protocols, networked devices would have no standardized way to format, transmit, or interpret data. Protocols solve critical problems in communication:

- **Identified Sender and Receiver**: Ensuring the correct source and destination are specified so data reaches the right host.
- **Common Language and Grammar**: Establishing a shared format so that the message is understood by both parties.
- **Speed and Timing of Delivery**: Controlling the rate of data flow and ensuring timely, ordered delivery.
- **Confirmation or Acknowledgement Requirements**: Verifying that data has been received and understood, enabling retransmission when needed.

---

## Characteristics of Network Communication Protocols

All network communication protocols share the following fundamental characteristics:

- **Message Encoding**: Defines how data is converted into a suitable format for transmission (e.g., binary, ASCII, Unicode). The sender encodes the message, and the receiver decodes it back into a usable form.
- **Message Formatting and Encapsulation**: Specifies the structure of the message, including headers, trailers, and payload. Each layer adds its own header (encapsulation) as data moves down the stack.
- **Message Size**: Defines size constraints for messages. Large messages are broken into smaller frames or segments that comply with the maximum transmission unit (MTU) of the network.
- **Message Timing**: Controls flow rate, response timeouts, and the order in which messages are sent and received. Includes mechanisms like flow control and congestion avoidance.
- **Message Delivery Options**: Defines how the message can be delivered:
  - **Unicast**: One-to-one communication.
  - **Multicast**: One-to-many communication (specific group).
  - **Broadcast**: One-to-all communication on a network segment.
  - **Anycast**: One-to-nearest communication (used in IPv6/CDNs).

---

## Protocol Interaction

When data is sent across a network, multiple protocols work together across different layers. Each protocol handles a specific part of the communication process.

```text
  Sender                                                  Receiver
 ┌──────────────────┐                              ┌──────────────────┐
 │  Application      │  HTTP request/response       │  Application      │
 │  Layer (HTTP)     │◄────────────────────────────►│  Layer (HTTP)     │
 ├──────────────────┤                              ├──────────────────┤
 │  Transport        │  TCP segments                │  Transport        │
 │  Layer (TCP)      │◄────────────────────────────►│  Layer (TCP)      │
 ├──────────────────┤                              ├──────────────────┤
 │  Internet         │  IP packets                  │  Internet         │
 │  Layer (IP)       │◄────────────────────────────►│  Layer (IP)       │
 ├──────────────────┤                              ├──────────────────┤
 │  Network Access   │  Ethernet frames             │  Network Access   │
 │  Layer (Ethernet) │◄────────────────────────────►│  Layer (Ethernet) │
 └──────────────────┘                              └──────────────────┘
          │                                                  │
          └──────────── Physical Medium (cables, ────────────┘
                        wireless, fiber, etc.)
```

### HTTP (Hypertext Transfer Protocol)

- **Layer**: Application
- **Role**: An application protocol regulating interaction between a web server and a web client.
- **Dependency**: Relies on TCP for reliable delivery and IP for addressing and routing.

### TCP (Transmission Control Protocol)

- **Layer**: Transport
- **Role**: Controls individual conversations and breaks down HTTP messages into smaller chunks called **segments**.
- **Management**: Manages the size and rate of message exchange between server and clients. Provides flow control, error detection, and ordered delivery.

### IP (Internet Protocol)

- **Layer**: Internet
- **Role**: Encapsulates TCP segments into **packets**, assigns source and destination IP addresses, and routes them to the destination across networks.

### Ethernet

- **Layer**: Network Access
- **Role**: Encapsulates IP packets into **frames**, handles MAC addressing, and manages physical transfer over the network medium (copper, fiber, wireless).

---

## TCP/IP Protocol Suite

The TCP/IP model organizes protocols into four layers. Each layer provides services to the layer above it.

| Layer | Category | Protocol | Full Name |
|---|---|---|---|
| **Application** | Name System | DNS | Domain Name System |
| | Host Config | BOOTP | Bootstrap Protocol |
| | Host Config | DHCP | Dynamic Host Configuration Protocol |
| | Email | SMTP | Simple Mail Transfer Protocol |
| | Email | POP3 | Post Office Protocol v3 |
| | Email | IMAP | Internet Message Access Protocol |
| | File Transfer | FTP | File Transfer Protocol |
| | File Transfer | TFTP | Trivial File Transfer Protocol |
| | Web | HTTP | Hypertext Transfer Protocol |
| | Web | HTTPS | HTTP Secure (HTTP over TLS) |
| | Remote Access | SSH | Secure Shell |
| | Remote Access | Telnet | Teletype Network |
| **Transport** | Reliable | TCP | Transmission Control Protocol |
| | Unreliable | UDP | User Datagram Protocol |
| **Internet** | Addressing | IP (v4/v6) | Internet Protocol |
| | Translation | NAT | Network Address Translation |
| | Support | ICMP | Internet Control Message Protocol |
| | Routing | OSPF | Open Shortest Path First |
| | Routing | EIGRP | Enhanced Interior Gateway Routing Protocol |
| | Routing | BGP | Border Gateway Protocol |
| **Network Access** | Resolution | ARP | Address Resolution Protocol |
| | WAN | PPP | Point-to-Point Protocol |
| | LAN | Ethernet | IEEE 802.3 |
| | Wireless | Wi-Fi | IEEE 802.11 |

---

## TCP Segment Header

The TCP header is 20 bytes minimum (without options) and contains all the fields needed for reliable, ordered, and error-checked delivery.

```text
 0                   1                   2                   3
 0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1
├─┴─┴─┴─┴─┴─┴─┴─┴─┴─┴─┴─┴─┴─┴─┴─┴─┴─┴─┴─┴─┴─┴─┴─┴─┴─┴─┴─┴─┴─┴─┴─┤
│                       Source Port (16)        │  Dest Port (16)    │
├───────────────────────────────────────────────┴────────────────────┤
│                       Sequence Number (32)                         │
├────────────────────────────────────────────────────────────────────┤
│                    Acknowledgment Number (32)                      │
├────────┬──────┬─┬─┬─┬─┬─┬─┬──────────────────────────────────────┤
│Data    │Reser-│U│A│P│R│S│F│                                        │
│Offset  │ ved  │R│C│S│S│Y│I│           Window Size (16)             │
│ (4)    │ (6)  │G│K│H│T│N│N│                                        │
├────────┴──────┴─┴─┴─┴─┴─┴─┼──────────────────────────────────────┤
│       Checksum (16)        │      Urgent Pointer (16)              │
├────────────────────────────┴──────────────────────────────────────┤
│                       Options (variable)                           │
├────────────────────────────────────────────────────────────────────┤
│                       Data (payload)                               │
└────────────────────────────────────────────────────────────────────┘
```

**Key fields:**

- **Source / Destination Port**: Identify the sending and receiving application (16 bits each).
- **Sequence Number**: Tracks the order of bytes in the stream (32 bits).
- **Acknowledgment Number**: Confirms receipt of data up to this byte (32 bits).
- **Flags**: Control bits — URG, ACK, PSH, RST, SYN, FIN — manage connection state.
- **Window Size**: Flow control; indicates how many bytes the receiver can accept (16 bits).
- **Checksum**: Error detection for the header and data (16 bits).

---

## TCP Congestion Control

TCP uses congestion control algorithms to prevent network overload:

- **Slow Start**: The sender starts with a small congestion window and doubles it each round-trip time (RTT) until a threshold is reached.
- **Congestion Avoidance**: After the threshold, the window increases linearly (additive increase).
- **On Timeout**: The algorithm resets to the **Slow Start** phase (congestion window drops to 1 MSS).
- **On 3 Duplicate ACKs**: The algorithm enters the **Congestion Avoidance** phase (fast recovery), halving the congestion window instead of resetting.

---

## TCP 3-Way Handshake

TCP uses a three-way handshake to establish a reliable connection before data transfer begins.

```text
    Client                                       Server
      │                                            │
      │  ──── SYN (seq=x) ──────────────────────►  │
      │       (Client wants to connect)             │
      │                                            │
      │  ◄─── SYN-ACK (seq=y, ack=x+1) ─────────  │
      │       (Server acknowledges and responds)    │
      │                                            │
      │  ──── ACK (ack=y+1) ────────────────────►  │
      │       (Client confirms, connection open)    │
      │                                            │
      │  ════ Data Transfer Begins ════════════════ │
      │                                            │
```

**Step 1 — SYN**: The client sends a segment with the SYN flag set and an initial sequence number (ISN). This tells the server the client wants to start communication.

**Step 2 — SYN-ACK**: The server responds with both SYN and ACK flags set. The ACK acknowledges the client's sequence number (x+1), and the SYN provides the server's own initial sequence number.

**Step 3 — ACK**: The client sends a final ACK confirming the server's sequence number (y+1). The connection is now established and both sides can begin data transfer.

---

## UDP Header

UDP is a lightweight, connectionless transport protocol. Its header is only 8 bytes, making it much simpler than TCP. UDP provides no guarantees for delivery, ordering, or error recovery.

```text
 0                   1                   2                   3
 0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1
├─┴─┴─┴─┴─┴─┴─┴─┴─┴─┴─┴─┴─┴─┴─┴─┴─┴─┴─┴─┴─┴─┴─┴─┴─┴─┴─┴─┴─┴─┴─┴─┤
│       Source Port (16)         │     Destination Port (16)          │
├────────────────────────────────┼────────────────────────────────────┤
│        Length (16)             │         Checksum (16)              │
├────────────────────────────────┴────────────────────────────────────┤
│                          Data (payload)                             │
└─────────────────────────────────────────────────────────────────────┘
```

**Key fields:**

- **Source / Destination Port**: Identify the sending and receiving application (16 bits each).
- **Length**: Total length of the UDP header plus data in bytes (16 bits).
- **Checksum**: Optional in IPv4, mandatory in IPv6. Used for error detection (16 bits).

---

## TCP vs UDP Comparison

| Feature | TCP | UDP |
|---|---|---|
| Connection | Connection-oriented (3-way handshake) | Connectionless |
| Reliability | Guaranteed delivery with ACKs | No delivery guarantee |
| Ordering | Maintains packet order | No ordering |
| Speed | Slower (overhead from reliability) | Faster (minimal overhead) |
| Header Size | 20–60 bytes | 8 bytes |
| Flow Control | Yes (sliding window) | No |
| Use Cases | Web (HTTP), email, file transfer | DNS, streaming, VoIP, gaming |

---

## Common Protocols Reference

| Protocol | Port(s) | Layer | Transport | Description |
|---|---|---|---|---|
| FTP | 20, 21 | Application | TCP | File transfer (data and control channels) |
| SSH | 22 | Application | TCP | Secure remote login and command execution |
| Telnet | 23 | Application | TCP | Unencrypted remote login (legacy) |
| SMTP | 25 | Application | TCP | Sending email between mail servers |
| DNS | 53 | Application | TCP/UDP | Resolves domain names to IP addresses |
| DHCP | 67, 68 | Application | UDP | Automatic IP address assignment |
| TFTP | 69 | Application | UDP | Simple file transfer (no authentication) |
| HTTP | 80 | Application | TCP | Web page transfer (unencrypted) |
| POP3 | 110 | Application | TCP | Retrieving email from a mail server |
| IMAP | 143 | Application | TCP | Accessing email on a mail server |
| HTTPS | 443 | Application | TCP | Secure web page transfer (HTTP over TLS) |
| RDP | 3389 | Application | TCP/UDP | Remote desktop access (Windows) |
| ICMP | — | Internet | — | Network diagnostics (ping, traceroute) |
| ARP | — | Network Access | — | Maps IP addresses to MAC addresses |
