# netstat and ss — Viewing Network Connections

`netstat` and `ss` are command-line tools for inspecting network connections, routing tables, interface statistics, and socket state. `ss` is the modern replacement for `netstat` and is significantly faster on systems with many connections.

---

## Key Concepts

- **Socket** — An endpoint for communication, identified by IP address + port + protocol.
- **Listening socket** — A server socket waiting for incoming connections.
- **Established socket** — An active two-way connection between two endpoints.
- **State** — The current phase of a TCP connection (e.g., `LISTEN`, `ESTABLISHED`, `TIME_WAIT`).

---

## ss (Socket Statistics) — Recommended

`ss` reads directly from the kernel and is faster than `netstat`. It is the default tool on modern Linux distributions.

### Basic Usage

```bash
ss -tuln          # Show all listening TCP and UDP sockets (no DNS lookup)
ss -tulnp         # Same, but also show the process (PID/name) using each socket
ss -ta            # Show all TCP connections (listening + established)
ss -ua            # Show all UDP sockets
ss -s             # Summary statistics
```

### Common Options

| Option | Description                                                  |
|:-------|:-------------------------------------------------------------|
| `-t`   | Show TCP sockets                                             |
| `-u`   | Show UDP sockets                                             |
| `-l`   | Show only listening sockets                                  |
| `-a`   | Show all sockets (listening + non-listening)                 |
| `-n`   | Do not resolve service names or hostnames (faster output)    |
| `-p`   | Show process (PID and name) for each socket                  |
| `-e`   | Show extended socket information (UID, inode)                |
| `-r`   | Resolve hostnames (reverse DNS)                              |
| `-o`   | Show timer information                                       |
| `-i`   | Show internal TCP information                                |
| `-4`   | Show IPv4 sockets only                                       |
| `-6`   | Show IPv6 sockets only                                       |

### Example Output

```text
$ ss -tulnp
Netid  State    Recv-Q  Send-Q   Local Address:Port    Peer Address:Port  Process
tcp    LISTEN   0       128      0.0.0.0:22            0.0.0.0:*          users:(("sshd",pid=1234,fd=3))
tcp    LISTEN   0       511      0.0.0.0:80            0.0.0.0:*          users:(("nginx",pid=2345,fd=6))
tcp    LISTEN   0       511      0.0.0.0:443           0.0.0.0:*          users:(("nginx",pid=2345,fd=7))
tcp    ESTAB    0       0        192.168.1.5:22        192.168.1.100:54321 users:(("sshd",pid=3456,fd=4))
udp    UNCONN   0       0        0.0.0.0:68            0.0.0.0:*          users:(("dhclient",pid=789,fd=5))
```

| Column             | Meaning                                                        |
|:-------------------|:---------------------------------------------------------------|
| Netid              | Protocol (`tcp`, `udp`, `unix`)                                |
| State              | Connection state (`LISTEN`, `ESTAB`, `TIME-WAIT`, etc.)        |
| Recv-Q / Send-Q    | Receive and send queue sizes                                   |
| Local Address:Port | The address and port on this machine                           |
| Peer Address:Port  | The address and port of the remote end                         |
| Process            | The process using the socket (requires `-p` and root)          |

### Filtering with ss

```bash
# Filter by state
ss -t state established      # Only established TCP connections
ss -t state listening        # Only listening TCP sockets
ss -t state time-wait        # Connections in TIME_WAIT

# Filter by port
ss -tnp sport = :22          # Connections where source port is 22
ss -tnp dport = :80          # Connections destined for port 80

# Filter by remote address
ss -t dst 192.168.1.100      # Connections to a specific remote host

# Filter by local address
ss -t src 192.168.1.5        # Connections from a specific local IP

# Show sockets with a specific process
ss -tlnp | grep nginx
```

---

## netstat — Legacy (Still Widely Available)

`netstat` is available on Linux, macOS, and Windows. On newer Linux distributions it may need to be installed separately (`net-tools` package).

### Basic Usage

```bash
netstat -tuln         # Show listening TCP and UDP sockets
netstat -tulnp        # Same, with process information (root may be needed)
netstat -an           # All connections and listening ports, numeric addresses
netstat -r            # Routing table
netstat -i            # Network interface statistics
netstat -s            # Protocol statistics (packets, errors, drops)
```

