* connect two networks trough a tunnel (ports are not exposed on the internet)
* end ueser (remote worker) to connect to office LAN
* Options: OpenVPN, SSH, LLTP, IPSec
* 


<h1>How does VPN tunnelling work?</h1>

The issue is, even if there is no physical tunnel linking the two LAN routers, the data may still be accessed.
However, the data is placed in a safe envelope, much like a letter, and is then encrypted so that it cannot be hacked or viewed.
Encapsulation is the process of putting data to be transferred into an envelope or another packet.

Do you believe that because the internet is a public network, the data you transmit to networks such as Amazon may be hacked?

To some extent, it cannot be hacked due to a feature known as end-to-end encryption.
Only the two communicating users will be able to see the data in this system. 


# Virtual Private Network (VPN)

## **Overview**
A Virtual Private Network (VPN) is a technology that creates a secure and encrypted connection over a less secure network, such as the internet. It allows remote users to securely connect to a private network.

## **Types of VPN**

### 1. **Site-to-Site VPN**
   - Connects entire networks to each other.
   - Used for connecting branch offices to a central office.

### 2. **Remote Access VPN**
   - Connects individual users to a remote network.
   - Used by employees to access their company's intranet remotely.

### 3. **VPN Protocols**
   - **PPTP (Point-to-Point Tunneling Protocol)**
     - Older and less secure.
     - Port 1723, easy to set up.
   - **L2TP/IPsec (Layer 2 Tunneling Protocol)**
     - L2TP combined with IPsec for added security.
     - Port 500, more secure than PPTP.
   - **OpenVPN**
     - Open-source and highly secure.
     - Customizable, requires third-party software.
   - **SSTP (Secure Socket Tunneling Protocol)**
     - Integrated into Windows and uses SSL/TLS encryption.
     - Port 443, bypasses most firewalls.

## **Benefits of Using VPN**

### 1. **Security**
   - Encrypts data, ensuring privacy and protection against unauthorized access.

### 2. **Remote Access**
   - Allows users to access a network from any location.

### 3. **Anonymity**
   - Masks IP address, providing privacy and access to geo-restricted content.

### 4. **Cost-Effective**
   - Provides a cost-efficient solution for connecting to a private network.

### 5. **Bypass Censorship**
   - Allows users to access blocked websites and services.

## **VPN Components**

### 1. **VPN Client**
   - Software or hardware that initiates a connection to the VPN server.

### 2. **VPN Server**
   - Accepts requests from VPN clients and creates a secure tunnel for data transmission.

### 3. **VPN Gateway**
   - Facilitates communication between VPN server and the protected internal network.

### 4. **Tunnel**
   - An encrypted connection through which data is transmitted securely.

### 5. **Encryption**
   - The process of converting data into a coded format to prevent unauthorized access.

## **Security Concerns and Limitations**

### 1. **Speed**
   - VPNs can potentially slow down internet speeds due to encryption overhead.

### 2. **Reliability**
   - Connection may drop, causing temporary loss of protection.

### 3. **Legal and Policy Issues**
   - Some regions may have restrictions on VPN usage.

### 4. **Data Logging**
   - Some VPN providers may log user data, which can lead to privacy concerns.

## **VPN Applications**
- **Business**: Securely connecting remote branches and employees.
- **Personal Use**: Accessing geo-restricted content, ensuring privacy.
- **Education**: Providing secure access to educational resources.

## **Best Practices**
- Use reputable VPN providers.
- Ensure strong encryption methods are used.
- Regularly update VPN software to ensure security and compatibility.


## WHICH LAYER?

    Network Layer (Layer 3): VPNs are most commonly associated with the Network Layer, where routing and IP addressing occur. VPNs create a virtual network that routes data across the internet in a way that emulates a private network connection. This can involve encrypting the data and encapsulating it in IP packets to be sent across the public internet while making it appear as if it's part of a private network.

    Session Layer (Layer 5): Some VPN protocols can also operate at the Session Layer, where they can manage and control the dialog between applications on different devices. This layer ensures that a session is established, maintained, and properly terminated when no longer needed.

    Transport Layer (Layer 4): Some aspects of VPNs can also be linked to the Transport Layer, particularly when considering transport mode in IPsec, where only the payload of the packet is encrypted and not the header.

    Application Layer (Layer 7): Some user-facing VPN services work as applications that can be installed on devices. These services are built on top of network and session layer protocols but are implemented in a way that is easy for end-users to interact with, providing them control at the application layer.

**Conclusion**: VPNs play a vital role in ensuring privacy and security in network communications by establishing encrypted tunnels over insecure networks.
