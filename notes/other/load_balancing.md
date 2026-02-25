# Load Balancing

## Introduction

Load balancing distributes incoming network traffic across multiple backend servers to
ensure no single server is overwhelmed. It improves **availability**, **reliability**,
and **scalability** of applications and services.

A load balancer sits between clients and a pool of servers, deciding which server should
handle each request.

## Why Load Balancing Matters

```text
  Without Load Balancing:             With Load Balancing:

  Client A ──┐                        Client A ──┐
  Client B ──┼──> [Single Server]     Client B ──┼──> [Load Balancer] ──> Server 1
  Client C ──┘    (overloaded)        Client C ──┘         │          ──> Server 2
                                                           │          ──> Server 3
                                                      distributes
                                                      traffic evenly
```

**Benefits:**
- **High availability** — If one server fails, traffic is redirected to healthy servers.
- **Scalability** — Add servers to handle more traffic.
- **Performance** — Distribute load to reduce response times.
- **Maintenance** — Servers can be taken offline for updates without downtime.

## Load Balancing Algorithms

### Round Robin

Distributes requests sequentially across servers in order.

```text
  Request 1 → Server A
  Request 2 → Server B
  Request 3 → Server C
  Request 4 → Server A  (cycle repeats)
```

- Simple and effective when servers have equal capacity.
- Does not account for current server load.

### Weighted Round Robin

Like round robin, but servers with higher capacity receive more requests.

```text
  Server A (weight 3): gets 3 out of every 5 requests
  Server B (weight 2): gets 2 out of every 5 requests
```

### Least Connections

Routes each new request to the server with the fewest active connections.

- Better for uneven request durations (e.g., some requests are slow, others fast).

### Weighted Least Connections

Combines least connections with server weights — a higher-capacity server is preferred
even if connection counts are similar.

### IP Hash

Uses the client's IP address to determine which server receives the request. The same
client always reaches the same server (provides session persistence without cookies).

### Least Response Time

Routes to the server with the lowest current response time and fewest connections.

## Types of Load Balancers

### Layer 4 (Transport Layer)

Operates at the TCP/UDP level. Routes traffic based on IP address and port number
without inspecting the application payload.

```text
  Client ──> [L4 Load Balancer] ──> Backend
             routes based on:
             - Source/Dest IP
             - Source/Dest Port
             - Protocol (TCP/UDP)
```

- **Pros:** Very fast, low overhead, protocol-agnostic.
- **Cons:** Cannot make decisions based on HTTP content (URL, headers, cookies).

### Layer 7 (Application Layer)

Operates at the HTTP/HTTPS level. Can inspect headers, URLs, cookies, and content to
make intelligent routing decisions.

```text
  Client ──> [L7 Load Balancer] ──> Backend
             routes based on:
             - URL path (/api → API servers)
             - Host header (api.example.com vs www.example.com)
             - Cookie / session ID
             - HTTP method
```

- **Pros:** Content-based routing, SSL termination, caching, compression.
- **Cons:** Higher resource usage; must parse application data.

### Comparison

| Feature              | Layer 4                    | Layer 7                         |
|----------------------|----------------------------|---------------------------------|
| Decision based on    | IP + port                  | HTTP content (URL, headers)     |
| Speed                | Faster                     | Slightly slower                 |
| SSL termination      | No (pass-through)          | Yes                             |
| Content routing      | No                         | Yes                             |
| Protocol support     | Any TCP/UDP                | HTTP, HTTPS, WebSocket          |
| Use case             | High-throughput TCP        | Web applications, APIs          |

## Health Checks

Load balancers perform **health checks** to detect unhealthy servers and stop sending
traffic to them.

```text
  Load Balancer                Server A    Server B    Server C
       |                          |           |           |
       |--- health check -------->| ✓ OK      |           |
       |--- health check --------------------->| ✓ OK     |
       |--- health check ---------------------------------------->| ✗ FAIL
       |                          |           |           |
       | Routes traffic to A and B only                   |
```

**Types of health checks:**
- **TCP** — Can a TCP connection be established?
- **HTTP** — Does a specific URL return a 200 OK?
- **Custom** — Run a script that checks application-specific health.

## Session Persistence (Sticky Sessions)

Some applications require that a client's requests always go to the same server
(e.g., server-side sessions, shopping carts).

| Method              | Description                                         |
|---------------------|-----------------------------------------------------|
| **Cookie-based**    | Load balancer sets a cookie identifying the server  |
| **IP hash**         | Client IP determines the server                     |
| **URL parameter**   | Session ID in the URL maps to a server              |

**Trade-off:** Sticky sessions reduce the effectiveness of load distribution and can
create imbalanced load if some sessions are heavier than others.

## Common Load Balancing Software and Services

| Tool / Service       | Type             | Description                                |
|----------------------|------------------|--------------------------------------------|
| **Nginx**            | Software L7      | Reverse proxy with load balancing           |
| **HAProxy**          | Software L4/L7   | High-performance open-source LB             |
| **Envoy**            | Software L7      | Cloud-native proxy for microservices        |
| **AWS ALB/NLB/CLB**  | Cloud service    | Application, Network, and Classic LBs       |
| **Google Cloud LB**  | Cloud service    | Global load balancing                       |
| **Azure Load Balancer** | Cloud service | L4 load balancer                            |
| **F5 BIG-IP**        | Hardware/Software| Enterprise application delivery controller  |

## DNS-Based Load Balancing

DNS can distribute traffic by returning different IP addresses for the same domain name.

```text
  dig example.com
  → 203.0.113.1  (Server A)
  → 203.0.113.2  (Server B)
  → 203.0.113.3  (Server C)
```

- Simple to implement via multiple A records.
- No health checking at the DNS level (unless using a service like Route 53, Cloudflare).
- TTL caching means failover is not instant.
