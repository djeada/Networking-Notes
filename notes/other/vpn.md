* connect two networks through a tunnel (ports are not exposed on the internet)
* end user (remote worker) to connect to office LAN
* Options: OpenVPN, SSH, LLTP, IPSec
* 


A Virtual Private Network (or VPN for short) is a technology that allows devices on separate networks to communicate securely by creating a dedicated path between each other over the Internet (known as a tunnel). Devices connected within this tunnel form their own private network.


For example, only devices within the same network (such as within a business) can directly communicate. However, a VPN allows two offices to be connected. Let's take the diagram below, where there are three networks:

    Network #1 (Office #1)
    Network #2 (Office #2)
    Network #3 (Two devices connected via a VPN)

The devices connected on Network #3 are still a part of Network #1 and Network #2 but also form together to create a private network (Network #3) that only devices that are connected via this VPN can communicate over.


Let's cover some of the other benefits offered by a VPN in the table below:


Benefit	Description
Allows networks in different geographical locations to be connected.	For example, a business with multiple offices will find VPNs beneficial, as it means that resources like servers/infrastructure can be accessed from another office.
Offers privacy.	

VPN technology uses encryption to protect data. This means that it can only be understood between the devices it was being sent from and is destined for, meaning the data isn't vulnerable to sniffing.

This encryption is useful in places with public WiFi, where no encryption is provided by the network. You can use a VPN to protect your traffic from being viewed by other people.
Offers anonymity.	

Journalists and activists depend upon VPNs to safely report on global issues in countries where freedom of speech is controlled.

Usually, your traffic can be viewed by your ISP and other intermediaries and, therefore, tracked. 

The level of anonymity a VPN provides is only as much as how other devices on the network respect privacy. For example, a VPN that logs all of your data/history is essentially the same as not using a VPN in this regard.

TryHackMe uses a VPN to connect you to our vulnerable machines without making them directly accessible on the Internet! This means that:

    You can securely interact with our machines
    Service providers such as ISPs don't think you are attacking another machine on the Internet (which could be against the terms of service)
    The VPN provides security to TryHackMe as vulnerable machines are not accessible using the Internet.


VPN technology has improved over the years. Let's explore some existing VPN technologies below:


VPN Technology	Description
PPP	

This technology is used by PPTP (explained below) to allow for authentication and provide encryption of data. VPNs work by using a private key and public certificate (similar to SSH). A private key & certificate must match for you to connect.

This technology is not capable of leaving a network by itself (non-routable).
PPTP	

The Point-to-Point Tunneling Protocol (PPTP) is the technology that allows the data from PPP to travel and leave a network. 

PPTP is very easy to set up and is supported by most devices. It is, however, weakly encrypted in comparison to alternatives.
IPSec	

Internet Protocol Security (IPsec) encrypts data using the existing Internet Protocol (IP) framework.

IPSec is difficult to set up in comparison to alternatives; however, if successful, it boasts strong encryption and is also supported on many devices.

## How Does VPN Tunnelling Work?

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
