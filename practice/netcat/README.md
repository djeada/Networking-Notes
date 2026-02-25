# Netcat (nc)

## Overview

Netcat (`nc`) is a versatile networking utility often called the "Swiss Army knife" of networking. It can read and write data across TCP and UDP connections, making it useful for testing connectivity, transferring files, port scanning, and creating simple client-server setups.

## Basic Usage

### TCP Client

Connect to a TCP service:

```bash
# Connect to a web server on port 80
nc example.com 80

# Then type an HTTP request manually:
# GET / HTTP/1.1
# Host: example.com
# (press Enter twice)
```

### TCP Server (Listener)

Listen for incoming TCP connections:

```bash
# Listen on port 12345
nc -l 12345

# Listen and keep listening after client disconnects (some versions)
nc -lk 12345
```

### UDP Client and Server

```bash
# UDP listener
nc -u -l 12345

# UDP client
nc -u targethost 12345
```

## Connection Testing

### Test if a Port is Open

```bash
# Test a single port (with timeout)
nc -zv example.com 80

# Test multiple ports
nc -zv example.com 80 443 22

# Test a range of ports
nc -zv example.com 20-25

# Test with a timeout
nc -zv -w 3 example.com 443
```

### Reading Connection Test Output

```text
$ nc -zv example.com 80
Connection to example.com (93.184.216.34) 80 port [tcp/http] succeeded!

$ nc -zv example.com 12345
nc: connect to example.com (93.184.216.34) port 12345 (tcp) failed: Connection refused
```

| Result               | Meaning                                      |
|----------------------|----------------------------------------------|
| `succeeded`          | Port is open and accepting connections       |
| `Connection refused` | Port is closed (host is up but not listening)|
| `timed out`          | Port is filtered or host is unreachable      |

## Common Options

| Option     | Description                                    |
|------------|------------------------------------------------|
| `-l`       | Listen mode (server)                           |
| `-p <port>`| Specify source port                            |
| `-u`       | Use UDP instead of TCP                         |
| `-z`       | Scan mode — check if port is open without sending data |
| `-v`       | Verbose output                                 |
| `-w <sec>` | Timeout for connections                        |
| `-k`       | Keep listening after client disconnects        |
| `-n`       | Do not resolve hostnames                       |
| `-e <cmd>` | Execute a command upon connection (not always available) |
| `-q <sec>` | Quit after EOF and delay of specified seconds  |

## Practical Exercises

### Exercise 1: Test Port Connectivity

Check if common services are reachable on a remote host:

```bash
nc -zv example.com 80    # HTTP
nc -zv example.com 443   # HTTPS
nc -zv example.com 22    # SSH
nc -zv example.com 53    # DNS
```

### Exercise 2: Simple Chat Between Two Machines

Set up a basic chat session between two terminals (or machines):

```bash
# Terminal 1 (listener)
nc -l 12345

# Terminal 2 (client)
nc localhost 12345
```

Type messages in either terminal and they appear in the other.

### Exercise 3: Transfer a File

Send a file from one machine to another:

```bash
# On the receiving end (listener)
nc -l 12345 > received_file.txt

# On the sending end
nc targethost 12345 < file_to_send.txt
```

### Exercise 4: Simple HTTP Request

Manually send an HTTP request and view the raw response:

```bash
echo -e "GET / HTTP/1.1\r\nHost: example.com\r\nConnection: close\r\n\r\n" | nc example.com 80
```

### Exercise 5: Port Scanning

Scan a range of ports to discover open services:

```bash
nc -zv -w 1 targethost 1-1024 2>&1 | grep succeeded
```

### Exercise 6: Test UDP Connectivity

Test a UDP service (e.g., DNS):

```bash
# Send a simple message via UDP
echo "test" | nc -u -w 1 targethost 53
```

### Exercise 7: Banner Grabbing

Connect to a service and capture its banner (the initial message it sends):

```bash
nc -v -w 3 targethost 22   # SSH banner
nc -v -w 3 targethost 25   # SMTP banner
nc -v -w 3 targethost 21   # FTP banner
```

## Netcat Variants

Different systems ship with different versions of netcat, which may support different options:

| Variant              | Package Name     | Notes                                           |
|----------------------|------------------|-------------------------------------------------|
| Traditional netcat   | `netcat-traditional` | Supports `-e` for command execution          |
| OpenBSD netcat       | `netcat-openbsd` | Default on many Linux distros; no `-e` flag     |
| Ncat (Nmap project)  | `ncat`           | TLS support, access control, most feature-rich  |

To check which version you have:

```bash
nc -h 2>&1 | head -3
# or
which nc && nc --version 2>&1 || nc -h 2>&1 | head -1
```
