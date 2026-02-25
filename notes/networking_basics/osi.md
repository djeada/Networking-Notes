# The OSI Reference Model

## Overview

The **Open Systems Interconnection (OSI) model** is a conceptual framework created by the
International Organization for Standardization (ISO) in 1984. It divides network communication
into seven abstraction layers, providing a universal language for networking and enabling
multi-vendor interoperability.

While the OSI model is primarily a reference tool (the **TCP/IP model** is what the internet
actually uses), it remains essential for understanding how network protocols interact,
diagnosing problems, and communicating about networking concepts.

> **Mnemonic (top-down):** **A**ll **P**eople **S**eem **T**o **N**eed **D**ata **P**rocessing
>
> **Mnemonic (bottom-up):** **P**lease **D**o **N**ot **T**hrow **S**ausage **P**izza **A**way

---

## The Seven Layers at a Glance

```text
 ┌───────────────────────────────────────────────────────────────────┐
 │                        OSI MODEL                                 │
 ├───────┬──────────────┬──────────────┬────────────────────────────┤
 │ Layer │ Name         │ Data Unit    │ Example Protocols/Devices  │
 ├───────┼──────────────┼──────────────┼────────────────────────────┤
 │   7   │ Application  │ Data         │ HTTP, FTP, SMTP, DNS, SSH  │
 ├───────┼──────────────┼──────────────┼────────────────────────────┤
 │   6   │ Presentation │ Data         │ SSL/TLS, JPEG, MPEG, ASCII │
 ├───────┼──────────────┼──────────────┼────────────────────────────┤
 │   5   │ Session      │ Data         │ NetBIOS, PPTP, RPC, SCP   │
 ├───────┼──────────────┼──────────────┼────────────────────────────┤
 │   4   │ Transport    │ Segment /    │ TCP, UDP, SCTP             │
 │       │              │ Datagram     │                            │
 ├───────┼──────────────┼──────────────┼────────────────────────────┤
 │   3   │ Network      │ Packet       │ IP, ICMP, IPSec, OSPF     │
 ├───────┼──────────────┼──────────────┼────────────────────────────┤
 │   2   │ Data Link    │ Frame        │ Ethernet, Wi-Fi (802.11),  │
 │       │              │              │ PPP, ARP, Switches         │
 ├───────┼──────────────┼──────────────┼────────────────────────────┤
 │   1   │ Physical     │ Bit          │ Cables, Hubs, Repeaters,   │
 │       │              │              │ Radio frequencies          │
 └───────┴──────────────┴──────────────┴────────────────────────────┘
```

---

## Quick Reference Table

| Layer | Name         | Description                                                                                               |
|:-----:|:-------------|:----------------------------------------------------------------------------------------------------------|
| 7     | Application  | Contains protocols used for process-to-process communications (e.g., web browsing, email)                 |
| 6     | Presentation | Provides common representation of data — handles encryption, compression, and format translation          |
| 5     | Session      | Manages sessions between applications — establishes, maintains, and terminates connections                |
| 4     | Transport    | Segments, transfers, and reassembles data; provides reliable (TCP) or fast (UDP) delivery                 |
| 3     | Network      | Routes packets across networks using logical addresses (IP); determines best path                        |
| 2     | Data Link    | Frames data for the physical medium; uses MAC addresses; handles error detection at the link level        |
| 1     | Physical     | Transmits raw bitstreams over physical media (electrical, optical, or radio signals)                      |

---

## Encapsulation and Decapsulation

When data travels from a sender to a receiver, each layer wraps (encapsulates) the data from
the layer above with its own header. The receiver reverses the process (decapsulation).

```text
  SENDER (Encapsulation)                      RECEIVER (Decapsulation)
  ════════════════════                        ══════════════════════════

  Layer 7  ┌──────────┐                       Layer 7  ┌──────────┐
  App      │   Data   │                       App      │   Data   │
           └──────────┘                                └──────────┘
                │                                           ▲
                ▼                                           │
  Layer 4  ┌─────┬──────────┐                 Layer 4  ┌─────┬──────────┐
  Transport│ TCP │   Data   │                 Transport│ TCP │   Data   │
           │ Hdr │          │                          │ Hdr │          │
           └─────┴──────────┘                          └─────┴──────────┘
                │              ═══ Segment ═══              ▲
                ▼                                           │
  Layer 3  ┌────┬─────┬──────────┐            Layer 3  ┌────┬─────┬──────────┐
  Network  │ IP │ TCP │   Data   │            Network  │ IP │ TCP │   Data   │
           │Hdr │ Hdr │          │                     │Hdr │ Hdr │          │
           └────┴─────┴──────────┘                     └────┴─────┴──────────┘
                │              ═══ Packet  ═══              ▲
                ▼                                           │
  Layer 2  ┌─────┬────┬─────┬──────────┬─────┐ Layer 2┌─────┬────┬─────┬──────────┬─────┐
  Data Link│Frame│ IP │ TCP │   Data   │ FCS │ D-Link │Frame│ IP │ TCP │   Data   │ FCS │
           │ Hdr │Hdr │ Hdr │          │     │        │ Hdr │Hdr │ Hdr │          │     │
           └─────┴────┴─────┴──────────┴─────┘        └─────┴────┴─────┴──────────┴─────┘
                │              ═══ Frame   ═══              ▲
                ▼                                           │
  Layer 1  ┌─────────────────────────────────┐ Layer 1 ┌─────────────────────────────────┐
  Physical │ 01101001 11010010 10110100 ...  │ Physical│ 01101001 11010010 10110100 ...  │
           └─────────────────────────────────┘         └─────────────────────────────────┘
                │              ═══ Bits    ═══              ▲
                └───────────────────────────────────────────┘
                          Physical Medium (cable / wireless)
```

