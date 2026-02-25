# Packet Switching

Packet switching is the dominant method of data transmission in modern networks.
Data is broken into small units called **packets**, each of which is routed
independently through the network. This contrasts with circuit switching, where a
dedicated path is established for the entire duration of a communication session.

---

## Circuit Switching vs Packet Switching

### Circuit Switching

A dedicated communication path is established between two endpoints before data
transfer begins. The path remains reserved for the entire session, even during
silence periods.

- Used in traditional telephone networks (PSTN).
- Three phases: **connection establishment**, **data transfer**, **connection release**.
- Guaranteed bandwidth but wasteful when the channel is idle.

```text
  Phone A                                          Phone B
    |                                                |
    |========= Dedicated Circuit =================== |
    |  (reserved for entire call duration)           |
    |                                                |
    |  Setup ------>  [Switch] ------> [Switch] ---> |
    |                                                |
    |  Data <==============================>  Data   |
    |                                                |
    |  Teardown --->  [Switch] ------> [Switch] ---> |
    |========= Circuit Released =====================|

  Resources reserved even during silence:
  |###DATA###|          silence          |###DATA###|
  |==========|===========================|==========|
       ^            wasted bandwidth           ^
```

### Packet Switching

Data is divided into packets, each containing a header with destination
information. Packets are routed independently and may take different paths.

- Used in the Internet, modern telephone networks, and virtually all data networks.
- No dedicated path — resources are shared.
- Better utilization of network bandwidth.

```text
  Host A                                           Host B
    |                                                |
    |--[Pkt 1]---> Router 1 ---> Router 3 --[Pkt 1]-->|
    |--[Pkt 2]---> Router 1 ---> Router 2 --\        |
    |--[Pkt 3]---> Router 2 -----+            \       |
    |                             |             \      |
    |                             +---> Router 3 -[Pkt 3]->|
    |                                           \-[Pkt 2]->|
    |                                                |
  Packets may arrive out of order and are reassembled
```

### Comparison Table

| Feature | Circuit Switching | Packet Switching |
|---|---|---|
| **Setup** | Connection must be established first | No setup needed; send immediately |
| **Path** | Dedicated, fixed path for entire session | No fixed path; each packet routed independently |
| **Addressing** | Full path address in each data unit | Destination address only; routers decide next hop |
| **Forwarding** | Data bypasses router queues | Store-and-forward through router queues |
| **Transmission** | Only by the source | By source and every intermediate router |
| **Delay** | Uniform / constant | Variable (depends on queuing, routing) |
| **Resources** | Reserved (may be wasted during silence) | Shared (efficient utilization) |
| **Congestion** | During connection establishment | During data transfer |
| **Fault Tolerance** | Low — path is fixed; link failure breaks connection | High — packets rerouted around failures |
| **Reliability** | Reliable; good for long, continuous streams | Best-effort; good for bursty data |
| **Speed** | Slower setup, guaranteed transfer rate | Fast startup, variable transfer rate |

---

## Components of Delay

Every packet traversing a network experiences four types of delay:

```text
  Source                Router                  Destination
    |                     |                        |
    |--[Packet]---------->|--[Packet]------------->|
    |                     |                        |
    |<-- Transmission --> |<--- Propagation ------>|
    |     Delay           |       Delay            |
    |                     |                        |
    |               +-----+-----+                  |
    |               | Processing|                  |
    |               |   Delay   |                  |
    |               +-----------+                  |
    |               | Queueing  |                  |
    |               |   Delay   |                  |
    |               +-----------+                  |

  Total delay (d_total) = d_trans + d_prop + d_proc + d_queue
```

### 1. Transmission (Serialization) Delay

Time to push all bits of the packet onto the link.

  d_trans = Packet Size (bits) / Link Bandwidth (bits/sec)

Example: 1500-byte packet on a 100 Mbps link
  d_trans = (1500 * 8) / (100 * 10^6) = 0.12 ms

### 2. Propagation Delay

Time for a signal to travel from sender to receiver across the physical medium.

  d_prop = Distance / Propagation Speed

- Propagation speed in copper: ~2 * 10^8 m/s
- Propagation speed in fiber: ~2 * 10^8 m/s
- Propagation speed in vacuum/air: ~3 * 10^8 m/s

Example: 1000 km fiber link
  d_prop = 1,000,000 / (2 * 10^8) = 5 ms

### 3. Processing Delay

Time a router takes to examine the packet header, check for errors, and
determine the output link. Typically microseconds in modern routers.

### 4. Queueing Delay

Time the packet waits in the router's output buffer before being transmitted.
Depends on traffic intensity:

  Traffic intensity = (Packet arrival rate * Packet size) / Link bandwidth

- If intensity < 1: queue is stable (small delays)
- If intensity >= 1: queue grows without bound (packets dropped)
- Most variable component of delay

---

## Store-and-Forward vs Cut-Through Switching

### Store-and-Forward

The switch/router must receive the **entire packet** before forwarding it.
This allows error checking (CRC) before forwarding.

```text
  Source           Switch              Destination
    |                |                     |
    |==[Full Pkt]==> |                     |
    |  (entire pkt   | (CRC check, then   |
    |   received)    |  forward)           |
    |                |==[Full Pkt]=======> |
    |                |                     |

  Time:
  |<-- Tt -->|       |<-- Tt -->|
  [transmit  ] wait  [transmit  ]
   to switch   for    to dest
               full
               pkt
```

