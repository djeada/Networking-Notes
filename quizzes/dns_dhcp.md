
1. **What does the term "lease" mean in the context of DHCP?**
   - The duration for which an IP address is allocated to a device
   - The time needed for DNS to look up a domain name
   - The interval required for completing a data transfer
   - The validity period of a registered domain name

2. **Which type of DNS record maps a domain name directly to an IP address?**
   - A record
   - CNAME record
   - MX record
   - TXT record

3. **What function does a DNS resolver perform?**
   - It translates domain names into their corresponding IP addresses
   - It hands out IP addresses to network devices
   - It controls and routes network traffic
   - It prevents access to harmful websites

4. **What is the purpose of a PTR record in DNS?**
   - To resolve an IP address back to a domain name
   - To specify the mail server for a domain
   - To alias one domain name to another
   - To hold supplementary information about the domain

5. **What is the main role of DNS?**
   - Blocking access to certain websites or services
   - Encrypting data sent across the Internet
   - Converting domain names into IP addresses
   - Routing email traffic between mail servers

6. **Which DNS record type identifies the mail server that handles email for a given domain?**
   - MX record
   - PTR record
   - A record
   - CNAME record

7. **What does the abbreviation DHCP represent?**
   - Dynamic Host Configuration Protocol
   - Domain Host Control Protocol
   - Dynamic Hypertext Configuration Process
   - Data Handling Control Protocol

8. **What occurs once a DHCP lease reaches its expiration?**
   - The IP address is released back into the available pool for reassignment
   - The device permanently loses network connectivity
   - The DNS server removes the corresponding entry
   - The IP address becomes permanently bound to the device

9. **What is the primary purpose of DHCP on a network?**
   - Automatically distributing IP addresses to connected devices
   - Resolving domain names to IP addresses
   - Blocking malicious or unwanted websites
   - Directing data traffic between separate networks

10. **What advantage does DHCP provide for network administration?**
    - It streamlines the management of IP address assignments
    - It boosts the throughput of network traffic
    - It encrypts all data transmissions on the network
    - It prevents unauthorized devices from joining the network

11. **Which transport protocol does DNS mainly rely on for name resolution queries?**
    - UDP
    - TCP
    - HTTP
    - ICMP

12. **Which of the following best describes a core capability of DHCP?**
    - Automated allocation of IP addresses to hosts
    - Requiring administrators to manually enter IP addresses
    - Providing encryption for network communications
    - Converting domain names into IP addresses

13. **What is the DORA process in DHCP?**
    - The four-step exchange (Discover, Offer, Request, Acknowledge) used to assign an IP address
    - A method for encrypting DHCP messages
    - A DNS delegation technique for subdomains
    - A process for renewing expired SSL certificates

14. **What is DNS cache poisoning?**
    - An attack that inserts forged DNS records into a resolver's cache to redirect traffic
    - A method of clearing outdated entries from the DNS cache
    - A technique for speeding up DNS resolution by pre-loading entries
    - A firewall rule that blocks DNS traffic from untrusted sources

15. **What role does a DHCP relay agent serve?**
    - It forwards DHCP requests from clients to a DHCP server located on a different subnet
    - It caches DHCP leases to speed up address assignment
    - It converts DHCP messages into DNS queries
    - It encrypts communication between DHCP clients and servers


1. **Two devices on the network share the same IP address, causing intermittent connectivity problems. What is a likely explanation?**
   - A DHCP server malfunction or a conflict with a manually configured static IP address
   - A misconfiguration on the DNS server
   - An incorrect subnet mask setting
   - Outdated firmware on the network router

2. **A user can reach a website by entering its IP address but not by typing the domain name. What is the most probable issue?**
   - The DNS server is failing to resolve the domain name properly
   - The DHCP server has stopped running
   - The user's assigned IP address is incorrect
   - A firewall rule is blocking access to the website

3. **A network device obtains an IP address in the 169.254.x.x range. What does this signify?**
    - The device could not reach a DHCP server and assigned itself a link-local address
    - The DNS server is experiencing a malfunction
    - The device has been connected to an incorrect network segment
    - A static IP address has been manually configured on the device

4. **A client machine fails to obtain an IP address automatically. What should you investigate first on the DHCP server?**
   - Verify that the DHCP service is active and running
   - Manually configure an IP address on the client
   - Restart the DNS server
   - Power-cycle the client device

5. **Several clients are receiving duplicate IP addresses from the DHCP server. What is the first thing you should examine?**
    - Confirm that the DHCP scope does not contain overlapping address ranges
    - Restart the DNS service
    - Extend the DHCP lease duration
    - Enable DNS scavenging

6. **You need to guarantee that a particular device always gets the same IP address from DHCP. How would you set this up?**
   - Create a DHCP reservation tied to the device's MAC address
   - Assign a static IP address directly on the device
   - Extend the lease duration on the DHCP server
   - Add a CNAME record in DNS for the device

7. **You want to assign an IP address to a client for only 24 hours. What DHCP setting should you adjust?**
   - Configure a lease time of 24 hours for that address
   - Set up a static IP address on the client device
   - Place the client in a separate DHCP scope
   - Modify the DNS server configuration

8. **When setting up a new device, what details would a DHCP server typically provide?**
   - An IP address, subnet mask, default gateway, and DNS server address
   - Only a domain name
   - A permanent static IP address
   - A list of allowed websites

9. **You need to associate a domain name with an IP address and also enable reverse lookups. Which pair of DNS records should you create?**
   - A record and PTR record
   - MX record and CNAME record
   - NS record and SOA record
   - TXT record and SRV record

10. **After adding a new DNS entry, users report that the domain name takes a long time to resolve. What is a plausible explanation?**
    - DNS propagation has not yet completed across all name servers
    - The DNS server itself is offline
    - The DHCP lease time is configured too short
    - The DHCP address pool has been exhausted

11. **Your organization recently registered a new domain, but employees on the internal network cannot access it. What DNS change is most likely needed?**
    - Create an A record for the new domain on the internal DNS server
    - Increase the DHCP lease time
    - Reconfigure the subnet mask on network devices
    - Restart the DHCP server

12. **You are setting up DNS for a new web server. Which record type would you use to link the server's hostname to its IP address?**
    - A record
    - MX record
    - SRV record
    - CNAME record

13. **A branch office has no local DHCP server, yet devices there need IP addresses from the central server. What should you deploy?**
    - A DHCP relay agent on the branch office network
    - A secondary DNS server at the branch
    - A static route to the central DHCP server
    - A VPN tunnel exclusively for DHCP traffic

14. **Users report being redirected to a fraudulent website when they visit a well-known domain. What DNS-related attack might be occurring?**
    - DNS cache poisoning, where forged records redirect users to malicious sites
    - A DHCP scope exhaustion attack
    - A brute-force attack against the DNS server
    - An ARP spoofing attack on the local network
