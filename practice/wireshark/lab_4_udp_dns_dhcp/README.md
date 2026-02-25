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

## Exact Commands

### Terminal A (UDP server)

```bash
cd /home/runner/work/Networking-Notes/Networking-Notes
python3 scripts/transport/udp_server.py -b 127.0.0.1 -p 9998
```

### Terminal B (UDP client + DNS generator)

```bash
cd /home/runner/work/Networking-Notes/Networking-Notes
python3 scripts/transport/udp_client.py -s 127.0.0.1 -p 9998 -m "udp datagram 1"
python3 scripts/transport/udp_client.py -s 127.0.0.1 -p 9998 -m "udp datagram 2"
python3 scripts/application/dns_lookup.py example.com --all
python3 scripts/application/dns_lookup.py github.com --all
```

### Optional DHCP capture trigger (Linux)

```bash
sudo dhclient -r && sudo dhclient
```

If DHCP traffic is not visible on your interface, complete DNS/UDP analysis and mark DHCP as environment-dependent.
