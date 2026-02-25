# Ethernet

Ethernet is the most widely used LAN (Local Area Network) technology in the world.
It operates primarily at the **Data Link Layer (Layer 2)** and the **Physical Layer
(Layer 1)** of the OSI model. Ethernet defines how devices on a shared medium
communicate using frames, MAC addresses, and well-defined access methods.

---

## Introduction and History

- **1973**: Robert Metcalfe invented Ethernet at Xerox PARC (Palo Alto Research Center).
- **1980**: DEC, Intel, and Xerox published the DIX Ethernet standard (Ethernet II).
- **1983**: IEEE formalized Ethernet as the **IEEE 802.3** standard.
- **1995**: Fast Ethernet (100 Mbps) introduced as IEEE 802.3u.
- **1999**: Gigabit Ethernet (1 Gbps) over copper as IEEE 802.3ab.
- **2010+**: 40 Gbps and 100 Gbps standards (802.3ba). 400 Gbps (802.3bs) followed.
- Today, Ethernet supports speeds from 10 Mbps to 400 Gbps and beyond, serving
  everything from home networks to hyperscale data centers.

### Key Properties

- **Backward Compatibility**: Newer standards remain compatible with older ones through auto-negotiation.
- **Versatility**: Supports copper (twisted pair), fiber optic, and even coaxial media.
- **IEEE 802.3**: Defines rules for configuring an Ethernet network, specifies
  interactions between Ethernet elements, and ensures multi-vendor compatibility.

---

## Ethernet in the OSI Model

```text
+--------------------------------------------------+
|            Network Layer (Layer 3)                |
|            IP addressing and routing              |
+--------------------------------------------------+
|  Data Link Layer (Layer 2)                        |
|  +--------------------------------------------+  |
|  |  LLC sublayer (IEEE 802.2)                  |  |
|  |  - Protocol multiplexing                    |  |
|  |  - Flow control                             |  |
|  +--------------------------------------------+  |
|  |  MAC sublayer (IEEE 802.3)                  |  |
|  |  - MAC addressing                           |  |
|  |  - Frame construction / parsing             |  |
|  |  - CSMA/CD access method                    |  |
|  +--------------------------------------------+  |
+--------------------------------------------------+
|            Physical Layer (Layer 1)               |
|            Electrical/optical signaling           |
|            Cable specifications                   |
+--------------------------------------------------+
```

---

## Ethernet Frame Structure

An Ethernet II (DIX) frame is structured as follows:

```text
+----------+----------+----------+------+-----------------+-----+
| Preamble |  Dest    |  Source  | Type |     Payload     | FCS |
| + SFD    |  MAC     |  MAC    |      |                 |     |
+----------+----------+----------+------+-----------------+-----+
| 8 bytes  | 6 bytes  | 6 bytes |  2B  |  46-1500 bytes  | 4B  |
```

| Field | Size | Description |
|---|---|---|
| **Preamble + SFD** | 8 bytes | 7 bytes of `10101010` pattern for clock sync, followed by 1 byte Start Frame Delimiter (`10101011`) |
| **Destination MAC** | 6 bytes | MAC address of the intended receiver |
| **Source MAC** | 6 bytes | MAC address of the sender |
| **Type / EtherType** | 2 bytes | Identifies the upper-layer protocol (e.g., `0x0800` = IPv4, `0x0806` = ARP, `0x86DD` = IPv6) |
| **Payload** | 46–1500 bytes | Data from the upper layer. Padded to 46 bytes minimum |
| **FCS** | 4 bytes | Frame Check Sequence (CRC-32) for error detection |

- **Minimum frame size**: 64 bytes (excluding preamble) — ensures collision detection in CSMA/CD.
- **Maximum frame size**: 1518 bytes (excluding preamble).
- **MTU (Maximum Transmission Unit)**: 1500 bytes (payload only).
- **Jumbo Frames**: Non-standard frames with payloads up to 9000 bytes, supported by many switches and NICs.

---

## MAC Address Structure

A MAC (Media Access Control) address is a 48-bit (6-byte) hardware identifier,
written as 12 hexadecimal digits.

```text
  MAC Address:  AA:BB:CC:DD:EE:FF

  +------------------------+------------------------+
  |          OUI           |     Serial Number      |
  |  (Organizationally     |   (Assigned by the     |
  |   Unique Identifier)   |    vendor/NIC maker)   |
  +------------------------+------------------------+
  |  AA  :  BB  :  CC      |  DD  :  EE  :  FF      |
  | <--- 24 bits (3B) ---> | <--- 24 bits (3B) ---> |

  Bit layout of first octet (AA):
  +---+---+---+---+---+---+---+---+
  | 7 | 6 | 5 | 4 | 3 | 2 | 1 | 0 |
  +---+---+---+---+---+---+---+---+
                              |   |
                              |   +-- I/G bit: 0 = Unicast
                              |               1 = Multicast
                              +------ U/L bit: 0 = Globally unique (BIA)
                                               1 = Locally administered
```

