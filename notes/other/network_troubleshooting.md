# Network Troubleshooting

## Introduction

Network troubleshooting is the process of diagnosing and resolving connectivity,
performance, and configuration problems. A systematic approach — combined with the
right tools — is essential for efficient diagnosis.

## Troubleshooting Methodology

```text
  1. Identify the problem
     ▼
  2. Establish a theory of probable cause
     ▼
  3. Test the theory
     ▼
  4. Establish a plan of action
     ▼
  5. Implement the solution
     ▼
  6. Verify full functionality
     ▼
  7. Document the solution
```

A common approach is to work through the **OSI model** from the bottom up:

1. **Physical** — Is the cable plugged in? Is the link light on?
2. **Data Link** — Are MAC addresses correct? Is the switch port up?
3. **Network** — Can you ping the gateway? Is the IP/subnet correct?
4. **Transport** — Is the port open? Is the firewall blocking traffic?
5. **Application** — Is the service running? Are DNS records correct?

## Essential Troubleshooting Tools

### ping

Tests basic connectivity by sending ICMP Echo Request packets and waiting for replies.

```bash
# Basic ping
ping 192.168.1.1

# Ping with count limit
ping -c 4 google.com

# Ping with specific packet size
ping -s 1472 -M do 192.168.1.1    # test MTU (1472 + 28 byte header = 1500)
```

**What it tells you:**
- Whether the host is reachable
- Round-trip time (latency)
- Packet loss percentage

### traceroute / tracert

Shows the path packets take from source to destination, listing each hop along the way.

```bash
# Linux
traceroute google.com

# Windows
tracert google.com

# Use TCP instead of UDP/ICMP (better through firewalls)
traceroute -T -p 443 google.com
```

**What it tells you:**
- Where in the path a failure or high latency occurs
- Each router (hop) between you and the destination

### nslookup / dig

Query DNS records to verify name resolution.

```bash
# Basic lookup
nslookup example.com
dig example.com

# Query specific record type
dig example.com MX
nslookup -type=MX example.com

# Query a specific DNS server
dig @8.8.8.8 example.com
nslookup example.com 8.8.8.8

# Trace full DNS resolution path
dig +trace example.com
```

### netstat / ss

Display network connections, listening ports, and routing tables.

```bash
# Show all listening TCP ports (Linux)
ss -tlnp
# or
netstat -tlnp

# Show all established connections
ss -tnp

# Show UDP listeners
ss -ulnp

# Show routing table
netstat -rn
# or
ip route show
```

### ip (iproute2)

Modern replacement for `ifconfig`, `route`, and `arp` on Linux.

```bash
# Show IP addresses
ip addr show

# Show routing table
ip route show

# Show ARP/neighbor table
ip neigh show

# Show link (interface) status
ip link show

# Bring an interface up/down
ip link set eth0 up
ip link set eth0 down
```

### curl / wget

Test HTTP(S) connectivity and application-layer behavior.

```bash
# Test web server response
curl -I https://example.com          # headers only
curl -v https://example.com          # verbose with TLS details

# Test specific port
curl -v telnet://192.168.1.1:22      # check if SSH port is open

# Download a file
wget https://example.com/file.zip
```

### tcpdump

Capture and analyze network packets on the command line.

```bash
# Capture all traffic on an interface
sudo tcpdump -i eth0

# Capture traffic on a specific port
sudo tcpdump -i eth0 port 80

# Capture traffic to/from a specific host
sudo tcpdump -i eth0 host 192.168.1.100

# Save capture to a file (for Wireshark analysis)
sudo tcpdump -i eth0 -w capture.pcap

# Read a capture file
tcpdump -r capture.pcap
```

### nmap

Network scanner for discovering hosts, open ports, and services.

```bash
# Scan common ports on a host
nmap 192.168.1.1

# Scan a range of hosts
nmap 192.168.1.0/24

# Scan specific ports
nmap -p 22,80,443 192.168.1.1

# Service version detection
nmap -sV 192.168.1.1

# OS detection
nmap -O 192.168.1.1
```

### mtr

Combines `ping` and `traceroute` into a single real-time display.

```bash
mtr google.com
mtr --report -c 100 google.com    # generate a report after 100 cycles
```

## Quick Reference: Tool by Symptom

| Symptom                          | First tool to use       | What to check                     |
|----------------------------------|-------------------------|-----------------------------------|
| No connectivity at all           | `ping` (gateway)        | Physical link, IP config          |
| Can ping IP but not hostname     | `dig` / `nslookup`     | DNS resolution                    |
| Slow connection                  | `mtr` / `traceroute`   | Latency per hop, packet loss      |
| Connection refused               | `ss` / `nmap`          | Service running? Port open?       |
| Intermittent drops               | `mtr` / `ping -c 1000` | Packet loss at specific hops      |
| Website not loading              | `curl -v`              | HTTP response, TLS errors         |
| Unknown traffic on network       | `tcpdump` / Wireshark  | Packet capture and analysis       |
| Need to find hosts on subnet     | `nmap -sn`             | Host discovery ping sweep         |

## Common Issues and Solutions

| Problem                       | Likely Cause                    | Solution                              |
|-------------------------------|---------------------------------|---------------------------------------|
| Duplicate IP address          | DHCP conflict or static clash   | Release/renew DHCP; fix static config |
| Default gateway unreachable   | Misconfigured gateway IP        | Verify gateway IP and subnet mask     |
| DNS resolution failure        | Wrong DNS server, DNS down      | Test with `dig @8.8.8.8`; check `/etc/resolv.conf` |
| High latency to remote host   | Congested link, bad route       | `traceroute` to identify the slow hop |
| Port blocked                  | Firewall rule                   | Check `iptables`/`nft` rules, security groups |
| Interface has no IP            | DHCP server unreachable         | Check DHCP server; try static IP      |
