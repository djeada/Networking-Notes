
#### Q. Within the same subnet, IP addresses must be:

* [x] Unique
* [ ] Allowed to repeat
* [ ] Unique only for servers, not laptops
* [ ] Unique only if using DHCP

#### Q. Two separate VPCs (not connected) can both use `10.0.0.0/16`:

* [ ] Never
* [x] Yes, because they are separate routing domains
* [ ] Only if they are in the same region
* [ ] Only if they use different subnets

#### Q. Public IPv4 addresses must be unique:

* [ ] Only inside a VPC
* [ ] Only inside a subnet
* [x] Globally on the public internet
* [ ] Only inside a container network

#### Q. If two VPCs with overlapping CIDRs are peered, the main issue is:

* [ ] Faster routing
* [x] Ambiguous routing / traffic can't be directed correctly
* [ ] Pods stop getting IPs but VMs work fine
* [ ] Nothing—overlaps are recommended

#### Q. A VM in a VPC subnet:

* [ ] Automatically creates a new private IP universe
* [x] Gets an IP from the subnet it's attached to
* [ ] Has no IP until it runs Docker
* [ ] Always gets a public IP

#### Q. Typical Docker container IPs (bridge network) are:

* [ ] Globally unique public IPs
* [x] Unique only within the Docker network on that host
* [ ] The same as the host VM's IP
* [ ] Unique across the entire VPC automatically

#### Q. In Kubernetes, pods consume subnet/VPC IPs directly when:

* [x] Using a CNI that assigns VPC/subnet IPs to pods
* [ ] Using any Ingress controller
* [ ] Using DNS
* [ ] Using Helm charts

#### Q. When a container (or pod) with a private IP accesses the internet, it usually goes through:

* [ ] ARP
* [x] NAT (e.g., host NAT, NAT gateway, egress)
* [ ] VLAN tagging
* [ ] BGP peering to the ISP

#### Q. Why is IPv4 "~4 billion" addresses?

* [ ] ISPs reserve most addresses for themselves
* [x] IPv4 uses 32-bit addressing (2³²)
* [ ] NAT reduces the number of addresses available
* [ ] VPCs consume half of all IPs

#### Q. "An ISP is like a huge private network and exposes only some public IPs to the internet" best matches:

* [ ] CDN
* [x] Carrier-Grade NAT (CGNAT)
* [ ] Layer 2 switching
* [ ] ARP spoofing

#### Q. You try to VPC-peer two VPCs that both use `10.0.0.0/16`. What happens most commonly?

* [ ] Peering succeeds; routing automatically "figures it out"
* [x] Peering is blocked or routes can't be added because CIDRs overlap
* [ ] Only DNS breaks; routing still works
* [ ] Only inbound traffic fails; outbound works

#### Q. Suppose the platform lets you connect overlapping networks using some workaround. What is the core technical problem overlap creates?

* [ ] Duplicate MAC addresses
* [x] Ambiguous routing: the same destination IP could exist in both networks
* [ ] ARP stops working globally
* [ ] TCP ports collide

#### Q. You have two networks connected (VPN/peering/transit) and both contain a host with IP `10.0.5.10`. From one side, sending traffic to `10.0.5.10` will:

* [ ] Always reach both hosts
* [x] Reach whichever route is more specific / preferred, making the other unreachable
* [ ] Be load-balanced across both hosts
* [ ] Reach neither host

#### Q. Best fix when you must connect two networks with overlapping IP ranges (and can't re-IP immediately) is usually:

* [ ] Enable ARP proxying on all hosts
* [x] Use NAT between networks (e.g., map one side to a translated range)
* [ ] Increase MTU
* [ ] Turn off routing tables

#### Q. On a single LAN, two machines are configured with the same IP `192.168.1.50`. Most likely symptom:

* [ ] Everything works, but slower
* [x] Random/flapping connectivity because ARP tables keep changing
* [ ] Only DNS breaks
* [ ] Only HTTPS breaks

#### Q. If two machines have the same IP but are in different isolated LANs (not connected), what happens?

* [ ] The internet breaks
* [x] Nothing—no conflict because they're separate routing domains
* [ ] Both machines become unreachable
* [ ] DHCP stops working everywhere

#### Q. You run Docker on a VM. Docker's default bridge uses `172.17.0.0/16`, but your company network/VPC also uses `172.17.0.0/16`. Likely issue:

* [ ] Containers can't talk to each other
* [ ] Outbound internet stops for the VM entirely
* [x] Routing conflicts: VM may not reach real `172.17.x.x` addresses correctly (or vice versa)
* [ ] Only Kubernetes breaks

#### Q. Two different Docker hosts both use the default `172.17.0.0/16` for containers. Is that a problem by itself?

