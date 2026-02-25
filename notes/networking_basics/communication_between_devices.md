# Communication Between Devices

## Introduction

Communication between devices on a network is the fundamental purpose of networking. Whether two computers are sitting on the same desk or are located on opposite sides of the globe, they follow a structured set of rules (protocols) to exchange data reliably. Understanding how this communication works—from the physical signals on the wire to the application-level messages—is essential for anyone working with networks.

At its core, device communication involves a **sender**, a **receiver**, and a **medium** (wired or wireless) through which data travels. Along the way, various network components forward, filter, and route traffic to ensure it reaches the correct destination.

---

## How Devices Communicate — The Path of a Packet

The following diagram shows the typical path data takes when traveling between two devices across the internet:

```text
 Device A                                                         Device B
 ┌──────────┐    ┌────────┐    ┌────────┐            ┌────────┐    ┌────────┐    ┌──────────┐
 │          │    │        │    │        │            │        │    │        │    │          │
 │   App    │───▶│  NIC   │───▶│ Switch │───▶┌──────┐│ Router │───▶│ Switch │───▶│  NIC     │───▶ App
 │          │    │        │    │        │    │Router│├────────┘    │        │    │          │
 └──────────┘    └────────┘    └────────┘    │  A   │             └────────┘    └──────────┘
                                             └──┬───┘
                                                │
                                           ┌────┴─────┐
                                           │ Internet │
                                           │ (many    │
                                           │ routers) │
                                           └────┬─────┘
                                                │
                                             ┌──┴───┐
                                             │Router│
                                             │  B   │
                                             └──────┘
```

**Key components along the path:**

| Component  | Role                                                        |
|------------|-------------------------------------------------------------|
| **NIC**    | Network Interface Card — converts data to/from signals      |
| **Switch** | Forwards frames within a local network (Layer 2)            |
| **Router** | Routes packets between different networks (Layer 3)         |
| **Internet** | A global collection of interconnected routers and networks |

---

## Communication Modes

Network communication can be classified into four main modes based on how many recipients are involved.

### Unicast (One-to-One)

A single sender transmits data to a single specific receiver. This is the most common mode used for everyday communication such as web browsing or SSH sessions.

```text
  ┌──────┐                        ┌──────┐
  │  A   │───────────────────────▶│  B   │
  └──────┘                        └──────┘
   Sender        (one-to-one)     Receiver
```

### Broadcast (One-to-All)

A single sender transmits data to **all** devices on the local network segment. Used by protocols like ARP and DHCP for discovery purposes.

```text
                                  ┌──────┐
                            ┌────▶│  B   │
                            │     └──────┘
  ┌──────┐    ┌────────┐    │     ┌──────┐
  │  A   │───▶│ Switch │────┼────▶│  C   │
  └──────┘    └────────┘    │     └──────┘
   Sender     (one-to-all)  │     ┌──────┐
                            └────▶│  D   │
                                  └──────┘
```

### Multicast (One-to-Many)

A single sender transmits data to a **specific group** of interested receivers. Used for video streaming, online gaming, and routing protocol updates (e.g., OSPF).

```text
                                  ┌──────┐
                            ┌────▶│  B   │  ← subscribed
                            │     └──────┘
  ┌──────┐    ┌────────┐    │     ┌──────┐
  │  A   │───▶│ Switch │────┤     │  C   │  ← NOT subscribed
  └──────┘    └────────┘    │     └──────┘
   Sender    (one-to-many)  │     ┌──────┐
                            └────▶│  D   │  ← subscribed
                                  └──────┘
```

### Anycast (One-to-Nearest)

A single sender transmits data, and it is delivered to the **topologically nearest** member of a group of potential receivers. Commonly used by CDNs and DNS root servers.

```text
  ┌──────┐          ┌──────┐
  │  A   │─────X───▶│ B1   │  (same IP, farther away)
  └──────┘ \        └──────┘
   Sender   \
    (one-to- \      ┌──────┐
    nearest)  └────▶│ B2   │  ← nearest replica receives it
                    └──────┘
```

---

## The Communication Process

When data is sent from one device to another, it goes through a well-defined process:

### 1. Encapsulation (Sender Side)

Data is wrapped in headers (and sometimes trailers) as it moves down the protocol stack:

```text
 Application Data
       │
       ▼
 ┌─────────────────────────────────┐
 │ App Header │    Data            │   (Layer 7 — Application)
 └─────────────────────────────────┘
       │
       ▼
 ┌─────────────────────────────────────┐
 │ TCP/UDP Hdr │ App Header │  Data    │   (Layer 4 — Transport)
 └─────────────────────────────────────┘
       │
       ▼
 ┌─────────────────────────────────────────┐
 │ IP Hdr │ TCP/UDP Hdr │ App Hdr │ Data   │   (Layer 3 — Network)
 └─────────────────────────────────────────┘
       │
       ▼
 ┌──────────────────────────────────────────────────┐
 │ Frame Hdr │ IP Hdr │ TCP/UDP │ App │ Data │ FCS  │  (Layer 2 — Data Link)
 └──────────────────────────────────────────────────┘
```

