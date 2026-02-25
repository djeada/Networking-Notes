# UDP (User Datagram Protocol)

## Introduction

UDP is a **connectionless**, **lightweight** transport layer protocol defined in RFC 768. Unlike TCP, UDP does not establish a connection before sending data — it simply sends datagrams and hopes they arrive. There are no handshakes, no acknowledgments, and no guaranteed delivery. This makes UDP extremely fast and efficient for use cases where speed matters more than reliability.

UDP is used by DNS, DHCP, SNMP, video/audio streaming, online gaming, and VoIP.

---

## UDP Header

The UDP header is only **8 bytes** — much smaller than TCP's minimum 20-byte header.

```text
 0                   1                   2                   3
 0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
|          Source Port          |       Destination Port        |
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
|            Length             |           Checksum            |
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
|                                                               |
|                         Data / Payload                        |
|                                                               |
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
```

### Header Fields

| Field | Size | Description |
|---|---|---|
| Source Port | 16 bits | Port opened by the sender. Randomly chosen from available ports (0–65535). |
| Destination Port | 16 bits | Port of the application on the remote host (e.g., 53 for DNS). Not chosen randomly. |
| Length | 16 bits | Total length of the UDP datagram (header + data) in bytes. Minimum is 8 (header only). |
| Checksum | 16 bits | Optional error-detection value (mandatory in IPv6). Covers header and data. |

---

## Key Characteristics of UDP

- **Connectionless** — No handshake or connection setup. Each datagram is independent.
- **Unreliable** — No guarantees of delivery, ordering, or duplicate protection.
- **No flow control** — The sender can transmit as fast as it wants; the receiver may drop packets.
- **No congestion control** — UDP does not back off when the network is congested.
- **Low overhead** — Only 8 bytes of header per datagram.
- **Fast** — No round-trip delays for connection setup or acknowledgments.

---

## UDP Communication Model

UDP uses a simple fire-and-forget model. There is no handshake and no acknowledgment.

```text
     Client                                   Server
       |                                         |
       |  UDP Datagram (data)                     |
       |----------------------------------------->|
       |                                         |
       |  UDP Datagram (data)                     |
       |----------------------------------------->|
       |                                         |
       |  UDP Datagram (response)                 |
       |<-----------------------------------------|
       |                                         |

   * No connection setup          * No ACKs
   * No guaranteed delivery       * No ordering
   * Datagrams may arrive out of order, duplicated, or not at all
```

Compare this to TCP, which requires a full three-way handshake before any data is sent.

---

## UDP Socket Programming

In the UDP packet payload, a port number identifies the target application. The OS maintains a mapping of port numbers to open sockets.

### Client vs Server

| Role | Description |
|---|---|
| **Client** | The OS chooses a unique ephemeral port number when sending to a remote server. The client must know the server's IP address and port. |
| **Server** | You create a socket, bind it to a specific port, and listen for incoming datagrams addressed to that IP + port combination. |

```text
  Client (ephemeral port 54321)           Server (port 53 - DNS)
       |                                         |
       |  "Query: example.com"                    |
       |  src=54321, dst=53                       |
       |----------------------------------------->|
       |                                         |
       |  "Answer: 93.184.216.34"                 |
       |  src=53, dst=54321                       |
       |<-----------------------------------------|
       |                                         |
```

---

## Use Cases for UDP

| Use Case | Why UDP? |
|---|---|
| **DNS** | Quick single request/response lookups. Retrying a lost query is cheaper than maintaining a connection. |
| **Video/Audio Streaming** | A few lost frames are acceptable; low latency is critical. |
| **Online Gaming** | Real-time position updates must be fast; stale data is useless anyway. |
| **VoIP** | Voice calls need low latency; minor packet loss causes only brief glitches. |
| **DHCP** | Client has no IP address yet, so a connectionless broadcast is required. |
| **SNMP** | Simple network monitoring queries that are lightweight and fast. |
| **TFTP** | Trivial file transfers on local networks where simplicity is preferred. |

---

## Advantages and Disadvantages

| Advantages | Disadvantages |
|---|---|
| Very fast — no connection overhead | No guarantee of delivery |
| Low latency — no handshake delay | Packets can arrive out of order |
| Small header — only 8 bytes | No built-in congestion control |
| Supports broadcast and multicast | Application must handle reliability if needed |
| Simple to implement | No flow control — receiver can be overwhelmed |
