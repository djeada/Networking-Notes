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

## Exact Commands

Use three terminals while Wireshark is capturing on your active interface.

### Terminal A (TCP server)

```bash
cd /home/runner/work/Networking-Notes/Networking-Notes
python3 scripts/transport/tcp_server.py -b 127.0.0.1 -p 9999
```

### Terminal B (generate ICMP + TCP + UDP)

```bash
cd /home/runner/work/Networking-Notes/Networking-Notes
ping -c 4 8.8.8.8
python3 scripts/transport/tcp_client.py -s 127.0.0.1 -p 9999 -m "lab2 tcp test"
python3 scripts/transport/udp_client.py -s 127.0.0.1 -p 9998 -m "lab2 udp test"
```

### Terminal C (UDP server, optional but recommended)

```bash
cd /home/runner/work/Networking-Notes/Networking-Notes
python3 scripts/transport/udp_server.py -b 127.0.0.1 -p 9998
```