### Example Output

```text
$ netstat -tulnp
Proto  Recv-Q  Send-Q  Local Address     Foreign Address   State     PID/Program name
tcp    0       0       0.0.0.0:22        0.0.0.0:*         LISTEN    1234/sshd
tcp    0       0       0.0.0.0:80        0.0.0.0:*         LISTEN    2345/nginx
tcp    0       0       192.168.1.5:22    192.168.1.100:54321 ESTABLISHED 3456/sshd
tcp6   0       0       :::443            :::*              LISTEN    2345/nginx
udp    0       0       0.0.0.0:68        0.0.0.0:*                   789/dhclient
```

### Windows netstat

```cmd
netstat -an           :: All connections, numeric
netstat -b            :: Show executable (requires admin)
netstat -o            :: Show PID for each connection
netstat -r            :: Routing table
netstat -e            :: Interface statistics
```

---

## TCP Connection States

| State          | Meaning                                                                                          |
|:---------------|:-------------------------------------------------------------------------------------------------|
| `LISTEN`       | Server socket waiting for incoming connection requests                                           |
| `SYN_SENT`     | Client has sent a SYN; waiting for SYN-ACK from server                                          |
| `SYN_RECV`     | Server received a SYN; sent SYN-ACK; waiting for ACK                                            |
| `ESTABLISHED`  | Connection is active — data can flow in both directions                                          |
| `FIN_WAIT1`    | Local side sent FIN; waiting for ACK                                                             |
| `FIN_WAIT2`    | Received ACK for our FIN; waiting for remote FIN                                                 |
| `TIME_WAIT`    | Both sides have exchanged FINs; waiting to ensure the remote side received the final ACK         |
| `CLOSE_WAIT`   | Remote side sent FIN; local application has not yet closed the socket                            |
| `LAST_ACK`     | Waiting for final ACK of the FIN sent by the remote side                                         |
| `CLOSING`      | Both sides sent FIN simultaneously; waiting for each other's ACK                                 |
| `CLOSED`       | No connection                                                                                    |

```text
  TCP Connection Lifecycle (simplified)

  Client                              Server
    │                                   │
    │──── SYN ──────────────────────────>│  SYN_SENT / SYN_RECV
    │<─── SYN-ACK ──────────────────────│
    │──── ACK ──────────────────────────>│  ESTABLISHED
    │                                   │
    │  ← data flows →                   │
    │                                   │
    │──── FIN ──────────────────────────>│  FIN_WAIT1
    │<─── ACK ──────────────────────────│  FIN_WAIT2
    │<─── FIN ──────────────────────────│  TIME_WAIT
    │──── ACK ──────────────────────────>│  CLOSED
```

---

## Practical Scenarios

### Find what process is listening on a port

```bash
# Is anything listening on port 8080?
ss -tlnp | grep :8080
# or
netstat -tlnp | grep :8080
```

### Count connections per state

```bash
ss -tan | awk '{print $1}' | sort | uniq -c | sort -rn
```

### Find established connections to a specific host

```bash
ss -tn dst 93.184.216.34
```

### Check for a high number of TIME_WAIT sockets

A large number of `TIME_WAIT` connections is normal on busy servers (each lasts ~60 seconds). If it causes port exhaustion, consider enabling `net.ipv4.tcp_tw_reuse`.

```bash
ss -tan state time-wait | wc -l
```

### View the routing table

```bash
ss does not show routing; use:
ip route show
# or (legacy)
netstat -r
route -n
```

---

## Quick Comparison: ss vs netstat

| Feature            | `ss`                           | `netstat`                      |
|:-------------------|:-------------------------------|:-------------------------------|
| Speed              | Fast (reads kernel directly)   | Slower (reads `/proc/net/`)    |
| Default on modern Linux | Yes                       | May need `net-tools` package   |
| Filtering          | Powerful built-in filters      | Limited; pipe to `grep`        |
| Availability       | Linux only                     | Linux, macOS, Windows          |
| Output format      | More concise                   | More traditional               |

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
