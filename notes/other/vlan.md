# VLAN (Virtual Local Area Network)

## Introduction

A VLAN (Virtual Local Area Network) is a logical grouping of devices on one or more switches that can communicate as if they were on the same physical LAN, regardless of their physical location. VLANs allow a single physical switch to be partitioned into multiple isolated broadcast domains.

Without VLANs, every device connected to a switch is in the same broadcast domain — a broadcast sent by one device reaches every other device on that switch. VLANs solve this by creating separate broadcast domains, so traffic from one VLAN cannot reach devices in another VLAN without passing through a router.

## Why Use VLANs?

- **Security** — Isolate sensitive departments (e.g., finance) from general traffic.
- **Performance** — Reduce broadcast traffic by limiting the broadcast domain size.
- **Management** — Group devices logically (by department, function, or project) rather than by physical location.
- **Flexibility** — Move users between VLANs without changing physical cabling.

## VLAN Segmentation

In the example below, a single physical switch carries two VLANs. The Sales and Accounting departments can both access the internet through the router, but they cannot communicate directly with each other at Layer 2.

```text
                        [Router]
                           │
                      [Switch Port 1]
                      (Trunk Port)
                           │
 ┌─────────────────────────┼──────────────────────────┐
 │                      [Switch]                       │
 │                                                     │
 │   VLAN 10 (Sales)           VLAN 20 (Accounting)    │
 │  ┌──────────────┐          ┌──────────────┐         │
 │  │ [PC1] [PC2]  │          │ [PC3] [PC4]  │         │
 │  │ [PC5]        │          │ [PC6]        │         │
 │  └──────────────┘          └──────────────┘         │
 │                                                     │
 │  Ports 2-5: Access         Ports 6-9: Access        │
 │  VLAN 10                   VLAN 20                  │
 └─────────────────────────────────────────────────────┘
```

PC1, PC2, and PC5 (VLAN 10) can communicate with each other freely. PC3, PC4, and PC6 (VLAN 20) can communicate with each other freely. But VLAN 10 devices **cannot** reach VLAN 20 devices without going through the router (inter-VLAN routing).

## Types of VLANs

| VLAN Type        | Purpose                                                                 |
|------------------|-------------------------------------------------------------------------|
| **Data VLAN**    | Carries regular user-generated traffic (the most common type)           |
| **Voice VLAN**   | Dedicated to VoIP traffic; ensures QoS for voice calls                  |
| **Management VLAN** | Used for switch/router management traffic (SSH, SNMP, web GUI)      |
| **Native VLAN**  | The default VLAN for untagged traffic on a trunk port (default: VLAN 1) |
| **Default VLAN** | VLAN 1 on most switches; all ports belong to it initially               |

## VLAN Tagging (802.1Q)

When a frame needs to travel between switches (or between a switch and a router) over a **trunk link**, the switch inserts a 4-byte **802.1Q tag** into the Ethernet frame header. This tag identifies which VLAN the frame belongs to.

```text
 Standard Ethernet Frame:
 ┌──────────┬──────────┬──────┬─────────┬─────┐
 │ Dst MAC  │ Src MAC  │ Type │ Payload │ FCS │
 └──────────┴──────────┴──────┴─────────┴─────┘

 802.1Q Tagged Frame:
 ┌──────────┬──────────┬────────────┬──────┬─────────┬─────┐
 │ Dst MAC  │ Src MAC  │ 802.1Q Tag │ Type │ Payload │ FCS │
 └──────────┴──────────┴────────────┴──────┴─────────┴─────┘
                        │          │
                        ▼          ▼
                  ┌──────────────────┐
                  │ TPID   │ TCI    │
                  │ 0x8100 │        │
                  │        │ PCP    │ (3 bits - priority)
                  │        │ DEI    │ (1 bit  - drop eligible)
                  │        │ VID    │ (12 bits - VLAN ID: 0-4095)
                  └──────────────────┘
```

- **TPID (Tag Protocol Identifier)**: Set to `0x8100` to indicate an 802.1Q-tagged frame.
- **VID (VLAN Identifier)**: 12-bit field that identifies the VLAN (0–4095; usable range is 1–4094).
- **PCP (Priority Code Point)**: 3-bit field for QoS prioritization.

## Trunk Ports vs Access Ports

| Feature          | Access Port                              | Trunk Port                                |
|------------------|------------------------------------------|-------------------------------------------|
| **VLANs**        | Belongs to a single VLAN                 | Carries traffic for multiple VLANs        |
| **Tagging**      | Frames are untagged                      | Frames are tagged with 802.1Q             |
| **Connected to** | End devices (PCs, printers, phones)      | Other switches, routers, or servers       |
| **Native VLAN**  | N/A                                      | Untagged frames assigned to native VLAN   |

