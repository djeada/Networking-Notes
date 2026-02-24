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
