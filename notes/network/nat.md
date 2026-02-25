# NAT (Network Address Translation)

**NAT** is a process where a router translates one IP address into another, most commonly mapping private (internal) IP addresses to a single public IP address. It was created to solve two key problems:

1. **IPv4 address exhaustion** — there are not enough public IPv4 addresses for every device.
2. **Security** — without NAT, every device would have a public IP address and could potentially be accessed from anywhere on the internet.

---

## How NAT Works

```text
     Private Network                    Router (NAT)                 Internet
  +-------------------+          +---------------------+       +----------------+
  | 192.168.1.10:4020 |---+      |                     |       |                |
  | 192.168.1.11:4030 |---+----->| Private  ->  Public |------>| Web Server     |
  | 192.168.1.12:4040 |---+      | 192.168.1.x   203.0.113.5  | 93.184.216.34  |
  +-------------------+          |                     |       |                |
                                 |  NAT Translation    |       +----------------+
                                 |  Table:             |
                                 |  192.168.1.10:4020  |
                                 |    -> 203.0.113.5:5001
                                 |  192.168.1.11:4030  |
                                 |    -> 203.0.113.5:5002
                                 |  192.168.1.12:4040  |
                                 |    -> 203.0.113.5:5003
                                 +---------------------+
```

The router maintains a **NAT translation table** to map outgoing requests from internal devices to unique port numbers on the public IP, and routes return traffic back to the correct internal device.

---

## Types of NAT

### 1. Static NAT (SNAT)

A **one-to-one** permanent mapping between a private IP and a public IP. Used when an internal server must be reachable from the internet at a consistent address.

```text
  Private IP         Public IP
  +-------------+    +---------------+
  | 192.168.1.10| <->| 203.0.113.10  |   (always mapped)
  +-------------+    +---------------+
  | 192.168.1.11| <->| 203.0.113.11  |   (always mapped)
  +-------------+    +---------------+
```

### 2. Dynamic NAT (DNAT)

Maps private IPs to a **pool of public IPs** on a first-come, first-served basis. The mapping is temporary and released when the session ends. Also called **IP masquerading**.

```text
  Private IP           Public IP Pool
  +-------------+      +-----------------+
  | 192.168.1.10| ---->| 203.0.113.10    |  (temporary)
  +-------------+      +-----------------+
  | 192.168.1.11| ---->| 203.0.113.11    |  (temporary)
  +-------------+      +-----------------+
  | 192.168.1.12| ---->|  (waiting...)   |  (pool exhausted)
  +-------------+      +-----------------+
```

### 3. PAT (Port Address Translation) / NAT Overload

The most common type of NAT. **Many private IPs** share a **single public IP**, differentiated by unique port numbers. This is what most home routers use.

```text
  Private Network              Router (PAT)              Internet
  +--------------------+    +------------------+     +----------------+
  | 192.168.1.10:3000  |--->| 203.0.113.5:5001 |---->|                |
  | 192.168.1.11:3000  |--->| 203.0.113.5:5002 |---->| Remote Server  |
  | 192.168.1.12:4000  |--->| 203.0.113.5:5003 |---->|                |
  +--------------------+    +------------------+     +----------------+
                             (single public IP,
                              different ports)
```

---

## Port Forwarding

**Port forwarding** is a NAT configuration that directs incoming traffic on a specific port of the public IP to a specific device and port on the private network. This allows external users to reach internal services (e.g., a web server or game server).

```text
  Internet                      Router                    Private Network
  +----------+            +-----------------+          +------------------+
  | Client   |  request   | Public IP       |  forward | 192.168.1.10     |
  | anywhere |----------->| 203.0.113.5:80  |--------->| :80 (Web Server) |
  +----------+            +-----------------+          +------------------+
                          | 203.0.113.5:22  |--------->| 192.168.1.20     |
                          |                 |          | :22 (SSH Server) |
                          +-----------------+          +------------------+
```

---

## NAT Traversal Challenges

NAT can create difficulties for certain applications:

- **Peer-to-peer connections**: Both peers may be behind NAT, making direct connections difficult. Techniques like **STUN**, **TURN**, and **ICE** (used in WebRTC) help establish connections through NAT.
- **Incoming connections**: By default, NAT blocks unsolicited inbound traffic. Port forwarding or UPnP is required to allow external access to internal services.
- **VoIP and gaming**: Real-time applications can suffer from NAT-related latency and connectivity issues.
- **IPsec VPNs**: NAT modifies IP headers, which can break IPsec authentication. **NAT-T (NAT Traversal)** encapsulates IPsec packets in UDP to work around this.

---

## NAT vs Subnetting

| Feature          | Subnetting                                                        | NAT                                                               |
|------------------|-------------------------------------------------------------------|-------------------------------------------------------------------|
| **Definition**   | Dividing a network into smaller segments (subnets).               | Remapping one IP address space into another by modifying packet headers. |
| **Primary Use**  | Create smaller, manageable networks from a larger network.        | Allow multiple devices to share a single public IP for internet access. |
| **Objective**    | Improve performance, efficient IP allocation, isolate hosts.      | Conserve IPv4 addresses, hide internal IPs for basic security.    |
| **Operation**    | Divides based on subnet mask (network vs host portion).           | Translates private IPs to public IPs via router or firewall.      |
| **IP Addresses** | Each subnet has network, host, and broadcast addresses.           | Uses two sets: internal (private) and external (public).          |
| **Routing**      | Routers use subnet info for efficient routing decisions.          | NAT devices translate between private and public networks.        |
| **Visibility**   | Subnets are visible internally and externally if routed.          | Internal addresses are hidden from the external network.          |
| **Configuration**| Requires planning for IP ranges, masks, and topology.             | Configured on routers/firewalls with static or dynamic mappings.  |
| **Scalability**  | Highly scalable with careful IP planning.                         | Scalable internally, limited by available public IPs.             |
| **Common Usage** | Medium to large networks for efficient IP management.             | Nearly all networks where IP conservation matters.                |

---

## NAT vs Proxy

| Parameter                 | NAT                                                        | Proxy (Forward Proxy)                                   |
|---------------------------|------------------------------------------------------------|---------------------------------------------------------|
| **OSI Layer**             | Layer 3/4 (Network/Transport)                              | Layer 7 (Application)                                   |
| **Connection Type**       | Single continuous connection (with IP translation)         | Two separate connections: client-proxy, proxy-server     |
| **Data Handling**         | Cannot read or modify encrypted data; only rewrites IPs    | Can decrypt, inspect, modify, cache, and filter data     |
| **Primary Function**      | IP address conservation and basic security by IP masking   | Content filtering, caching, and enforcing network policies |
| **Visibility to Hosts**   | Typically invisible; operates transparently                | Both client and server are aware of the proxy            |
| **Application Specificity** | Operates at the IP level, not protocol-specific          | Protocol-specific (e.g., HTTP, FTP)                      |
| **Data Exposure**         | No exposure of user data if encrypted                      | User data exposed to proxy when decrypted                |
| **Security Impact**       | Basic security by hiding internal IP addresses             | Enhanced security by controlling traffic at application layer |
| **Configuration**         | No special configuration on end hosts                      | May require configuration on client devices              |
| **Overhead**              | Low; primarily IP address rewriting                        | Higher; processing at the application level              |
| **Common Use Cases**      | Conserving public IPs, simple network security             | Web filtering, bypassing geo-restrictions, caching       |
| **Cost**                  | Low; implemented on existing network devices               | Higher; may require dedicated hardware/software          |
