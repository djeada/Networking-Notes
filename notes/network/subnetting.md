# Subnetting

**Subnetting** is the process of dividing a larger network into smaller, more manageable sub-networks (subnets). It is essential for efficient IP address allocation, improved security through network isolation, and better network performance by reducing broadcast domains.

**Why is subnetting needed?**

- In small home networks, a single subnet with up to 254 devices is usually sufficient.
- Businesses and offices have many more devices (PCs, printers, cameras, sensors) and need logical separation.
- A café, for example, benefits from two subnets: one for employees and point-of-sale devices, and another for public Wi-Fi — keeping them isolated while sharing an internet connection.

Subnetting provides:

- **Efficiency** — reduces unnecessary broadcast traffic.
- **Security** — isolates sensitive network segments.
- **Full control** — enables granular IP address management.

---

## Subnet Masks and the AND Operation

A **subnet mask** determines which part of a 32-bit IP address identifies the network and which part identifies the host. The network address is found by performing a **bitwise AND** between the IP address and the subnet mask.

```text
  IP Address:    192.168.1.100
                 11000000.10101000.00000001.01100100

  Subnet Mask:   255.255.255.0   (/24)
                 11111111.11111111.11111111.00000000

  AND operation: -----------------------------------
  Network Addr:  11000000.10101000.00000001.00000000
                 192.168.1.0

  |<--- Network Portion --->|<--- Host Portion --->|
  |      (first 24 bits)    |    (last 8 bits)     |
```

- If the destination IP is on the **same subnet**, the packet is delivered directly within the subnet.
- If the destination IP is on a **different subnet**, the packet is forwarded to the default gateway.

---

## CIDR Notation

**CIDR (Classless Inter-Domain Routing)** notation uses a slash followed by the number of network bits, replacing the older classful addressing system.

| CIDR Notation | Subnet Mask       | Total Addresses | Usable Hosts | Block Size |
|---------------|-------------------|-----------------|-------------|------------|
| /24           | 255.255.255.0     | 256             | 254         | 256        |
| /25           | 255.255.255.128   | 128             | 126         | 128        |
| /26           | 255.255.255.192   | 64              | 62          | 64         |
| /27           | 255.255.255.224   | 32              | 30          | 32         |
| /28           | 255.255.255.240   | 16              | 14          | 16         |
| /29           | 255.255.255.248   | 8               | 6           | 8          |
| /30           | 255.255.255.252   | 4               | 2           | 4          |
| /31           | 255.255.255.254   | 2               | 0*          | 2          |
| /32           | 255.255.255.255   | 1               | 0*          | 1          |

*`/31` is used for point-to-point links (RFC 3021). `/32` identifies a single host.*

---

## Network Address, Host Address, and Broadcast Address

Every subnet reserves two addresses: the **network address** (first) and the **broadcast address** (last). All addresses in between are available for hosts.

```text
  Subnet: 192.168.1.0/24

  |  Network Addr  |       Usable Host Range        | Broadcast Addr |
  +----------------+--------------------------------+----------------+
  |  192.168.1.0   | 192.168.1.1  ...  192.168.1.254| 192.168.1.255  |
  +----------------+--------------------------------+----------------+
        ^                    ^                              ^
   Cannot assign       Assign to devices            Cannot assign
   to a host           (254 usable hosts)           to a host
```

| Type             | Purpose                                                              | Example         |
|------------------|----------------------------------------------------------------------|-----------------|
| **Network Address**  | Identifies the start of the network; used in routing tables.     | 192.168.1.0     |
| **Host Address**     | Assigned to individual devices on the subnet.                    | 192.168.1.100   |
| **Default Gateway**  | A device (usually the router) that forwards traffic to other networks. Typically uses the first or last usable address. | 192.168.1.1 or 192.168.1.254 |
| **Broadcast Address**| Used to send data to all hosts on the subnet.                    | 192.168.1.255   |

---

## Step-by-Step Subnetting Guide

