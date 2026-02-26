

### 1) Within the same subnet, IP addresses must be:

A) Unique
B) Allowed to repeat
C) Unique only for servers, not laptops
D) Unique only if using DHCP

**Answer:** A

---

### 2) Two separate VPCs (not connected) can both use `10.0.0.0/16`:

A) Never
B) Yes, because they are separate routing domains
C) Only if they are in the same region
D) Only if they use different subnets

**Answer:** B

---

### 3) Public IPv4 addresses must be unique:

A) Only inside a VPC
B) Only inside a subnet
C) Globally on the public internet
D) Only inside a container network

**Answer:** C

---

### 4) If two VPCs with overlapping CIDRs are peered, the main issue is:

A) Faster routing
B) Ambiguous routing / traffic can’t be directed correctly
C) Pods stop getting IPs but VMs work fine
D) Nothing—overlaps are recommended

**Answer:** B

---

### 5) A VM in a VPC subnet:

A) Automatically creates a new private IP universe
B) Gets an IP from the subnet it’s attached to
C) Has no IP until it runs Docker
D) Always gets a public IP

**Answer:** B

---

### 6) Typical Docker container IPs (bridge network) are:

A) Globally unique public IPs
B) Unique only within the Docker network on that host
C) The same as the host VM’s IP
D) Unique across the entire VPC automatically

**Answer:** B

---

### 7) In Kubernetes, pods consume **subnet/VPC IPs directly** when:

A) Using a CNI that assigns VPC/subnet IPs to pods
B) Using any Ingress controller
C) Using DNS
D) Using Helm charts

**Answer:** A

---

### 8) When a container (or pod) with a private IP accesses the internet, it usually goes through:

A) ARP
B) NAT (e.g., host NAT, NAT gateway, egress)
C) VLAN tagging
D) BGP peering to the ISP

**Answer:** B

---

### 9) Why is IPv4 “~4 billion” addresses?

A) ISPs reserve most addresses for themselves
B) IPv4 uses 32-bit addressing (2³²)
C) NAT reduces the number of addresses available
D) VPCs consume half of all IPs

**Answer:** B

---

### 10) “An ISP is like a huge private network and exposes only some public IPs to the internet” best matches:

A) CDN
B) Carrier-Grade NAT (CGNAT)
C) Layer 2 switching
D) ARP spoofing

**Answer:** B

### 1) You try to VPC-peer two VPCs that both use `10.0.0.0/16`. What happens most commonly?

A) Peering succeeds; routing automatically “figures it out”
B) Peering is blocked or routes can’t be added because CIDRs overlap
C) Only DNS breaks; routing still works
D) Only inbound traffic fails; outbound works

**Answer:** B

---

### 2) Suppose the platform *lets* you connect overlapping networks using some workaround. What is the core technical problem overlap creates?

A) Duplicate MAC addresses
B) Ambiguous routing: the same destination IP could exist in both networks
C) ARP stops working globally
D) TCP ports collide

**Answer:** B

---

### 3) You have two networks connected (VPN/peering/transit) and **both contain a host with IP `10.0.5.10`**. From one side, sending traffic to `10.0.5.10` will:

A) Always reach both hosts
B) Reach whichever route is more specific / preferred, making the other unreachable
C) Be load-balanced across both hosts
D) Reach neither host

**Answer:** B

---

### 4) Best fix when you must connect two networks with overlapping IP ranges (and can’t re-IP immediately) is usually:

A) Enable ARP proxying on all hosts
B) Use NAT between networks (e.g., map one side to a translated range)
C) Increase MTU
D) Turn off routing tables

**Answer:** B

---

### 5) On a single LAN, two machines are configured with the same IP `192.168.1.50`. Most likely symptom:

A) Everything works, but slower
B) Random/flapping connectivity because ARP tables keep changing
C) Only DNS breaks
D) Only HTTPS breaks

**Answer:** B

---

### 6) If two machines have the same IP but are in **different isolated LANs** (not connected), what happens?

A) The internet breaks
B) Nothing—no conflict because they’re separate routing domains
C) Both machines become unreachable
D) DHCP stops working everywhere

**Answer:** B

---

### 7) You run Docker on a VM. Docker’s default bridge uses `172.17.0.0/16`, but your company network/VPC also uses `172.17.0.0/16`. Likely issue:

