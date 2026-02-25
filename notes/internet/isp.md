# ISP (Internet Service Provider)

## Introduction

An Internet Service Provider (ISP) is a company that provides individuals and organizations with access to the internet. ISPs own and operate portions of the network infrastructure (routers, cables, and access points) that make up the internet. They range from small local providers serving a single town to massive global carriers whose backbone networks span continents.

The internet is made up of many separate networks linked together. ISPs are the organizations that interconnect these networks, forming the global internet.

## ISP Hierarchy

ISPs are organized into a tiered hierarchy based on the scope and reach of their networks:

```text
                  ┌──────────────────────┐
                  │  Tier 1 / Global ISP │
                  │  (e.g., Lumen, NTT)  │
                  └──────────┬───────────┘
                             │
              ┌──────────────┴──────────────┐
              │                             │
     ┌────────┴────────┐          ┌─────────┴───────┐
     │  Tier 2          │          │  Tier 2          │
     │  Regional ISP    │          │  Regional ISP    │
     └────────┬─────────┘          └────────┬────────┘
              │                             │
    ┌─────────┴──────┐            ┌─────────┴──────┐
    │                │            │                │
 ┌──┴───┐      ┌────┴──┐     ┌──┴───┐      ┌────┴──┐
 │Tier 3│      │Tier 3 │     │Tier 3│      │Tier 3 │
 │Local │      │Local  │     │Local │      │Local  │
 │ISP   │      │ISP    │     │ISP   │      │ISP    │
 └──┬───┘      └───┬───┘     └──┬───┘      └───┬───┘
    │              │             │              │
 [Homes]       [Homes]       [Homes]       [Homes]
```

### Tier 1 ISPs (Global / Backbone)

Tier 1 ISPs own and operate the **internet backbone** — the high-capacity fiber optic networks that carry traffic across continents. They do not pay any other network for transit because they can reach every part of the internet through **settlement-free peering** with other Tier 1 providers. Examples include Lumen (CenturyLink), NTT, Telia, and Cogent.

### Tier 2 ISPs (Regional)

Tier 2 ISPs operate regional networks that connect cities and states within a country. They **peer** with some networks for free but must **purchase transit** from Tier 1 ISPs to reach the full internet. They serve as intermediaries between local ISPs and the global backbone.

### Tier 3 ISPs (Local / Access)

Tier 3 ISPs are the "last mile" providers that connect end users (homes and small businesses) to the internet. They purchase transit from Tier 2 or Tier 1 ISPs. These are the companies most people interact with directly (e.g., a local cable or DSL provider).

Note: Some local ISPs connect directly to a global ISP, bypassing regional ISPs, to provide better performance for their customers.

## Peering and Transit

**Transit** is a paid relationship where one ISP pays another to carry its traffic to the rest of the internet. **Peering** is a mutual arrangement where two networks agree to exchange traffic directly, usually for free (settlement-free peering).

```text
 Without Peering:                    With Peering:

 [User] -> [Local ISP]              [User] -> [Local ISP]
              |                                   |
        [Regional ISP]              [Direct Peering Link]
              |                                   |
        [Tier 1 ISP]                [Google Server]
              |
        [Regional ISP]
              |
        [Google Server]
```

Large content providers like Google, Netflix, and Meta maintain their own networks and establish **direct peering** with local ISPs. By placing servers (or cache appliances) inside or near the local ISP's network, they bypass the need for traffic to traverse the full ISP hierarchy. This reduces latency and cost for both parties.

## Internet Exchange Points (IXPs)

An **Internet Exchange Point (IXP)** is a physical facility where multiple ISPs and networks come together to exchange traffic. Rather than each ISP establishing individual peering connections with every other ISP, they all connect to a shared switching fabric at the IXP.

Benefits of IXPs:
- **Reduced latency** — Local traffic stays local instead of traveling through distant backbone networks.
- **Lower costs** — ISPs avoid paying transit fees for traffic that can be exchanged locally.
- **Improved redundancy** — Multiple peering options provide failover paths.

Major IXPs include DE-CIX (Frankfurt), AMS-IX (Amsterdam), LINX (London), and IX.br (São Paulo).

## Types of Internet Connections

| Connection Type | Medium             | Download Speed      | Latency  | Notes                                    |
|-----------------|--------------------|---------------------|----------|------------------------------------------|
| **DSL**         | Copper phone lines | 1–100 Mbps          | Medium   | Speed degrades with distance from CO     |
| **Cable**       | Coaxial cable      | 10–1000 Mbps        | Medium   | Shared bandwidth with neighbors          |
| **Fiber**       | Fiber optic        | 100 Mbps–10 Gbps    | Low      | Fastest and most reliable                |
| **Satellite**   | Radio waves        | 10–300 Mbps         | High     | Available in remote areas; high latency  |
| **Cellular**    | Radio waves (4G/5G)| 10 Mbps–1+ Gbps     | Variable | Mobile connectivity; 5G approaches fiber |
| **Fixed Wireless** | Radio waves     | 10–1000 Mbps        | Medium   | Point-to-point or point-to-multipoint    |

The choice of connection type depends on availability, budget, required speed, and acceptable latency. Fiber optic is generally the best option where available, while satellite and cellular serve areas where wired infrastructure is impractical.
