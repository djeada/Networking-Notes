# TCP vs UDP Comparison

## Introduction

The transport layer provides two main protocols: **TCP** (Transmission Control Protocol) and **UDP** (User Datagram Protocol). Both sit on top of IP and use port numbers to deliver data to the correct application, but they make very different trade-offs.

- **TCP** provides a reliable, ordered byte stream over an unreliable Internet — using sequence numbers, acknowledgments, checksums, and flow/congestion control.
- **UDP** provides a fast, minimal datagram service with almost no overhead — no connection setup, no guarantees, and no retransmissions.

Understanding when to use each protocol is a fundamental networking skill.

---

## Side-by-Side: TCP Connection vs UDP Fire-and-Forget

```text
         TCP (Connection-Oriented)              UDP (Connectionless)

  Client              Server             Client              Server
    |                    |                  |                    |
    | 1. SYN             |                  |  Datagram 1        |
    |------------------->|                  |------------------->|
    |                    |                  |                    |
    | 2. SYN/ACK         |                  |  Datagram 2        |
    |<-------------------|                  |------------------->|
    |                    |                  |                    |
    | 3. ACK             |                  |  Datagram 3        |
    |------------------->|                  |------------------->|
    |                    |                  |                    |
    | Data + ACK         |                  |     (done!)        |
    |------------------->|                  |                    |
    |<-------------------|                  
    |  ...               |                  * No handshake
    |                    |                  * No ACKs
    | FIN/ACK exchange   |                  * No guaranteed delivery
    |------------------->|                  * No ordering
    |<-------------------|
    |------------------->|
    |                    |
```

---

## Comprehensive Comparison Table

| Feature | TCP | UDP |
|---|---|---|
| **Connection** | Connection-oriented (3-way handshake) | Connectionless (no handshake) |
| **Reliability** | Guaranteed delivery with retransmissions | No delivery guarantees |
| **Ordering** | Data arrives in order (sequence numbers) | No ordering guarantees |
| **Duplicate Protection** | Yes (via sequence numbers) | No |
| **Error Detection** | Checksum (mandatory) | Checksum (optional in IPv4, mandatory in IPv6) |
| **Flow Control** | Yes (sliding window) | No |
| **Congestion Control** | Yes (slow start, congestion avoidance) | No |
| **Speed** | Slower (overhead from handshake, ACKs) | Faster (minimal overhead) |
| **Header Size** | 20–60 bytes | 8 bytes |
| **Broadcast/Multicast** | Not supported | Supported |
| **State** | Stateful (tracks connection) | Stateless |
| **Data Boundary** | Byte stream (no message boundaries) | Preserves message boundaries (datagrams) |
| **Use Cases** | Web, email, file transfer, SSH | DNS, streaming, gaming, VoIP |

---

## Header Size Comparison

```text
  TCP Header (minimum 20 bytes):
  +--------+--------+--------+--------+
  |     Source Port  |   Dest Port     |   4 bytes
  +--------+--------+--------+--------+
  |          Sequence Number           |   4 bytes
  +--------+--------+--------+--------+
  |       Acknowledgment Number        |   4 bytes
  +--------+--------+--------+--------+
  |Offset|Rsv| Flags|   Window Size    |   4 bytes
  +--------+--------+--------+--------+
  |      Checksum    | Urgent Pointer  |   4 bytes
  +--------+--------+--------+--------+
  |         Options (variable)         |   0-40 bytes
  +--------+--------+--------+--------+
                                         = 20-60 bytes total

  UDP Header (fixed 8 bytes):
  +--------+--------+--------+--------+
  |     Source Port  |   Dest Port     |   4 bytes
  +--------+--------+--------+--------+
  |       Length     |    Checksum     |   4 bytes
  +--------+--------+--------+--------+
                                         = 8 bytes total

  Overhead ratio:  TCP = 2.5x to 7.5x more header than UDP
```

---

## When to Use TCP vs UDP

### Use TCP When:

- **Data integrity is critical** — every byte must arrive correctly (file transfers, web pages).
- **Order matters** — data must be processed in sequence (database transactions).
- **Reliability is required** — lost packets must be retransmitted (email delivery).
- **You need flow/congestion control** — large transfers over unpredictable networks.

### Use UDP When:

- **Speed and low latency are critical** — real-time applications (gaming, VoIP).
- **Losing a few packets is acceptable** — streaming media (a dropped frame is fine).
- **Simple request/response** — DNS queries, DHCP discovery.
- **Broadcast or multicast** — service discovery, network announcements.
- **Application handles reliability** — QUIC, custom game protocols.

---

## Protocols That Use Each

| TCP | UDP |
|---|---|
| HTTP / HTTPS (web) | DNS (domain name lookups) |
| FTP (file transfer) | DHCP (IP address assignment) |
| SMTP / IMAP / POP3 (email) | SNMP (network monitoring) |
| SSH (secure shell) | TFTP (trivial file transfer) |
| Telnet (remote terminal) | RTP (real-time audio/video) |
| BGP (border gateway routing) | NTP (network time protocol) |
| MySQL / PostgreSQL (databases) | Syslog (logging) |
| LDAP (directory services) | mDNS (multicast DNS) |

> **Note:** Some applications implement additional features over their chosen protocol. For example, HTTPS adds TLS encryption over TCP, and QUIC builds reliable streams over UDP.

---

## Real-World Analogies

| Analogy | TCP | UDP |
|---|---|---|
| **Mail** | Registered mail — you get delivery confirmation, the letter is tracked, and it arrives in order. If lost, it is resent. | Postcards — you drop them in the mailbox and hope they arrive. No tracking, no confirmation. |
| **Conversation** | Phone call — you establish a connection ("Hello?"), confirm the other person is there, speak in turns, and say goodbye. | Shouting across a room — you yell your message and hope the other person hears it. |
| **Delivery** | Courier service — guaranteed delivery, signature required, items packed in order. | Throwing newspapers onto porches — fast, cheap, and most of them land where they should. |

```text
  TCP = Registered Mail                    UDP = Postcards

  +----------+     +-----------+          +----------+     +-----------+
  |  Sender  |     |  Receiver |          |  Sender  |     |  Receiver |
  +----+-----+     +-----+-----+          +----+-----+     +-----+-----+
       |                  |                     |                  |
       | "Can you sign?"  |                     | "Here you go!"   |
       |----------------->|                     |----------------->|
       |                  |                     |                  |
       | "Yes, go ahead"  |                     |     (maybe it    |
       |<-----------------|                     |      arrives,    |
       |                  |                     |      maybe not)  |
       | "Here's the      |                     |                  |
       |  package + track#"|                    
       |----------------->|
       |                  |
       | "Received, signed"|
       |<-----------------|
       |                  |
```
