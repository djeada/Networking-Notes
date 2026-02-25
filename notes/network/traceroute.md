# Traceroute

**Traceroute** is a network diagnostic tool that maps the path packets take from your machine to a destination host. It reveals every router (hop) along the way and measures the round-trip time to each one, making it invaluable for identifying where delays or failures occur in a network path.

---

## How Traceroute Works

Traceroute exploits the **TTL (Time To Live)** field in IP packets. It sends a series of packets with incrementally increasing TTL values. Each router that forwards the packet decrements the TTL by 1; when TTL reaches 0, the router drops the packet and sends back an **ICMP Time Exceeded** message, revealing its identity.

```text
  Source                Router 1          Router 2          Destination
    |                      |                 |                   |
    |--- TTL=1 ----------->|                 |                   |
    |<-- ICMP Time Exceeded|                 |                   |
    |                      |                 |                   |
    |--- TTL=2 ----------->|--- TTL=1 ----->|                   |
    |                      |<-- ICMP Time Exceeded               |
    |<------- forwarded ---|                 |                   |
    |                      |                 |                   |
    |--- TTL=3 ----------->|--- TTL=2 ----->|--- TTL=1 -------->|
    |                      |                 |                   |
    |<-------------- Destination Reached (port unreachable) ----|
    |                      |                 |                   |
```

### Step-by-Step Process

1. Send a packet with **TTL=1**. The first router decrements it to 0, drops it, and returns an ICMP Time Exceeded message. Record the router's IP and round-trip time.
2. Send a packet with **TTL=2**. It passes the first router (TTL becomes 1) and is dropped by the second router. Record that hop.
3. Repeat with **TTL=3, 4, 5...** until the packet reaches the destination, which responds with an ICMP Port Unreachable (UDP traceroute) or Echo Reply (ICMP traceroute).
4. At each TTL value, typically **3 probes** are sent to measure variability in latency.

---

## Example Traceroute Output

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

---

## Interpreting Results

| Symbol / Pattern         | Meaning                                                     |
|--------------------------|-------------------------------------------------------------|
| `* * *`                  | Router did not respond (may be blocking ICMP or UDP probes) |
| Sudden large time jump   | Possible congestion or a long-distance link (e.g., undersea cable) |
| Consistent high latency  | Congestion at that hop or beyond                            |
| Same IP repeated         | Routing loop (rare)                                         |
| `!H`                     | Host unreachable                                            |
| `!N`                     | Network unreachable                                         |
| `!X`                     | Communication administratively prohibited (firewall)        |

**Note**: Asterisks (`* * *`) do not always mean a problem — many routers are configured to silently drop traceroute probes for security reasons.

---

## Traceroute vs Tracert (Linux vs Windows)

| Feature            | `traceroute` (Linux/macOS)           | `tracert` (Windows)                  |
|--------------------|--------------------------------------|--------------------------------------|
| **Default Protocol** | UDP packets to high ports           | ICMP Echo Request                    |
| **Max Hops**       | 30 (default)                         | 30 (default)                         |
| **Options**        | Many (`-I` for ICMP, `-T` for TCP)   | Fewer (`-d` to skip DNS lookup)      |
| **Output**         | 3 RTT values per hop                 | 3 RTT values per hop                 |

---

## tcptraceroute

If you have trouble with a TCP connection, use **tcptraceroute**. It sends TCP SYN packets instead of UDP or ICMP, which helps find firewalls that block standard traceroute probes while allowing TCP traffic through.

```text
$ tcptraceroute example.com 443
 1  gateway (192.168.1.1)          1.234 ms
 2  isp-router (10.0.0.1)         5.678 ms
 3  core-router.isp.net           12.345 ms
 4  example.com (93.184.216.34)   30.123 ms  [open]
```

**Use cases**: Diagnosing connectivity to HTTP, HTTPS, SSH, SMTP, POP3, IMAP, and other TCP services. Normal traceroute uses UDP (or ICMP), which may be blocked where TCP is allowed.

---

## Common Traceroute Options

| Option              | Description                                          |
|---------------------|------------------------------------------------------|
| `-m <max_hops>`     | Set maximum number of hops (default: 30)             |
| `-q <nqueries>`     | Number of probes per hop (default: 3)                |
| `-w <seconds>`      | Wait time for each response (default: 5s)            |
| `-I`                | Use ICMP Echo instead of UDP (Linux)                 |
| `-T`                | Use TCP SYN instead of UDP (Linux)                   |
| `-p <port>`         | Set destination port number                          |
| `-n`                | Do not resolve IP addresses to hostnames             |
| `-4` / `-6`         | Force IPv4 or IPv6                                   |