A) Containers can’t talk to each other
B) Outbound internet stops for the VM entirely
C) Routing conflicts: VM may not reach real `172.17.x.x` addresses correctly (or vice versa)
D) Only Kubernetes breaks

**Answer:** C

---

### 8) Two different Docker hosts both use the default `172.17.0.0/16` for containers. Is that a problem by itself?

A) Yes, containers across hosts will collide automatically
B) No, not unless you try to route container networks between hosts without NAT/overlay
C) Yes, Docker refuses to start
D) Only if the hosts are in the same subnet

**Answer:** B

---

### 9) You publish a container port with `-p 80:80` on a host. You try to run a second container also with `-p 80:80`. What happens?

A) Both run and Docker load-balances
B) The second fails because host port 80 is already in use
C) Both run, but only HTTPS works
D) The second steals the port silently

**Answer:** B

---

### 10) In Kubernetes, why can pod IP overlap be worse than Docker overlap in some CNIs?

A) Pods don’t use IPs at all
B) Some CNIs assign real subnet/VPC IPs to pods, so overlap affects VPC routing directly
C) Kubernetes disables NAT always
D) Pods share MAC addresses across nodes

**Answer:** B

---

### 11) Your cluster uses a CNI where pods consume subnet IPs. You scale pods and suddenly new pods stay Pending with IP errors. Most likely bottleneck:

A) CPU limits
B) Subnet IP exhaustion
C) Disk I/O
D) DNS cache

**Answer:** B

---

### 12) You want two overlapping VPCs to communicate without re-IPing either side. Which approach is most realistic?

A) Turn on DHCP relay
B) Use NAT gateway/instance or dedicated NAT appliance between them
C) Increase the VPC’s CIDR size
D) Use IPv6 only on one side, no routing changes needed

**Answer:** B


1. What is the decimal (base 10) value of the binary (base 2) number "1001"?

    - 7
    - 8
    - 9
    - 10

2. Which subnet mask is typically associated with a Class B network?

    - 255.255.0.0
    - 255.0.0.0
    - 255.255.255.0
    - 255.255.255.255

3. How many octets define the network portion of a Class C IP address?

    - 1
    - 2
    - 3
    - 4

4. What is the decimal equivalent of the binary number "0110"?

    - 4
    - 5
    - 6
    - 7

5. In a Class A network, which part of the IP address identifies the network?

    - The first octet
    - The first two octets
    - The first three octets
    - The last octet

6. What is "1101" in binary when converted to decimal?

    - 13
    - 9
    - 5
    - 3

7. How many bits represent the host portion of a Class B IP address?

    - 8 bits
    - 16 bits
    - 24 bits
    - 32 bits

8. Which of the following is a valid Class C subnet mask?

    - 255.255.255.0
    - 255.255.0.0
    - 255.0.0.0
    - 239.255.255.255

9. What is the decimal value of the binary number "0011"?

    - 1
    - 2
    - 3
    - 4

10. How many octets identify the network portion of a Class A IP address?

    - 1
    - 2
    - 3
    - 4

11. Convert the binary number "1010" to its decimal representation.

    - 8
    - 9
    - 10
    - 11

12. Which subnet mask is most commonly used with a Class C network?

    - 255.255.255.0
    - 255.255.0.0
    - 255.0.0.0
    - 239.255.255.255

13. What does CIDR notation represent and how is it written?

    - A method of specifying IP addresses and their associated network prefix length, written as an address followed by a slash and a number (e.g., 192.168.1.0/24)
    - A way to encrypt IP packets using a cryptographic key
    - A protocol for assigning IP addresses dynamically to hosts
    - A DNS record type used for reverse lookups

14. Which of the following ranges is reserved for private IPv4 addresses?

    - 10.0.0.0 to 10.255.255.255
    - 8.8.0.0 to 8.8.255.255
    - 200.0.0.0 to 200.255.255.255
    - 169.254.0.0 to 169.254.0.255

15. What is the purpose of the loopback address 127.0.0.1?

    - It allows a device to send network traffic to itself for testing and diagnostics
    - It serves as the default gateway for all local networks
    - It is used to broadcast messages to every host on the network
    - It identifies the DNS server assigned to the device

16. How many usable host addresses are available in a /24 (255.255.255.0) network?

    - 254
    - 255
    - 256
    - 252

17. What is the decimal equivalent of the binary number "1111"?

    - 13
    - 14
    - 15
    - 16
