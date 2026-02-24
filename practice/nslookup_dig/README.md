# DNS Lookup Tools: nslookup, dig, and host

## Overview

DNS lookup tools let you query DNS servers to resolve domain names, troubleshoot DNS issues, and inspect DNS records. The three most common tools are:

| Tool       | Best For                                      | Availability            |
|------------|-----------------------------------------------|-------------------------|
| `nslookup` | Quick interactive or non-interactive lookups  | Linux, macOS, Windows   |
| `dig`      | Detailed queries with full response parsing   | Linux, macOS            |
| `host`     | Simple, concise lookups                       | Linux, macOS            |

---

## nslookup

### Basic Queries

```bash
# Look up the A record (IPv4 address) for a domain
nslookup example.com

# Look up using a specific DNS server
nslookup example.com 8.8.8.8

# Look up a specific record type
nslookup -type=MX example.com
nslookup -type=AAAA example.com
nslookup -type=NS example.com
nslookup -type=TXT example.com
```

### Reading nslookup Output

```text
$ nslookup example.com
Server:		127.0.0.53
Address:	127.0.0.53#53

Non-authoritative answer:
Name:	example.com
Address: 93.184.216.34
```

| Field                    | Meaning                                           |
|--------------------------|---------------------------------------------------|
| `Server` / `Address`    | The DNS server that answered the query             |
| `Non-authoritative`     | The answer came from a cache, not the authoritative server |
| `Name` / `Address`      | The resolved domain and its IP address             |

### Interactive Mode

```bash
$ nslookup
> server 8.8.8.8
Default server: 8.8.8.8
> set type=MX
> example.com
```

---

## dig (Domain Information Groper)

`dig` is the most powerful DNS lookup tool, providing complete control over queries and detailed output.

### Basic Queries

```bash
# Simple A record lookup
dig example.com

# Query a specific record type
dig example.com MX
dig example.com AAAA
dig example.com NS
dig example.com TXT
dig example.com SOA

# Short output (just the answer)
dig example.com +short

# Query a specific DNS server
dig @8.8.8.8 example.com

# Trace the full resolution path from root servers
dig example.com +trace

# Reverse DNS lookup
dig -x 93.184.216.34
```

### Reading dig Output

```text
$ dig example.com

; <<>> DiG 9.18.1 <<>> example.com
;; global options: +cmd
;; Got answer:
;; ->>HEADER<<- opcode: QUERY, status: NOERROR, id: 12345
;; flags: qr rd ra; QUERY: 1, ANSWER: 1, AUTHORITY: 0, ADDITIONAL: 1

;; QUESTION SECTION:
;example.com.                   IN      A

;; ANSWER SECTION:
example.com.            86400   IN      A       93.184.216.34

;; Query time: 23 msec
;; SERVER: 127.0.0.53#53(127.0.0.53)
;; WHEN: Mon Jan 01 12:00:00 UTC 2024
;; MSG SIZE  rcvd: 56
```

| Section          | Meaning                                                |
|------------------|--------------------------------------------------------|
| HEADER           | Response status (`NOERROR`, `NXDOMAIN`, `SERVFAIL`)   |
| flags            | `qr`=response, `rd`=recursion desired, `ra`=recursion available |
| QUESTION SECTION | What was asked                                         |
| ANSWER SECTION   | The DNS records returned                               |
| `86400`          | TTL in seconds (how long the record can be cached)     |
| Query time       | How long the lookup took                               |

### Useful dig Options

| Option            | Description                                     |
|-------------------|-------------------------------------------------|
| `+short`          | Show only the answer (no headers or metadata)   |
| `+trace`          | Trace delegation from root servers              |
| `+noall +answer`  | Show only the answer section                    |
| `+dnssec`         | Request DNSSEC records                          |
| `-x <IP>`         | Perform a reverse DNS lookup                    |
| `@<server>`       | Query a specific DNS server                     |
| `+tcp`            | Use TCP instead of UDP                          |

---

## host

`host` provides concise output for quick DNS lookups.

```bash
# Simple lookup
host example.com

# Reverse lookup
host 93.184.216.34

# Specific record type
host -t MX example.com
host -t NS example.com
host -t AAAA example.com

# Use a specific DNS server
host example.com 8.8.8.8
```

```text
$ host example.com
example.com has address 93.184.216.34
example.com has IPv6 address 2606:2800:220:1:248:1893:25c8:1946
example.com mail is handled by 0 .
```

---

## Practical Exercises

### Exercise 1: Resolve a Domain with All Three Tools

Compare the output of all three tools for the same domain:

```bash
nslookup example.com
dig example.com
host example.com
```

Note how each tool presents the same information differently.

### Exercise 2: Investigate DNS Record Types

Use `dig` to query every common record type for a domain:

```bash
dig example.com A +short
dig example.com AAAA +short
dig example.com MX +short
dig example.com NS +short
dig example.com TXT +short
dig example.com SOA +short
```

### Exercise 3: Trace DNS Resolution

Follow the complete path of a DNS query from root servers to the authoritative answer:

```bash
dig example.com +trace
```

Observe how the query moves from root servers (`.`) to TLD servers (`.com`) to the authoritative name server for the domain.

### Exercise 4: Reverse DNS Lookup

Find the hostname associated with an IP address:

```bash
dig -x 8.8.8.8
host 8.8.8.8
nslookup 8.8.8.8
```

### Exercise 5: Compare DNS Servers

Query the same domain against different public DNS servers and compare response times:

```bash
dig @8.8.8.8 example.com        # Google DNS
dig @1.1.1.1 example.com        # Cloudflare DNS
dig @208.67.222.222 example.com  # OpenDNS
dig @9.9.9.9 example.com        # Quad9 DNS
```

Look at the `Query time` in each response to compare speed.

### Exercise 6: Check DNS Propagation

After changing a DNS record, verify that different servers see the updated value:

```bash
dig @8.8.8.8 yourdomain.com A +short
dig @1.1.1.1 yourdomain.com A +short
dig @ns1.yourdomain.com yourdomain.com A +short
```

### Exercise 7: Inspect TTL Values

Query a record and observe its TTL, then query again after waiting:

```bash
dig example.com A | grep -A1 "ANSWER SECTION"
# Wait 30 seconds, then repeat
sleep 30
dig example.com A | grep -A1 "ANSWER SECTION"
```

The TTL should have decreased, showing the cache countdown.
