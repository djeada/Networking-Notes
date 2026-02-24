# Network Connection Inspection: netstat and ss

## Overview

`netstat` and `ss` display information about network connections, listening ports, routing tables, and interface statistics. They are essential for understanding what services are running on a machine, which ports are open, and what connections are active.

| Tool      | Status                     | Speed   | Notes                              |
|-----------|----------------------------|---------|-------------------------------------|
| `netstat` | Legacy (part of net-tools) | Slower  | Widely available, familiar syntax   |
| `ss`      | Modern replacement         | Faster  | Reads directly from kernel; preferred on modern Linux |

---

## ss (Socket Statistics)

### Listing Connections

```bash
# Show all TCP connections
ss -t

# Show all listening TCP sockets
ss -tln

# Show all listening UDP sockets
ss -uln

# Show all connections (TCP + UDP) with process info
ss -tulnp

# Show all sockets (including Unix domain sockets)
ss -a
```

### Reading ss Output

```text
$ ss -tulnp
Netid  State   Recv-Q  Send-Q   Local Address:Port   Peer Address:Port   Process
tcp    LISTEN  0       128      0.0.0.0:22            0.0.0.0:*           users:(("sshd",pid=1234,fd=3))
tcp    LISTEN  0       511      0.0.0.0:80            0.0.0.0:*           users:(("nginx",pid=5678,fd=6))
tcp    ESTAB   0       0        192.168.1.10:22       192.168.1.5:54321   users:(("sshd",pid=9012,fd=4))
udp    UNCONN  0       0        127.0.0.53:53         0.0.0.0:*           users:(("systemd-resolve",pid=567,fd=12))
```

| Column          | Meaning                                               |
|-----------------|-------------------------------------------------------|
| Netid           | Protocol (`tcp`, `udp`, `unix`)                       |
| State           | Connection state (`LISTEN`, `ESTAB`, `TIME-WAIT`, etc.) |
| Recv-Q / Send-Q | Receive and send queue sizes                         |
| Local Address:Port | The address and port on this machine               |
| Peer Address:Port  | The address and port of the remote end              |
| Process         | The process using the socket (requires `-p` and root) |

### Filtering with ss

```bash
# Show connections to a specific port
ss -tn 'dport = :443'

# Show connections from a specific IP
ss -tn 'src 192.168.1.10'

# Show connections in ESTABLISHED state
ss -tn state established

# Show connections in TIME-WAIT state
ss -tn state time-wait

# Show sockets with a specific process
ss -tlnp | grep nginx
```

### Common ss Options

| Option   | Description                                     |
|----------|-------------------------------------------------|
| `-t`     | Show TCP sockets                                |
| `-u`     | Show UDP sockets                                |
| `-l`     | Show listening sockets only                     |
| `-n`     | Show numeric addresses (skip DNS resolution)    |
| `-p`     | Show process using each socket (needs root)     |
| `-a`     | Show all sockets (listening + non-listening)    |
| `-s`     | Show socket statistics summary                  |
| `-o`     | Show timer information                          |
| `-e`     | Show detailed socket information                |
| `-i`     | Show internal TCP information                   |

---

## netstat

### Common Commands

```bash
# Show all listening TCP ports with process info
netstat -tlnp

# Show all listening UDP ports with process info
netstat -ulnp

# Show all connections
netstat -an

# Show routing table
netstat -rn

# Show interface statistics
netstat -i

# Show network statistics by protocol
netstat -s
```

### Reading netstat Output

```text
$ netstat -tlnp
Proto  Recv-Q  Send-Q  Local Address    Foreign Address   State    PID/Program name
tcp    0       0       0.0.0.0:22       0.0.0.0:*         LISTEN   1234/sshd
tcp    0       0       0.0.0.0:80       0.0.0.0:*         LISTEN   5678/nginx
tcp6   0       0       :::443           :::*              LISTEN   5678/nginx
```

### Common netstat Options

| Option   | Description                                     |
|----------|-------------------------------------------------|
| `-t`     | Show TCP connections                            |
| `-u`     | Show UDP connections                            |
| `-l`     | Show listening sockets only                     |
| `-n`     | Show numeric addresses (no DNS resolution)      |
| `-p`     | Show PID and program name (needs root)          |
| `-r`     | Show routing table                              |
| `-i`     | Show network interface table                    |
| `-s`     | Show protocol statistics                        |
| `-a`     | Show all sockets                                |

---

## Practical Exercises

### Exercise 1: Find All Listening Services

List every service listening on your machine:

```bash
ss -tulnp
```

Identify which ports are open and what programs are using them. Ask yourself: are any of these unexpected?

### Exercise 2: Monitor Active Connections

Watch active TCP connections in real time:

```bash
watch -n 1 'ss -tn state established'
```

Open a web browser and navigate to a site. Observe new connections appearing.

### Exercise 3: Find Which Process Uses a Port

Determine what process is listening on a specific port:

```bash
ss -tlnp | grep ':80'
# or with netstat
netstat -tlnp | grep ':80'
```

### Exercise 4: Count Connections by State

Get a summary of TCP connection states:

```bash
ss -s
```

Or count each state manually:

```bash
ss -tan | awk '{print $1}' | sort | uniq -c | sort -rn
```

### Exercise 5: Check for Connections to a Specific Host

Find all connections to or from a specific IP:

```bash
ss -tn 'dst 93.184.216.34 or src 93.184.216.34'
```

### Exercise 6: View Routing Table

Display the routing table to understand how traffic is directed:

```bash
ss -r
# or
netstat -rn
# or using ip command
ip route show
```

### Exercise 7: Detect TIME-WAIT Accumulation

A large number of `TIME-WAIT` sockets can indicate a connection churn issue:

```bash
ss -tn state time-wait | wc -l
```

## TCP Connection States Reference

```text
  Client                              Server
    |                                    |
    |--- SYN --------------------------->|  (SYN_SENT / SYN_RECV)
    |<-- SYN+ACK ------------------------|
    |--- ACK --------------------------->|  (ESTABLISHED)
    |                                    |
    |          ... data transfer ...     |
    |                                    |
    |--- FIN --------------------------->|  (FIN_WAIT_1)
    |<-- ACK ----------------------------|  (CLOSE_WAIT / FIN_WAIT_2)
    |<-- FIN ----------------------------|  (LAST_ACK)
    |--- ACK --------------------------->|  (TIME_WAIT -> CLOSED)
```

| State          | Description                                        |
|----------------|----------------------------------------------------|
| `LISTEN`       | Waiting for incoming connections                   |
| `SYN_SENT`     | Client has sent SYN, waiting for SYN-ACK          |
| `SYN_RECV`     | Server received SYN, sent SYN-ACK, waiting for ACK |
| `ESTABLISHED`  | Connection is open and data can flow               |
| `FIN_WAIT_1`   | Sent FIN, waiting for ACK                          |
| `FIN_WAIT_2`   | Received ACK for FIN, waiting for peer's FIN       |
| `CLOSE_WAIT`   | Received FIN, waiting for application to close     |
| `LAST_ACK`     | Sent FIN after receiving peer's FIN, waiting for ACK |
| `TIME_WAIT`    | Waiting to ensure peer received final ACK (2×MSL)  |
| `CLOSED`       | Connection fully terminated                        |
