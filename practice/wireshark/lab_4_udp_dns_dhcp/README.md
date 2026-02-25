# Lab 4: UDP, DNS, and DHCP Analysis

## Objective

Understand UDP behavior and analyze two common UDP-based protocols: DNS and DHCP.

## UDP vs TCP at a Glance

```text
TCP: handshake + sequencing + retransmission
UDP: no handshake, message-oriented, lower overhead
```

## Steps

1. Apply `udp` filter and identify baseline UDP traffic.
2. Generate DNS traffic:
   - run `nslookup example.com`
   - or open a new domain in browser
3. Apply `dns` filter and pair request/response packets.
4. If DHCP is present, apply `bootp` filter and inspect Discover/Offer/Request/Ack.
5. Compare one TCP flow and one UDP flow from your trace.

## Expected Observations

- DNS request ID matches DNS response ID.
- UDP packets do not contain TCP flags.
- DHCP exchanges reveal address assignment process when visible.
