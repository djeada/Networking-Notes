# How the Internet Works

## Overview

The internet is a global network of interconnected networks that allows billions of devices to communicate with each other. It is not owned by any single entity — it is a decentralized system of networks operated by ISPs, governments, universities, and private companies, all agreeing to exchange traffic using standardized protocols (primarily TCP/IP).

Information is sent across the internet in small units called **packets**. Each packet contains the IP addresses of the sender and receiver, allowing routers to forward it hop by hop until it reaches its destination.

## The Internet as a Network of Networks

The internet connects LANs (Local Area Networks) around the world into one massive interconnected system. No single router or cable carries all traffic — instead, data travels through a hierarchy of networks.

```text
 [Your Device]
      |
 [Home Router]
      |
 [Local ISP]
      |
 [Regional ISP / IXP]
      |
 [Internet Backbone (Tier 1 Networks)]
      |
 [Regional ISP / IXP]
      |
 [Destination ISP]
      |
 [Web Server]
```

Why not have one giant central router? Because a single router would need millions of ports, would have to handle all global traffic, and would be a **single point of failure** — if it went down, the entire internet would go down with it. The decentralized design provides redundancy and resilience.

## What Happens When You Type a URL in the Browser

When you type a URL like `https://www.example.com` and press Enter, a complex chain of events occurs in milliseconds:

1. **Check the cache** — The browser checks its local cache for a fresh copy of the page. If found, it displays the cached content immediately.
2. **DNS lookup** — The browser resolves the domain name to an IP address. It checks the browser cache, OS cache, and router cache. If none have the answer, a recursive DNS query is sent to the configured DNS resolver (see DNS Resolution below).
3. **TCP connection** — The browser initiates a TCP three-way handshake (`SYN` → `SYN-ACK` → `ACK`) with the server at the resolved IP address.
4. **TLS handshake** — If the URL uses HTTPS, a TLS handshake establishes an encrypted session.
5. **HTTP request** — The browser sends an HTTP request (e.g., `GET /index.html`) to the web server.
6. **Server processing** — The web server (Apache, Nginx, IIS, etc.) processes the request and generates an HTTP response containing HTML, CSS, JavaScript, and other resources.
7. **Browser rendering** — The browser parses the HTML, fetches additional resources (images, scripts, stylesheets), builds the DOM, and renders the page on screen.

```text
 Browser                    DNS Server          Web Server
    |                           |                    |
    |--- DNS Query ----------->|                    |
    |<-- IP Address -----------|                    |
    |                                                |
    |--- TCP SYN ---------------------------------->|
    |<-- TCP SYN-ACK -------------------------------|
    |--- TCP ACK ---------------------------------->|
    |                                                |
    |--- TLS Handshake (if HTTPS) ----------------->|
    |<-- TLS Handshake -----------------------------|
    |                                                |
    |--- HTTP GET /index.html --------------------->|
    |<-- HTTP 200 OK + HTML ------------------------|
    |                                                |
    |--- Requests for CSS, JS, images ------------->|
    |<-- Additional resources ----------------------|
```

## Internet Infrastructure

### Submarine Cables

The vast majority of international internet traffic travels through **fiber optic cables** laid on the ocean floor. These submarine cables connect continents and carry data at the speed of light through glass fibers. If a submarine cable is damaged (by anchors, earthquakes, or marine life), it can disrupt internet connectivity for entire regions.

### Internet Exchange Points (IXPs)

An IXP is a physical location where multiple ISPs and networks connect to exchange traffic directly, rather than routing through third parties. IXPs reduce latency, lower costs, and keep local traffic local. Major IXPs include DE-CIX (Frankfurt), AMS-IX (Amsterdam), and LINX (London).

### Data Centers

Large-scale services (Google, Amazon, Netflix) operate data centers around the world. These facilities house thousands of servers and are strategically placed near IXPs and population centers to minimize latency. Content Delivery Networks (CDNs) cache copies of content at edge locations closer to end users.

## How Devices Connect to the Internet

A typical home or office connects to the internet through a chain of devices:

- **Modem** — Converts the signal from your ISP (over coax, DSL, or fiber) into Ethernet signals your local network can use.
- **Router** — Assigns local IP addresses (via DHCP), performs NAT (Network Address Translation), and routes traffic between your LAN and the internet. A home router typically combines a router, switch, wireless access point, and sometimes a modem into one device.
- **ISP** — Your Internet Service Provider connects your router to its network and from there to the broader internet.

```text
 [PC / Phone / Laptop]
        |  (Wi-Fi or Ethernet)
 [Home Router + Switch + AP]
        |  (Ethernet)
 [Modem]
        |  (Coax / DSL / Fiber)
 [ISP Network]
        |
 [Internet]
```

A switch is sufficient to create a LAN, but to reach the internet you need a router that acts as a **gateway** — the exit point from your local network to the outside world.

## DNS Resolution

The Domain Name System (DNS) translates human-readable domain names (like `www.example.com`) into IP addresses (like `93.184.216.34`). Without DNS, you would need to memorize numeric addresses for every website.

The DNS lookup process follows a hierarchy:

1. **Browser cache** — Has this domain been resolved recently?
2. **OS cache** — The operating system maintains its own DNS cache.
3. **Router cache** — The home router may cache recent lookups.
4. **Recursive resolver** — Typically operated by your ISP or a public DNS service (e.g., `8.8.8.8`). If it does not have the answer cached, it queries authoritative servers.
5. **Root name server** — Directs the query to the appropriate TLD server (e.g., `.com`).
6. **TLD name server** — Directs the query to the authoritative name server for the domain.
7. **Authoritative name server** — Returns the final IP address for the requested domain.

## Packet Routing

When a computer in India sends a packet to a computer in Mexico, the packet does not travel in a single direct path. Instead, it is forwarded **hop by hop** through a series of routers. Each router examines the destination IP address, consults its **routing table**, and forwards the packet to the next best hop.

```text
 [Source: India]
      |
 [Router A] --routing table--> best next hop
      |
 [Router B] --routing table--> best next hop
      |
 [Router C] --routing table--> best next hop
      |
 [Submarine Cable]
      |
 [Router D] --routing table--> best next hop
      |
 [Router E] --routing table--> best next hop
      |
 [Destination: Mexico]
```

Key points about packet routing:

- Each router makes an **independent forwarding decision** based on its own routing table.
- The request and the response may take **different paths** through the network.
- Routing protocols like **BGP** (Border Gateway Protocol) allow routers to share reachability information and select optimal paths.
- If a link fails, routers can reroute traffic along alternative paths, providing **fault tolerance**.

## The Internet Is a Network of Networks

When you request a video from YouTube, you are communicating with high-powered computers called **servers**. To avoid a single point of failure, services like YouTube deploy servers in data centers distributed around the world. **Streaming** is the process of delivering data in small pieces (packets) so playback can begin before the entire file is downloaded.

The internet is not a single network — it is a **network of networks**: home networks, corporate networks, ISP networks, and backbone networks all interconnected through standardized protocols, peering agreements, and shared infrastructure.
