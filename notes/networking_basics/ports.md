# Ports

## What Is a Port?

A **port** is a logical endpoint for network communication. It is represented as a 16-bit unsigned integer, giving a range of **0 to 65535**. While an IP address identifies a host on a network, a port number identifies a specific service or process running on that host. Together, the IP address and port number allow network traffic to be directed to the correct application.

```text
┌──────────────────────────────────────────────────────┐
│                   Network Host                       │
│              IP: 192.168.1.10                        │
│                                                      │
│   ┌──────────┐  ┌──────────┐  ┌──────────┐          │
│   │ Web Srv  │  │ SSH Srv  │  │ DB Srv   │          │
│   │ Port 80  │  │ Port 22  │  │ Port 3306│          │
│   └────▲─────┘  └────▲─────┘  └────▲─────┘          │
│        │              │              │               │
└────────┼──────────────┼──────────────┼───────────────┘
         │              │              │
   ──────┴──────────────┴──────────────┴────── Network

   192.168.1.10:80    192.168.1.10:22   192.168.1.10:3306
```

When a client connects to a server, it targets a specific IP address **and** port. The combination uniquely identifies the service the client wants to reach.

---

## Port Ranges

The Internet Assigned Numbers Authority (IANA) divides the port number space into three ranges:

| Range | Name | Description |
|---|---|---|
| 0 – 1023 | **Well-Known Ports** | Reserved for common system services. On most operating systems, binding to these ports requires elevated (root/admin) privileges. Assigned by IANA. |
| 1024 – 49151 | **Registered Ports** | Can be registered with IANA by software vendors for specific applications, but are generally available for user processes. |
| 49152 – 65535 | **Dynamic / Ephemeral Ports** | Used by the operating system for temporary, short-lived client-side connections. Assigned automatically when a client opens an outbound connection. |

---

## Well-Known Ports Reference

| Port | Protocol | Service | Description |
|---|---|---|---|
| 20 | TCP | FTP (Data) | File Transfer Protocol – data channel |
| 21 | TCP | FTP (Control) | File Transfer Protocol – command/control channel |
| 22 | TCP | SSH | Secure Shell – encrypted remote login and command execution |
| 23 | TCP | Telnet | Unencrypted remote login (legacy, insecure) |
| 25 | TCP | SMTP | Simple Mail Transfer Protocol – sending email |
| 53 | TCP/UDP | DNS | Domain Name System – name resolution |
| 67 | UDP | DHCP (Server) | Dynamic Host Configuration Protocol – server listens here |
| 68 | UDP | DHCP (Client) | Dynamic Host Configuration Protocol – client listens here |
| 69 | UDP | TFTP | Trivial File Transfer Protocol |
| 80 | TCP | HTTP | Hypertext Transfer Protocol – unencrypted web traffic |
| 110 | TCP | POP3 | Post Office Protocol v3 – retrieving email |
| 119 | TCP | NNTP | Network News Transfer Protocol |
| 123 | UDP | NTP | Network Time Protocol – clock synchronization |
| 143 | TCP | IMAP | Internet Message Access Protocol – retrieving email |
| 161 | UDP | SNMP | Simple Network Management Protocol – monitoring |
| 162 | UDP | SNMP Trap | SNMP notifications/alerts |
| 389 | TCP | LDAP | Lightweight Directory Access Protocol |
| 443 | TCP | HTTPS | HTTP over TLS/SSL – encrypted web traffic |
| 445 | TCP | SMB | Server Message Block – Windows file sharing |
| 465 | TCP | SMTPS | SMTP over SSL (legacy) |
| 514 | UDP | Syslog | System logging |
| 587 | TCP | SMTP (Submission) | Email submission (with STARTTLS) |
| 993 | TCP | IMAPS | IMAP over SSL/TLS |
| 995 | TCP | POP3S | POP3 over SSL/TLS |
| 3306 | TCP | MySQL | MySQL database server |
| 3389 | TCP | RDP | Remote Desktop Protocol (Windows) |
| 5432 | TCP | PostgreSQL | PostgreSQL database server |
| 5900 | TCP | VNC | Virtual Network Computing – remote desktop |
| 6379 | TCP | Redis | Redis in-memory data store |
| 8080 | TCP | HTTP (Alt) | Common alternative HTTP port for proxies/dev servers |
| 27017 | TCP | MongoDB | MongoDB database server |

