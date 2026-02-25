

1. **Which scenario could cause a stateful firewall to inadvertently block legitimate traffic?**
   - When the traffic does not correspond to any existing session in the connection state table
   - When the traffic is encrypted using TLS
   - When both the source and destination ports happen to be the same
   - When the traffic uses a non-standard port number

2. **What best describes the function of an IDS within a network?**
   - A system that observes network traffic for unusual activity and raises alerts
   - A system that actively stops malicious traffic using predefined rules
   - A firewall responsible for filtering both inbound and outbound traffic
   - A device that encrypts traffic flowing between network segments

3. **What is the core distinction between a stateful firewall and a stateless firewall?**
   - A stateful firewall monitors the state of active connections and uses that context to make filtering decisions
   - A stateless firewall filters traffic based solely on fixed rules with no awareness of connection state
   - A stateful firewall only examines packet headers, whereas a stateless firewall inspects full packet contents
   - A stateless firewall offers greater security than a stateful firewall

4. **An IDS flags certain traffic as suspicious, but upon closer review the traffic turns out to be harmless. What is this called?**
   - A false positive
   - A false negative
   - A true positive
   - A true negative

5. **How does an IPS differ from antivirus software in terms of where and how it operates?**
   - An IPS inspects and blocks network traffic in real time, while antivirus software scans and removes malicious files on individual devices
   - An IPS only identifies known threats, while antivirus software can detect both known and unknown threats
   - An IPS runs on endpoints, while antivirus software operates on network traffic
   - An IPS and antivirus software perform identical functions in different environments

6. **What type of firewall is best suited for filtering traffic based on specific applications rather than just addresses and ports?**
   - Application-layer firewall
   - Packet-filtering firewall
   - Stateless firewall
   - Circuit-level gateway

7. **What action does an IPS take upon identifying a potential threat in network traffic?**
   - It notifies the administrator and blocks the suspicious traffic immediately
   - It records the event and sends a notification without blocking any traffic
   - It diverts the traffic to a honeypot for further analysis
   - It passes the traffic to an IDS for additional inspection

8. **What best describes a hybrid IDS/IPS system?**
    - A system capable of both detecting and preventing threats, depending on its configuration
    - A system that switches between detection and prevention modes based on traffic volume
    - A system that needs separate IDS and IPS hardware to operate
    - A system focused exclusively on host-based threat detection

9. **What key benefit does a stateful firewall have over a stateless one?**
   - It can factor in the history of a traffic flow when enforcing security policies, enabling more dynamic rules
   - It processes packets faster because it only inspects headers
   - It consumes less processing power and memory
   - It automatically drops all traffic by default

10. **What is the primary role of an IPS when compared with a traditional firewall?**
    - An IPS can block threats in real time through deep packet inspection, while a firewall mainly filters traffic by IP addresses and ports
    - An IPS is used solely for monitoring, while a firewall actively blocks threats
    - An IPS handles encrypted traffic more efficiently than a firewall
    - An IPS eliminates the need for a firewall on a secure network

11. **Where in the network should an IDS be placed to achieve the greatest visibility?**
    - Directly behind the firewall
    - Between the router and the internal network
    - On every individual host in the network
    - At the network perimeter, before the firewall

12. **What is a potential drawback of configuring an IPS with overly aggressive rules?**
    - It may mistakenly block legitimate traffic, causing network disruptions
    - It demands constant manual updates to its detection signatures
    - It might fail to generate alerts for traffic it has blocked
    - It becomes unable to operate in real time

13. **What is a DMZ (demilitarized zone) in network security?**
    - A network segment that sits between the internal network and the Internet, hosting public-facing services
    - A firewall rule that blocks all inbound traffic by default
    - A type of IDS that monitors traffic at every network node
    - An encrypted tunnel between two private networks

14. **What does deep packet inspection (DPI) allow a firewall or IPS to do?**
    - Examine the full contents of network packets, including the payload, to identify threats or policy violations
    - Only inspect packet headers for source and destination information
    - Encrypt packets before forwarding them to their destination
    - Compress network traffic to improve throughput

15. **What distinguishes a network-based IDS (NIDS) from a host-based IDS (HIDS)?**
    - A NIDS monitors traffic on a network segment, while a HIDS monitors activity on a single host or endpoint
    - A NIDS only detects external threats, while a HIDS only detects internal threats
    - A NIDS replaces the need for a firewall, while a HIDS does not
    - A NIDS and HIDS use identical detection techniques but differ in vendor support

16. **What is a next-generation firewall (NGFW)?**
    - A firewall that combines traditional packet filtering with application awareness, intrusion prevention, and threat intelligence
    - A firewall that only uses stateless rules for maximum performance
    - A legacy firewall upgraded with additional RAM and CPU resources
    - A purely cloud-based firewall that cannot run on premises

17. **How can a zero-day exploit challenge an IDS or IPS deployment?**
    - Because the attack leverages a previously unknown vulnerability, signature-based detection may fail to recognize it
    - Because the IDS or IPS automatically shuts down when it encounters unknown traffic
    - Because zero-day exploits only target endpoints, not network traffic
    - Because zero-day exploits are always encrypted and invisible to inspection
