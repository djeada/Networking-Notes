# Ping

## Overview

`ping` is one of the most fundamental network diagnostic tools. It sends **ICMP Echo Request** packets to a target host and listens for **ICMP Echo Reply** responses, measuring round-trip time and packet loss. Use it as a first step to verify whether a remote host is reachable and to gauge network latency.

## How Ping Works

```text
  Source                                  Destination
    |                                          |
    |--- ICMP Echo Request (seq=1) ----------->|
    |<-- ICMP Echo Reply   (seq=1) ------------|
    |                                          |
    |--- ICMP Echo Request (seq=2) ----------->|
    |<-- ICMP Echo Reply   (seq=2) ------------|
    |                                          |
```

1. The source sends an ICMP Echo Request with a sequence number and timestamp.
2. The destination receives the request and replies with an ICMP Echo Reply.
3. The source calculates the round-trip time (RTT) from the timestamp difference.

## Basic Usage

```bash
# Ping a host by domain name
ping example.com

# Ping a host by IP address
ping 8.8.8.8

# Ping with a specific count (stop after 5 packets)
ping -c 5 example.com

# Ping with a specific interval (every 0.5 seconds)
ping -i 0.5 example.com

# Ping with a specific packet size (1000 bytes)
ping -s 1000 example.com
```

## Reading Ping Output

```text
$ ping -c 4 example.com
PING example.com (93.184.216.34) 56(84) bytes of data.
64 bytes from 93.184.216.34: icmp_seq=1 ttl=56 time=11.6 ms
64 bytes from 93.184.216.34: icmp_seq=2 ttl=56 time=11.4 ms
64 bytes from 93.184.216.34: icmp_seq=3 ttl=56 time=11.5 ms
64 bytes from 93.184.216.34: icmp_seq=4 ttl=56 time=11.3 ms

--- example.com ping statistics ---
4 packets transmitted, 4 received, 0% packet loss, time 3004ms
rtt min/avg/max/mdev = 11.300/11.450/11.600/0.112 ms
```

| Field        | Meaning                                                                 |
|--------------|-------------------------------------------------------------------------|
| `icmp_seq`   | Sequence number — helps detect packet loss or reordering                |
| `ttl`        | Time To Live — number of hops remaining before the packet is discarded  |
| `time`       | Round-trip time in milliseconds                                         |
| `packet loss`| Percentage of packets that did not receive a reply                      |
| `rtt min/avg/max/mdev` | Latency statistics across all packets                        |

## Common Options

| Option            | Description                                        |
|-------------------|----------------------------------------------------|
| `-c <count>`      | Stop after sending `count` packets                 |
| `-i <interval>`   | Wait `interval` seconds between packets            |
| `-s <size>`       | Set the payload size in bytes (default 56)         |
| `-t <ttl>`        | Set the IP Time To Live                            |
| `-W <timeout>`    | Time to wait for a response (seconds)              |
| `-q`              | Quiet output — only show summary                   |
| `-f`              | Flood ping (requires root) — send packets as fast as possible |
| `-4` / `-6`       | Force IPv4 or IPv6                                 |
| `-I <interface>`  | Use a specific network interface                   |

## Practical Exercises

### Exercise 1: Test Basic Connectivity

Verify that your machine can reach a well-known public DNS server:

```bash
ping -c 4 8.8.8.8
```

If this succeeds but `ping -c 4 google.com` fails, your DNS resolution may be broken.

### Exercise 2: Compare Latency to Different Hosts

Ping several hosts and compare the average round-trip times:

```bash
ping -c 10 8.8.8.8        # Google DNS
ping -c 10 1.1.1.1        # Cloudflare DNS
ping -c 10 208.67.222.222 # OpenDNS
```

### Exercise 3: Detect Packet Loss

Ping a host with a large count and check the summary for packet loss:

```bash
ping -c 100 example.com
```

If the packet loss percentage is above 0%, investigate potential network issues between your machine and the destination.

### Exercise 4: Test Path MTU

Send increasingly large packets to find the Maximum Transmission Unit (MTU) along the path. The `-M do` flag sets the "Don't Fragment" bit:

```bash
ping -c 3 -s 1472 -M do example.com   # typical MTU 1500 - 28 byte header = 1472
ping -c 3 -s 1473 -M do example.com   # should fail if MTU is 1500
```

### Exercise 5: Ping Your Default Gateway

Find your default gateway and ping it to test your local network connection:

```bash
ip route | grep default
ping -c 4 <gateway_ip>
```

## Troubleshooting with Ping

| Symptom                         | Likely Cause                                          |
|---------------------------------|-------------------------------------------------------|
| `Destination Host Unreachable`  | No route to the host; check routing table and gateway |
| `Request timed out`             | Host is down, firewall blocking ICMP, or packet loss  |
| High or variable RTT            | Network congestion, long-distance link, or Wi-Fi issues |
| 100% packet loss                | Host down, ICMP blocked by firewall, or wrong address |
| TTL expired in transit          | Routing loop or too many hops                         |

## Ping vs Ping6

On some systems, `ping` defaults to IPv4. Use `ping6` or `ping -6` to explicitly test IPv6 connectivity:

```bash
ping6 -c 4 ipv6.google.com
# or
ping -6 -c 4 ipv6.google.com
```
