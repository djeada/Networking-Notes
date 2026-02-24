# iptables and nftables

## Overview

`iptables` (legacy) and `nftables` (modern replacement) are Linux utilities for configuring the kernel's packet filtering rules. They control which network traffic is allowed, blocked, or modified as it enters, leaves, or passes through a system. Understanding firewall rules is essential for securing servers and troubleshooting connectivity issues.

## iptables Basics

### Tables and Chains

iptables organizes rules into **tables**, each containing **chains** of rules:

```text
                    ┌─────────────────────────────────────────────┐
                    │               iptables Tables               │
                    ├─────────────┬───────────┬───────────────────┤
                    │   filter    │    nat    │      mangle       │
                    │  (default)  │           │                   │
                    ├─────────────┼───────────┼───────────────────┤
                    │  INPUT      │ PREROUTING│  PREROUTING       │
                    │  FORWARD    │ OUTPUT    │  INPUT            │
                    │  OUTPUT     │ POSTROUTING│ FORWARD          │
                    │             │           │  OUTPUT           │
                    │             │           │  POSTROUTING      │
                    └─────────────┴───────────┴───────────────────┘
```

| Table    | Purpose                                              |
|----------|------------------------------------------------------|
| `filter` | Default table for accepting, dropping, or rejecting packets |
| `nat`    | Network Address Translation (SNAT, DNAT, masquerade) |
| `mangle` | Packet alteration (TTL, TOS, marking)                |

| Chain        | When Rules Apply                                     |
|--------------|------------------------------------------------------|
| `INPUT`      | Packets destined for the local machine               |
| `OUTPUT`     | Packets originating from the local machine           |
| `FORWARD`    | Packets being routed through the machine             |
| `PREROUTING` | Before routing decision (DNAT)                       |
| `POSTROUTING`| After routing decision (SNAT, masquerade)            |

### Packet Flow

```text
                          INCOMING PACKET
                               │
                          ┌────▼────┐
                          │PREROUTING│ (nat, mangle)
                          └────┬────┘
                               │
                     ┌─── Routing ───┐
                     │   Decision    │
                     └───┬──────┬───┘
                         │      │
                For local?  Forward?
                    │           │
               ┌────▼──┐  ┌────▼───┐
               │ INPUT │  │FORWARD │
               │(filter)│  │(filter)│
               └────┬──┘  └────┬───┘
                    │           │
              Local Process     │
                    │           │
               ┌────▼──┐       │
               │OUTPUT │       │
               │(filter)│       │
               └────┬──┘       │
                    │           │
                    └─────┬─────┘
                     ┌────▼─────┐
                     │POSTROUTING│ (nat, mangle)
                     └────┬─────┘
                          │
                    OUTGOING PACKET
```

### Viewing Rules

```bash
# List all rules in the filter table
sudo iptables -L -n -v

# List rules with line numbers
sudo iptables -L -n --line-numbers

# List rules in a specific chain
sudo iptables -L INPUT -n -v

# List NAT rules
sudo iptables -t nat -L -n -v
```

### Managing Rules

```bash
# Set default policy (ACCEPT or DROP)
sudo iptables -P INPUT DROP
sudo iptables -P FORWARD DROP
sudo iptables -P OUTPUT ACCEPT

# Allow loopback traffic
sudo iptables -A INPUT -i lo -j ACCEPT

# Allow established and related connections
sudo iptables -A INPUT -m state --state ESTABLISHED,RELATED -j ACCEPT

# Allow SSH from a specific subnet
sudo iptables -A INPUT -p tcp --dport 22 -s 192.168.1.0/24 -j ACCEPT

# Allow HTTP and HTTPS from anywhere
sudo iptables -A INPUT -p tcp --dport 80 -j ACCEPT
sudo iptables -A INPUT -p tcp --dport 443 -j ACCEPT

# Allow ping (ICMP)
sudo iptables -A INPUT -p icmp --icmp-type echo-request -j ACCEPT

# Drop all other incoming traffic (explicit, if default is also DROP)
sudo iptables -A INPUT -j DROP

# Delete a rule by line number
sudo iptables -D INPUT 3

# Flush all rules in a chain
sudo iptables -F INPUT

# Flush all rules in all chains
sudo iptables -F
```

### Rule Targets

| Target   | Action                                        |
|----------|-----------------------------------------------|
| `ACCEPT` | Allow the packet through                      |
| `DROP`   | Silently discard the packet                   |
| `REJECT` | Discard and send an error response to sender  |
| `LOG`    | Log the packet and continue to next rule      |
| `SNAT`   | Source NAT (change source address)            |
| `DNAT`   | Destination NAT (change destination address)  |
| `MASQUERADE` | Dynamic SNAT (for outbound NAT)          |

