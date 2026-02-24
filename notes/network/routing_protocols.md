# Routing Protocols

## Introduction

Routing protocols allow routers to dynamically learn about remote networks and select the
best path for forwarding packets. Without routing protocols, an administrator would need
to manually configure every route on every router — an approach that does not scale.

Routing protocols exchange information between routers so that each builds and maintains
a **routing table** with the best known path to every reachable destination.

## Static vs Dynamic Routing

| Aspect              | Static Routing                          | Dynamic Routing                          |
|---------------------|-----------------------------------------|------------------------------------------|
| Configuration       | Manual per route per router             | Routers discover routes automatically    |
| Scalability         | Poor — impractical for large networks   | Good — adapts as the network grows       |
| Convergence         | Instant (no protocol to converge)       | Takes time after topology changes        |
| Resource usage      | Minimal (no CPU/bandwidth for updates)  | Uses CPU, memory, and bandwidth          |
| Best for            | Small networks, default routes, stubs   | Medium to large networks                 |

## Categories of Routing Protocols

```text
  Routing Protocols
  ├── Interior Gateway Protocols (IGP)
  │   ├── Distance Vector
  │   │   ├── RIP
  │   │   └── EIGRP
  │   └── Link-State
  │       ├── OSPF
  │       └── IS-IS
  └── Exterior Gateway Protocol (EGP)
      └── Path Vector
          └── BGP
```

- **IGP** (Interior Gateway Protocol) — used within a single autonomous system (AS).
- **EGP** (Exterior Gateway Protocol) — used between autonomous systems. BGP is the
  only EGP in use today.

## Distance Vector Protocols

Each router shares its **routing table** (a vector of distances) with its directly
connected neighbors at regular intervals. Routers do not have a complete view of the
network topology.

### RIP (Routing Information Protocol)

- Uses **hop count** as the metric (maximum 15 hops; 16 = unreachable).
- Sends full routing table updates every **30 seconds**.
- Simple to configure but slow to converge.
- **RIPv1**: Classful (no subnet mask in updates), broadcast-based.
- **RIPv2**: Classless (carries subnet mask), multicast `224.0.0.9`.
- Uses **UDP port 520**.

```text
  Router A            Router B            Router C
  10.0.1.0/24         10.0.2.0/24         10.0.3.0/24
       |                   |                   |
       |-- "I can reach    |                   |
       |   10.0.1.0,       |                   |
       |   distance 0" --->|                   |
       |                   |-- "I can reach    |
       |                   |   10.0.1.0,       |
       |                   |   distance 1;     |
       |                   |   10.0.2.0,       |
       |                   |   distance 0" --->|
```

### EIGRP (Enhanced Interior Gateway Routing Protocol)

- Cisco-proprietary (now partially open in RFC 7868).
- Uses a **composite metric** based on bandwidth, delay, reliability, and load.
- Sends partial updates only when changes occur (not periodic full updates).
- Maintains a **topology table** with backup routes (feasible successors).
- Converges faster than RIP.

## Link-State Protocols

Each router builds a complete **map of the network topology** by flooding link-state
advertisements (LSAs). Every router independently calculates the shortest path using
Dijkstra's algorithm (SPF — Shortest Path First).

### OSPF (Open Shortest Path First)

- The most widely used IGP.
- Uses **cost** as the metric (based on interface bandwidth: cost = reference BW / interface BW).
- Defined in **RFC 2328** (OSPFv2 for IPv4) and **RFC 5340** (OSPFv3 for IPv6).
- Uses **multicast** addresses `224.0.0.5` (all OSPF routers) and `224.0.0.6` (DR/BDR).
- Supports **areas** to limit the scope of LSA flooding and reduce resource usage.

```text
                     Area 0 (Backbone)
                ┌────────────────────────┐
                │  Router A ── Router B  │
                │      │           │     │
                └──────┼───────────┼─────┘
                       │           │
                ┌──────┼──┐  ┌────┼──────┐
                │  Area 1 │  │  Area 2   │
                │ Router C │  │ Router D  │
                │ Router E │  │ Router F  │
                └─────────┘  └───────────┘
```

**Key OSPF concepts:**
- **DR / BDR** (Designated Router / Backup DR) — elected on multi-access segments to
  reduce the number of adjacencies.
- **Hello packets** — sent every 10 seconds (broadcast) or 30 seconds (NBMA) to
  discover and maintain neighbor relationships.
- **LSA types** — different types describe different parts of the topology (router LSA,
  network LSA, summary LSA, etc.).

### IS-IS (Intermediate System to Intermediate System)

- Common in large ISP and service provider networks.
- Similar to OSPF (link-state, Dijkstra-based) but uses a different addressing scheme
  (CLNS/NET addresses).
- Scales very well for large flat networks.

## Path Vector Protocol — BGP

### BGP (Border Gateway Protocol)

BGP is the routing protocol that glues the internet together. It routes traffic between
**autonomous systems** (AS) — each AS is a network or group of networks under a single
administrative domain.

- Defined in **RFC 4271** (BGP-4).
- Uses **TCP port 179** for reliable neighbor communication.
- The metric is the **AS path** — the list of autonomous systems a route traverses.
- BGP selects routes based on **policies** and **path attributes**, not just shortest path.

```text
  AS 100                AS 200               AS 300
  ┌──────────┐         ┌──────────┐         ┌──────────┐
  │ ISP A    │── eBGP ─│ ISP B    │── eBGP ─│ ISP C    │
  │          │         │          │         │          │
  │ iBGP    │         │ iBGP    │         │          │
  │ routers  │         │ routers  │         │          │
  └──────────┘         └──────────┘         └──────────┘
```

- **eBGP** (External BGP) — sessions between routers in different autonomous systems.
- **iBGP** (Internal BGP) — sessions between routers within the same AS.

**Key BGP path attributes:**
- **AS_PATH** — list of ASes the route has traversed (shorter is preferred).
- **NEXT_HOP** — IP address of the next hop.
- **LOCAL_PREF** — preference within the local AS (higher is preferred).
- **MED** (Multi-Exit Discriminator) — preference hint to neighboring AS.
- **ORIGIN** — how the route was learned (IGP, EGP, or incomplete).

## Administrative Distance

When multiple routing protocols provide a route to the same destination, the router
uses **administrative distance** (AD) to decide which source to trust.

| Source               | AD  |
|----------------------|----:|
| Connected interface  |   0 |
| Static route         |   1 |
| eBGP                 |  20 |
| EIGRP (internal)     |  90 |
| OSPF                 | 110 |
| IS-IS                | 115 |
| RIP                  | 120 |
| EIGRP (external)     | 170 |
| iBGP                 | 200 |

Lower AD is preferred. If AD is the same, the routing protocol's own metric breaks the tie.

## Convergence

Convergence is the time it takes for all routers to agree on the current network topology
after a change (link failure, new route, etc.).

| Protocol | Convergence Speed | Reason                                        |
|----------|-------------------|-----------------------------------------------|
| RIP      | Slow (minutes)    | Periodic updates; count-to-infinity problem   |
| EIGRP    | Fast (seconds)    | Feasible successors provide instant failover  |
| OSPF     | Moderate (seconds)| SPF recalculation after LSA flooding          |
| BGP      | Slow (minutes)    | Policy-based; conservative timer defaults     |
