# Firewall

## Introduction

A firewall is a network security device (hardware, software, or both) that monitors and controls incoming and outgoing traffic based on a set of predefined security rules. Think of a firewall as border security for a network — it decides what traffic is allowed to enter and exit.

An administrator can configure a firewall to permit or deny traffic based on:

- **Source address** — Where is the traffic coming from?
- **Destination address** — Where is the traffic going?
- **Port number** — What service is the traffic for (e.g., port 80 for HTTP)?
- **Protocol** — Is the traffic TCP, UDP, ICMP, or something else?
- **Application** — Which application is generating the traffic (in next-gen firewalls)?

Firewalls perform **packet inspection** to determine the answers to these questions and enforce the configured policy.

## Firewall Placement in a Network

```text
                          ┌──────────┐
   [Internet] ──────────> │ Firewall │ ──────────> [Internal Network]
                          └──────────┘
                               │
                    Inspects every packet
                    against its rule set
```

Firewalls are typically placed at the **network perimeter** — the boundary between an untrusted external network (the internet) and a trusted internal network. They can also be placed between internal network segments to enforce micro-segmentation.

## Types of Firewalls

### 1. Packet Filtering Firewall

The simplest type. It examines each packet's header (source/destination IP, port, protocol) and compares it against a set of static rules. It does not track connection state.

- **Pros**: Fast, low resource usage
- **Cons**: Cannot detect attacks that span multiple packets; no awareness of connection state

### 2. Stateful Inspection Firewall

Tracks the **state of active connections** (e.g., TCP handshake progress). Instead of evaluating each packet in isolation, it understands whether a packet is part of a new, established, or related connection.

- **Pros**: More intelligent than packet filtering; blocks packets that do not belong to a valid connection
- **Cons**: Higher resource usage; can still be bypassed by application-layer attacks

### 3. Proxy Firewall (Application Gateway)

Acts as an **intermediary** between the client and the server. The client connects to the proxy, and the proxy creates a separate connection to the server. The firewall can inspect the full content of the traffic at the application layer.

- **Pros**: Deep inspection; hides internal network details
- **Cons**: Slower (breaks and re-establishes connections); may not support all protocols

### 4. Next-Generation Firewall (NGFW)

Combines traditional firewall capabilities with additional features such as **deep packet inspection (DPI)**, **intrusion prevention systems (IPS)**, **application awareness**, and **threat intelligence** feeds.

- **Pros**: Comprehensive protection; identifies applications regardless of port
- **Cons**: Expensive; complex to configure and maintain

## Stateful vs Stateless Firewall

| Feature                | Stateful Firewall                          | Stateless Firewall                        |
|------------------------|--------------------------------------------|-------------------------------------------|
| **Inspection**         | Tracks full connection state               | Inspects each packet independently        |
| **Decision basis**     | Connection history + rules                 | Static rules only                         |
| **Resource usage**     | Higher (maintains state table)             | Lower (no state tracking)                 |
| **Intelligence**       | Can block based on connection behavior     | Only matches against predefined rules     |
| **Example behavior**   | Allows return traffic for established connections automatically | Requires explicit rules for both directions |
| **DDoS handling**      | Can be overwhelmed by state-table exhaustion | Handles high-volume traffic more efficiently |
| **Best for**           | General-purpose network security           | High-throughput scenarios (e.g., DDoS mitigation) |

## Firewall Rules and Rule Processing

Firewall rules are processed **top to bottom** in order. The first rule that matches a packet determines the action. If no rule matches, the **default policy** applies (typically deny/drop).

```text
 Incoming Packet
      │
      ▼
 ┌─────────────┐    Match?    ┌────────┐
 │  Rule 1     │──── Yes ────>│ ALLOW  │
 └──────┬──────┘              └────────┘
        │ No
        ▼
 ┌─────────────┐    Match?    ┌────────┐
 │  Rule 2     │──── Yes ────>│ DENY   │
 └──────┬──────┘              └────────┘
        │ No
        ▼
 ┌─────────────┐    Match?    ┌────────┐
 │  Rule 3     │──── Yes ────>│ ALLOW  │
 └──────┬──────┘              └────────┘
        │ No
        ▼
 ┌─────────────────┐
 │ Default Policy  │ (typically DENY)
 └─────────────────┘
```

**Rule order matters.** A more specific rule should be placed above a more general rule. For example, if you want to block one IP address but allow all other traffic, the deny rule for that IP must come before the general allow rule.

## DMZ (Demilitarized Zone)

A DMZ is a network segment that sits between the external (untrusted) network and the internal (trusted) network. Public-facing servers (web servers, email servers, DNS servers) are placed in the DMZ so they are accessible from the internet but isolated from the internal network.

```text
                    ┌──────────────┐
  [Internet] ──────>│ Outer        │
                    │ Firewall     │
                    └──────┬───────┘
                           │
                    ┌──────┴───────┐
                    │     DMZ      │
                    │ [Web Server] │
                    │ [Mail Server]│
                    └──────┬───────┘
                           │
                    ┌──────┴───────┐
                    │ Inner        │
                    │ Firewall     │
                    └──────┬───────┘
                           │
                    [Internal Network]
                    [Workstations, DB]
```

If an attacker compromises a server in the DMZ, the inner firewall still protects the internal network. This **defense-in-depth** approach limits the blast radius of a breach.

## iptables / nftables Examples

On Linux, firewalls are commonly managed with **iptables** (legacy) or **nftables** (modern replacement).

### iptables Examples

```bash
# Set default policy to drop all incoming traffic
iptables -P INPUT DROP

# Allow incoming SSH (port 22) from a specific subnet
iptables -A INPUT -p tcp --dport 22 -s 192.168.1.0/24 -j ACCEPT

# Allow incoming HTTP and HTTPS
iptables -A INPUT -p tcp --dport 80 -j ACCEPT
iptables -A INPUT -p tcp --dport 443 -j ACCEPT

# Allow traffic on established/related connections
iptables -A INPUT -m state --state ESTABLISHED,RELATED -j ACCEPT

# Drop all other incoming traffic (redundant with policy, but explicit)
iptables -A INPUT -j DROP
```

### nftables Examples

```bash
# Create a table and chain
nft add table inet filter
nft add chain inet filter input { type filter hook input priority 0 \; policy drop \; }

# Allow established/related connections
nft add rule inet filter input ct state established,related accept

# Allow SSH from a specific subnet
nft add rule inet filter input ip saddr 192.168.1.0/24 tcp dport 22 accept

# Allow HTTP and HTTPS
nft add rule inet filter input tcp dport { 80, 443 } accept
```

Firewalls range from dedicated hardware appliances found in enterprise networks to software firewalls running on residential routers or individual hosts. Regardless of form factor, the core function remains the same: inspect traffic and enforce a security policy.