---

## nftables Basics

`nftables` is the successor to iptables, offering a cleaner syntax and better performance.

### Basic Commands

```bash
# List all rules
sudo nft list ruleset

# Create a table
sudo nft add table inet filter

# Create a chain with a default policy
sudo nft add chain inet filter input { type filter hook input priority 0 \; policy drop \; }

# Add rules
sudo nft add rule inet filter input ct state established,related accept
sudo nft add rule inet filter input iif lo accept
sudo nft add rule inet filter input tcp dport 22 accept
sudo nft add rule inet filter input tcp dport { 80, 443 } accept
sudo nft add rule inet filter input icmp type echo-request accept

# Delete a rule (by handle number)
sudo nft -a list chain inet filter input  # show handle numbers
sudo nft delete rule inet filter input handle 5

# Flush a chain
sudo nft flush chain inet filter input

# Delete a table
sudo nft delete table inet filter
```

### nftables vs iptables Comparison

| Feature              | iptables                    | nftables                         |
|----------------------|-----------------------------|----------------------------------|
| Syntax               | Command-line flags          | Structured, scripting-friendly   |
| Performance          | Good                        | Better (fewer kernel operations) |
| Protocol families    | Separate tools (ip6tables, arptables) | Unified (`inet` family) |
| Atomic rule updates  | No                          | Yes                              |
| Sets and maps        | Limited (ipset)             | Native support                   |

---

## Practical Exercises

### Exercise 1: View Current Firewall Rules

Check what rules are currently active:

```bash
sudo iptables -L -n -v --line-numbers
# or with nftables
sudo nft list ruleset
```

### Exercise 2: Build a Basic Firewall

Create a minimal but functional firewall:

```bash
# Flush existing rules
sudo iptables -F

# Set default policies
sudo iptables -P INPUT DROP
sudo iptables -P FORWARD DROP
sudo iptables -P OUTPUT ACCEPT

# Allow loopback
sudo iptables -A INPUT -i lo -j ACCEPT

# Allow established connections
sudo iptables -A INPUT -m state --state ESTABLISHED,RELATED -j ACCEPT

# Allow SSH
sudo iptables -A INPUT -p tcp --dport 22 -j ACCEPT

# Allow ping
sudo iptables -A INPUT -p icmp --icmp-type echo-request -j ACCEPT

# Verify
sudo iptables -L -n -v
```

### Exercise 3: Log Dropped Packets

Add a logging rule before the drop rule to see what is being blocked:

```bash
sudo iptables -A INPUT -j LOG --log-prefix "IPTables-Dropped: " --log-level 4
sudo iptables -A INPUT -j DROP
```

View the logs:

```bash
sudo dmesg | grep "IPTables-Dropped"
# or
sudo journalctl -k | grep "IPTables-Dropped"
```

### Exercise 4: Port Forwarding with NAT

Forward traffic arriving on port 8080 to an internal server on port 80:

```bash
# Enable IP forwarding
sudo sysctl -w net.ipv4.ip_forward=1

# Add DNAT rule
sudo iptables -t nat -A PREROUTING -p tcp --dport 8080 -j DNAT --to-destination 192.168.1.100:80

# Allow forwarded traffic
sudo iptables -A FORWARD -p tcp -d 192.168.1.100 --dport 80 -j ACCEPT

# Add SNAT/masquerade for return traffic
sudo iptables -t nat -A POSTROUTING -j MASQUERADE
```

### Exercise 5: Rate Limiting

Protect against brute-force attacks by limiting connection rate:

```bash
# Allow only 3 new SSH connections per minute from any single IP
sudo iptables -A INPUT -p tcp --dport 22 -m state --state NEW -m recent --set --name SSH
sudo iptables -A INPUT -p tcp --dport 22 -m state --state NEW -m recent --update --seconds 60 --hitcount 4 --name SSH -j DROP
```

### Exercise 6: Save and Restore Rules

Persist your firewall rules across reboots:

```bash
# Save current rules
sudo iptables-save > /tmp/iptables-rules.txt

# View saved rules
cat /tmp/iptables-rules.txt

# Restore rules
sudo iptables-restore < /tmp/iptables-rules.txt
```

On systems with `iptables-persistent`:

```bash
sudo apt install iptables-persistent
sudo netfilter-persistent save
sudo netfilter-persistent reload
```
