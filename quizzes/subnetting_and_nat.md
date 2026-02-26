
#### Q. What is the primary purpose of subnetting a network?

* [x] Dividing a large network into smaller, more manageable sub-networks
* [ ] Encrypting data as it travels between networks
* [ ] Assigning domain names to IP addresses
* [ ] Increasing the speed of individual network connections

#### Q. How many usable host addresses are available in a /24 subnet?

* [x] 254
* [ ] 256
* [ ] 255
* [ ] 252

#### Q. Why are two addresses in every subnet reserved and cannot be assigned to hosts?

* [x] One is the network address and the other is the broadcast address
* [ ] They are reserved for the default gateway and the DNS server
* [ ] They are used for multicast traffic
* [ ] They are required by the DHCP server

#### Q. What operation is performed between an IP address and a subnet mask to determine the network address?

* [x] Bitwise AND
* [ ] Bitwise OR
* [ ] Bitwise XOR
* [ ] Addition

#### Q. In CIDR notation, what does /26 indicate?

* [x] The first 26 bits of the address represent the network portion
* [ ] The subnet contains 26 usable hosts
* [ ] The address belongs to Class C
* [ ] There are 26 subnets in the network

#### Q. How many usable host addresses does a /30 subnet provide?

* [x] 2
* [ ] 4
* [ ] 6
* [ ] 0

#### Q. What is the main advantage of VLSM (Variable Length Subnet Masking)?

* [x] Different subnets can use different mask sizes to allocate addresses more efficiently
* [ ] It allows the use of IPv6 addresses on an IPv4 network
* [ ] It encrypts all traffic between subnets
* [ ] It eliminates the need for a default gateway

#### Q. What is the primary purpose of NAT (Network Address Translation)?

* [x] Translating private IP addresses to public IP addresses for internet access
* [ ] Resolving domain names to IP addresses
* [ ] Assigning IP addresses to devices on a network
* [ ] Encrypting data between two networks

#### Q. Which type of NAT allows many internal devices to share a single public IP address by using different port numbers?

* [x] PAT (Port Address Translation) / NAT Overload
* [ ] Static NAT
* [ ] Dynamic NAT
* [ ] Bi-directional NAT

#### Q. What does a Static NAT mapping provide?

* [x] A permanent one-to-one mapping between a private IP and a public IP
* [ ] A temporary IP address from a shared pool
* [ ] A random public IP assigned to each session
* [ ] A single public IP shared by all internal devices

#### Q. What key problem does NAT help solve in IPv4 networking?

* [x] The exhaustion of available public IPv4 addresses
* [ ] The slow speed of DNS resolution
* [ ] The lack of encryption in network communication
* [ ] The inability to use wireless connections

#### Q. What is the purpose of port forwarding on a router?

* [x] Redirecting incoming traffic on a specific public port to a specific internal device and port
* [ ] Blocking all incoming traffic on a specific port
* [ ] Automatically assigning port numbers to internal devices
* [ ] Encrypting traffic on a specific port

#### Q. When configuring port forwarding, what information must be specified?

* [x] The external port, internal IP address, internal port, and protocol (TCP or UDP)
* [ ] Only the external port number
* [ ] The MAC address of the target device and the VLAN ID
* [ ] The domain name and DNS server address

#### Q. Why is it recommended to assign a static IP address or DHCP reservation to a device that uses port forwarding?

* [x] So the forwarding rule always points to the correct internal device even if it restarts
* [ ] Static IPs provide faster network speeds
* [ ] Port forwarding only works with static IP addresses at the ISP level
* [ ] DHCP reservations encrypt the forwarded traffic

#### Q. What technique allows peer-to-peer applications like WebRTC to establish connections through NAT devices?

* [x] STUN, TURN, and ICE protocols
* [ ] DNS round-robin
* [ ] ARP spoofing
* [ ] DHCP relay agents

#### Q. How does Dynamic NAT differ from Static NAT?

* [x] Dynamic NAT assigns public IPs from a pool on a first-come, first-served basis rather than using a fixed mapping
* [ ] Dynamic NAT does not require a router
* [ ] Dynamic NAT encrypts all translated traffic
* [ ] Dynamic NAT maps multiple private IPs to a single public IP using port numbers

#### Q. What security benefit does NAT provide to an internal network?

* [x] It hides the internal IP addresses from external networks
* [ ] It encrypts all traffic leaving the network
* [ ] It prevents malware from being downloaded
* [ ] It blocks all inbound connections automatically

#### Q. A /25 subnet mask divides a /24 network into how many equally sized subnets?

* [x] 2
* [ ] 4
* [ ] 8
* [ ] 1

#### Q. What is the total number of IP addresses (including network and broadcast) in a /26 subnet?

* [x] 64
* [ ] 62
* [ ] 32
* [ ] 128

#### Q. What type of link commonly uses a /30 subnet because only two host addresses are needed?

* [x] A point-to-point link between two routers
* [ ] A large office LAN
* [ ] A wireless access point network
* [ ] A data center server farm