- **Latency**: At least one full transmission delay per hop.
- **Advantage**: Corrupted frames are detected and dropped.
- **Used in**: Most routers, many enterprise switches.

### Cut-Through

The switch begins forwarding the packet as soon as it reads the destination
address (first 6 bytes for Ethernet), without waiting for the entire frame.

```text
  Source           Switch              Destination
    |                |                     |
    |==[Hdr]=        |                     |
    |   (dest addr   |==[Hdr]=             |
    |    read)       |  (forwarding        |
    |==[...rest]=    |   starts)           |
    |                |==[...rest]========> |
    |                |                     |

  Time:
  |<- Tt ->|                               |
  |        |<- very small ->|<--- Tt ----->|
  [transmit]  [switch delay] [to dest      ]
```

- **Latency**: Much lower per hop (only reads header before forwarding).
- **Disadvantage**: Cannot check CRC; corrupted frames may be forwarded.
- **Variant — Fragment-Free**: Waits for first 64 bytes (minimum frame size) to filter out collision fragments.

---

## Round Trip Time (RTT) and Jitter

### Round Trip Time

RTT is the time for a packet to travel from source to destination and back.

```text
  Source                                    Destination
    |                                          |
    |-------- Request Packet ----------------->|
    |            d1 (one-way delay)            |
    |                                          |
    |<------- Response Packet -----------------|
    |            d2 (return delay)             |
    |                                          |

  RTT = d1 + d2
  (d1 and d2 may differ if paths are asymmetric)
```

- **Measured with**: `ping` command (sends ICMP echo request, measures time to echo reply)
- **Typical values**:
  - Same LAN: < 1 ms
  - Same city: 5–20 ms
  - Cross-continent: 50–100 ms
  - Intercontinental: 100–300 ms

### Jitter

Jitter is the **variation** in delay between packets in a stream.

```text
  Packet 1:  RTT = 50 ms
  Packet 2:  RTT = 55 ms
  Packet 3:  RTT = 48 ms
  Packet 4:  RTT = 70 ms   <-- spike (queuing delay)
  Packet 5:  RTT = 52 ms

  Jitter = variation in these values
  Average RTT = 55 ms, but individual packets vary
```

Sources of jitter:
- **Queueing delay**: Most common source. Varies with network load.
- **Route changes**: Propagation delay changes if packets take different paths.
- **Wireless links**: Transmission delay varies due to changing link conditions.
- **Impact**: Critical for real-time applications (VoIP, video calls, online gaming).

---

## Throughput and Latency

### Throughput

Throughput is the actual rate of successful data transfer over a link or path.

  Throughput = Data transferred / Time taken

- **Bottleneck link**: The link with the smallest bandwidth on the path determines the end-to-end throughput.
- Throughput <= min(bandwidth of each link on the path)
- Shared links reduce effective throughput (e.g., 10 flows sharing a 100 Mbps link each get ~10 Mbps)

```text
  Source ---[10 Mbps]--- R1 ---[1 Mbps]--- R2 ---[10 Mbps]--- Dest
                                  ^
                            Bottleneck link
                     End-to-end throughput <= 1 Mbps
```

### Latency

Latency is the total time for a packet to travel from source to destination.

  Latency = Transmission delay + Propagation delay + Processing delay + Queueing delay

**Latency-sensitive applications**:
- High-frequency trading (microseconds matter)
- Real-time voice/video (Zoom, Teams)
- Online multiplayer gaming
- Remote surgery / telemedicine

**Bandwidth vs Latency**: High bandwidth does not mean low latency. A satellite
link may have high bandwidth (100 Mbps) but high latency (600 ms RTT). A local
Ethernet link has both high bandwidth and low latency.

---

## Packet Structure

Every packet contains a header with control information and a payload with user data.
The exact structure depends on the protocol, but the general concept is:

```text
  +--------------------------------------------------+
  |                    Packet                         |
  +--------+-----------------------------------------+
  | Header |              Payload (Data)              |
  +--------+-----------------------------------------+

  Header contents (typical IP packet):
  +------+------+-----+-------+-------+------+-------+--------+
  | Ver  | IHL  | ToS | Total | Ident | Flags| TTL   | Proto  |
  |      |      |     | Len   |       | +Off |       |        |
  +------+------+-----+-------+-------+------+-------+--------+
  | Source IP Address                                          |
  +------------------------------------------------------------+
  | Destination IP Address                                     |
  +------------------------------------------------------------+
  |                     Payload / Data                         |
  |                   (e.g., TCP segment)                      |
  +------------------------------------------------------------+

  Encapsulation at each layer:
  +------------------------------------------------------------+
  | L2 Hdr | L3 Hdr | L4 Hdr |   Application Data   | L2 Trl |
  | (MAC)  | (IP)   | (TCP)  |                       | (FCS)  |
  +------------------------------------------------------------+
  |<------------ Ethernet Frame --------------------------->|
```

Each layer adds its own header (and sometimes trailer) around the data from the
layer above — this process is called **encapsulation**.
