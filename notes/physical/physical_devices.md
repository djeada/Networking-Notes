# Physical Devices

Understanding the differences between network devices is essential for grasping how data moves through a network. Each device operates at a specific layer of the OSI model and serves a distinct purpose.

## Network Device Overview

The following diagram shows where common physical devices sit in a typical network:

```text
  Internet
     |
  [Modem] ---- Converts ISP signal to Ethernet
     |
  [Router] ---- Routes between networks (Layer 3)
     |
     +------ [Firewall] (optional, filters traffic)
     |
  [Switch] ---- Forwards frames by MAC address (Layer 2)
   / | \  \
  /  |  \  \-------[Access Point] ---- Wireless clients
 /   |   \                              (Wi-Fi)
[PC] [PC] [Server]
```

---

## Hub

- **OSI Layer:** Layer 1 (Physical)
- **Function:** Receives an electrical signal on one port and repeats (broadcasts) it out to **all** other ports.
- **Connection:** Connects devices within a single Local Area Network (LAN).
- **Collision Domain:** All hosts connected through a hub share a **single** [collision domain](https://en.wikipedia.org/wiki/Collision_domain), meaning signals sent by any two devices can collide.
- **Intelligence:** None — a hub has no understanding of MAC or IP addresses.

### Signal Broadcast Behavior

When Host A sends a frame, the hub floods it to every other port:

```text
  Host A sends frame to Host C:

  [Host A]---->|            |---->[Host B]  (receives frame, ignores)
               |            |
               |   [HUB]    |
               |            |
  [Host D]<---|            |---->[Host C]  (receives frame, accepts)

  Result: ALL hosts receive the frame. Only Host C processes it.
           Hub = "dumb repeater"
```

> **Note:** Hubs are largely obsolete and have been replaced by switches in modern networks.

---

## Switch

- **OSI Layer:** Layer 2 (Data Link)
- **Function:** Forwards frames based on **MAC addresses** using a MAC address table (CAM table).
- **Connection:** Connects devices within a LAN. Can connect multiple sub-LANs.
- **Collision Domain:** Each port on a switch is its own [collision domain](https://en.wikipedia.org/wiki/Collision_domain).
- **Broadcast Domain:** All ports share the same [broadcast domain](https://en.wikipedia.org/wiki/Broadcast_domain) (unless VLANs are configured).

Switches are used to build LAN networks. Devices connect to the switch via copper cables (CAT-5e, CAT-6) or fiber optic connections plugged into LAN ports. CAT-6 cables allow for faster data transmission than CAT-5.

### MAC Address Table Forwarding

The switch learns which MAC address is on which port and forwards frames only to the correct destination:

```text
  MAC Address Table:
  +----------+-----------+
  | Port     | MAC Addr  |
  +----------+-----------+
  | Fa0/1    | AA:AA:AA  |
  | Fa0/2    | BB:BB:BB  |
  | Fa0/3    | CC:CC:CC  |
  | Fa0/4    | DD:DD:DD  |
  +----------+-----------+

  Host A (AA:AA:AA) sends a frame to Host C (CC:CC:CC):

  [Host A] Fa0/1 ---|                  |--- Fa0/2 [Host B]
                     |                  |   (no frame sent)
                     |    [SWITCH]      |
                     |                  |
  [Host D] Fa0/4 ---|                  |--- Fa0/3 [Host C]
                        (no frame sent)     (frame delivered)

  Result: Only Host C receives the frame. Much more efficient than a hub.
```

---

## Router

- **OSI Layer:** Layer 3 (Network)
- **Function:** Routes packets between **different networks** based on IP addresses using a routing table.
- **Connection:** Connects multiple LANs and Wide Area Networks (WANs) together.
- **Domains:** Each router interface creates a separate collision domain **and** broadcast domain.

### Routing Between Networks

The router examines the destination IP address and forwards the packet to the correct network:

```text
  LAN 1: 192.168.1.0/24              LAN 2: 10.0.0.0/24
  ========================            ========================

  [PC1]---+                                      +---[PC3]
          |                                      |
  [PC2]---[Switch A]---[Router]---[Switch B]---[PC4]
                        |     |
            192.168.1.1 |     | 10.0.0.1
                  (interface)  (interface)

  Routing Table:
  +------------------+-----------+-------------+
  | Destination      | Next Hop  | Interface   |
  +------------------+-----------+-------------+
  | 192.168.1.0/24   | Directly  | Gig0/0      |
  | 10.0.0.0/24      | Directly  | Gig0/1      |
  | 0.0.0.0/0        | ISP       | Gig0/2      |
  +------------------+-----------+-------------+

  PC1 (192.168.1.10) sends a packet to PC4 (10.0.0.20):
    1. Frame arrives at Router on Gig0/0
    2. Router checks routing table -> destination is on Gig0/1
    3. Router forwards packet out Gig0/1 to Switch B
    4. Switch B delivers frame to PC4
```

---

## Modem

- **OSI Layer:** Layer 1 (Physical) / Layer 2 (Data Link)
- **Function:** **Mo**dulates and **dem**odulates signals — converts digital data from your network into the signal type used by your ISP (DSL, cable, fiber) and vice versa.
- **Connection:** Bridges your home/office network to the Internet Service Provider.

### How a Modem Works

```text
  Your Network                    ISP Network
  (Digital)                       (Analog/Optical)

  [Router]----[Modem] )))~~signal~~((( [ISP Equipment]----Internet
                 |
          Modulation: Digital -> Analog (outgoing)
          Demodulation: Analog -> Digital (incoming)
```

> **Note:** Many ISPs provide a combined modem/router device (often called a gateway).

---

## Access Point

- **OSI Layer:** Layer 2 (Data Link)
- **Function:** Provides wireless (Wi-Fi) connectivity to a wired network. Operates similarly to a switch but for wireless clients.
- **Connection:** Connects wireless devices (laptops, phones) to the wired LAN.

```text
  Wired LAN                          Wireless Clients
  =========                          ================

  [Switch]----[Access Point]  )))    [Laptop]
                              )))    [Phone]
                              )))    [Tablet]

  The AP bridges wireless frames to/from the wired network.
```

> Access points can operate in different modes including root mode, bridge mode, and repeater mode.

---

## Repeater

- **OSI Layer:** Layer 1 (Physical)
- **Function:** Regenerates and amplifies a weakened signal to extend the range of a network segment.
- **Connection:** Sits between two segments of the same network.

```text
  Segment 1                                Segment 2
  =========                                =========

  [PC A]----cable (100m)----[Repeater]----cable (100m)----[PC B]

  Without repeater: signal degrades after ~100m (for copper).
  With repeater:    signal is regenerated, extending the reach.
```

---

## Bridge

- **OSI Layer:** Layer 2 (Data Link)
- **Function:** Connects two separate LAN segments and filters traffic based on MAC addresses. Precursor to the modern switch.
- **Connection:** Divides a network into segments to reduce collision domains.

```text
  Segment 1                        Segment 2
  =========                        =========

  [PC A]---[PC B]---[Bridge]---[PC C]---[PC D]

  If PC A sends to PC B:
    -> Bridge sees destination is on Segment 1
    -> Bridge does NOT forward to Segment 2 (filters)

  If PC A sends to PC C:
    -> Bridge sees destination is on Segment 2
    -> Bridge forwards the frame across
```

> A switch is essentially a multiport bridge with hardware-based forwarding.

---

## Comparison Table

| Device       | OSI Layer        | Uses Addresses | Broadcast Domain       | Collision Domain        |
|--------------|------------------|----------------|------------------------|-------------------------|
| Hub          | Layer 1          | None           | Single (shared)        | Single (shared)         |
| Repeater     | Layer 1          | None           | Single (shared)        | Single (shared)         |
| Bridge       | Layer 2          | MAC            | Single (shared)        | Separate per segment    |
| Switch       | Layer 2          | MAC            | Single (shared/VLANs)  | Separate per port       |
| Access Point | Layer 2          | MAC            | Single (shared)        | Shared (wireless medium)|
| Router       | Layer 3          | IP             | Separate per interface | Separate per interface  |
| Modem        | Layer 1 / 2      | Varies         | N/A (signal conversion)| N/A (signal conversion) |