---

## Detailed Layer Descriptions

### Layer 1: Physical Layer

- **Function:** Transmits raw bitstreams (1s and 0s) over a physical medium. Defines the
  electrical, optical, or radio specifications for activating, maintaining, and deactivating
  physical links.
- **Key Responsibilities:**
  - Bit-level transmission and reception
  - Defining cable types, pin layouts, voltages, and signal timing
  - Encoding schemes (e.g., Manchester encoding, NRZ)
  - Physical topology (bus, star, ring, mesh)
- **Devices:** Hubs, repeaters, cables (Cat5e/6, fiber optic), network interface cards (NICs)
- **Troubleshooting at this layer:**
  - Are all cables properly plugged in?
  - Is the NIC functioning (link light on)?
  - Could it be a damaged or faulty cable?
  - Is there electromagnetic interference?

### Layer 2: Data Link Layer

- **Function:** Packages raw bits from Layer 1 into frames, adds physical (MAC) addresses
  for local delivery, and handles error detection at the link level.
- **Key Responsibilities:**
  - Framing — wrapping packets in frames with headers and trailers
  - MAC addressing — using 48-bit hardware addresses (e.g., `AA:BB:CC:DD:EE:FF`)
  - Error detection via Frame Check Sequence (FCS) / CRC
  - Flow control on the local link
  - Media access control (CSMA/CD for Ethernet, CSMA/CA for Wi-Fi)
- **Sub-layers:**
  - **LLC (Logical Link Control):** Interfaces with Layer 3; handles multiplexing
  - **MAC (Media Access Control):** Controls how devices gain access to the medium
- **Devices:** Switches, bridges, wireless access points
- **Troubleshooting at this layer:**
  - Has the switch gone bad or is a port disabled?
  - Are there MAC address table issues or duplicate MACs?
  - Is there a VLAN misconfiguration?

### Layer 3: Network Layer

- **Function:** Handles logical addressing (IP addresses) and determines the best path
  for data to travel across interconnected networks (routing).
- **Key Responsibilities:**
  - IP addressing (IPv4 and IPv6)
  - Routing — selecting optimal paths using protocols like OSPF, BGP, EIGRP
  - Packet forwarding and fragmentation
  - Quality of Service (QoS) tagging
- **Devices:** Routers, Layer 3 switches
- **Troubleshooting at this layer:**
  - Is the router functioning correctly?
  - Do I have the correct IP address / subnet mask / default gateway?
  - Can I ping the destination? (`ping`, `traceroute`)
  - Are there routing table issues?

### Layer 4: Transport Layer

- **Function:** Provides end-to-end communication services. Segments data for transport
  and reassembles it at the destination. Adds source and destination port numbers.
- **Key Responsibilities:**
  - **TCP (Transmission Control Protocol):** Connection-oriented, reliable delivery,
    three-way handshake (SYN → SYN-ACK → ACK), flow control, error recovery
  - **UDP (User Datagram Protocol):** Connectionless, best-effort delivery, low overhead,
    used for streaming, DNS lookups, VoIP
  - Port numbering (0–65535) to identify applications
  - Segmentation and reassembly
- **Troubleshooting at this layer:**
  - Is the correct port open? (`netstat`, `ss`)
  - Is a firewall blocking traffic on a specific port?
  - Are TCP connections timing out or resetting?

### Layer 5: Session Layer

- **Function:** Establishes, manages, and terminates sessions (dialogues) between
  applications on different hosts.
- **Key Responsibilities:**
  - Session establishment, maintenance, and teardown
  - Dialog control — half-duplex or full-duplex communication
  - Synchronization — inserting checkpoints for long transfers so sessions can resume
    after interruption
  - Authentication and authorization at the session level
- **Protocols:** NetBIOS, PPTP, RPC, SCP
- **Troubleshooting at this layer:**
  - Are sessions being established correctly?
  - Is authentication succeeding?
  - Are you connecting to the correct server address?

### Layer 6: Presentation Layer

- **Function:** Translates data between the application layer and the network. Acts as a
  data translator, ensuring that data from the sending application can be read by the
  receiving application.
