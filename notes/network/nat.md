* It was created to solve the problem of limited number of IPv4 addresses.
* Previously each device got its own PUBLIC IP address (connected with switch to default gateway).
* Another thing is security. IP of each device is public so can potentially be accessed from anywhere.
* NAT is a process where a router translates one IP address into another.

4 types of NAT:
* Static nat (SNAT)
* Dynamic nat (DNAT) (ip masquerading, private addresses are rotated)
* Port address translation (PAT)
* port forwarding (requests with one port can be translated to another port locally)

With PAT each host on the LAN is translated to the routers WAN-side public IP address, with a different port number.

## NAT vs Subnetting

| Feature         | Subnetting                                          | NAT (Network Address Translation)                               |
|-----------------|-----------------------------------------------------|-----------------------------------------------------------------|
| **Definition**  | Subnetting is the process of dividing a network into smaller network segments or subnets. | NAT is a method used to remap one IP address space into another by modifying network address information in the IP header of packets while they are in transit. |
| **Primary Use** | To create multiple smaller, manageable networks from a larger network. | To allow multiple devices on a private network to share a single public IP address for accessing external networks like the internet. |
| **Objective**   | - Improve network performance and speed. <br> - Efficient IP address allocation. <br> - Enhance security by isolating groups of hosts. | - Conserve IPv4 addresses by allowing multiple private IP addresses to share one public IP address. <br> - Provide a type of firewall by hiding internal IP addresses. |
| **Operation**   | Involves dividing a network based on subnet mask which determines the network and host part of an IP address. | Translates private IP addresses to a public IP address and vice versa. This is usually done by a router or firewall. |
| **IP Addresses**| Each subnet has a unique network address, a range of host addresses, and a broadcast address. | Utilizes two sets of IP addresses: internal (private) and external (public). |
| **Routing**     | Routers use subnet information to make efficient routing decisions. | Routers or NAT devices translate addresses between private internal networks and the external public network. |
| **Visibility**  | Subnets are visible to both internal and external networks if properly routed. | Internal addresses are typically not visible to the external network, providing a layer of privacy and security. |
| **Configuration**| Requires careful planning for IP range, subnet mask, and understanding of network topology. | Configured on routers and firewalls, often with dynamic or static mapping of addresses. |
| **Scalability** | Highly scalable, but requires careful planning for IP address allocation and subnet sizing. | Offers scalability in terms of internal network size, but limited by the number of available public IP addresses. |
| **Common Usage**| Used extensively in medium to large-sized networks for efficient IP management. | Widely used in almost all types of networks, especially where IP address conservation is important. |

 ## NAT and Proxy
Here's a comparison table between NAT and Proxy based on the provided descriptions:

| **Parameter**               | **NAT (Network Address Translation)**                              | **Proxy (Forward Proxy)**                               |
|-----------------------------|-------------------------------------------------------------------|---------------------------------------------------------|
| **OSI Layer**               | Layer 3/4 (Network/Transport Layer)                               | Layer 7 (Application Layer)                             |
| **Connection Type**         | Single continuous connection from client to server (with IP translation) | Two separate connections: client to proxy, proxy to server |
| **Data Handling**           | Cannot read or modify encrypted data; only changes IP addresses   | Can decrypt, inspect, modify, cache, and filter data    |
| **Primary Function**        | IP address conservation and basic security by IP masking          | Content filtering, caching, and enforcing network policies |
| **Visibility to End Hosts** | Typically invisible to end hosts; operates transparently          | Both client and server are aware of proxy's presence    |
| **Application Specificity** | Operates at the IP level, not protocol-specific                   | Protocol-specific, e.g., HTTP, FTP                      |
| **Data Exposure**           | No exposure of user data if encrypted                             | User data exposed to proxy when decrypted               |
| **Security Impact**         | Provides basic security by hiding internal IP addresses           | Enhances security by controlling traffic at the application level |
| **Configuration**           | No special configuration needed on end hosts                     | May require configuration on client devices             |
| **Overhead**                | Low overhead; primarily IP address rewriting                      | Higher overhead due to processing at the application level |
| **Common Use Cases**        | Conserving public IPs, simple network security                    | Web content filtering, bypassing geo-restrictions, caching |
| **Cost**                    | Low, can be implemented on existing network devices               | Higher, may require dedicated hardware/software         |

This table highlights the key differences and similarities between NAT and forward proxies, focusing on their roles, functions, and how they operate within a network.
