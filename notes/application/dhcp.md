# DHCP (Dynamic Host Configuration Protocol)

## Introduction

The Dynamic Host Configuration Protocol (DHCP) is an application-layer protocol that
automatically assigns IP addresses and other network configuration parameters to devices
on a network. Without DHCP, an administrator would need to manually configure every
device — DHCP automates this process.

- DHCP uses **UDP** on **port 67** (server) and **port 68** (client).
- It is defined in **RFC 2131**.

## How DHCP Works

DHCP follows a four-step process commonly known as **DORA**:

```text
  Client                                DHCP Server
    |                                        |
    |---1. DHCP Discover (broadcast)-------->|
    |                                        |
    |<--2. DHCP Offer (unicast/broadcast)----|
    |                                        |
    |---3. DHCP Request (broadcast)--------->|
    |                                        |
    |<--4. DHCP Acknowledgment (unicast)-----|
    |                                        |
    | Client now has an IP address and       |
    | network configuration.                 |
```

### Step-by-Step

1. **Discover** — The client broadcasts a `DHCPDISCOVER` message on the local network
   to find available DHCP servers. The client has no IP address yet, so the source
   address is `0.0.0.0` and the destination is `255.255.255.255`.

2. **Offer** — Each DHCP server that receives the discover message responds with a
   `DHCPOFFER` containing an available IP address and configuration parameters.

3. **Request** — The client selects one offer and broadcasts a `DHCPREQUEST` message
   indicating which server's offer it has accepted.

4. **Acknowledgment** — The chosen server sends a `DHCPACK` confirming the lease. The
   client can now use the assigned IP address for the duration of the lease.

## Information Provided by DHCP

DHCP can supply more than just an IP address:

| Parameter              | DHCP Option | Example              |
|------------------------|:-----------:|----------------------|
| IP Address             | —           | `192.168.1.100`      |
| Subnet Mask            | Option 1    | `255.255.255.0`      |
| Default Gateway        | Option 3    | `192.168.1.1`        |
| DNS Server(s)          | Option 6    | `8.8.8.8`            |
| Lease Time             | Option 51   | `86400` (seconds)    |
| Domain Name            | Option 15   | `example.local`      |

## DHCP Lease Lifecycle

```text
  ┌──────────────┐
  │  No Address  │
  └──────┬───────┘
         │ DORA process
         ▼
  ┌──────────────┐
  │  Lease       │──── Lease expires ──── back to No Address
  │  Acquired    │
  └──────┬───────┘
         │ At 50% of lease time (T1)
         ▼
  ┌──────────────┐
  │  Renewal     │──── Server responds ──── Lease extended
  │  (unicast)   │
  └──────┬───────┘
         │ At 87.5% of lease time (T2)
         ▼
  ┌──────────────┐
  │  Rebinding   │──── Any server responds ──── Lease extended
  │  (broadcast) │──── No response ──── Lease expires
  └──────────────┘
```

- **T1 (Renewal timer)**: At 50% of the lease duration, the client unicasts a renewal
  request to the server that granted the lease.
- **T2 (Rebinding timer)**: At 87.5% of the lease duration, if renewal failed, the
  client broadcasts a request to any available DHCP server.
- If no server responds by the time the lease expires, the client loses its IP address.

## DHCP Relay

In networks with multiple subnets, broadcast messages do not cross router boundaries.
A **DHCP relay agent** (often configured on the router) forwards DHCP messages between
clients on one subnet and a DHCP server on another.

```text
  Client (Subnet A)       Router (Relay Agent)       DHCP Server (Subnet B)
       |                         |                           |
       |-- DHCP Discover ------->|                           |
       |  (broadcast)            |-- DHCP Discover --------->|
       |                         |  (unicast to server)      |
       |                         |<-- DHCP Offer ------------|
       |<-- DHCP Offer ----------|                           |
       |                         |                           |
```

## DHCP vs Static IP Assignment

| Aspect             | DHCP                                | Static                             |
|--------------------|-------------------------------------|-------------------------------------|
| Configuration      | Automatic                           | Manual per device                   |
| Administration     | Centralized on DHCP server          | Must configure each device          |
| IP conflicts       | Managed by the server               | Risk of duplicate assignments       |
| Best for           | End-user devices, large networks    | Servers, printers, network devices  |
| Flexibility        | Easy to change network settings     | Requires reconfiguring each device  |

