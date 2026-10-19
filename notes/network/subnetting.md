# Subnetting

**Subnetting** is the process of dividing a larger network into smaller, more manageable sub-networks (subnets). The examples below use IPv4. Subnets help organize addresses; separate VLANs or physical segments define broadcast domains, and routing/firewall rules control traffic between them.

**Why is subnetting needed?**

- In small home networks, a single subnet with up to 254 devices is usually sufficient.
- Businesses and offices have many more devices (PCs, printers, cameras, sensors) and need logical separation.
- A café, for example, can use separate subnets and VLANs for employee devices and public Wi-Fi, with firewall rules controlling traffic between them.

Subnetting provides:

- **Efficiency** — supports smaller broadcast domains when paired with separate Layer 2 segments.
- **Security** — supports isolation when paired with access controls.
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

- For a directly connected destination, the host normally resolves the destination's MAC address with ARP and sends the frame on that link.
- For other destinations, the host selects a route, often via the default gateway. A more specific route takes precedence over the default.

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
| /31           | 255.255.255.254   | 2               | 2*          | 2          |
| /32           | 255.255.255.255   | 1               | 1*          | 1          |

For ordinary IPv4 subnets through `/30`, usable hosts = `2^(32 - prefix length) - 2`. A `/31` point-to-point link uses both addresses as endpoints ([RFC 3021](https://www.rfc-editor.org/rfc/rfc3021.html)); a `/32` identifies one address, often used in a host route or on a loopback interface. Neither uses a directed broadcast address. These counts do not include cloud-provider reservations.

---

## Network Address, Host Address, and Broadcast Address

An ordinary IPv4 subnet through `/30` reserves the **network address** (first) and the **broadcast address** (last). The addresses between them are available for interfaces, including the gateway. For a `/24`, using one address for the gateway leaves at most 253 for other devices. The `/31` and `/32` cases are exceptions, as described above.

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
| Addresses per Subnet| 256 | 128 | **64**  | 32  | 16  | 8   | 4   | 2   | 1   |
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

For the parent network `10.0.0.0/8`:

| Purpose | Subnet | Usable Hosts | Address Range (Including Network and Broadcast) |
|---------|--------|-------------:|-------------------------------------------------|
| Large office | `10.0.0.0/24` | 254 | 10.0.0.0–10.0.0.255 |
| Small lab | `10.0.1.0/27` | 30 | 10.0.1.0–10.0.1.31 |
| Point-to-point link | `10.0.1.32/30` | 2 | 10.0.1.32–10.0.1.35 |
| Server room | `10.0.1.48/28` | 14 | 10.0.1.48–10.0.1.63 |

Each subnet starts on a boundary matching its block size. A `/28` starts at a multiple of 16 in the final octet: `.36/28` would normalize to `.32/28` and overlap the point-to-point subnet. `.48/28` is the next aligned block; `.36`–`.47` remains unallocated.

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

- **Public subnets** have a route to an Internet Gateway. Direct IPv4 internet connectivity also requires a public IPv4 address and suitable security group and network ACL rules.
- **Private subnets** have no direct route to an Internet Gateway. A public NAT Gateway can provide outbound IPv4 internet access; it does not accept unsolicited inbound connections.
- Each subnet belongs to one availability zone. Deploying resources across subnets in different zones can improve fault tolerance.
- For ordinary AWS IPv4 subnet allocations, AWS reserves five addresses, so a `/28` has 11 assignable addresses. This differs from the generic IPv4 host-count table above.

**Question:**
If Kubernetes pods consume VPC subnet addresses and the subnet has only 10 free addresses, how can you add capacity?

**Answer:**
In AWS, an existing subnet's CIDR cannot be resized. Add a new, non-overlapping subnet in available VPC address space, or associate an additional VPC CIDR block and create subnets there. Then configure worker nodes and the CNI to use the new capacity, checking routes and access controls.

A new VPC is another option when isolation or address planning requires it, but it adds routing and connectivity work. Adding a VPC CIDR does not automatically enlarge existing subnets or move pods into new ones.

## Practice and References

- [Subnetting and NAT quiz](../../quizzes/subnetting_and_nat.md)
- [Subnet calculator](../../scripts/network/subnet_calculator.py) and [CIDR host explorer](../../scripts/network/cidr_to_hosts.py)
- [RFC 3021: IPv4 /31 point-to-point links](https://www.rfc-editor.org/rfc/rfc3021.html)
- [AWS subnet sizing](https://docs.aws.amazon.com/vpc/latest/userguide/subnet-sizing.html)
- [AWS CreateSubnet: CIDR restrictions](https://docs.aws.amazon.com/AWSEC2/latest/APIReference/API_CreateSubnet.html)
- [AWS: Add or remove a VPC CIDR block](https://docs.aws.amazon.com/vpc/latest/userguide/add-ipv4-cidr.html)
