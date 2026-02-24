# ping

`ping` is one of the most fundamental network diagnostic tools. It uses **ICMP (Internet Control Message Protocol) Echo Request** messages to test whether a host is reachable and to measure round-trip time (RTT).

---

## How ping Works

```text
  Source                              Destination
    │                                     │
    │──── ICMP Echo Request (type 8) ────>│
    │                                     │
    │<─── ICMP Echo Reply   (type 0) ─────│
    │                                     │
    │       RTT = reply_time - send_time  │
```

`ping` sends one ICMP Echo Request per second by default and waits for the corresponding Echo Reply. For each reply received it reports the RTT. At the end it prints summary statistics.

---

## Basic Usage

```bash
ping example.com          # Ping until Ctrl+C (Linux/macOS)
ping -c 4 example.com     # Send exactly 4 packets
ping 192.168.1.1          # Ping by IP address
ping -6 example.com       # Force IPv6 (uses ICMPv6)
ping -4 example.com       # Force IPv4
```

On **Windows**, `ping` sends 4 packets by default:

```cmd
ping example.com
ping -n 10 example.com    # Send 10 packets
ping -t  example.com      # Ping continuously until Ctrl+C
```

---

## Example Output

```text
$ ping -c 5 example.com
PING example.com (93.184.216.34) 56(84) bytes of data.
64 bytes from 93.184.216.34: icmp_seq=1 ttl=56 time=11.2 ms
64 bytes from 93.184.216.34: icmp_seq=2 ttl=56 time=10.8 ms
64 bytes from 93.184.216.34: icmp_seq=3 ttl=56 time=11.1 ms
64 bytes from 93.184.216.34: icmp_seq=4 ttl=56 time=12.3 ms
64 bytes from 93.184.216.34: icmp_seq=5 ttl=56 time=10.9 ms

--- example.com ping statistics ---
5 packets transmitted, 5 received, 0% packet loss, time 4005ms
rtt min/avg/max/mdev = 10.8/11.26/12.3/0.55 ms
```

### Fields Explained

| Field        | Meaning                                                                      |
|:-------------|:-----------------------------------------------------------------------------|
| `bytes`      | Size of the ICMP payload (default 56 bytes + 8-byte ICMP header = 64 bytes) |
| `icmp_seq`   | Sequence number — gaps indicate lost packets                                 |
| `ttl`        | Time To Live in the reply — decremented by each router en route              |
| `time`       | Round-trip time (RTT) in milliseconds                                        |
| `packet loss`| Percentage of sent packets that received no reply                            |
| `mdev`       | Mean deviation — measures RTT variability (jitter)                           |

---

## Common Options

| Option (Linux)      | Option (Windows)  | Description                                    |
|:--------------------|:------------------|:-----------------------------------------------|
| `-c <count>`        | `-n <count>`      | Number of echo requests to send                |
| `-i <interval>`     | N/A               | Interval between requests in seconds (default 1s) |
| `-s <size>`         | `-l <size>`       | Payload size in bytes (default 56/32)          |
| `-t <ttl>`          | `-i <TTL>`        | Set the TTL for outgoing packets               |
| `-W <timeout>`      | `-w <timeout>`    | Wait time for each reply (seconds / ms)        |
| `-q`                | N/A               | Quiet mode — only print summary                |
| `-v`                | N/A               | Verbose output                                 |
| `-f`                | N/A               | Flood ping — send packets as fast as possible (root required) |
| `-4` / `-6`         | `-4` / `-6`       | Force IPv4 or IPv6                             |
| `-I <interface>`    | N/A               | Send from a specific network interface         |

---

## Interpreting Results

| Result                          | Possible Cause                                              |
|:--------------------------------|:------------------------------------------------------------|
| All replies received, low RTT   | Host is up, network path is healthy                         |
| 100% packet loss                | Host is down, unreachable, or blocking ICMP                 |
| Intermittent packet loss        | Network congestion, unstable link, or faulty hardware       |
| High RTT (e.g., > 200 ms)       | Long-distance route, congestion, or slow DNS                |
| High `mdev` (jitter)            | Inconsistent network performance — bad for VoIP/gaming      |
| `Request timeout`               | ICMP blocked by firewall, or host unreachable               |
| `Destination Host Unreachable`  | Router has no route to the host                             |
| `TTL expired in transit`        | Routing loop or TTL too low                                 |

---

## Diagnosing with ping

### Step 1 — Ping the loopback address
```bash
ping 127.0.0.1      # Verify the TCP/IP stack on your own machine
ping ::1            # IPv6 loopback
```

### Step 2 — Ping your default gateway
```bash
ping 192.168.1.1    # Verify local LAN connectivity
```

### Step 3 — Ping a public IP (skip DNS)
```bash
ping 8.8.8.8        # Verify internet connectivity (Google's DNS)
```

### Step 4 — Ping by hostname (test DNS)
```bash
ping example.com    # If this fails but step 3 succeeds, DNS is the problem
```

---

## ping and Firewalls

Many hosts and firewalls are configured to **block ICMP** for security reasons. A failed ping does not necessarily mean the host is down — it may simply not respond to ICMP Echo Requests. Use `traceroute`, `curl`, or `nmap` to determine whether the host is actually reachable on a specific port.

```bash
# Check if a web server is up even if it doesn't respond to ping
curl -I http://example.com
```

---

## Advanced: Flood Ping and Packet Size

```bash
# Flood ping — requires root; measures link reliability under load
sudo ping -f -c 10000 192.168.1.1

# Large payload — test fragmentation (MTU discovery)
ping -s 1472 example.com    # 1472 + 28 byte headers = 1500 bytes (standard MTU)
ping -M do -s 1473 example.com  # Set DF bit; returns error if fragmentation needed
```

The **MTU (Maximum Transmission Unit)** is typically 1500 bytes on Ethernet. Packets larger than the MTU must be fragmented. Testing with progressively larger sizes can help identify MTU-related issues on a path.
