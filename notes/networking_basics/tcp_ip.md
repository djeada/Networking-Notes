# TCP/IP Model

## Overview

The **TCP/IP model** (also known as the **Internet Protocol Suite**) is the foundational
communication framework for the modern internet. Developed by the U.S. Department of Defense
in the 1970s, it defines how data is packetized, addressed, transmitted, routed, and received
across interconnected networks.

Unlike the theoretical 7-layer OSI model, the TCP/IP model is a practical, implementation-driven
architecture organized into **4 layers**. Each layer provides services to the layer above it and
consumes services from the layer below it, creating a clean separation of concerns.

Key principles of the TCP/IP model:

- **Abstraction and layering** — each layer hides its internal complexity from the others.
- **Encapsulation** — data is wrapped with protocol headers as it moves down the stack.
- **Interoperability** — standardized protocols allow diverse hardware and software to communicate.
- A **byte stream** is a sequence of bytes that can be written to and read from across the network.

---

## The 4-Layer TCP/IP Stack

```text
┌──────────────────────────────────────────────────────────────────┐
│                      APPLICATION LAYER                           │
│                                                                  │
│   Protocols: HTTP, HTTPS, FTP, SMTP, DNS, SSH, DHCP, SNMP,      │
│              Telnet, POP3, IMAP, NTP, TFTP, RDP                  │
│                                                                  │
│   Data Unit: Messages / Data                                     │
├──────────────────────────────────────────────────────────────────┤
│                      TRANSPORT LAYER                             │
│                                                                  │
│   Protocols: TCP (Transmission Control Protocol)                 │
│              UDP (User Datagram Protocol)                        │
│                                                                  │
│   Data Unit: Segments (TCP) / Datagrams (UDP)                    │
├──────────────────────────────────────────────────────────────────┤
│                      INTERNET LAYER                              │
│                                                                  │
│   Protocols: IP (IPv4, IPv6), ICMP, ARP, IGMP, RARP             │
│                                                                  │
│   Data Unit: Packets                                             │
├──────────────────────────────────────────────────────────────────┤
│                  NETWORK ACCESS / LINK LAYER                     │
│                                                                  │
│   Protocols: Ethernet (802.3), Wi-Fi (802.11), PPP,              │
│              ARP (also here), MAC, DSL, Frame Relay              │
│                                                                  │
│   Data Unit: Frames / Bits                                       │
└──────────────────────────────────────────────────────────────────┘
```

---

## OSI vs TCP/IP Model Mapping

```text
        OSI Model                          TCP/IP Model
  ┌───────────────────┐
  │  7 - Application  │
  ├───────────────────┤            ┌───────────────────────┐
  │  6 - Presentation │ ─────────>│      Application      │
  ├───────────────────┤            └───────────────────────┘
  │  5 - Session      │
  ├───────────────────┤            ┌───────────────────────┐
  │  4 - Transport    │ ─────────>│      Transport        │
  ├───────────────────┤            └───────────────────────┘
  │  3 - Network      │ ─────────>┌───────────────────────┐
  ├───────────────────┤            │      Internet         │
  │                   │            └───────────────────────┘
  │  2 - Data Link    │ ─────────>┌───────────────────────┐
  ├───────────────────┤            │   Network Access      │
  │  1 - Physical     │ ─────────>│      (Link)           │
  └───────────────────┘            └───────────────────────┘
```

The OSI layers 5, 6, and 7 (Session, Presentation, Application) are merged into a single
**Application** layer in the TCP/IP model. OSI layers 1 and 2 (Physical and Data Link) are
combined into the **Network Access** layer.

---

## Layer Details

### Layer 4 — Application Layer

The topmost layer provides network services directly to end-user applications. It represents
data to the user and handles encoding, dialog control, and high-level protocols.

| Protocol | Port(s)  | Purpose                                      |
|----------|----------|----------------------------------------------|
| HTTP     | 80       | Web page transfer (HyperText Transfer)       |
| HTTPS    | 443      | Encrypted web traffic (HTTP over TLS/SSL)    |
| FTP      | 20, 21   | File transfers between hosts                 |
| SSH      | 22       | Secure remote login and command execution    |
| Telnet   | 23       | Remote login (unencrypted, legacy)           |
| SMTP     | 25       | Sending email                                |
| DNS      | 53       | Domain name to IP address resolution         |
| DHCP     | 67, 68   | Dynamic IP address assignment                |
| TFTP     | 69       | Trivial file transfer (no authentication)    |
| POP3     | 110      | Retrieving email from a server               |
| IMAP     | 143      | Accessing email on a server                  |
| SNMP     | 161, 162 | Network device management and monitoring     |
| NTP      | 123      | Clock synchronization across networks        |
| RDP      | 3389     | Remote desktop access (Windows)              |

