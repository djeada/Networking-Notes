# DNS (Domain Name System)

## Introduction

The Domain Name System (DNS) is a hierarchical, distributed naming system that translates
human-readable domain names (e.g., `www.example.com`) into IP addresses (e.g., `93.184.216.34`).
It acts as the "phone book" of the internet, allowing users to access websites using memorable
names instead of numeric addresses.

- DNS requests are sent from a client to a DNS server listed in `/etc/resolv.conf`.
- Uses **port 53**, typically over **UDP** (falls back to TCP for large responses).
- DNS requests and responses can be observed using packet capture tools like Wireshark.

## DNS Hierarchy

DNS is organized as a tree structure. Each level delegates authority to the next.

```text
                        . (Root)
                        |
          +-------------+-------------+
          |             |             |
        .com          .edu          .uk        <-- TLD (Top-Level Domain)
          |             |             |
     +----+----+     stanford      .co.uk
     |         |        |             |
  google    amazon    puffer       bbc         <-- Authoritative
     |
  +--+--+
  |     |
 mail  maps                                   <-- Subdomains
```

**Example**: The FQDN `puffer.stanford.edu.` is divided into:
- Root: `"."`
- TLD: `edu`
- Second-level: `stanford`
- Host: `puffer`

## Hierarchy of Name Servers

### 1. Root Name Servers
- There are 13 logical root server clusters (A through M), distributed worldwide via anycast.
- Contacted by name servers that cannot resolve a name.
- They do not know the final answer but direct queries to the appropriate TLD server.

### 2. Top-Level Domain (TLD) Servers
- Responsible for top-level domains (e.g., `.com`, `.org`, `.edu`, `.uk`, `.fr`).
- Contain information about authoritative domain servers for second-level domains.

### 3. Authoritative Name Servers
- Provide the definitive answer for domains they are responsible for.
- Maintained by an organization or its DNS hosting provider.
- Example: To reach `cse.dtu.in`, the root server directs to the `.in` TLD, which
  directs to the authoritative server for `dtu.in`.

## DNS Resolution Process

### Recursive Resolution

In recursive resolution, the client's resolver asks its local DNS server, which then
handles all further queries on behalf of the client.

```text
  Client          Local DNS        Root Server     TLD Server    Authoritative
    |   (Resolver)    |                |               |               |
    |---1. Query----->|                |               |               |
    |                 |---2. Query---->|               |               |
    |                 |<--3. Referral--|               |               |
    |                 |---4. Query------------------->|               |
    |                 |<--5. Referral-----------------|               |
    |                 |---6. Query--------------------------------------->|
    |                 |<--7. Answer---------------------------------------|
    |<--8. Answer-----|                |               |               |
    |                 |                |               |               |
```

1. Client sends query for `www.example.com` to its local DNS resolver.
2. Local resolver queries a root name server.
3. Root server responds with a referral to the `.com` TLD server.
4. Local resolver queries the `.com` TLD server.
5. TLD server responds with a referral to the authoritative server for `example.com`.
6. Local resolver queries the authoritative name server.
7. Authoritative server returns the IP address.
8. Local resolver returns the answer to the client.

### Iterative Resolution

In iterative resolution, each server returns the best answer it has (often a referral),
and the querying server follows up itself.

```text
  Client              Root Server      TLD Server     Authoritative
    |                      |               |               |
    |---1. Query---------->|               |               |
    |<--2. "Ask .com TLD"--|               |               |
    |---3. Query-------------------------->|               |
    |<--4. "Ask ns.example.com"------------|               |
    |---5. Query---------------------------------------------->|
    |<--6. Answer (IP)------------------------------------------|
    |                      |               |               |
```

## DNS Record Types

| Record | Name                  | Purpose                                           | Example                              |
|--------|-----------------------|---------------------------------------------------|--------------------------------------|
| A      | Address               | Maps hostname to IPv4 address                     | `example.com -> 93.184.216.34`       |
| AAAA   | IPv6 Address          | Maps hostname to IPv6 address                     | `example.com -> 2606:2800:220:1:...` |
| CNAME  | Canonical Name        | Alias for another domain name                     | `www.example.com -> example.com`     |
| MX     | Mail Exchange         | Specifies mail servers for the domain             | `example.com -> mail.example.com`    |
| NS     | Name Server           | Delegates a zone to authoritative name servers    | `example.com -> ns1.example.com`     |
| PTR    | Pointer               | Reverse DNS lookup (IP to hostname)               | `34.216.184.93 -> example.com`       |
| TXT    | Text                  | Arbitrary text (SPF, DKIM, verification)          | `"v=spf1 include:_spf.google.com"`   |
| SOA    | Start of Authority    | Administrative info about the zone                | Serial, refresh, retry, expire, TTL  |
| SRV    | Service               | Specifies host/port for specific services         | `_sip._tcp.example.com`             |

## Types of Domains

### 1. Generic Domains (gTLDs)
- Examples:
  - `.com` (Commercial)
  - `.edu` (Educational)
  - `.mil` (Military)
  - `.org` (Non-profit organization)
  - `.net` (Network infrastructure, now general use)
  - `.gov` (Government)
  - `.info`, `.io`, `.dev` (Newer gTLDs)

### 2. Country Code Domains (ccTLDs)
- Examples:
  - `.in` (India)
  - `.us` (United States)
  - `.uk` (United Kingdom)
  - `.de` (Germany)
  - `.jp` (Japan)

### 3. Inverse Domain (in-addr.arpa)
- Used for reverse DNS — mapping an IP address back to a domain name.
- IPv4 reverse lookups use the `in-addr.arpa` zone with octets reversed.
- Example: To find the hostname for `192.0.2.1`, query `1.2.0.192.in-addr.arpa`.

## DNS Caching

DNS caching stores resolved records at various levels to reduce lookup time and
network traffic.

```text
  Browser Cache  ->  OS Cache  ->  Resolver Cache  ->  Full Lookup
  (seconds)         (minutes)      (hours/days)        (recursive)
```

- **Browser cache**: The browser stores recent DNS lookups for a short period.
- **Operating system cache**: The OS maintains a system-wide DNS cache
  (e.g., `systemd-resolved` on Linux, `dnsmasq`, or the Windows DNS Client service).
- **Resolver cache**: The local DNS resolver (e.g., your ISP or `8.8.8.8`) caches
  responses according to the record's **TTL (Time to Live)** value.
- **TTL**: Each DNS record includes a TTL (in seconds) that tells caches how long
  the record is valid. After expiration, a fresh lookup is performed.

## DNS Tools

### `nslookup`
Query DNS records interactively or non-interactively:
```bash
nslookup www.example.com
nslookup -type=MX example.com
```

### `dig` (Domain Information Groper)
Detailed DNS lookups with full response information:
```bash
dig www.example.com
dig example.com MX +short
dig @8.8.8.8 example.com A       # query a specific DNS server
dig example.com +trace            # trace the full resolution path
```

### `host`
Simple DNS lookup utility:
```bash
host www.example.com
host -t AAAA example.com
```

## Conclusion

DNS is a systematic, hierarchical structure that facilitates the translation of
human-readable domain names to IP addresses. Its distributed design provides
redundancy, scalability, and efficient resolution through caching at multiple levels.