**Problem**: You are given the network `192.168.4.0/24` and need to create **3 subnetworks** (office, front desk, storage). Each subnet needs a network ID, subnet mask, host ID range, usable host count, and broadcast ID.

**Step 1**: Determine the number of subnets needed and find the next power of 2.

| Subnets         | 1   | 2   | **4**   | 8   | 16  | 32  | 64  | 128 | 256 |
|-----------------|-----|-----|---------|-----|-----|-----|-----|-----|-----|
| Hosts per Subnet| 256 | 128 | **64**  | 32  | 16  | 8   | 4   | 2   | 1   |
| Subnet Mask     | /24 | /25 | **/26** | /27 | /28 | /29 | /30 | /31 | /32 |

We need 3 subnets. The next power of 2 is **4**, giving us a **/26** mask with **64 addresses** per subnet.

**Step 2**: Calculate each subnet's addressing.

| Network ID      | Subnet Mask | Host ID Range                     | Usable Hosts  | Broadcast ID    |
|-----------------|-------------|-----------------------------------|---------------|-----------------|
| 192.168.4.0     | /26         | 192.168.4.1 - 192.168.4.62       | 64 - 2 = 62   | 192.168.4.63    |
| 192.168.4.64    | /26         | 192.168.4.65 - 192.168.4.126     | 64 - 2 = 62   | 192.168.4.127   |
| 192.168.4.128   | /26         | 192.168.4.129 - 192.168.4.190    | 64 - 2 = 62   | 192.168.4.191   |
| 192.168.4.192   | /26         | 192.168.4.193 - 192.168.4.254    | 64 - 2 = 62   | 192.168.4.255   |

**Step 3**: Assign subnets to purposes (the 4th subnet is a spare).

### Verification Example

Are two hosts on the same subnet?

- **Address A**: 192.168.10.32, Mask: 255.255.255.0
- **Address B**: 192.168.10.67, Mask: 255.255.255.0

Both resolve to network address **192.168.10.0** — they are on the **same network**. Broadcast address: 192.168.10.255. Usable hosts: 254.

---

## Variable Length Subnet Masking (VLSM)

**VLSM** allows subnets of different sizes within the same network, instead of using one uniform subnet mask. This avoids wasting IP addresses when different segments need different numbers of hosts.

```text
  Network: 10.0.0.0/8

  Subnet A (large office):   10.0.0.0/24    --> 254 hosts
  Subnet B (small lab):      10.0.1.0/27    -->  30 hosts
  Subnet C (point-to-point): 10.0.1.32/30   -->   2 hosts
  Subnet D (server room):    10.0.1.36/28   -->  14 hosts
```

With VLSM, each subnet is sized to match its actual need, conserving address space.

---

## Subnetting in the Cloud: AWS VPC Example

```text
+---------------------------------------------------------------+
|                           AWS VPC                             |
|                                                               |
|  +-------------------+          +-------------------+         |
|  |   Subnet 0        |          |   Subnet 1        |         |
|  |   (Public)        |          |   (Private)       |         |
|  |  [Web Server]     |          |  [Application]    |         |
|  |  [Load Balancer]  |          |  [Service 2]      |         |
|  +--------+----------+          +---------+---------+         |
|           |                               |                   |
|           |                               |                   |
|           v                               v                   |
|  +--------+----------+          +---------+---------+         |
|  |   Subnet 2        |          |   Subnet 3        |         |
|  |   (Private)       |          |   (Public)        |         |
|  |  [Database]       |          |  [Cache Server]   |         |
|  |                   |          |                   |         |
|  +-------------------+          +-------------------+         |
|                                                               |
|  [Internet Gateway] <-------> Subnet 0 & Subnet 3            |
|  [NAT Gateway]      <-------> Subnet 1 & Subnet 2            |
+---------------------------------------------------------------+
```

- **Public subnets** have routes to the Internet Gateway for inbound/outbound internet traffic.
- **Private subnets** use a NAT Gateway for outbound-only internet access.
- Subnets in different availability zones provide fault tolerance.