---

## Many Connections on a Single Port

A server can accept a very large number of simultaneous connections on a single port. The limit is **not** the port number itself; rather, it is constrained by the number of file descriptors the kernel supports (e.g., 2048 by default, but tunable much higher).

The key concept is that a TCP connection is uniquely identified by a **four-tuple**:

```text
(Source IP, Source Port, Destination IP, Destination Port)
```

So even though many clients connect to the same destination port, each connection remains unique because the source side differs:

```text
  Client A                          Server
  10.0.0.2:51234  ──────────►  192.168.1.10:80
  Client B                          │
  10.0.0.3:49876  ──────────►  192.168.1.10:80
  Client C                          │
  10.0.0.2:52345  ──────────►  192.168.1.10:80
                                    │
                   All three are distinct connections
                   on the SAME server port (80).
```

### Outbound Connection Limits

A machine can only make about **~64K outbound connections per IP address**, because the source port is a 16-bit number (0–65535) and each outbound connection consumes one ephemeral port. You can extend this by assigning additional IP addresses to the machine—each address provides its own 64K port space.

In practice you will hit other limits first:

* More connections than a single box can handle for performance reasons (CPU, memory, file descriptors).
* Load balancers will distribute connections across multiple servers for availability anyway.

---

## Sockets

A **socket** is the combination of an IP address and a port number, written as `IP:Port` (e.g., `192.168.1.10:443`). It is the fundamental endpoint for sending and receiving data.

```text
  Socket = IP Address + Port Number

  Example:  192.168.1.10:443
            └──────┬─────┘ └┬┘
            IP Address     Port
```

A full network connection is defined by a **pair of sockets** (one on each side):

```text
  Local Socket              Remote Socket
  192.168.1.10:443    <──>  10.0.0.5:52140
```

In programming, a socket is also an API abstraction (e.g., Berkeley sockets) that applications use to read from and write to the network.

---

## Port States

When scanning or troubleshooting a host, ports are commonly described by three states:

| State | Meaning |
|---|---|
| **Open** | A service is actively listening and accepting connections on this port. |
| **Closed** | No service is listening. The host responds (e.g., with a TCP RST) to indicate nothing is there. |
| **Filtered** | A firewall, packet filter, or other network device is blocking probes. No response is received, or an ICMP unreachable message is returned. It is unclear whether the port is open or closed. |

Understanding port states is critical for network security:

* **Open** ports represent the attack surface of a host—only ports needed for legitimate services should be open.
* **Closed** ports confirm the host is reachable but has no service on that port.
* **Filtered** ports suggest a firewall is in place, which is generally the desired posture for unused ports.

---

## Checking Ports with Common Tools

### `netstat` (legacy, available almost everywhere)

```bash
# Show all listening TCP ports with process info
netstat -tlnp

# Show all connections (listening and established)
netstat -anp
```

### `ss` (modern replacement for netstat on Linux)

```bash
# Show listening TCP sockets with process info
ss -tlnp

# Show all TCP connections
ss -tanp

# Filter by a specific port
ss -tlnp sport = :443
```

### `lsof` (list open files, including network sockets)

```bash
# Show what process is using a specific port
lsof -i :80

# Show all network connections for a specific process
lsof -i -a -p <PID>
```

### `nmap` (network scanner / port scanner)

```bash
# Scan the 1000 most common ports on a host
nmap 192.168.1.10

# Scan a specific port range
nmap -p 1-1024 192.168.1.10

# Scan all 65535 ports
nmap -p- 192.168.1.10

# Detect services and versions on open ports
nmap -sV 192.168.1.10
```