* [ ] Yes, containers across hosts will collide automatically
* [x] No, not unless you try to route container networks between hosts without NAT/overlay
* [ ] Yes, Docker refuses to start
* [ ] Only if the hosts are in the same subnet

#### Q. You publish a container port with `-p 80:80` on a host. You try to run a second container also with `-p 80:80`. What happens?

* [ ] Both run and Docker load-balances
* [x] The second fails because host port 80 is already in use
* [ ] Both run, but only HTTPS works
* [ ] The second steals the port silently

#### Q. In Kubernetes, why can pod IP overlap be worse than Docker overlap in some CNIs?

* [ ] Pods don't use IPs at all
* [x] Some CNIs assign real subnet/VPC IPs to pods, so overlap affects VPC routing directly
* [ ] Kubernetes disables NAT always
* [ ] Pods share MAC addresses across nodes

#### Q. Your cluster uses a CNI where pods consume subnet IPs. You scale pods and suddenly new pods stay Pending with IP errors. Most likely bottleneck:

* [ ] CPU limits
* [x] Subnet IP exhaustion
* [ ] Disk I/O
* [ ] DNS cache

#### Q. You want two overlapping VPCs to communicate without re-IPing either side. Which approach is most realistic?

* [ ] Turn on DHCP relay
* [x] Use NAT gateway/instance or dedicated NAT appliance between them
* [ ] Increase the VPC's CIDR size
* [ ] Use IPv6 only on one side, no routing changes needed

#### Q. What is the decimal (base 10) value of the binary (base 2) number "1001"?

* [ ] 7
* [ ] 8
* [x] 9
* [ ] 10

#### Q. Which subnet mask is typically associated with a Class B network?

* [x] 255.255.0.0
* [ ] 255.0.0.0
* [ ] 255.255.255.0
* [ ] 255.255.255.255

#### Q. How many octets define the network portion of a Class C IP address?

* [ ] 1
* [ ] 2
* [x] 3
* [ ] 4

#### Q. What is the decimal equivalent of the binary number "0110"?

* [ ] 4
* [ ] 5
* [x] 6
* [ ] 7

#### Q. In a Class A network, which part of the IP address identifies the network?

* [x] The first octet
* [ ] The first two octets
* [ ] The first three octets
* [ ] The last octet

#### Q. What is "1101" in binary when converted to decimal?

* [x] 13
* [ ] 9
* [ ] 5
* [ ] 3

#### Q. How many bits represent the host portion of a Class B IP address?

* [ ] 8 bits
* [x] 16 bits
* [ ] 24 bits
* [ ] 32 bits

#### Q. Which of the following is a valid Class C subnet mask?

* [x] 255.255.255.0
* [ ] 255.255.0.0
* [ ] 255.0.0.0
* [ ] 239.255.255.255

#### Q. What is the decimal value of the binary number "0011"?

* [ ] 1
* [ ] 2
* [x] 3
* [ ] 4

#### Q. How many octets identify the network portion of a Class A IP address?

* [x] 1
* [ ] 2
* [ ] 3
* [ ] 4

#### Q. Convert the binary number "1010" to its decimal representation.

* [ ] 8
* [ ] 9
* [x] 10
* [ ] 11

#### Q. Which subnet mask is most commonly used with a Class C network?

* [x] 255.255.255.0
* [ ] 255.255.0.0
* [ ] 255.0.0.0
* [ ] 239.255.255.255

#### Q. What does CIDR notation represent and how is it written?

* [x] A method of specifying IP addresses and their associated network prefix length, written as an address followed by a slash and a number (e.g., 192.168.1.0/24)
* [ ] A way to encrypt IP packets using a cryptographic key
* [ ] A protocol for assigning IP addresses dynamically to hosts
* [ ] A DNS record type used for reverse lookups

#### Q. Which of the following ranges is reserved for private IPv4 addresses?

* [x] 10.0.0.0 to 10.255.255.255
* [ ] 8.8.0.0 to 8.8.255.255
* [ ] 200.0.0.0 to 200.255.255.255
* [ ] 169.254.0.0 to 169.254.0.255

#### Q. What is the purpose of the loopback address 127.0.0.1?

* [x] It allows a device to send network traffic to itself for testing and diagnostics
* [ ] It serves as the default gateway for all local networks
* [ ] It is used to broadcast messages to every host on the network
* [ ] It identifies the DNS server assigned to the device

#### Q. How many usable host addresses are available in a /24 (255.255.255.0) network?

* [x] 254
* [ ] 255
* [ ] 256
* [ ] 252

#### Q. What is the decimal equivalent of the binary number "1111"?

* [ ] 13
* [ ] 14
* [x] 15
* [ ] 16
