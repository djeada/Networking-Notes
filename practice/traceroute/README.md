# Traceroute

## Overview

`traceroute` (Linux/macOS) and `tracert` (Windows) map the path that packets take from your machine to a destination host. By revealing every intermediate router (hop) and measuring round-trip time to each one, traceroute helps identify where delays, packet loss, or routing failures occur in the network path.

## How Traceroute Works

Traceroute sends packets with incrementally increasing **TTL (Time To Live)** values. Each router along the path decrements the TTL by 1. When TTL reaches 0, the router drops the packet and sends back an **ICMP Time Exceeded** message, revealing its IP address and allowing the round-trip time to be calculated.

```text
  Source              Hop 1             Hop 2             Destination
    |                   |                 |                    |
    |--- TTL=1 -------->|                 |                    |
    |<-- Time Exceeded--|                 |                    |
    |                   |                 |                    |
    |--- TTL=2 -------->|--- TTL=1 ----->|                    |
    |                   |<-- Time Exceeded|                    |
    |<---- forwarded ---|                 |                    |
    |                   |                 |                    |
    |--- TTL=3 -------->|--- TTL=2 ----->|--- TTL=1 --------->|
    |<-------------- Destination Reached (Echo Reply) --------|
```

## Basic Usage

```bash
# Trace route to a host
traceroute example.com

# Use ICMP instead of UDP (useful when UDP is blocked)
traceroute -I example.com

# Use TCP SYN packets (useful when both UDP and ICMP are blocked)
traceroute -T example.com

# Limit the maximum number of hops
traceroute -m 15 example.com

# Skip DNS resolution for faster output
traceroute -n example.com
```

## Reading Traceroute Output

```text
$ traceroute example.com
traceroute to example.com (93.184.216.34), 30 hops max, 60 byte packets
 1  gateway (192.168.1.1)        1.234 ms   1.112 ms   1.056 ms
 2  isp-router (10.0.0.1)       5.678 ms   5.432 ms   5.321 ms
 3  core-router.isp.net          12.345 ms  12.123 ms  12.456 ms
 4  * * *
 5  peer-router.cdn.net          25.678 ms  25.432 ms  25.890 ms
 6  example.com (93.184.216.34)  30.123 ms  30.456 ms  30.789 ms
```

| Column           | Meaning                                                     |
|------------------|-------------------------------------------------------------|
| Hop number       | Position along the path (1 = first router)                  |
| Hostname (IP)    | Identity of the router at that hop                          |
| Three RTT values | Round-trip time for each of the three probe packets         |
| `* * *`          | Router did not respond (may be blocking probes)             |

## Common Options

| Option          | Description                                             |
|-----------------|---------------------------------------------------------|
| `-m <max_hops>` | Maximum number of hops to probe (default: 30)          |
| `-q <nqueries>` | Number of probes per hop (default: 3)                  |
| `-w <seconds>`  | Timeout for each probe response (default: 5s)          |
| `-I`            | Use ICMP Echo instead of UDP                           |
| `-T`            | Use TCP SYN instead of UDP                             |
| `-p <port>`     | Set destination port (useful for testing specific services) |
| `-n`            | Do not resolve hostnames (faster output)               |
| `-4` / `-6`     | Force IPv4 or IPv6                                     |

## Practical Exercises

### Exercise 1: Trace a Path to a Public Server

Run a basic traceroute and observe the hops:

```bash
traceroute -n example.com
```

Count how many hops are involved. Note which hops have the highest latency.

### Exercise 2: Compare UDP, ICMP, and TCP Traceroute

Some routers treat different protocols differently. Compare the results:

```bash
traceroute example.com          # UDP (default)
traceroute -I example.com       # ICMP
traceroute -T -p 443 example.com  # TCP to HTTPS port
```

Note any hops that appear in one trace but show `* * *` in another.

### Exercise 3: Identify Latency Jumps

Trace a distant host and identify where the biggest latency increase occurs:

```bash
traceroute -n google.com
```

A large jump between two hops often indicates a long-distance link (e.g., crossing an ocean) or network congestion.

### Exercise 4: Test a Specific Port

Use TCP traceroute to test connectivity to a specific service port:

```bash
# Trace to an HTTP server
traceroute -T -p 80 example.com

# Trace to an SSH server
traceroute -T -p 22 your-server.com
```

This helps identify if a firewall is blocking traffic to a specific port.

### Exercise 5: Trace with MTR (Combination of Ping and Traceroute)

`mtr` combines traceroute and ping into a single tool for continuous monitoring:

```bash
mtr example.com
mtr -n --report -c 100 example.com
```

`mtr` shows real-time statistics (loss %, sent, last, avg, best, worst) for every hop.

## Interpreting Common Patterns

| Pattern                    | Meaning                                              |
|----------------------------|------------------------------------------------------|
| `* * *` at one hop         | Router not responding to probes (often normal)       |
| `* * *` at all remaining hops | Destination unreachable or heavily firewalled     |
| Sudden large latency jump  | Long-distance link or congestion                     |
| Latency increases then decreases | ICMP rate limiting at that router (misleading) |
| Same IP at multiple hops   | Possible routing loop                                |
| `!H` / `!N` / `!X`        | Host/Network unreachable or administratively prohibited |

## Traceroute on Different Platforms

| Feature              | `traceroute` (Linux/macOS) | `tracert` (Windows) | `mtr` (Linux/macOS) |
|----------------------|---------------------------|---------------------|----------------------|
| Default protocol     | UDP                       | ICMP                | ICMP                 |
| TCP support          | Yes (`-T`)                | No                  | Yes (`--tcp`)        |
| Continuous monitoring | No                       | No                  | Yes                  |
| DNS resolution       | Yes (disable with `-n`)   | Yes (disable `-d`)  | Yes (disable `-n`)   |