**Key responsibilities:**
- Encoding and formatting data for the network
- Session management and dialog control
- User authentication at the application level

---

### Layer 3 — Transport Layer

Supports communication between different devices across diverse networks. It provides
end-to-end data transfer, error recovery, and flow control.

#### TCP (Transmission Control Protocol)
- **Connection-oriented** — establishes a session via a 3-way handshake before data transfer
- **Reliable delivery** — guarantees all packets arrive in order and retransmits lost packets
- **Flow control** — uses windowing to prevent overwhelming the receiver
- **Use cases:** Web browsing, email, file transfers, any application needing reliability

```text
  TCP 3-Way Handshake

  Client                     Server
    │                           │
    │ ──── SYN ───────────────> │   Step 1: Client sends SYN
    │                           │
    │ <─── SYN-ACK ─────────── │   Step 2: Server responds with SYN-ACK
    │                           │
    │ ──── ACK ───────────────> │   Step 3: Client sends ACK
    │                           │
    │    Connection Established │
    │ <════ Data Transfer ════> │
    │                           │
```

#### UDP (User Datagram Protocol)
- **Connectionless** — no handshake; data is sent immediately
- **Unreliable** — no guarantee of delivery, ordering, or duplicate protection
- **Low overhead** — minimal header size (8 bytes vs TCP's 20+ bytes)
- **Use cases:** DNS lookups, video streaming, online gaming, VoIP

```text
  TCP vs UDP Comparison

  ┌──────────────────────┬───────────────┬───────────────┐
  │ Feature              │     TCP       │     UDP       │
  ├──────────────────────┼───────────────┼───────────────┤
  │ Connection           │ Required      │ Not required  │
  │ Reliability          │ Guaranteed    │ Best-effort   │
  │ Ordering             │ Preserved     │ Not preserved │
  │ Speed                │ Slower        │ Faster        │
  │ Header Size          │ 20-60 bytes   │ 8 bytes       │
  │ Flow Control         │ Yes (window)  │ No            │
  │ Error Checking       │ Yes + recovery│ Checksum only │
  │ Use Case             │ Web, Email    │ DNS, Streaming│
  └──────────────────────┴───────────────┴───────────────┘
```

---

### Layer 2 — Internet Layer

Determines the best path through the network for packets to travel from source to destination.
This layer handles logical addressing, routing, and packet forwarding.

| Protocol | Purpose                                                      |
|----------|--------------------------------------------------------------|
| IPv4     | 32-bit addressing (e.g., 192.168.1.1), most widely deployed |
| IPv6     | 128-bit addressing (e.g., 2001:db8::1), successor to IPv4   |
| ICMP     | Error reporting and diagnostics (ping, traceroute)           |
| ARP      | Resolves IP addresses to MAC (hardware) addresses            |
| IGMP     | Manages multicast group memberships                          |
| RARP     | Resolves MAC addresses to IP addresses (legacy)              |

**Key responsibilities:**
- Logical addressing (IP addresses)
- Routing packets across networks
- Fragmentation and reassembly of packets
- Error detection and reporting (ICMP)

---

### Layer 1 — Network Access / Link Layer

The bottom layer controls the hardware devices and media that make up the physical network.
It defines how bits are placed onto the network medium and manages access to shared media.

| Protocol / Standard | Medium     | Description                             |
|---------------------|------------|-----------------------------------------|
| Ethernet (802.3)    | Wired      | LAN standard using CSMA/CD              |
| Wi-Fi (802.11)      | Wireless   | WLAN standard using CSMA/CA             |
| PPP                 | Serial     | Point-to-Point Protocol for direct links|
| DSL                 | Copper     | Digital Subscriber Line for broadband   |
| Frame Relay         | WAN        | Packet-switched WAN technology (legacy) |

**Key responsibilities:**
- Physical addressing (MAC addresses)
- Media access control (who transmits when)
- Frame formatting and error detection (CRC)
- Converting data into electrical, optical, or radio signals

---

## Encapsulation

As data moves **down** through the layers, each layer wraps the data with its own header
(and sometimes trailer). This process is called **encapsulation**. The reverse process at
the receiving host is called **de-encapsulation**.

```text
  Sending Host                                          Receiving Host
  (top to bottom)                                       (bottom to top)

  ┌─────────────────────────────────┐
  │            Data                 │  ◄── Application Layer
  └─────────────────────────────────┘
                  │ encapsulate
                  ▼
  ┌──────┬──────────────────────────┐
  │TCP/  │         Data             │  ◄── Transport Layer
  │UDP   │                          │
  │Header│                          │
  └──────┴──────────────────────────┘
                  │ encapsulate
                  ▼
  ┌──────┬──────┬──────────────────────────┐
  │  IP  │TCP/  │         Data             │  ◄── Internet Layer
  │Header│UDP   │                          │
  │      │Header│                          │
  └──────┴──────┴──────────────────────────┘
                  │ encapsulate
                  ▼
  ┌───────┬──────┬──────┬──────────────────────────┬─────────┐
  │ Frame │  IP  │TCP/  │         Data             │  Frame  │
  │ Header│Header│UDP   │                          │ Trailer │
  │       │      │Header│                          │  (FCS)  │
  └───────┴──────┴──────┴──────────────────────────┴─────────┘
       ▲                                                ▲
       └── Network Access Layer ────────────────────────┘
```

**Data unit names at each layer:**

```text
  Application Layer    ──>  Data / Message
  Transport Layer      ──>  Segment (TCP) or Datagram (UDP)
  Internet Layer       ──>  Packet
  Network Access Layer ──>  Frame
  Physical Medium      ──>  Bits (1s and 0s)
```

---

## Data Flow Through the Layers

When a user requests a web page, the data flows through each layer of the TCP/IP stack:

```text
  ┌──────────────────────────────────────────────────────────────────┐
  │  Sender (Client)                Receiver (Server)                │
  │                                                                  │
  │  Application  ──────────────────────────────>  Application       │
  │      │                                              ▲            │
  │      ▼                                              │            │
  │  Transport    ──────────────────────────────>  Transport         │
  │      │                                              ▲            │
  │      ▼                                              │            │
  │  Internet     ── Router ── Router ── Router ─>  Internet         │
  │      │                                              ▲            │
  │      ▼                                              │            │
  │  Link Layer   ──────────────────────────────>  Link Layer        │
  │      │                                              ▲            │
  │      ▼              Physical Medium                 │            │
  │      └──────── Bits on the Wire / Air ──────────────┘            │
  └──────────────────────────────────────────────────────────────────┘
```

**Step-by-step example — loading `http://example.com`:**

1. **Application Layer** — The browser generates an HTTP GET request for the web page.
2. **Transport Layer** — TCP breaks the request into segments, adds port numbers
   (source: random high port, destination: 80), and initiates a 3-way handshake.
3. **Internet Layer** — IP adds source and destination IP addresses and determines
   the best route via routing tables.
4. **Network Access Layer** — The frame is constructed with MAC addresses and
   transmitted as electrical signals, light pulses, or radio waves.
5. At the **receiver**, the process reverses: headers are stripped at each layer
   until the original HTTP request reaches the server application.

---

## OSI vs TCP/IP Comparison

| Aspect              | OSI Model                        | TCP/IP Model                     |
|---------------------|----------------------------------|----------------------------------|
| Layers              | 7                                | 4                                |
| Developed by        | ISO (International Standards Org)| U.S. Department of Defense (DoD) |
| Approach            | Theoretical / reference model    | Practical / implementation-based |
| Session Layer       | Separate (Layer 5)               | Merged into Application          |
| Presentation Layer  | Separate (Layer 6)               | Merged into Application          |
| Physical Layer      | Separate (Layer 1)               | Merged into Network Access       |
| Protocol definition | Model came first, then protocols | Protocols came first, then model |
| Reliability         | Less widely implemented directly | Foundation of the modern internet|
| Transport protocols | Defines connection/connectionless| TCP (reliable) and UDP (fast)    |
| Usage today         | Teaching and reference            | Real-world networking            |

---

## Summary

The TCP/IP model is the backbone of all modern network communication. Its four layers
provide a clean, practical architecture:

```text
  Layer 4 — Application    : What the user interacts with
  Layer 3 — Transport      : How data is delivered reliably (or quickly)
  Layer 2 — Internet       : Where data is routed across networks
  Layer 1 — Network Access : How bits physically travel on the medium
```

Each layer is **isolated** and communicates only with its corresponding layer on the
destination host. This separation allows each layer to evolve independently — for example,
switching from Ethernet to Wi-Fi at the Link layer requires no changes to TCP or HTTP above.
