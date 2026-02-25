# Datagrams

A **datagram** is the fundamental unit of data transfer on the internet. The internet provides the abstraction of datagrams for communication — each datagram is an independent, self-contained packet that carries enough information to be routed from source to destination without relying on prior exchanges. Reliability is built on top of this basic service by higher-level protocols.

---

## IP Datagram Structure

An IPv4 datagram consists of a header followed by a data payload. The header contains all the information routers need to forward the packet.

```text
  0                   1                   2                   3
  0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1
 +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
 |Version|  IHL  |    DSCP   |ECN|         Total Length          |
 +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
 |         Identification        |Flags|    Fragment Offset      |
 +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
 |  Time to Live |    Protocol   |       Header Checksum         |
 +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
 |                       Source IP Address                       |
 +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
 |                    Destination IP Address                     |
 +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
 |                    Options (if IHL > 5)                       |
 +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
 |                                                               |
 |                         Data Payload                          |
 |                      (up to ~1500 bytes)                      |
 |                                                               |
 +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
```

Key header fields:

| Field               | Size     | Purpose                                                |
|---------------------|----------|--------------------------------------------------------|
| Version             | 4 bits   | IP version (4 for IPv4)                                |
| IHL                 | 4 bits   | Header length in 32-bit words                          |
| Total Length        | 16 bits  | Entire datagram size (header + data) in bytes          |
| TTL                 | 8 bits   | Hop limit; decremented at each router                  |
| Protocol            | 8 bits   | Upper-layer protocol (e.g., 6=TCP, 17=UDP)             |
| Source IP Address   | 32 bits  | Sender's IP address                                    |
| Destination IP Address | 32 bits | Receiver's IP address                               |
| Header Checksum     | 16 bits  | Error-checking for the header                          |

---

## Best-Effort Delivery

Datagrams are delivered on a **best-effort** basis — the network makes no guarantees. This means a datagram may be:

1. **Delivered quickly** (ideal case).
2. **Delivered with corrupted data**.
3. **Delivered late or out of order**.
4. **Delivered to or from the wrong address**.
5. **Not delivered at all** (dropped).
6. **Delivered with tampered data** (maliciously).
7. **Delivered multiple times** (duplicated).

This minimal-guarantee approach keeps the network layer simple and fast, pushing reliability concerns to higher layers (e.g., TCP).

---

## TTL and Loop Prevention

The **Time To Live (TTL)** field prevents datagrams from looping infinitely through the network. Each router decrements the TTL by 1; when it reaches 0, the datagram is dropped and an ICMP "Time Exceeded" message is sent back to the sender.

```text
  Source           Router A          Router B          Router C
    |   TTL=3        |                 |                 |
    |--------------->|   TTL=2         |                 |
    |                |---------------->|   TTL=1         |
    |                |                 |---------------->|
    |                |                 |                 | TTL=0 -> DROP
    |                |                 |                 |
    |<- - - - - - - - - - - ICMP Time Exceeded - - - - -|
```

**Traceroute** exploits this mechanism by sending packets with incrementally increasing TTL values to discover each hop along the path.

---

## Internet Datagram vs User Datagram

| Feature              | Internet Datagram (IP)              | User Datagram (UDP)                   |
|----------------------|-------------------------------------|---------------------------------------|
| **Protocol**         | IP (Internet Protocol)              | UDP (User Datagram Protocol)          |
| **Scope**            | Machine to machine                  | Application to application            |
| **Addressing**       | IP addresses (source and destination)| Port numbers (source and destination)|
| **Layer**            | Network (Layer 3)                   | Transport (Layer 4)                   |

---

## Encapsulation

Data is wrapped in successive layers of headers as it moves down the protocol stack, like nested envelopes. Each layer only examines the header relevant to it.

```text
 +----------------------------------------------------------+
 |  Ethernet Frame Header                                   |
 |  +----------------------------------------------------+  |
 |  |  IP Header (Internet Datagram)                     |  |
 |  |  +----------------------------------------------+  |  |
 |  |  |  UDP/TCP Header (Transport)                  |  |  |
 |  |  |  +----------------------------------------+  |  |  |
 |  |  |  |  Application Data (e.g., DNS query)    |  |  |  |
 |  |  |  +----------------------------------------+  |  |  |
 |  |  +----------------------------------------------+  |  |
 |  +----------------------------------------------------+  |
 +----------------------------------------------------------+

  Who examines what:
  - NIC / Switch    -> Ethernet header (MAC addresses)
  - Router          -> IP header (destination IP, TTL, checksum)
  - OS Kernel       -> UDP/TCP header (port numbers)
  - Application     -> Application data (payload)
```

---

## Dot-Decimal Notation

**IPv4 addresses** are composed of 32 bits (4 bytes). In **dot-decimal notation**, each byte is represented as a decimal number (0-255) separated by dots.

```text
  Binary:       11000000.10101000.00000001.00000001
  Dot-decimal:  192     .168     .1       .1
```

IPv6 addresses use 128 bits, written as eight groups of four hexadecimal digits separated by colons (e.g., `2001:0db8:85a3::8a2e:0370:7334`).

---

## Reliable Applications on Unreliable Datagrams

Higher-level protocols and applications build reliability on top of the best-effort datagram service:

- **DNS** (Domain Name System) maps hostnames to IP addresses using UDP datagrams. It handles reliability through simple retransmission on timeout.
  - Application Layer: DNS
  - Transport Layer: UDP
  - Internet Layer: IP
- **TCP** provides reliable, ordered delivery by adding acknowledgments, retransmissions, and flow control on top of IP datagrams.
