# VPN (Virtual Private Network)

## Introduction

A Virtual Private Network (VPN) is a technology that creates a secure, encrypted connection over an untrusted network (typically the internet). VPNs allow devices on separate networks to communicate as if they were on the same private LAN, by establishing a dedicated encrypted path called a **tunnel**.

VPNs are used to:
- Connect remote workers to a corporate LAN
- Link branch offices together over the internet
- Protect privacy on public Wi-Fi
- Bypass geographic restrictions or censorship
- Access resources that are not exposed to the public internet

## How a VPN Works

```text
 [Remote User]                                    [Corporate Network]
  (Laptop)                                         ┌────────────────┐
      │                                            │ [File Server]  │
      │  ╔═══════════════════════════════════╗     │ [Database]     │
      └──║  Encrypted VPN Tunnel             ║─────│ [Intranet]     │
         ║  (over the public internet)       ║     └────────────────┘
         ╚═══════════════════════════════════╝
                        │
              [Public Internet]
              (untrusted network)
```

The VPN client on the remote device encrypts all traffic before sending it over the internet. The VPN server (or gateway) at the corporate network decrypts the traffic and forwards it to the internal network. Return traffic follows the reverse path.

## Types of VPN

### Site-to-Site VPN

Connects two entire networks (e.g., two office locations) through a persistent VPN tunnel between their routers or firewalls. All traffic between the sites flows through the tunnel automatically — individual users do not need VPN client software.

```text
  Office A (LAN)                                   Office B (LAN)
 ┌──────────────┐                                 ┌──────────────┐
 │ [PC] [PC]    │                                 │ [PC] [PC]    │
 │ [Switch]     │                                 │ [Switch]     │
 │ [VPN Router] │                                 │ [VPN Router] │
 └──────┬───────┘                                 └──────┬───────┘
        │                                                │
        │  ╔══════════════════════════════════════╗      │
        └──║  Site-to-Site VPN Tunnel             ║──────┘
           ╚══════════════════════════════════════╝
```

### Remote Access VPN

Allows individual users to connect to a remote network from any location. The user runs VPN client software that authenticates with the VPN server and establishes an encrypted tunnel.

```text
 [Remote Employee]                [VPN Server / Gateway]
  (VPN Client)                          │
      │                          [Corporate LAN]
      │  ╔═════════════════╗     ┌──────┴───────┐
      └──║  VPN Tunnel     ║─────│ [Servers]    │
         ╚═════════════════╝     │ [Printers]   │
              │                  │ [Intranet]   │
        [Public Internet]        └──────────────┘
```

## VPN Protocols

| Protocol          | Layer | Encryption         | Speed   | Security | Notes                                         |
|-------------------|-------|--------------------|---------|----------|-----------------------------------------------|
| **PPTP**          | 2     | MPPE (weak)        | Fast    | Low      | Easy to set up; considered insecure; port 1723 |
| **L2TP/IPsec**    | 2/3   | IPsec (AES)        | Medium  | High     | Double encapsulation; port 500/4500            |
| **OpenVPN**       | 3     | OpenSSL (AES-256)  | Medium  | High     | Open-source; highly configurable; TCP/UDP      |
| **WireGuard**     | 3     | ChaCha20, Curve25519| Fast   | High     | Modern, minimal codebase; UDP only             |
| **SSTP**          | 2     | SSL/TLS (AES)      | Medium  | High     | Microsoft; uses port 443; bypasses firewalls   |
| **IKEv2/IPsec**   | 3     | IPsec (AES)        | Fast    | High     | Good for mobile; handles network switching     |

## How VPN Tunneling Works

VPN tunneling wraps (encapsulates) the original data packet inside a new packet with an encrypted payload. The outer packet header contains the VPN endpoint addresses, while the original packet (with its private IP addresses) is hidden inside.