### 2. Addressing

- **MAC Address** (Layer 2): Identifies devices on the same local network segment.
- **IP Address** (Layer 3): Identifies devices across networks globally.
- **Port Number** (Layer 4): Identifies the specific application or service.

### 3. Routing

Routers examine the destination IP address and consult their routing tables to determine the best next hop toward the destination network.

### 4. Decapsulation (Receiver Side)

The reverse of encapsulation — each layer strips its header and passes the payload up to the next layer until the application receives the original data.

---

## Common Communication Protocols

| Protocol       | Layer       | Port(s)       | Purpose                          |
|----------------|-------------|---------------|----------------------------------|
| **HTTP**       | Application | 80            | Web page and data transfer       |
| **HTTPS**      | Application | 443           | Encrypted web communication      |
| **FTP**        | Application | 20, 21        | File transfer (legacy)           |
| **SFTP**       | Application | 22            | Secure file transfer over SSH    |
| **SSH**        | Application | 22            | Secure remote shell access       |
| **SMTP**       | Application | 25, 587       | Sending email                    |
| **IMAP**       | Application | 143, 993      | Retrieving email (synced)        |
| **POP3**       | Application | 110, 995      | Retrieving email (download)      |
| **DNS**        | Application | 53            | Domain name to IP resolution     |

---

## The Request-Response Cycle

Most application-layer communication follows a request-response pattern:

```text
  Client                                           Server
 ┌────────┐                                       ┌────────┐
 │        │ ──── 1. SYN (connection request) ────▶│        │
 │        │ ◀─── 2. SYN-ACK (acknowledged) ────── │        │
 │        │ ──── 3. ACK (connection open) ───────▶│        │
 │        │                                       │        │
 │        │ ──── 4. HTTP GET /index.html ────────▶│        │
 │        │ ◀─── 5. HTTP 200 OK + HTML ────────── │        │
 │        │                                       │        │
 │        │ ──── 6. FIN (close request) ─────────▶│        │
 │        │ ◀─── 7. FIN-ACK (close acknowledged)──│        │
 └────────┘                                       └────────┘
   Steps 1-3: TCP three-way handshake
   Steps 4-5: Application data exchange
   Steps 6-7: Connection teardown
```

---

## Synchronous vs Asynchronous Communication

**Synchronous communication** requires both the sender and receiver to be active at the same time. The sender waits (blocks) until a response is received before continuing.

- Example: HTTP request-response, SSH session, video call.

**Asynchronous communication** does not require both parties to be active simultaneously. The sender can continue working after transmitting without waiting for an immediate response.

- Example: Email (SMTP), message queues, webhook callbacks.

| Aspect              | Synchronous               | Asynchronous                |
|---------------------|---------------------------|-----------------------------|
| **Blocking**        | Yes — sender waits        | No — sender continues       |
| **Latency impact**  | Directly affects sender   | Decoupled from sender       |
| **Complexity**      | Simpler to reason about   | Requires message handling   |
| **Use case**        | Real-time interactions    | Background processing       |

---

## Connection-Oriented vs Connectionless Communication

| Aspect              | Connection-Oriented (TCP)                  | Connectionless (UDP)                  |
|---------------------|--------------------------------------------|---------------------------------------|
| **Setup**           | Requires handshake before data transfer    | No setup — send immediately           |
| **Reliability**     | Guaranteed delivery, ordering, error check | Best-effort — no delivery guarantee   |
| **Overhead**        | Higher (headers, ACKs, retransmissions)    | Lower (minimal header)               |
| **Speed**           | Slower due to overhead                     | Faster for real-time data             |
| **Use cases**       | Web (HTTP), email (SMTP), file transfer    | DNS queries, video streaming, gaming  |
| **Flow control**    | Yes — adjusts to receiver capacity         | No — sender transmits at will         |
| **State**           | Stateful — tracks connection               | Stateless — each packet independent   |

---

## Practical Note: Preferring HTTP for Data Transfer

For modern application-to-application file and data transfer, **HTTP/HTTPS is generally preferred** over legacy protocols like FTP, SCP, rsync, or SMB. Key reasons include:

- **Validation**: HTTP endpoints can validate incoming data and reject malformed payloads with meaningful error codes.
- **Firewall-friendly**: Port 443 (HTTPS) is open on virtually every network, reducing connectivity issues.
- **Tooling**: Every language and platform has mature HTTP client libraries.
- **Security**: HTTPS provides encryption by default via TLS.

For transferring files via HTTP from shell scripts or cron jobs, tools like
[tbzuploader](https://github.com/guettli/tbzuploader) can be used. This also eliminates the need for
[inotify](https://en.wikipedia.org/wiki/Inotify)-based file-watching daemons — data arrives via HTTP requests instead of being polled from the filesystem.