```text
 [PC] ──── Access Port (VLAN 10) ──── [Switch A]
                                           │
                                      Trunk Port
                                     (carries VLAN 10,
                                      VLAN 20, VLAN 30)
                                           │
                                      Trunk Port
                                           │
 [PC] ──── Access Port (VLAN 20) ──── [Switch B]
```

## Inter-VLAN Routing

Since VLANs are separate broadcast domains, a **Layer 3 device** (router or Layer 3 switch) is required for traffic to flow between VLANs. There are two common approaches:

### Router-on-a-Stick

A single router interface is connected to the switch via a trunk link. The router creates **sub-interfaces**, each assigned to a different VLAN. Frames arrive tagged, the router routes between sub-interfaces, and sends them back tagged for the destination VLAN.

```text
                    [Router]
                  eth0.10 (10.0.10.1) ── VLAN 10 gateway
                  eth0.20 (10.0.20.1) ── VLAN 20 gateway
                      │ (trunk link)
                   [Switch]
                  /         \
        [VLAN 10 PCs]    [VLAN 20 PCs]
        10.0.10.x        10.0.20.x
```

### Layer 3 Switch (SVI)

A Layer 3 switch can route between VLANs internally using **Switched Virtual Interfaces (SVIs)** — virtual interfaces assigned to each VLAN. This eliminates the need for an external router and provides faster inter-VLAN routing.

```text
           [Layer 3 Switch]
          SVI VLAN 10: 10.0.10.1
          SVI VLAN 20: 10.0.20.1
          (internal routing engine)
                /         \
      [VLAN 10 PCs]    [VLAN 20 PCs]
      10.0.10.x        10.0.20.x
```

## VLAN Configuration Examples

### Cisco IOS

```text
! Create VLANs
Switch(config)# vlan 10
Switch(config-vlan)# name Sales
Switch(config)# vlan 20
Switch(config-vlan)# name Accounting

! Assign access port to VLAN
Switch(config)# interface FastEthernet0/1
Switch(config-if)# switchport mode access
Switch(config-if)# switchport access vlan 10

! Configure trunk port
Switch(config)# interface GigabitEthernet0/1
Switch(config-if)# switchport mode trunk
Switch(config-if)# switchport trunk allowed vlan 10,20

! Verify
Switch# show vlan brief
Switch# show interfaces trunk
```

### Linux (using `ip` command)

```bash
# Create VLAN sub-interface on eth0
ip link add link eth0 name eth0.10 type vlan id 10
ip addr add 10.0.10.1/24 dev eth0.10
ip link set eth0.10 up

ip link add link eth0 name eth0.20 type vlan id 20
ip addr add 10.0.20.1/24 dev eth0.20
ip link set eth0.20 up
```

## Benefits of VLANs

- **Security** — Sensitive traffic (e.g., management, finance) is isolated from general user traffic. An attacker who compromises a device on one VLAN cannot directly access devices on another VLAN.
- **Reduced broadcast traffic** — Broadcasts are confined to the VLAN, reducing unnecessary traffic on the overall network.
- **Simplified management** — Devices can be grouped logically without rewiring. Moving a user to a different department is a port configuration change, not a physical move.
- **Improved performance** — Smaller broadcast domains mean less overhead on each device and more available bandwidth for actual data.
- **Regulatory compliance** — VLANs help meet requirements that mandate network segmentation (e.g., PCI DSS for payment card data).

## VLAN Best Practices

1. **Change the native VLAN** — Do not use VLAN 1 as the native VLAN on trunk ports. Assign an unused VLAN as the native VLAN to prevent VLAN hopping attacks.
2. **Disable unused ports** — Shut down switch ports that are not in use and assign them to a "parking lot" VLAN.
3. **Use dedicated management VLAN** — Do not manage switches over the default VLAN. Use a separate management VLAN with restricted access.
4. **Prune VLANs on trunks** — Only allow necessary VLANs on trunk links. Do not carry all VLANs everywhere.
5. **Document VLAN assignments** — Maintain a record of which VLANs exist, their purpose, IP subnets, and port assignments.
6. **Use voice VLANs for VoIP** — Separate voice traffic from data traffic to ensure quality of service.
7. **Implement private VLANs** — For additional isolation within a VLAN (e.g., preventing communication between hosts in the same VLAN).