- **Key Responsibilities:**
  - Data format translation (e.g., EBCDIC to ASCII)
  - Encryption and decryption (e.g., SSL/TLS encryption)
  - Data compression and decompression (e.g., JPEG, MPEG, GIF)
  - Character encoding (e.g., UTF-8)
  - Serialization (e.g., JSON, XML formatting)
- **Troubleshooting at this layer:**
  - Is data being encrypted/decrypted properly?
  - Are character encoding issues causing garbled text?
  - Is there a certificate or TLS handshake failure?

### Layer 7: Application Layer

- **Function:** The layer closest to the end user. Provides network services directly
  to user applications. This is where users interact with the network.
- **Key Responsibilities:**
  - Providing user interfaces and network services to applications
  - Identifying communication partners and resource availability
  - Synchronizing communication
- **Common Protocols:**
  - **HTTP/HTTPS** — Web browsing
  - **FTP/SFTP** — File transfers
  - **SMTP/POP3/IMAP** — Email
  - **DNS** — Domain name resolution
  - **SSH** — Secure remote access
  - **DHCP** — Dynamic IP address assignment
  - **SNMP** — Network management
- **Troubleshooting at this layer:**
  - Is the application returning errors?
  - Is DNS resolving correctly? (`nslookup`, `dig`)
  - Is the web server responding? (`curl`, browser dev tools)

---

## OSI Model vs. TCP/IP Model

The TCP/IP model is the practical implementation used on the internet. It consolidates
the seven OSI layers into four (or five, depending on the interpretation).

```text
  ┌─────────────────────────┐     ┌─────────────────────────┐
  │       OSI Model         │     │      TCP/IP Model       │
  │      (7 Layers)         │     │      (4 Layers)         │
  ├─────────────────────────┤     ├─────────────────────────┤
  │ 7 │ Application         │ ──┐ │                         │
  ├───┤                     │   │ │                         │
  │ 6 │ Presentation        │ ──┼─│  4 │ Application        │
  ├───┤                     │   │ │                         │
  │ 5 │ Session             │ ──┘ │                         │
  ├─────────────────────────┤     ├─────────────────────────┤
  │ 4 │ Transport           │ ────│  3 │ Transport          │
  ├─────────────────────────┤     ├─────────────────────────┤
  │ 3 │ Network             │ ────│  2 │ Internet           │
  ├─────────────────────────┤     ├─────────────────────────┤
  │ 2 │ Data Link           │ ──┐ │                         │
  ├───┤                     │   ├─│  1 │ Network Access     │
  │ 1 │ Physical            │ ──┘ │    │ (Link)             │
  └─────────────────────────┘     └─────────────────────────┘
```

| OSI Layer(s)              | TCP/IP Layer      | Key Protocols                     |
|:--------------------------|:------------------|:----------------------------------|
| 7, 6, 5 — Application,   | Application       | HTTP, FTP, SMTP, DNS, SSH, TLS    |
| Presentation, Session     |                   |                                   |
| 4 — Transport             | Transport         | TCP, UDP                          |
| 3 — Network               | Internet          | IP, ICMP, IGMP                   |
| 2, 1 — Data Link,        | Network Access    | Ethernet, Wi-Fi, PPP, ARP         |
| Physical                  | (Link)            |                                   |

---

## Troubleshooting with the OSI Model

The OSI model provides a structured approach to diagnosing network issues. Start from the
bottom (Layer 1) and work your way up, or start from the top (Layer 7) and work down.

```text
  Layer 7  Application    ──▶  Is the app working? Check logs, HTTP status codes
  Layer 6  Presentation   ──▶  Encoding issues? TLS/SSL certificate valid?
  Layer 5  Session        ──▶  Can sessions be established? Auth working?
  Layer 4  Transport      ──▶  Correct port open? Firewall rules? TCP handshake?
  Layer 3  Network        ──▶  Can you ping it? Correct IP? Route exists?
  Layer 2  Data Link      ──▶  Switch port up? VLAN correct? ARP resolving?
  Layer 1  Physical       ──▶  Cable plugged in? Link light on? NIC enabled?
```

**Bottom-up approach (most common):**

1. **Physical** — Check cables, link lights, NIC status
2. **Data Link** — Verify switch port status, check for MAC/ARP issues
3. **Network** — Ping the gateway, check IP config (`ipconfig` / `ifconfig` / `ip a`)
4. **Transport** — Test port connectivity (`telnet`, `nc`, `Test-NetConnection`)
5. **Session** — Verify session establishment and authentication
6. **Presentation** — Check for encoding or encryption errors
7. **Application** — Test the application directly, check logs

---

## Conclusion

- The OSI model is a **reference framework**, not a strict implementation — real-world
  protocols often span multiple layers.
- Understanding the OSI model helps you **communicate clearly** about networking concepts
  and **troubleshoot systematically** by isolating problems to a specific layer.
- The **TCP/IP model** is the practical counterpart that powers the modern internet, but the
  OSI model's seven-layer approach provides finer granularity for analysis and learning.