```text
 Original Packet:
 ┌────────────┬────────────┬──────────────────┐
 │ IP Header  │ TCP Header │    Payload       │
 │ Src: 10.0  │            │  (your data)     │
 │ Dst: 10.1  │            │                  │
 └────────────┴────────────┴──────────────────┘

 After VPN Encapsulation:
 ┌─────────────┬──────────┬──────────────────────────────────────┐
 │ New IP Hdr  │ VPN Hdr  │         Encrypted Payload            │
 │ Src: 203.0  │ (ESP /   │ ┌────────────┬──────────┬─────────┐ │
 │ Dst: 198.51 │  TLS)    │ │ IP Header  │TCP Header│ Payload │ │
 │ (public IPs)│          │ │ Src: 10.0  │          │ (data)  │ │
 │             │          │ │ Dst: 10.1  │          │         │ │
 │             │          │ └────────────┴──────────┴─────────┘ │
 └─────────────┴──────────┴──────────────────────────────────────┘
```

The outer IP header uses **public IP addresses** so the packet can be routed across the internet. The inner (original) packet uses **private IP addresses** and is invisible to anyone intercepting the traffic — they see only the encrypted blob.

## VPN Components

- **VPN Client** — Software (or hardware) on the user's device that initiates the VPN connection, handles authentication, and encrypts/decrypts traffic.
- **VPN Server** — Accepts incoming VPN connections, authenticates clients, and terminates the encrypted tunnel. Can be a dedicated appliance or software on a server.
- **VPN Gateway** — Sits at the edge of a network and facilitates communication between the VPN tunnel and the internal network.
- **Tunnel** — The encrypted logical connection between client and server through which all data flows.

## Benefits of VPN

- **Security** — Encrypts all data in transit, protecting against eavesdropping and man-in-the-middle attacks.
- **Remote access** — Employees can securely access corporate resources from anywhere in the world.
- **Privacy** — Masks the user's real IP address and encrypts traffic, making it difficult for ISPs or attackers to monitor activity.
- **Anonymity** — Journalists and activists use VPNs to protect their identity in regions where freedom of speech is restricted.
- **Bypass censorship** — Access blocked websites and services by routing traffic through a server in an unrestricted region.
- **Cost-effective** — Connecting remote offices via VPN over the internet is far cheaper than dedicated leased lines.

## Security Concerns and Limitations

- **Speed reduction** — Encryption and encapsulation add overhead, which can reduce throughput and increase latency.
- **Connection drops** — If the VPN connection drops, traffic may briefly travel unencrypted (mitigated by a "kill switch").
- **Data logging** — Some VPN providers log user activity, undermining the privacy benefits. Choose providers with a verified no-log policy.
- **Legal restrictions** — Some countries restrict or ban VPN usage entirely.
- **Not a complete security solution** — A VPN protects data in transit but does not protect against malware, phishing, or compromised endpoints.
- **End-to-end encryption** — Protocols like HTTPS already provide encryption between browser and server. A VPN adds an additional layer but is not a substitute for application-level security.

## VPN at Different OSI Layers

VPN technologies operate at various layers of the OSI model:

| OSI Layer               | VPN Technology           | Description                                                    |
|-------------------------|--------------------------|----------------------------------------------------------------|
| **Layer 2 (Data Link)** | PPTP, L2TP, SSTP         | Tunnels Layer 2 frames; can carry non-IP protocols             |
| **Layer 3 (Network)**   | IPsec, WireGuard, OpenVPN (tun) | Tunnels IP packets; most common VPN layer             |
| **Layer 4 (Transport)** | IPsec transport mode     | Encrypts only the payload of IP packets, not the header        |
| **Layer 5 (Session)**   | SSL/TLS-based VPNs       | Manages secure sessions between endpoints                      |
| **Layer 7 (Application)** | VPN client apps        | User-facing software that wraps lower-layer VPN protocols      |

Most VPNs are associated with **Layer 3 (Network Layer)**, where they create virtual network interfaces and route encrypted IP packets across the internet.
