# tcpdump — Packet Capture and Analysis

`tcpdump` is a command-line packet analyser that captures and displays network traffic in real time. It is pre-installed on most Unix/Linux/macOS systems and is the foundation of many other network analysis tools (including Wireshark's underlying library, `libpcap`).

---

## How tcpdump Works

`tcpdump` places a network interface into **promiscuous mode**, allowing it to capture all frames that arrive at that interface — not just those addressed to the host. It then applies a filter (BPF — Berkeley Packet Filter) and prints matching packets.

```text
  Network Interface (eth0)
         │
         │  all packets arrive here
         ▼
  ┌─────────────────────┐
  │  BPF filter kernel  │  ← apply your filter expression
  └──────────┬──────────┘
             │  matching packets only
             ▼
  ┌─────────────────────┐
  │     tcpdump         │  print to terminal or write to .pcap file
  └─────────────────────┘
```

---

## Basic Usage

```bash
# Root (or CAP_NET_RAW capability) is required
sudo tcpdump                          # Capture on default interface
sudo tcpdump -i eth0                  # Capture on a specific interface
sudo tcpdump -i any                   # Capture on all interfaces
sudo tcpdump -c 100                   # Stop after 100 packets
sudo tcpdump -n                       # Don't resolve hostnames
sudo tcpdump -nn                      # Don't resolve hostnames or port names
sudo tcpdump -v                       # Verbose (more header detail)
sudo tcpdump -vv                      # Very verbose
sudo tcpdump -X                       # Print packet data in hex and ASCII
sudo tcpdump -A                       # Print packet data in ASCII only
sudo tcpdump -q                       # Quiet — print less information per packet
```

---

## Listing Interfaces

```bash
sudo tcpdump -D                       # List available network interfaces
ip link show                          # Alternative: list interfaces
```

---

## Saving and Reading Captures

```bash
# Save captured packets to a file (pcap format, readable by Wireshark)
sudo tcpdump -i eth0 -w capture.pcap

# Save with automatic file rotation (100 MB per file, up to 5 files)
sudo tcpdump -i eth0 -w capture.pcap -C 100 -W 5

# Read a previously saved capture file
tcpdump -r capture.pcap
tcpdump -r capture.pcap -nn          # Don't resolve names

# Read with a filter
tcpdump -r capture.pcap 'tcp port 80'
```

---

## Filtering (BPF Filter Expressions)

Filters are the most powerful feature of tcpdump. They use **Berkeley Packet Filter (BPF)** syntax.

### Filter by Protocol

```bash
sudo tcpdump tcp                      # TCP traffic only
sudo tcpdump udp                      # UDP traffic only
sudo tcpdump icmp                     # ICMP (ping) traffic only
sudo tcpdump arp                      # ARP traffic only
sudo tcpdump ip6                      # IPv6 traffic only
```

### Filter by Host

```bash
sudo tcpdump host 192.168.1.100       # Traffic to or from a specific host
sudo tcpdump src 192.168.1.100        # Traffic from a specific host
sudo tcpdump dst 192.168.1.100        # Traffic to a specific host
sudo tcpdump host example.com         # Traffic to/from a hostname
```

### Filter by Port

```bash
sudo tcpdump port 80                  # Traffic on port 80 (src or dst)
sudo tcpdump src port 80              # Traffic from port 80
sudo tcpdump dst port 443             # Traffic to port 443
sudo tcpdump portrange 8000-9000      # Traffic on a port range
```

### Filter by Network

```bash
sudo tcpdump net 192.168.1.0/24       # Traffic to/from an entire subnet
sudo tcpdump src net 10.0.0.0/8       # Traffic from a specific network
```

### Combining Filters

Use `and`, `or`, `not` (or `&&`, `||`, `!`) to combine expressions:

```bash
sudo tcpdump 'tcp and port 80'
sudo tcpdump 'host 192.168.1.1 and port 22'
sudo tcpdump 'tcp port 80 or tcp port 443'
sudo tcpdump 'not port 22'            # Exclude SSH traffic
sudo tcpdump 'host 192.168.1.100 and (port 80 or port 443)'

# Capture SYN packets only (new TCP connections)
sudo tcpdump 'tcp[tcpflags] & (tcp-syn) != 0 and tcp[tcpflags] & (tcp-ack) == 0'

# Capture TCP traffic to port 443 from a specific subnet
sudo tcpdump 'src net 10.0.0.0/8 and dst port 443 and tcp'
```

### Filter by Packet Size

```bash
sudo tcpdump 'greater 1000'           # Packets larger than 1000 bytes
sudo tcpdump 'less 100'               # Packets smaller than 100 bytes
```

---

## Example Output

```text
$ sudo tcpdump -nn -i eth0 tcp port 80 -c 5
tcpdump: verbose output suppressed, use -v or -vv for full protocol decode
listening on eth0, link-type EN10MB (Ethernet), capture size 262144 bytes
14:23:01.123456 IP 192.168.1.5.54321 > 93.184.216.34.80: Flags [S], seq 12345, win 64240, length 0
14:23:01.145678 IP 93.184.216.34.80 > 192.168.1.5.54321: Flags [S.], seq 67890, ack 12346, win 65535, length 0
14:23:01.145900 IP 192.168.1.5.54321 > 93.184.216.34.80: Flags [.], ack 67891, win 502, length 0
14:23:01.146000 IP 192.168.1.5.54321 > 93.184.216.34.80: Flags [P.], seq 1:78, ack 1, win 502, length 77
14:23:01.200000 IP 93.184.216.34.80 > 192.168.1.5.54321: Flags [P.], seq 1:520, ack 78, win 510, length 519
5 packets captured
```

### TCP Flags Reference

| Flag  | Meaning                                              |
|:------|:-----------------------------------------------------|
| `[S]` | SYN — connection initiation                          |
| `[S.]`| SYN-ACK — server accepting connection                |
| `[.]` | ACK — acknowledgement (no data)                      |
| `[P.]`| PSH-ACK — data push                                  |
| `[F.]`| FIN-ACK — connection teardown                        |
| `[R]` | RST — connection reset                               |
| `[R.]`| RST-ACK — connection reset with acknowledgement      |

---

## Practical Examples

### Capture HTTP traffic and display content

```bash
sudo tcpdump -i eth0 -A 'tcp port 80'
```

### Watch DNS queries

```bash
sudo tcpdump -i eth0 -nn 'udp port 53'
```

### Monitor ICMP (ping) traffic

```bash
sudo tcpdump -i eth0 icmp
```

### Capture a TCP three-way handshake

```bash
sudo tcpdump -i eth0 -nn 'host 93.184.216.34 and tcp'
```

### Capture traffic from a specific subnet, excluding SSH

```bash
sudo tcpdump -i eth0 'net 192.168.1.0/24 and not port 22'
```

### Capture HTTPS traffic (to analyze metadata; content is encrypted)

```bash
sudo tcpdump -i eth0 -nn 'tcp port 443'
```

---

## Common Options Reference

| Option          | Description                                                      |
|:----------------|:-----------------------------------------------------------------|
| `-i <iface>`    | Interface to capture on (`any` for all)                          |
| `-c <count>`    | Stop after capturing `count` packets                             |
| `-n`            | Don't resolve hostnames                                          |
| `-nn`           | Don't resolve hostnames or port names                            |
| `-v` / `-vv`    | Verbose / very verbose output                                    |
| `-X`            | Print hex + ASCII of packet payload                              |
| `-A`            | Print ASCII of packet payload                                    |
| `-w <file>`     | Write packets to a pcap file                                     |
| `-r <file>`     | Read packets from a pcap file                                    |
| `-C <size>`     | Rotate capture file when it reaches `size` MB                    |
| `-W <count>`    | Keep only `count` rotate files                                   |
| `-s <snaplen>`  | Capture `snaplen` bytes per packet (default 262144, 0 = full)    |
| `-e`            | Print Ethernet (MAC) addresses                                   |
| `-t`            | Don't print timestamps                                           |
| `-tttt`         | Print human-readable timestamps                                  |
| `-D`            | List available interfaces                                        |

---

## tcpdump vs Wireshark

| Feature           | tcpdump                             | Wireshark                            |
|:------------------|:------------------------------------|:-------------------------------------|
| Interface         | Command-line only                   | Graphical + command-line (`tshark`)  |
| Platform          | Unix/Linux/macOS (winpcap on Windows)| Cross-platform                      |
| Live analysis     | Yes (terminal output)               | Yes (graphical real-time view)       |
| File format       | pcap / pcap-ng                      | pcap / pcap-ng (same format)        |
| Filtering         | BPF (capture-time and display)      | BPF capture + display filter syntax |
| Remote capture    | Yes (pipe via SSH)                  | Yes (remote capture interface)       |
| Protocol decode   | Basic                               | Deep protocol dissection             |
| Best for          | Quick CLI capture, remote servers   | Deep analysis, visual exploration    |

**Workflow:** Use `tcpdump` to capture on a remote server, then open the `.pcap` file in Wireshark for visual analysis:

```bash
# On the remote server
sudo tcpdump -i eth0 -w /tmp/capture.pcap

# Copy to local machine
scp user@remote:/tmp/capture.pcap .

# Open in Wireshark
wireshark capture.pcap
```

---

## Practical Exercises

### Exercise 1: Capture and Save for Wireshark

Capture traffic, save it, and analyze in Wireshark:

```bash
sudo tcpdump -i eth0 -c 500 -w /tmp/capture.pcap
```

Transfer the file to a machine with Wireshark and open it for graphical analysis.

### Exercise 2: Monitor HTTP Traffic (Advanced Filter)

Capture and display only HTTP packets that carry payload data (excludes handshake and ACK-only packets):

```bash
sudo tcpdump -nn -A 'tcp port 80 and (((ip[2:2] - ((ip[0]&0xf)<<2)) - ((tcp[12]&0xf0)>>2)) != 0)'
```

### Exercise 3: Detect ARP Traffic

Capture ARP requests and replies on the local network:

```bash
sudo tcpdump -nn arp
```

Watch for ARP requests ("who has 192.168.1.1?") and replies ("192.168.1.1 is at aa:bb:cc:dd:ee:ff").
