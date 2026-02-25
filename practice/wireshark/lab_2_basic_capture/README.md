# Lab 2: Basic Traffic Capture and Filters

## Objective

Capture common local traffic and isolate ARP, ICMP, TCP, and UDP packets with display filters.

## Why This Matters

Filtering is the core skill that turns packet capture into analysis. Without filters, traces quickly become too noisy to interpret.

## Traffic Plan

```text
ping 8.8.8.8        -> ICMP
open a website      -> TCP + TLS/HTTP
local network idle  -> ARP broadcasts
```

## Steps

1. Start a live capture on your active interface.
2. Generate traffic:
   - `ping 8.8.8.8 -c 4`
   - Open any website.
3. Apply filters one-by-one:
   - `arp`
   - `icmp`
   - `tcp`
   - `udp`
4. For each protocol, select one packet and record:
   - timestamp
   - source and destination
   - protocol-specific field (example: ICMP type)

## Expected Observations

- ARP packets show address resolution in local network segments.
- ICMP echo request/reply appears in pairs.
- TCP packets show connection-oriented behavior (SYN/ACK patterns).
- UDP packets appear without connection setup packets.