- **OUI**: First 3 bytes. Assigned by IEEE to the hardware vendor.
- **Serial Number**: Last 3 bytes. Assigned by the vendor to each NIC.
- **Broadcast MAC**: `FF:FF:FF:FF:FF:FF` (all bits set to 1).
- **Finding MAC addresses**:
  - Linux: `ip link show` or `ifconfig`
  - Windows: `ipconfig /all` or `getmac`
  - macOS: `ifconfig`

---

## Ethernet Switching

Ethernet switches operate at Layer 2 and forward frames based on their MAC
address tables.

### How a Switch Learns and Forwards

```text
   Host A                                       Host B
  (MAC: AA)                                    (MAC: BB)
     |                                            |
     | Port 1        SWITCH          Port 3       |
     +--------[1]---[  MAC   ]---[3]--------------+
                    [ Table  ]
                    [--------]
     +--------[2]---[        ]---[4]--------------+
     |              [        ]                    |
  Host C                                       Host D
  (MAC: CC)                                    (MAC: DD)

  MAC Address Table:
  +-----------+------+
  | MAC Addr  | Port |
  +-----------+------+
  | AA        |  1   |
  | BB        |  3   |
  | CC        |  2   |
  | DD        |  4   |
  +-----------+------+
```

### Frame Forwarding Behavior

| Frame Type | Behavior |
|---|---|
| **Known Unicast** | Switch looks up destination MAC in table, forwards to the specific port |
| **Unknown Unicast** | Destination MAC not in table; frame is flooded to all ports except the incoming port |
| **Broadcast** | Destination = `FF:FF:FF:FF:FF:FF`; flooded to all ports except the incoming port |
| **Multicast** | By default, flooded like broadcast; IGMP snooping can limit this |

### Learning Process

1. Frame arrives on Port 1 from Host A (source MAC = AA).
2. Switch records: MAC AA is reachable via Port 1.
3. Switch checks destination MAC in its table.
4. If found, forward to that port. If not found, flood.
5. Entries age out after a timer (typically 300 seconds) if no traffic is seen.

---

## Ethernet Standards

| Standard | Speed | Medium | Max Distance | IEEE |
|---|---|---|---|---|
| 10BASE-T | 10 Mbps | Cat 3+ UTP | 100 m | 802.3i |
| 100BASE-TX | 100 Mbps | Cat 5 UTP | 100 m | 802.3u |
| 100BASE-FX | 100 Mbps | Multimode Fiber | 400 m (HD), 2 km (FD) | 802.3u |
| 1000BASE-T | 1 Gbps | Cat 5e+ UTP | 100 m | 802.3ab |
| 1000BASE-SX | 1 Gbps | Multimode Fiber | 220–550 m | 802.3z |
| 1000BASE-LX | 1 Gbps | Single-mode Fiber | 5 km | 802.3z |
| 10GBASE-T | 10 Gbps | Cat 6a/7 UTP | 100 m | 802.3an |
| 10GBASE-SR | 10 Gbps | Multimode Fiber | 26–400 m | 802.3ae |
| 10GBASE-LR | 10 Gbps | Single-mode Fiber | 10 km | 802.3ae |
| 25GBASE-SR | 25 Gbps | Multimode Fiber | 100 m | 802.3by |
| 40GBASE-SR4 | 40 Gbps | Multimode Fiber | 100–150 m | 802.3ba |
| 100GBASE-SR10 | 100 Gbps | Multimode Fiber | 100–150 m | 802.3ba |
| 400GBASE-SR16 | 400 Gbps | Multimode Fiber | 100 m | 802.3bs |

- **Naming convention**: `[Speed]BASE-[Encoding/Medium]`
  - Speed in Mbps or Gbps
  - BASE = baseband signaling
  - T = twisted-pair copper, S = short-wavelength fiber, L = long-wavelength fiber

---

## Layer 2 vs Layer 3 Switching

| Feature | Layer 2 Switching | Layer 3 Switching (Routing) |
|---|---|---|
| **OSI Layer** | Data Link (Layer 2) | Network (Layer 3) |
| **Address Used** | MAC address | IP address |
| **Scope** | Within a single LAN / VLAN | Between different subnets / networks |
| **Speed** | Very fast (hardware-based, ASIC) | Slightly slower (routing table lookup) |
| **Broadcast Domain** | All ports in same VLAN share one | Each interface is a separate broadcast domain |
| **Protocols** | STP, VLANs, LACP | OSPF, BGP, RIP, static routes |
| **Use Case** | Connecting devices in same subnet | Connecting different subnets or WANs |

### Multi-Layer Switching

Modern enterprise switches often combine Layer 2 and Layer 3 functionality:
- Perform wire-speed routing between VLANs using hardware (ASICs).
- Support both switching (MAC-based) and routing (IP-based) in a single device.
- Provide flexibility in network design: use Layer 2 within access layer and
  Layer 3 at the distribution/core layers.
