# LAN and WAN

## LAN (Local Area Network)

A LAN is a network of devices connected within a small geographic area, such as a home, office, or school building. Devices in a LAN are typically linked via **switches** and **access points** using Ethernet cables or Wi-Fi.

```text
                    [Wireless Access Point]
                     /        |        \
               [Laptop]  [Phone]   [Tablet]
                          
 [PC 1]---[Switch]---[PC 2]
              |
           [PC 3]
              |
         [Printer]
```

When PC 1 sends data to PC 3, the data is broken into **packets** and sent to the switch. The switch inspects each packet's destination MAC address and forwards it only to the correct port where PC 3 is connected.

Key characteristics of a LAN:
- **Small geographic area** (single building or campus)
- **High speed** (typically 1 Gbps to 10 Gbps)
- **Low latency** (sub-millisecond)
- **Privately owned** and managed by a single organization
- Uses Ethernet (IEEE 802.3) and Wi-Fi (IEEE 802.11)

## WAN (Wide Area Network)

A WAN connects LANs that are geographically separated — across cities, countries, or continents. WANs use leased lines, MPLS circuits, VPN tunnels, or the public internet to link distant networks together.

```text
  Office A (LAN)                              Office B (LAN)
 ┌─────────────┐                             ┌─────────────┐
 │ [PC] [PC]   │                             │ [PC] [PC]   │
 │   [Switch]  │                             │   [Switch]  │
 │   [Router]  │                             │   [Router]  │
 └──────┬──────┘                             └──────┬──────┘
        │                                           │
        └───────── [ WAN Link / Internet ] ─────────┘
```

The key distinction between a WAN and the internet is **privacy**. A WAN is typically a private network connecting specific locations, whereas the internet is a public network open to everyone. Traffic on a WAN stays within the organization's control, while internet traffic passes through shared public infrastructure.

Key characteristics of a WAN:
- **Large geographic area** (cities, countries, continents)
- **Lower speed** than LAN (depends on link type)
- **Higher latency** due to distance
- May use third-party infrastructure (ISP circuits, MPLS, internet)

## LAN vs WAN Comparison

| Feature           | LAN                          | WAN                              |
|-------------------|------------------------------|----------------------------------|
| **Scope**         | Single building or campus    | Cities, countries, or global     |
| **Speed**         | 1–10 Gbps (or higher)       | 1 Mbps–10 Gbps (varies)         |
| **Latency**       | Sub-millisecond              | Milliseconds to hundreds of ms   |
| **Ownership**     | Privately owned              | Often uses third-party links     |
| **Cost**          | Low (own equipment)          | Higher (leased lines, services)  |
| **Security**      | More secure (local)          | Less secure (traverses internet) |
| **Key device**    | Switch                       | Router                           |
| **Example**       | Home or office network       | Corporate branch connections     |

## Other Network Types

| Type | Full Name                    | Scope                              | Example                        |
|------|------------------------------|-------------------------------------|-------------------------------|
| **PAN**  | Personal Area Network    | Within reach of a person (~10 m)   | Bluetooth headset to phone    |
| **MAN**  | Metropolitan Area Network| City or metro area                  | City-wide Wi-Fi, cable TV     |
| **SAN**  | Storage Area Network     | Data center                         | Fibre Channel storage fabric  |
| **CAN**  | Campus Area Network      | University or corporate campus      | Multiple buildings on campus  |

## Public vs Private WAN

### Private WAN

In a private WAN, an organization purchases a **dedicated line** (leased line or MPLS circuit) directly from an ISP. Traffic is isolated from the public internet, providing stronger security and guaranteed bandwidth. Private WANs are expensive, especially over long distances.

### Public WAN

A public WAN uses the **internet** as the transport medium. Traffic is encrypted using a VPN to create a secure tunnel over the shared public infrastructure. Public WANs are far more cost-effective but rely on the internet's best-effort delivery, which can introduce variable latency and packet loss.

Most organizations today use a combination: private links for critical connections and VPN over the internet for less sensitive traffic.

## VPN Tunneling

A VPN (Virtual Private Network) creates an encrypted tunnel over a public network, allowing two LANs (or a remote user and a LAN) to communicate privately. VPN tunneling encrypts data packets before they enter the public internet and decrypts them at the other end.

```text
  Office A (LAN)                                     Office B (LAN)
 ┌──────────────┐                                   ┌──────────────┐
 │  [PC] [PC]   │                                   │  [PC] [PC]   │
 │  [Switch]    │                                   │  [Switch]    │
 │  [Router/VPN]│                                   │  [Router/VPN]│
 └──────┬───────┘                                   └──────┬───────┘
        │                                                  │
        │  ╔══════════════════════════════════════════╗    │
        └──║  Encrypted VPN Tunnel over the Internet  ║────┘
           ╚══════════════════════════════════════════╝
```

Key points:
- Switches are used to build a LAN; routers are used to build a WAN.
- A LAN is inherently more secure than a WAN because its traffic never leaves the local network.
- VPNs add a layer of security to WANs but do not make them as secure as a truly private, isolated LAN.
- VPNs are also commonly used by individuals to access geo-restricted content or protect traffic on public Wi-Fi.
