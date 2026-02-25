# ARP (Address Resolution Protocol)

## Introduction

The Address Resolution Protocol (ARP) maps a known **network-layer address** (IPv4) to an
unknown **data-link-layer address** (MAC). When a host wants to send a frame on a local
network, it needs the destination's MAC address — ARP provides the mechanism to discover it.

- Defined in **RFC 826**.
- Operates between the **data link layer** and the **network layer**.
- Works only within a single broadcast domain (LAN).

## Why ARP Is Needed

IP addresses are logical and used for routing across networks. MAC addresses are physical
and used for frame delivery on a local link. A device may know the destination IP but not
the MAC address needed to construct an Ethernet frame.

```text
  Host A knows:          Host A needs:
  ┌─────────────────┐    ┌──────────────────────┐
  │ Dest IP:         │    │ Dest MAC: ??:??:??   │
  │ 192.168.1.20     │    │                      │
  └─────────────────┘    └──────────────────────┘

  ARP resolves:  192.168.1.20  →  AA:BB:CC:DD:EE:FF
```

## ARP Process

```text
  Host A                                       Host B
  192.168.1.10                                 192.168.1.20
  MAC: 11:22:33:44:55:66                       MAC: AA:BB:CC:DD:EE:FF
       |                                            |
       |--- ARP Request (broadcast) --------------->|  "Who has 192.168.1.20?
       |    Dest MAC: FF:FF:FF:FF:FF:FF             |   Tell 192.168.1.10"
       |                                            |
       |<-- ARP Reply (unicast) --------------------|  "192.168.1.20 is at
       |    Dest MAC: 11:22:33:44:55:66             |   AA:BB:CC:DD:EE:FF"
       |                                            |
```

1. **ARP Request** — Host A broadcasts a frame to all devices on the LAN asking
   "Who has IP 192.168.1.20? Tell 192.168.1.10."
2. **ARP Reply** — Host B recognizes its own IP and responds with a unicast frame
   containing its MAC address.
3. Host A stores the mapping in its **ARP cache** for future use.

## ARP Packet Structure

| Field                  | Size     | Description                                  |
|------------------------|----------|----------------------------------------------|
| Hardware Type          | 2 bytes  | Type of link layer (1 = Ethernet)            |
| Protocol Type          | 2 bytes  | Protocol address type (0x0800 = IPv4)        |
| Hardware Address Len   | 1 byte   | Length of MAC address (6 for Ethernet)        |
| Protocol Address Len   | 1 byte   | Length of IP address (4 for IPv4)             |
| Operation              | 2 bytes  | 1 = Request, 2 = Reply                       |
| Sender Hardware Addr   | 6 bytes  | MAC address of the sender                    |
| Sender Protocol Addr   | 4 bytes  | IP address of the sender                     |
| Target Hardware Addr   | 6 bytes  | MAC address of the target (0 in requests)    |
| Target Protocol Addr   | 4 bytes  | IP address of the target                     |

## ARP Cache

Every host maintains an ARP cache (also called an ARP table) — a mapping of IP addresses
to MAC addresses for recently communicated hosts.

```bash
# View ARP cache on Linux
arp -a
# or
ip neigh show

# View ARP cache on Windows
arp -a

# Manually add a static ARP entry
arp -s 192.168.1.20 AA:BB:CC:DD:EE:FF
```

Cache entries have a **timeout** (typically 60–300 seconds). If an entry expires, the host
must perform ARP again the next time it needs to reach that address.

## ARP When the Destination Is on a Different Subnet

When the destination IP is on a different network, the host sends the frame to its
**default gateway** (router). ARP resolves the router's MAC address, not the final
destination's.

```text
  Host A              Router                  Host B
  192.168.1.10        192.168.1.1             10.0.0.5
       |                   |                       |
       |  ARP: who has     |                       |
       |  192.168.1.1?     |                       |
       |------------------>|                       |
       |<-- Router MAC ----|                       |
       |                   |                       |
       | Frame: Dest MAC = Router MAC              |
       | IP Dest = 10.0.0.5                        |
       |------------------>|                       |
       |                   |--- routes packet ---->|
```

The IP destination remains `10.0.0.5`, but the Ethernet frame's destination MAC is the
router's MAC. The router then performs its own ARP on the destination subnet if needed.

## Gratuitous ARP

A gratuitous ARP is an ARP request or reply where the sender and target protocol addresses
are the same. Hosts send gratuitous ARPs to:

- **Announce their presence** on the network after boot.
- **Detect IP conflicts** — if another host replies, there is a duplicate IP.
- **Update ARP caches** — all hosts on the LAN update their cache with the new mapping
  (useful after a NIC replacement or failover).

## Proxy ARP

A router can answer ARP requests on behalf of hosts on a different subnet, making
separate subnets appear as one network. This is called **Proxy ARP** (RFC 1027).

```text
  Host A (10.0.1.5)        Router           Host B (10.0.2.8)
       |                     |                    |
       | ARP: who has        |                    |
       | 10.0.2.8?           |                    |
       |-------------------->|                    |
       |<-- Router's MAC ----|  (proxy ARP)       |
       |                     |                    |
```

The router replies with its own MAC. When Host A sends a frame to that MAC, the router
forwards it to Host B.

## ARP Security Concerns

### ARP Spoofing / ARP Poisoning

Because ARP has no authentication, an attacker can send forged ARP replies to associate
their MAC address with another host's IP. This enables:

- **Man-in-the-middle attacks** — attacker intercepts traffic between two hosts.
- **Denial of service** — traffic is redirected to a non-existent MAC.
- **Session hijacking** — attacker takes over an active session.

### Mitigations

| Technique                  | Description                                                   |
|----------------------------|---------------------------------------------------------------|
| **Dynamic ARP Inspection** | Switch feature that validates ARP packets against a trusted binding table. |
| **Static ARP entries**     | Manually configured entries that cannot be overwritten.       |
| **802.1X / Port Security** | Limits which devices can connect to a switch port.            |
| **ARP monitoring tools**   | Software like `arpwatch` that alerts on ARP table changes.    |

## ARP vs NDP (IPv6)

IPv6 replaces ARP with the **Neighbor Discovery Protocol (NDP)**, which uses ICMPv6
messages instead of a separate protocol. NDP provides the same address resolution
function and adds features like router discovery and address autoconfiguration.

| Feature            | ARP (IPv4)                     | NDP (IPv6)                         |
|--------------------|--------------------------------|------------------------------------|
| Layer              | Between L2 and L3              | ICMPv6 (L3)                       |
| Broadcast          | Yes (ARP request)              | No (uses multicast)                |
| Security           | None built-in                  | Can use SEND (Secure NDP)          |
| Additional roles   | Address resolution only         | Router discovery, autoconfiguration|
