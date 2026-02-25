# IP Protocol

## Introduction

The Internet Protocol (IP) is the principal network-layer protocol responsible for
addressing and routing packets across interconnected networks. Every device on the
internet is identified by an IP address, and IP provides the rules for how data is
packaged, addressed, transmitted, and received.

IP is a **connectionless**, **best-effort** protocol — it does not guarantee delivery,
ordering, or error correction. Reliable delivery is left to higher-layer protocols
such as TCP.

## IPv4 Header Structure

The IPv4 header is a minimum of 20 bytes (without options). Each row below
represents 32 bits (4 bytes).

```text
  0                   1                   2                   3
  0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1
  +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
  |Version|  IHL  |    DSCP   |ECN|         Total Length          |
  +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
  |        Identification         |Flags|    Fragment Offset      |
  +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
  |  Time to Live |   Protocol    |       Header Checksum         |
  +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
  |                      Source Address                           |
  +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
  |                   Destination Address                         |
  +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
  |                  Options (if IHL > 5)         |   Padding     |
  +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
  |                          Payload ...                          |
  +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
```

## IPv4 Header Fields Explained

| Field                | Bits | Description                                                                 |
|----------------------|-----:|-----------------------------------------------------------------------------|
| **Version**          |    4 | IP version — `4` for IPv4.                                                  |
| **IHL**              |    4 | Internet Header Length in 32-bit words (min 5 = 20 bytes).                  |
| **DSCP**             |    6 | Differentiated Services Code Point — QoS/priority marking.                  |
| **ECN**              |    2 | Explicit Congestion Notification.                                           |
| **Total Length**     |   16 | Total size of the datagram (header + payload) in bytes. Max 65,535.         |
| **Identification**   |   16 | Unique ID for the datagram — used to reassemble fragments.                  |
| **Flags**            |    3 | Control bits: Reserved (0), DF (Don't Fragment), MF (More Fragments).       |
| **Fragment Offset**  |   13 | Position of this fragment in the original datagram (in 8-byte units).       |
| **Time to Live**     |    8 | Hop limit — decremented by each router. Packet discarded when TTL = 0.     |
| **Protocol**         |    8 | Upper-layer protocol: `1` = ICMP, `6` = TCP, `17` = UDP.                   |
| **Header Checksum**  |   16 | Error-checking for the header only. Recomputed at each hop.                 |
| **Source Address**   |   32 | Sender's IPv4 address.                                                      |
| **Destination Addr** |   32 | Receiver's IPv4 address.                                                    |
| **Options**          |  var | Optional fields for record route, timestamps, etc. Rarely used today.       |

The data following the header is referred to as the **IP payload**.

## IPv6 Header Structure

IPv6 was designed to address IPv4 exhaustion and simplify header processing.
The IPv6 header is a fixed 40 bytes.

```text
  0                   1                   2                   3
  0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1
  +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
  |Version| Traffic Class |              Flow Label               |
  +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
  |        Payload Length          |  Next Header  |  Hop Limit   |
  +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
  |                                                               |
  +                                                               +
  |                      Source Address (128 bits)                 |
  +                                                               +
  |                                                               |
  +                                                               +
  |                                                               |
  +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
  |                                                               |
  +                                                               +
  |                   Destination Address (128 bits)               |
  +                                                               +
  |                                                               |
  +                                                               +
  |                                                               |
  +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
```

## IPv4 vs IPv6 Comparison

| Feature             | IPv4                          | IPv6                              |
|---------------------|-------------------------------|-----------------------------------|
| Address size        | 32 bits (4 bytes)             | 128 bits (16 bytes)               |
| Address format      | Dotted decimal (`192.0.2.1`)  | Hex colon (`2001:db8::1`)         |
| Address space       | ~4.3 billion                  | ~3.4 × 10³⁸                      |
| Header size         | 20–60 bytes (variable)        | 40 bytes (fixed)                  |
| Fragmentation       | Routers and sender            | Sender only (Path MTU Discovery)  |
| Checksum            | Yes (header only)             | No (removed for efficiency)       |
| NAT required        | Commonly                      | Not needed (enough addresses)     |
| IPsec               | Optional                      | Built-in support                  |
| Broadcast           | Yes                           | No (replaced by multicast)        |

## IP Fragmentation

When a datagram is too large for the Maximum Transmission Unit (MTU) of a link,
it must be fragmented.

```text
  Original Datagram (4000 bytes payload, MTU = 1500)
  +--------------------------------------------------+
  | IP Header |              Payload (4000 bytes)     |
  +--------------------------------------------------+
                          |
                   Fragmentation
                          |
          +---------------+----------------+
          |               |                |
  +-------------+  +-------------+  +-------------+
  | Hdr | 1480B |  | Hdr | 1480B |  | Hdr | 1040B |
  | MF=1        |  | MF=1        |  | MF=0        |
  | Offset=0    |  | Offset=185  |  | Offset=370  |
  +-------------+  +-------------+  +-------------+
     Fragment 1      Fragment 2      Fragment 3
```

- **Identification**: All fragments share the same ID from the original datagram.
- **MF (More Fragments)** flag: Set to 1 on all fragments except the last.
- **Fragment Offset**: Position of this fragment's data in units of 8 bytes.
- Reassembly occurs only at the **destination host**, not at intermediate routers.
- If any fragment is lost, the entire datagram is discarded.

## IP Routing Basics

Routers forward packets toward their destination by consulting a **routing table**.

```text
  Host A                                                 Host B
  10.0.1.5                                              10.0.2.8
     |                                                     |
     |          +----------+          +----------+         |
     +--------->| Router 1 |--------->| Router 2 |-------->+
                +----------+          +----------+
                10.0.1.1              10.0.2.1
```

Each routing table entry contains:
- **Destination network** — the target network address and subnet mask.
- **Next hop** — the IP address of the next router on the path.
- **Interface** — which network interface to forward the packet through.
- **Metric** — cost of the route (used to choose among multiple paths).

Key concepts:
- **Default route** (`0.0.0.0/0`) — used when no specific route matches.
- **Longest prefix match** — the most specific matching route is selected.
- Routing protocols (RIP, OSPF, BGP) allow routers to dynamically learn routes.
