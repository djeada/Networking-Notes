
#### Q. What does the term "lease" mean in the context of DHCP?

* [x] The duration for which an IP address is allocated to a device
* [ ] The time needed for DNS to look up a domain name
* [ ] The interval required for completing a data transfer
* [ ] The validity period of a registered domain name

#### Q. Which type of DNS record maps a domain name directly to an IP address?

* [x] A record
* [ ] CNAME record
* [ ] MX record
* [ ] TXT record

#### Q. What function does a DNS resolver perform?

* [x] It translates domain names into their corresponding IP addresses
* [ ] It hands out IP addresses to network devices
* [ ] It controls and routes network traffic
* [ ] It prevents access to harmful websites

#### Q. What is the purpose of a PTR record in DNS?

* [x] To resolve an IP address back to a domain name
* [ ] To specify the mail server for a domain
* [ ] To alias one domain name to another
* [ ] To hold supplementary information about the domain

#### Q. What is the main role of DNS?

* [ ] Blocking access to certain websites or services
* [ ] Encrypting data sent across the Internet
* [x] Converting domain names into IP addresses
* [ ] Routing email traffic between mail servers

#### Q. Which DNS record type identifies the mail server that handles email for a given domain?

* [x] MX record
* [ ] PTR record
* [ ] A record
* [ ] CNAME record

#### Q. What does the abbreviation DHCP represent?

* [x] Dynamic Host Configuration Protocol
* [ ] Domain Host Control Protocol
* [ ] Dynamic Hypertext Configuration Process
* [ ] Data Handling Control Protocol

#### Q. What occurs once a DHCP lease reaches its expiration?

* [x] The IP address is released back into the available pool for reassignment
* [ ] The device permanently loses network connectivity
* [ ] The DNS server removes the corresponding entry
* [ ] The IP address becomes permanently bound to the device

#### Q. What is the primary purpose of DHCP on a network?

* [x] Automatically distributing IP addresses to connected devices
* [ ] Resolving domain names to IP addresses
* [ ] Blocking malicious or unwanted websites
* [ ] Directing data traffic between separate networks

#### Q. What advantage does DHCP provide for network administration?

* [x] It streamlines the management of IP address assignments
* [ ] It boosts the throughput of network traffic
* [ ] It encrypts all data transmissions on the network
* [ ] It prevents unauthorized devices from joining the network

#### Q. Which transport protocol does DNS mainly rely on for name resolution queries?

* [x] UDP
* [ ] TCP
* [ ] HTTP
* [ ] ICMP

#### Q. Which of the following best describes a core capability of DHCP?

* [x] Automated allocation of IP addresses to hosts
* [ ] Requiring administrators to manually enter IP addresses
* [ ] Providing encryption for network communications
* [ ] Converting domain names into IP addresses

#### Q. What is the DORA process in DHCP?

* [x] The four-step exchange (Discover, Offer, Request, Acknowledge) used to assign an IP address
* [ ] A method for encrypting DHCP messages
* [ ] A DNS delegation technique for subdomains
* [ ] A process for renewing expired SSL certificates

#### Q. What is DNS cache poisoning?

* [x] An attack that inserts forged DNS records into a resolver's cache to redirect traffic
* [ ] A method of clearing outdated entries from the DNS cache
* [ ] A technique for speeding up DNS resolution by pre-loading entries
* [ ] A firewall rule that blocks DNS traffic from untrusted sources

#### Q. What role does a DHCP relay agent serve?

* [x] It forwards DHCP requests from clients to a DHCP server located on a different subnet
* [ ] It caches DHCP leases to speed up address assignment
* [ ] It converts DHCP messages into DNS queries
* [ ] It encrypts communication between DHCP clients and servers

#### Q. Two devices on the network share the same IP address, causing intermittent connectivity problems. What is a likely explanation?

* [x] A DHCP server malfunction or a conflict with a manually configured static IP address
* [ ] A misconfiguration on the DNS server
* [ ] An incorrect subnet mask setting
* [ ] Outdated firmware on the network router

#### Q. A user can reach a website by entering its IP address but not by typing the domain name. What is the most probable issue?

* [x] The DNS server is failing to resolve the domain name properly
* [ ] The DHCP server has stopped running
* [ ] The user's assigned IP address is incorrect
* [ ] A firewall rule is blocking access to the website

#### Q. A network device obtains an IP address in the 169.254.x.x range. What does this signify?

* [x] The device could not reach a DHCP server and assigned itself a link-local address
* [ ] The DNS server is experiencing a malfunction
* [ ] The device has been connected to an incorrect network segment
* [ ] A static IP address has been manually configured on the device

#### Q. A client machine fails to obtain an IP address automatically. What should you investigate first on the DHCP server?

* [x] Verify that the DHCP service is active and running
* [ ] Manually configure an IP address on the client
* [ ] Restart the DNS server
* [ ] Power-cycle the client device

#### Q. Several clients are receiving duplicate IP addresses from the DHCP server. What is the first thing you should examine?

* [x] Confirm that the DHCP scope does not contain overlapping address ranges
* [ ] Restart the DNS service
* [ ] Extend the DHCP lease duration
* [ ] Enable DNS scavenging

#### Q. You need to guarantee that a particular device always gets the same IP address from DHCP. How would you set this up?

* [x] Create a DHCP reservation tied to the device's MAC address
* [ ] Assign a static IP address directly on the device
* [ ] Extend the lease duration on the DHCP server
* [ ] Add a CNAME record in DNS for the device

