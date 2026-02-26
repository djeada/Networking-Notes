
#### Q. What is the primary purpose of a VPN (Virtual Private Network)?

* [x] Creating an encrypted tunnel over a public network to protect data in transit
* [ ] Increasing the bandwidth of an internet connection
* [ ] Replacing the need for a firewall
* [ ] Assigning IP addresses to devices on a network

#### Q. Which VPN type connects two entire networks, such as a branch office to a headquarters?

* [x] Site-to-Site VPN
* [ ] Remote Access VPN
* [ ] SSL VPN
* [ ] Client-to-Client VPN

#### Q. Which modern VPN protocol is known for its minimal codebase, fast performance, and use of UDP?

* [x] WireGuard
* [ ] OpenVPN
* [ ] L2TP/IPsec
* [ ] PPTP

#### Q. What limitation should users understand about VPN technology?

* [x] A VPN does not protect against malware or phishing attacks
* [ ] A VPN encrypts data stored on the local hard drive
* [ ] A VPN prevents all forms of network surveillance
* [ ] A VPN increases download speeds in all situations

#### Q. What is a forward proxy server used for?

* [x] Acting as an intermediary that makes requests on behalf of clients, providing anonymity and content filtering
* [ ] Distributing incoming traffic across multiple backend servers
* [ ] Assigning IP addresses to network devices
* [ ] Encrypting DNS queries

#### Q. What is the main role of a reverse proxy?

* [x] Sitting in front of servers to distribute requests, terminate TLS, and protect backend infrastructure
* [ ] Hiding the identity of client users from destination servers
* [ ] Providing a direct encrypted tunnel between two networks
* [ ] Storing DNS records for faster resolution

#### Q. Which proxy protocol supports both TCP and UDP traffic and provides optional authentication?

* [x] SOCKS5
* [ ] HTTP proxy
* [ ] SOCKS4
* [ ] Transparent proxy

#### Q. How does a transparent proxy differ from other proxies?

* [x] It intercepts traffic without requiring any configuration on the client device
* [ ] It encrypts all data passing through it
* [ ] It only works with HTTPS traffic
* [ ] It requires special software installed on every client

#### Q. What is the primary purpose of a load balancer in a network?

* [x] Distributing incoming traffic across multiple servers to prevent overload and improve availability
* [ ] Encrypting all network traffic between servers
* [ ] Assigning IP addresses to new servers
* [ ] Monitoring servers for security threats

#### Q. Which load balancing algorithm routes each new request to the next server in sequential order?

* [x] Round Robin
* [ ] Least Connections
* [ ] IP Hash
* [ ] Least Response Time

#### Q. Which load balancing algorithm directs traffic to the server with the fewest active connections?

* [x] Least Connections
* [ ] Round Robin
* [ ] Weighted Round Robin
* [ ] Random

#### Q. What is the key difference between a Layer 4 and a Layer 7 load balancer?

* [x] Layer 4 routes based on IP addresses and ports, while Layer 7 can inspect application-level content like HTTP headers and URLs
* [ ] Layer 4 is slower because it inspects packet content
* [ ] Layer 7 only works with UDP traffic
* [ ] Layer 4 can only balance traffic between two servers

#### Q. What is the purpose of health checks performed by a load balancer?

* [x] Detecting unhealthy servers and stopping traffic from being routed to them
* [ ] Encrypting data before sending it to backend servers
* [ ] Assigning new IP addresses to failed servers
* [ ] Logging all requests for auditing purposes

#### Q. Which load balancing method ensures that requests from the same client IP are always directed to the same backend server?

* [x] IP Hash
* [ ] Round Robin
* [ ] Least Connections
* [ ] Least Response Time

#### Q. What is the first step in a systematic network troubleshooting methodology?

* [x] Identify and define the problem
* [ ] Implement the solution
* [ ] Test a theory of probable cause
* [ ] Document the findings

#### Q. Which command-line tool shows the path that packets take through the network to reach a destination, listing each hop along the way?

* [x] traceroute (or tracert on Windows)
* [ ] ping
* [ ] netstat
* [ ] nslookup

#### Q. What tool would you use to capture and analyze individual network packets on an interface?

* [x] tcpdump
* [ ] ping
* [ ] traceroute
* [ ] dig

#### Q. A user can access websites by IP address but not by domain name. Which troubleshooting tool should you use first?

* [x] dig or nslookup to test DNS resolution
* [ ] traceroute to check the network path
* [ ] tcpdump to capture all traffic
* [ ] netstat to list open ports

#### Q. What is the standard MTU (Maximum Transmission Unit) size for Ethernet networks?

* [x] 1500 bytes
* [ ] 1024 bytes
* [ ] 576 bytes
* [ ] 9000 bytes

#### Q. How does a VPN differ from a proxy in terms of traffic scope?

* [x] A VPN typically encrypts all system traffic, while a proxy handles traffic only for specific applications or protocols
* [ ] A proxy encrypts all traffic, while a VPN handles only web traffic
* [ ] A VPN and a proxy handle traffic in exactly the same way
* [ ] A proxy routes traffic at the network layer, while a VPN works at the application layer
