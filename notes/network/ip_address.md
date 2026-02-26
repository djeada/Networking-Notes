# IP Addresses

An **IP address** (Internet Protocol address) is a unique numerical identifier assigned to every device connected to a network. IP addresses enable packets to find their route across the internet and are fundamental to how networked devices communicate.

- An IP address is not unique to a user or computer, but to a **Network Interface Card (NIC)**.
- A device can have multiple NICs and thus multiple IP addresses.
- IP addresses have a **hierarchical structure** and are network-specific.
- Some IP ranges are owned by organizations (e.g., Google owns 104.196.0.0-104.199.255.255).
- [XKCD map](https://xkcd.com/195/) provides a visual of IP ownership.

---

## IPv4

**IPv4** uses 32-bit addresses, allowing for 2^32 (approximately 4.3 billion) unique addresses. Addresses are written in **dotted-decimal notation**, where each of the four octets is a decimal number from 0 to 255.

```text
IPv4 Address: 192.168.1.100

 Octet 1      Octet 2      Octet 3      Octet 4
+----------+ +----------+ +----------+ +----------+
| 11000000 | | 10101000 | | 00000001 | | 01100100 |
+----------+ +----------+ +----------+ +----------+
    192          168           1            100

<-------- 32 bits (4 bytes) total -------->
```

### IPv4 Address Classes

IPv4 addresses are divided into five classes based on the leading bits of the first octet:

| Class | First Octet Range | Network Bits | Host Bits | Default Subnet Mask | Purpose                     |
|-------|-------------------|-------------|-----------|---------------------|-----------------------------|
| A     | 1 - 126           | 8           | 24        | 255.0.0.0           | Large networks              |
| B     | 128 - 191         | 16          | 16        | 255.255.0.0         | Medium networks             |
| C     | 192 - 223         | 24          | 8         | 255.255.255.0       | Small networks              |
| D     | 224 - 239         | N/A         | N/A       | N/A                 | Multicast                   |
| E     | 240 - 255         | N/A         | N/A       | N/A                 | Experimental / Reserved     |

- **Class A**: Each network gets up to 16,777,214 hosts.
- **Class C**: Most common class on the internet for smaller organizations.
- **Class D and E**: Not used for standard host addressing (multicast and experimental).

### Private vs Public IP Addresses

Certain IP ranges are reserved for **private** use within local networks and are not routable on the public internet. A router with NAT translates private addresses to a public address for internet access.

| Class | Private IP Range                  | CIDR Notation    |
|-------|-----------------------------------|------------------|
| A     | 10.0.0.0 - 10.255.255.255        | 10.0.0.0/8       |
| B     | 172.16.0.0 - 172.31.255.255      | 172.16.0.0/12    |
| C     | 192.168.0.0 - 192.168.255.255    | 192.168.0.0/16   |

```text
           Private Network                         Public Internet
  +-------------------------------+          +------------------------+
  |  Device A: 192.168.1.10      |          |                        |
  |  Device B: 192.168.1.11      +--[ Router/NAT ]--+ Public IP:     |
  |  Device C: 192.168.1.12      |   translates to  | 203.0.113.5    |
  +-------------------------------+   public IP      +------------------------+
         (Private IPs)                                  (Public IP)
```

---

## IPv6

**IPv6** uses 128-bit addresses, providing a vastly larger address space (2^128 addresses) to solve IPv4 exhaustion. Addresses are written as eight groups of four hexadecimal digits separated by colons.

```text
IPv6 Address: 2001:0db8:85a3:0000:0000:8a2e:0370:7334

  Group 1  Group 2  Group 3  Group 4  Group 5  Group 6  Group 7  Group 8
 +------+ +------+ +------+ +------+ +------+ +------+ +------+ +------+
 | 2001 | | 0db8 | | 85a3 | | 0000 | | 0000 | | 8a2e | | 0370 | | 7334 |
 +------+ +------+ +------+ +------+ +------+ +------+ +------+ +------+
 <16 bits each>

 <---------------------- 128 bits total -------------------------------->
```

- Leading zeros in a group can be omitted: `2001:db8:85a3::8a2e:370:7334`
- Consecutive groups of all zeros can be replaced with `::` (only once per address).
- IPv6 eliminates the need for NAT due to the vast address space.

---

## DHCP (Dynamic Host Configuration Protocol)

**DHCP** automatically assigns IP addresses to devices on a network, ensuring addresses are reused as devices connect and disconnect. The process follows the **DORA** sequence:

```text
     Client                          DHCP Server
       |                                  |
       |  1. DISCOVER (broadcast)         |
       |  "Any DHCP servers out there?"   |
       |--------------------------------->|
       |                                  |
       |  2. OFFER                        |
       |  "Here is 192.168.1.50"          |
       |<---------------------------------|
       |                                  |
       |  3. REQUEST                      |
       |  "I'd like 192.168.1.50 please"  |
       |--------------------------------->|
       |                                  |
       |  4. ACKNOWLEDGE                  |
       |  "192.168.1.50 is yours"         |
       |<---------------------------------|
       |                                  |
```

- **Discover**: Client broadcasts a request for an IP address.
- **Offer**: Server responds with an available IP address.
- **Request**: Client formally requests the offered IP.
- **Acknowledge**: Server confirms the assignment with a lease duration.

IP addresses assigned by DHCP are temporary. Switching networks (e.g., home Wi-Fi to a public network) results in a new IP address being assigned.

---

## MAC Address vs IP Address

| Feature         | MAC Address                          | IP Address                            |
|-----------------|--------------------------------------|---------------------------------------|
| **Layer**       | Data Link (Layer 2)                  | Network (Layer 3)                     |
| **Format**      | 48-bit, hex (e.g., `AA:BB:CC:DD:EE:FF`) | 32-bit IPv4 or 128-bit IPv6      |
| **Scope**       | Local network only                   | Global (routable across networks)     |
| **Assignment**  | Burned into NIC by manufacturer      | Assigned by network (DHCP or static)  |
| **Persistence** | Generally permanent (but spoofable)  | Changes with network connection       |
| **Visibility**  | Only visible on local LAN segment    | Visible to remote servers             |

- MAC addresses typically do not extend beyond the local network; web servers see IP and port, not MAC address.
- MAC addresses can be spoofed or randomly generated (e.g., by smartphones for privacy).

---

## Static vs Dynamic IP Addresses

| Feature          | Static IP                           | Dynamic IP                            |
|------------------|-------------------------------------|---------------------------------------|
| **Assignment**   | Manually configured                 | Automatically assigned via DHCP       |
| **Persistence**  | Does not change                     | May change on reconnection            |
| **Use Cases**    | Servers, printers, network devices  | End-user devices (laptops, phones)    |
| **Management**   | Requires manual tracking            | Managed automatically by DHCP server  |
| **Cost**         | Often costs more from ISPs          | Included with standard service        |

---

## Limitations of IP Addresses as Identifiers

- IP addresses are **not** unique identifiers for users or computers—they identify a device's connection to a network.
- IP-based identification can break if the address changes (e.g., rebooting, switching networks).
- A device can connect to multiple networks simultaneously with different IPs.
- For reliable device identification, hardware identifiers like CPU serial numbers are more appropriate, though MAC addresses can be overwritten and IP packets can be rerouted.

IP addresses are only required to be **unique within the network where they’re used for routing**. The trick is that there are *multiple layers of networks*, and layers can **reuse the same IP ranges** because of routing boundaries and NAT.

### Where IPs must be unique (and where they can repeat)

* **Within a subnet (LAN / VPC subnet):**
  Every interface in the same subnet must have a **unique IP**. If two machines in the same subnet had the same IP, traffic would break (ARP/neighbor discovery conflicts).

* **Within a VPC:**
  In most clouds, an IP should be **unique across the whole VPC**, because the VPC routes traffic between subnets. (Some platforms support advanced overlaps in special cases, but generally: assume unique in the VPC.)

* **Across different VPCs / different private networks:**
  IPs **can repeat**. You can have `10.0.0.0/16` in many different VPCs because they’re separate routing domains.
  The problem appears only when you want them to talk to each other (peering/VPN), because overlapping ranges make routing ambiguous.

* **Inside a VM:**
  A VM is just a machine on a network. Its NIC gets an IP from the subnet. It does **not** automatically get a “new universe” of IPs unless it *creates one* (like running Docker with its own bridge network).

* **Docker containers:**
  Commonly, Docker creates its own private network (e.g., `172.17.0.0/16`). Container IPs are unique **inside that Docker network** but can repeat elsewhere.
  Containers usually reach the outside world via **NAT through the host VM’s IP**.

* **Kubernetes pods:** (depends on CNI design)

  * In many clusters, each **pod gets an IP** from a **pod CIDR** that is routable inside the cluster/VPC. Pod IPs must be unique **within the cluster**.
  * If you’re using a CNI where pods use **VPC/subnet IPs directly** (like AWS VPC CNI style), then pods consume subnet IPs and uniqueness rules become the **same as the subnet/VPC**. That’s when you hit “only 10 IPs” fast.

### Where internet connectivity happens (public vs private IPv4)

* **Public IPv4 addresses must be globally unique** on the internet. That’s where the “~4 billion” limit comes from (IPv4 is 32-bit).
* Most devices today use **private IPs** (RFC1918 ranges like `10.x`, `172.16-31.x`, `192.168.x`) which **can repeat everywhere** because they are not routed on the public internet.
* To access the internet, private IP traffic is translated using **NAT**:

  * At home: your router NATs many devices to **one public IP**
  * In cloud: your instances/pods often go through a **NAT Gateway** or egress device that uses one/few public IPs

### Is an ISP like a “big VPC” that exposes only a few IPs?

Conceptually, yes:

* ISPs often give customers **private IPs** and then use **Carrier-Grade NAT (CGNAT)** so thousands of customers share a smaller pool of public IPv4 addresses.
* The ISP’s internal network can reuse private ranges and route internally, but only the ISP’s **public IP pool** is visible to the global internet.

### Quick rules of thumb

* **Must be unique:** within the same routed network domain (subnet/VPC/cluster depending on design).
* **Can repeat safely:** across isolated networks (different VPCs, different LANs, inside Docker networks), until you try to connect them.
* **Internet needs public IPs:** but most endpoints don’t get one—NAT lets many private IPs share one public IP.