#### Q. You want to assign an IP address to a client for only 24 hours. What DHCP setting should you adjust?

* [x] Configure a lease time of 24 hours for that address
* [ ] Set up a static IP address on the client device
* [ ] Place the client in a separate DHCP scope
* [ ] Modify the DNS server configuration

#### Q. When setting up a new device, what details would a DHCP server typically provide?

* [x] An IP address, subnet mask, default gateway, and DNS server address
* [ ] Only a domain name
* [ ] A permanent static IP address
* [ ] A list of allowed websites

#### Q. You need to associate a domain name with an IP address and also enable reverse lookups. Which pair of DNS records should you create?

* [x] A record and PTR record
* [ ] MX record and CNAME record
* [ ] NS record and SOA record
* [ ] TXT record and SRV record

#### Q. After adding a new DNS entry, users report that the domain name takes a long time to resolve. What is a plausible explanation?

* [x] DNS propagation has not yet completed across all name servers
* [ ] The DNS server itself is offline
* [ ] The DHCP lease time is configured too short
* [ ] The DHCP address pool has been exhausted

#### Q. Your organization recently registered a new domain, but employees on the internal network cannot access it. What DNS change is most likely needed?

* [x] Create an A record for the new domain on the internal DNS server
* [ ] Increase the DHCP lease time
* [ ] Reconfigure the subnet mask on network devices
* [ ] Restart the DHCP server

#### Q. You are setting up DNS for a new web server. Which record type would you use to link the server's hostname to its IP address?

* [x] A record
* [ ] MX record
* [ ] SRV record
* [ ] CNAME record

#### Q. A branch office has no local DHCP server, yet devices there need IP addresses from the central server. What should you deploy?

* [x] A DHCP relay agent on the branch office network
* [ ] A secondary DNS server at the branch
* [ ] A static route to the central DHCP server
* [ ] A VPN tunnel exclusively for DHCP traffic

#### Q. Users report being redirected to a fraudulent website when they visit a well-known domain. What DNS-related attack might be occurring?

* [x] DNS cache poisoning, where forged records redirect users to malicious sites
* [ ] A DHCP scope exhaustion attack
* [ ] A brute-force attack against the DNS server
* [ ] An ARP spoofing attack on the local network

#### Q. Which RFC defines the private IPv4 address ranges used in home and office networks?

* [x] RFC 1918
* [ ] RFC 2131
* [ ] RFC 791
* [ ] RFC 1027

#### Q. Which of the following is a valid RFC 1918 private IPv4 address range?

* [x] 172.16.0.0 – 172.31.255.255
* [ ] 172.0.0.0 – 172.15.255.255
* [ ] 192.0.0.0 – 192.167.255.255
* [ ] 10.0.0.0 – 10.127.255.255

#### Q. When a device joins a typical home Wi-Fi network, what entity defines the private subnet the device joins?

* [x] The router
* [ ] The connecting device itself
* [ ] The ISP's DHCP server
* [ ] The Wi-Fi access point firmware

#### Q. In a home network using the 192.168.1.0/24 subnet, how many usable host addresses are available for client devices?

* [x] 254
* [ ] 256
* [ ] 255
* [ ] 252

#### Q. A home router commonly performs which combination of roles simultaneously?

* [x] Wireless access point, DHCP server, default gateway, and NAT gateway
* [ ] DNS server, firewall, DHCP relay agent, and proxy server
* [ ] DHCP client, web server, VPN server, and switch
* [ ] Wireless access point, DNS resolver, load balancer, and DHCP relay agent

#### Q. During the DHCP DORA process, what source IP address does a Wi-Fi client use in its initial Discover message?

* [x] 0.0.0.0
* [ ] 255.255.255.255
* [ ] 127.0.0.1
* [ ] The client's previously assigned IP address

#### Q. What information does a home router's DHCP lease table record to track address assignments?

* [x] The assigned IP address, the client's MAC address, and the lease expiry time
* [ ] The client's hostname, assigned IP, and DNS server address
* [ ] The client's public IP, port number, and protocol type
* [ ] The client's MAC address and the time the device was manufactured

#### Q. DHCP prevents most duplicate IP address assignments. Under what common scenario can a duplicate address conflict still occur on a home network?

* [x] When a device is manually configured with a static IP address that falls within the DHCP pool
* [ ] When two devices request the same hostname from the DNS server
* [ ] When the DHCP lease time expires simultaneously on two devices
* [ ] When the router's firmware is out of date

#### Q. What mechanism do operating systems typically use to detect a duplicate IP address conflict on the local network?

* [x] ARP — a host sends a gratuitous ARP or ARP probe and detects a conflict if another device replies
* [ ] DHCP — the DHCP server queries all clients before issuing each new lease
* [ ] DNS — reverse DNS lookups identify conflicting records
* [ ] ICMP — a ping to the address reveals whether it is already in use

#### Q. Why can millions of home networks reuse the same private IP address ranges (e.g., 192.168.1.x) without conflict on the internet?

* [x] NAT translates private addresses to the network's unique public IP before traffic leaves the router
* [ ] Private addresses are automatically reassigned by the ISP to avoid duplication
* [ ] IPv6 tunnelling converts duplicate private addresses into unique global addresses
* [ ] RFC 1918 addresses are blocked by all internet routers and never appear in transit