## Common DHCP Server Software

- **ISC DHCP** (`dhcpd`) — widely used open-source DHCP server on Linux.
- **dnsmasq** — lightweight DNS and DHCP server, common on home routers.
- **Windows DHCP Server** — built into Windows Server.
- **Kea** — modern, open-source DHCP server from ISC (successor to `dhcpd`).

In Wi-Fi networks, the **access point** or **home router** typically acts as the DHCP
server, assigning addresses to all connected wireless clients.

## DHCP in a Home Wi-Fi Network

When a device connects to a typical home Wi-Fi network, it joins a **private subnet**
that is already defined by the router. The router's DHCP server assigns the device an
address from that subnet automatically.

### Private IPv4 Addresses (RFC 1918)

Home and office networks use **private IP address ranges** defined in RFC 1918. These
addresses are not routable on the public internet:

```text
10.0.0.0    – 10.255.255.255   (10.0.0.0/8)
172.16.0.0  – 172.31.255.255   (172.16.0.0/12)
192.168.0.0 – 192.168.255.255  (192.168.0.0/16)
```

### Typical Home Network Example

A common home setup using the `192.168.1.0/24` subnet:

```text
Role             Address          Notes
─────────────────────────────────────────────────
Router / GW      192.168.1.1      DHCP server, default gateway
Laptop           192.168.1.20     assigned by DHCP
Phone            192.168.1.21     assigned by DHCP
Tablet           192.168.1.22     assigned by DHCP
Subnet mask      255.255.255.0    → prefix length /24
```

All devices share the `192.168.1.0/24` subnet and can communicate directly with each
other without passing through the router.

### Router Roles in a Home Network

A single home router commonly performs several functions simultaneously:

- **Wireless access point** — provides Wi-Fi connectivity for client devices.
- **DHCP server** — assigns IP addresses, subnet mask, default gateway, and DNS
  server to each client.
- **Default gateway** — forwards traffic from the private subnet to external networks.
- **NAT gateway** — translates private addresses to the single public IP assigned by
  the ISP (see `notes/network/nat.md` for details).

### DORA on a Wi-Fi Client

When a device joins the Wi-Fi network, it has no IP address and follows the DORA
process to obtain one from the router's DHCP server:

```text
  Wi-Fi Client                          Home Router (DHCP Server)
       |                                          |
       |-- 1. Discover (broadcast) -------------->|  "Any DHCP server here?"
       |        src: 0.0.0.0, dst: 255.255.255.255|
       |                                          |
       |<-- 2. Offer ----------------------------|  "Use 192.168.1.20,
       |                                          |   GW: 192.168.1.1,
       |                                          |   lease: 24 h"
       |                                          |
       |-- 3. Request (broadcast) -------------->|  "I'll take 192.168.1.20."
       |                                          |
       |<-- 4. Acknowledge ----------------------|  "Confirmed. Lease granted."
       |                                          |
```

### Lease Table and Duplicate Address Prevention

The DHCP server keeps a **lease table** that records which address has been assigned
to which device (identified by MAC address):

```text
IP Address       MAC Address        Lease Expires
────────────────────────────────────────────────────
192.168.1.20     AA:BB:CC:DD:EE:01  2026-03-11 08:00
192.168.1.21     AA:BB:CC:DD:EE:02  2026-03-11 09:15
192.168.1.22     AA:BB:CC:DD:EE:03  2026-03-11 10:30
```

Before issuing a new lease, the server checks the table to ensure the address is not
already in use, preventing duplicate assignments under normal operation.

### IP Address Conflicts and Detection

DHCP prevents most conflicts, but a duplicate address can still arise when a device is
**manually configured with a static IP** that falls inside the DHCP pool:

```text
DHCP client  →  192.168.1.50  (assigned by router)
Static device →  192.168.1.50  (manually set — conflict!)
```

Operating systems typically detect this situation using **ARP**: on first use of an
address a host sends a gratuitous ARP (or ARP probe); if another device replies, both
devices report an IP address conflict. See `notes/data_link/arp.md` for the full ARP
and gratuitous-ARP mechanism.

To avoid such conflicts, configure the router's DHCP pool to exclude any addresses
reserved for static assignment (e.g., reserve `192.168.1.2`–`192.168.1.19` for static
devices and let DHCP assign from `192.168.1.20` upward).
