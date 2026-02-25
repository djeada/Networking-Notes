# Proxy Servers

## Introduction

A proxy server is an intermediary that sits between a client and a destination server.
Instead of connecting directly to a resource, the client sends requests to the proxy,
which forwards them on the client's behalf and returns the response.

Proxies serve various purposes: **caching**, **access control**, **anonymity**,
**security**, and **load distribution**.

## How a Proxy Works

```text
  Without Proxy:
  [Client] ──────────────────────────> [Destination Server]

  With Forward Proxy:
  [Client] ──> [Forward Proxy] ──────> [Destination Server]
                  │
            caches, filters,
            anonymizes

  With Reverse Proxy:
  [Client] ──────────────────> [Reverse Proxy] ──> [Backend Server A]
                                     │          ──> [Backend Server B]
                                     │          ──> [Backend Server C]
                               load balances,
                               caches, terminates TLS
```

## Forward Proxy vs Reverse Proxy

| Feature            | Forward Proxy                        | Reverse Proxy                        |
|--------------------|--------------------------------------|--------------------------------------|
| Sits in front of   | Clients                              | Servers                              |
| Client aware?      | Yes — client is configured to use it | No — client thinks it's the real server |
| Purpose            | Filter, cache, anonymize for clients | Protect, load balance, cache for servers |
| Configured by      | Client or client's network admin     | Server operator                      |
| Examples           | Squid, corporate web proxies         | Nginx, HAProxy, Cloudflare           |

## Types of Proxy Servers

### HTTP Proxy

Handles HTTP (and sometimes HTTPS) traffic. The client's browser is configured to
send requests to the proxy.

```text
  Client                    HTTP Proxy              Web Server
    |                          |                        |
    |--- GET http://site/ ---->|                        |
    |                          |--- GET / ------------->|
    |                          |<-- 200 OK -------------|
    |<-- 200 OK ---------------|                        |
```

### HTTPS / CONNECT Proxy

For HTTPS traffic, the client sends a `CONNECT` request. The proxy creates a TCP tunnel
and relays encrypted traffic without inspecting the content.

```text
  Client                    Proxy                   Server
    |--- CONNECT server:443 ->|                        |
    |<-- 200 Connection OK ---|                        |
    |=== TLS tunnel through proxy ===================>|
```

### SOCKS Proxy

Operates at a lower level than HTTP proxies — forwards any TCP (and optionally UDP)
traffic. Protocol-agnostic.

- **SOCKS4** — TCP only, no authentication.
- **SOCKS5** — TCP and UDP, supports authentication, DNS resolution at proxy.

### Transparent Proxy

Intercepts traffic without requiring any client configuration. Often deployed at the
network level (e.g., by ISPs or corporate gateways).

- Client is unaware the proxy exists.
- Used for content filtering, caching, and monitoring.

### Caching Proxy

Stores copies of frequently requested resources and serves them directly, reducing
bandwidth usage and improving response times.

```text
  Request 1: Client → Proxy → Server → Proxy (stores copy) → Client
  Request 2: Client → Proxy (cache hit) → Client  (no server contact)
```

## Common Proxy Software

| Software       | Type            | Description                                     |
|----------------|-----------------|-------------------------------------------------|
| **Squid**      | Forward/Caching | Open-source HTTP caching proxy                  |
| **Nginx**      | Reverse         | Web server and reverse proxy                    |
| **HAProxy**    | Reverse         | High-performance TCP/HTTP load balancer          |
| **Envoy**      | Reverse/Sidecar | Cloud-native proxy for microservices             |
| **Traefik**    | Reverse         | Automatic service discovery for containers       |
| **Privoxy**    | Forward         | Privacy-focused filtering proxy                  |

## Proxy Use Cases

| Use Case                   | Proxy Type        | Description                                  |
|----------------------------|-------------------|----------------------------------------------|
| Corporate content filter   | Forward           | Block access to prohibited websites          |
| Web acceleration           | Caching           | Cache static content to reduce latency       |
| Anonymity                  | Forward           | Hide client's real IP address                |
| Protect backend servers    | Reverse           | Shield origin servers from direct exposure   |
| TLS termination            | Reverse           | Handle TLS at the proxy, offloading servers  |
| API gateway                | Reverse           | Route, rate-limit, authenticate API requests |
| Bypass geo-restrictions    | Forward/SOCKS     | Route traffic through a different region     |

## Proxy vs VPN

| Feature            | Proxy                              | VPN                                   |
|--------------------|------------------------------------|---------------------------------------|
| Scope              | Per-application or per-protocol    | All traffic from the device           |
| Encryption         | Usually none (except HTTPS tunnel) | All traffic encrypted                 |
| Configuration      | Per-app or browser setting         | System-wide                           |
| Performance        | Low overhead                       | More overhead due to encryption       |
| Anonymity          | IP hidden from destination         | IP hidden + traffic encrypted         |
| Best for           | Web filtering, caching             | Privacy, secure remote access         |
