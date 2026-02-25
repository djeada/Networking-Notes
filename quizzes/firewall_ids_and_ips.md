

1. **What is the primary difference between a stateful and a stateless firewall?**
   - A stateful firewall tracks the state of active connections and makes decisions based on the context of the traffic.
   - A stateless firewall only filters traffic based on static rules without considering the state of the connection.
   - A stateful firewall only inspects the packet headers, while a stateless firewall inspects the entire packet.
   - A stateless firewall is more secure than a stateful firewall.

2. **Which of the following best describes an IDS in a network environment?**
   - A system that actively blocks malicious traffic based on predefined rules.
   - A system that monitors network traffic for suspicious activity and generates alerts.
   - A firewall that filters inbound and outbound traffic.
   - A device that encrypts traffic between different network segments.

3. **You’ve configured an IPS to monitor network traffic. What action does the IPS take when it detects a potential threat?**
   - It alerts the network administrator and blocks the suspicious traffic in real time.
   - It logs the event and sends a notification to the security team without blocking the traffic.
   - It redirects the traffic to a honeypot for further analysis.
   - It forwards the traffic to an IDS for deeper inspection.

4. **What is a key advantage of a stateful firewall compared to a stateless firewall?**
   - It can make decisions based on the history of traffic flow, allowing for more dynamic security policies.
   - It is faster because it only inspects the headers of packets.
   - It requires less processing power and memory.
   - It automatically blocks all traffic by default.

5. **When deploying an IDS, where should it be placed to maximize its effectiveness?**
   - Between the router and the internal network
   - Directly behind the firewall
   - On every host in the network
   - At the network's perimeter, before the firewall

6. **How does an IPS differ from an antivirus software in terms of functionality?**
   - An IPS monitors and blocks network traffic in real-time, while antivirus software scans and removes malicious files on a device.
   - An IPS only detects known threats, while antivirus software detects both known and unknown threats.
   - An IPS operates on endpoints, while antivirus software operates on network traffic.
   - An IPS and antivirus software perform the same functions but are used in different environments.

7. **Which scenario might cause a stateful firewall to block legitimate traffic?**
   - When the traffic does not match an existing session in the connection table.
   - When the traffic is encrypted.
   - When the source and destination ports are the same.
   - When the traffic is on a non-standard port.

8. **What type of firewall would be best for filtering traffic based on specific applications rather than just IP addresses and ports?**
   - Application-layer firewall
   - Packet-filtering firewall
   - Stateless firewall
   - Circuit-level gateway

9. **An IDS has generated an alert for suspicious activity, but upon review, the traffic is legitimate. What is this an example of?**
   - A false positive
   - A false negative
   - A true positive
   - A true negative

10. **What is the primary function of an IPS in comparison to a firewall?**
    - An IPS can block threats in real-time based on deep packet inspection, while a firewall primarily filters traffic based on IP addresses and ports.
    - An IPS is only used for monitoring, while a firewall actively blocks threats.
    - An IPS is more efficient in handling encrypted traffic than a firewall.
    - An IPS replaces the need for a firewall in a secure network.

11. **What could be a potential downside of an aggressively configured IPS?**
    - It may block legitimate traffic, leading to network disruptions.
    - It requires constant manual updates to its rule set.
    - It might not generate alerts for blocked traffic.
    - It cannot operate in real-time.

12. **Which of the following best describes a hybrid IDS/IPS system?**
    - A system that can both detect and block threats, depending on how it’s configured.
    - A system that alternates between detection and prevention modes based on traffic volume.
    - A system that requires both an IDS and an IPS to function properly.
    - A system that focuses on host-based detection only.
