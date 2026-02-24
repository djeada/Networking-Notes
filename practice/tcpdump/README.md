# tcpdump

## Overview

`tcpdump` is a command-line packet capture and analysis tool. It captures network traffic passing through a network interface and displays or saves it for later analysis. While Wireshark provides a graphical interface, `tcpdump` is essential for capturing traffic on remote servers, headless systems, and in automated scripts.

## Basic Usage

```bash
# Capture packets on the default interface
sudo tcpdump

# Capture on a specific interface
sudo tcpdump -i eth0

# Capture with verbose output
sudo tcpdump -v

# Capture and show packet contents in hex and ASCII
sudo tcpdump -XX

# Capture a specific number of packets
sudo tcpdump -c 50

# Capture without resolving hostnames (faster)
sudo tcpdump -n

# Capture without resolving hostnames or port names
sudo tcpdump -nn
```

## Saving and Reading Captures

```bash
# Save captured packets to a file (pcap format)
sudo tcpdump -i eth0 -w capture.pcap

# Read packets from a saved file
tcpdump -r capture.pcap

# Save with a packet count limit
sudo tcpdump -i eth0 -c 1000 -w capture.pcap
```

Saved `.pcap` files can be opened in Wireshark for detailed graphical analysis.

## Filtering Traffic

tcpdump uses **BPF (Berkeley Packet Filter)** syntax for filtering. Filters can be combined with `and`, `or`, and `not`.

### Filter by Host

```bash
# Capture traffic to or from a specific host
sudo tcpdump host 192.168.1.100

# Capture traffic from a specific source
sudo tcpdump src host 192.168.1.100

# Capture traffic to a specific destination
sudo tcpdump dst host 192.168.1.100
```

### Filter by Port

```bash
# Capture traffic on a specific port
sudo tcpdump port 80

# Capture traffic on a source port
sudo tcpdump src port 443

# Capture traffic on a destination port
sudo tcpdump dst port 22
```

### Filter by Protocol

```bash
# Capture only TCP traffic
sudo tcpdump tcp

# Capture only UDP traffic
sudo tcpdump udp

# Capture only ICMP traffic
sudo tcpdump icmp

# Capture only ARP traffic
sudo tcpdump arp
```

### Filter by Network

```bash
# Capture traffic on a specific subnet
sudo tcpdump net 192.168.1.0/24

# Capture traffic between two hosts
sudo tcpdump host 192.168.1.10 and host 192.168.1.20
```

### Combined Filters

```bash
# Capture HTTP traffic from a specific host
sudo tcpdump 'host 192.168.1.100 and port 80'

# Capture DNS queries
sudo tcpdump 'udp port 53'

# Capture all traffic except SSH (useful when capturing over SSH)
sudo tcpdump 'not port 22'

# Capture SYN packets only (new TCP connections)
sudo tcpdump 'tcp[tcpflags] & (tcp-syn) != 0 and tcp[tcpflags] & (tcp-ack) == 0'

# Capture TCP traffic to port 443 from a specific subnet
sudo tcpdump 'src net 10.0.0.0/8 and dst port 443 and tcp'
```

## Reading tcpdump Output

```text
$ sudo tcpdump -nn -c 3 port 80
14:30:01.123456 IP 192.168.1.10.54321 > 93.184.216.34.80: Flags [S], seq 1234567890, win 65535, length 0
14:30:01.145678 IP 93.184.216.34.80 > 192.168.1.10.54321: Flags [S.], seq 987654321, ack 1234567891, win 65535, length 0
14:30:01.145789 IP 192.168.1.10.54321 > 93.184.216.34.80: Flags [.], ack 1, win 65535, length 0
```

| Field                  | Meaning                                          |
|------------------------|--------------------------------------------------|
| `14:30:01.123456`      | Timestamp                                        |
| `IP`                   | Protocol (IP, IP6, ARP, etc.)                    |
| `192.168.1.10.54321`   | Source IP and port                                |
| `93.184.216.34.80`     | Destination IP and port                           |
| `Flags [S]`            | TCP flags (`S`=SYN, `.`=ACK, `F`=FIN, `R`=RST, `P`=PSH) |
| `seq`                  | Sequence number                                  |
| `ack`                  | Acknowledgment number                            |
| `win`                  | Window size                                      |
| `length`               | Payload length                                   |

### TCP Flag Reference

| Flag | Symbol | Meaning                        |
|------|--------|--------------------------------|
| SYN  | `S`    | Initiate connection            |
| ACK  | `.`    | Acknowledge received data      |
| FIN  | `F`    | Terminate connection           |
| RST  | `R`    | Reset connection               |
| PSH  | `P`    | Push data to application       |
| URG  | `U`    | Urgent data                    |

## Common Options

| Option          | Description                                        |
|-----------------|----------------------------------------------------|
| `-i <iface>`    | Capture on a specific interface                    |
| `-c <count>`    | Capture only `count` packets                       |
| `-w <file>`     | Write packets to a pcap file                       |
| `-r <file>`     | Read packets from a pcap file                      |
| `-n`            | Do not resolve hostnames                           |
| `-nn`           | Do not resolve hostnames or port names             |
| `-v` / `-vv`    | Verbose / very verbose output                      |
| `-XX`           | Show packet contents in hex and ASCII              |
| `-A`            | Show packet contents in ASCII only                 |
| `-e`            | Show link-layer (Ethernet) header                  |
| `-q`            | Quiet output (less protocol information)           |
| `-s <snaplen>`  | Set capture snapshot length (default: 262144 bytes)|
| `-D`            | List available interfaces                          |

## Practical Exercises

### Exercise 1: Capture a TCP Three-Way Handshake

Capture the SYN, SYN-ACK, and ACK packets when connecting to a web server:

```bash
# In one terminal, start capturing
sudo tcpdump -nn -c 10 'host example.com and port 80'

# In another terminal, make a connection
curl -s -o /dev/null http://example.com
```

Look for the three packets with flags `[S]`, `[S.]`, and `[.]`.

### Exercise 2: Capture DNS Queries

Observe DNS resolution in action:

```bash
# Start capturing DNS traffic
sudo tcpdump -nn 'udp port 53'

# In another terminal, perform a lookup
dig example.com
```

### Exercise 3: Capture and Save for Wireshark

Capture traffic, save it, and analyze in Wireshark:

```bash
sudo tcpdump -i eth0 -c 500 -w /tmp/capture.pcap
```

Transfer the file to a machine with Wireshark and open it for graphical analysis.

### Exercise 4: Monitor HTTP Traffic

Capture and display HTTP request headers:

```bash
sudo tcpdump -nn -A 'tcp port 80 and (((ip[2:2] - ((ip[0]&0xf)<<2)) - ((tcp[12]&0xf0)>>2)) != 0)'
```

### Exercise 5: Filter Out SSH While Capturing Remotely

When capturing on a remote server over SSH, exclude your own SSH session:

```bash
sudo tcpdump -nn 'not port 22'
```

### Exercise 6: Detect ARP Traffic

Capture ARP requests and replies on the local network:

```bash
sudo tcpdump -nn arp
```

Watch for ARP requests ("who has 192.168.1.1?") and replies ("192.168.1.1 is at aa:bb:cc:dd:ee:ff").
