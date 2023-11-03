## Commonly asked Computer Networks Interview Questions | Set 1


**What are Unicasting, Anycasting, Multicasting and Broadcasting?**\
If the message is sent from a source to a single destination node, it is
called Unicasting. This is typically done in networks.

If the message is sent from a source to any of the given destination
nodes. This is used a lot in Content delivery Systems where we want to
get content from any server.

If the message is sent to some subset of other nodes, it is called
Multicasting. Used in the situation when there are multiple receivers of
the same data. Like video conferencing, updating something on CDN
servers which have a replica of same data.\
If the message is sent to all the nodes in a network it is called
Broadcasting. This is typically used in Local networks, for example,
DHCP and ARP use broadcasting.


**What is Stop-and-Wait Protocol?**\
In Stop and wait protocol, a sender after sending a frame waits for an
acknowledgment of the frame and sends the next frame only when
acknowledgment of the frame has received.

**What is Piggybacking?**\
Piggybacking is used in bi-directional data transmission in the network
layer (OSI model). The idea is to improve efficiency piggyback
acknowledgment (of the received data) on the data frame (to be sent)
instead of sending a separate frame.          


**What is DHCP, how does it work?**

1.  The idea of DHCP (Dynamic Host Configuration Protocol) is to enable
    devices to get IP address without any manual configuration.

2.  The device sends a broadcast message saying “I am new here”

3.  The DHCP server sees the message and responds back to the device and
    typically allocates an IP address. All other devices on network
    ignore the message of the new device as they are not DHCP server.

In Wi-Fi networks, Access Points generally work as a DHCP server.

**What is ARP, how does it work?**\
ARP stands for Address Resolution Protocol. ARP is used to find LAN
address from the Network address. A node typically has destination IP to
send a packet, the nodes need link layer address to send a frame over a
local link. The ARP protocol helps here.

1.  The node sends a broadcast message to all nodes saying what is the
    MAC address of this IP address.

2.  Node with the provided IP address replies with the MAC address.

Like DHCP, ARP is a discovery protocol, but unlike DHCP there is not
server here.



**NOTES**

**OSI Layers, Data units and Functions:**

  **LAYERS**    |      **DATA UNITS**  |   **FUNCTIONS**
  --- | --- | ---
  Application Layer |  Data            |   Mail Services, Directory Services, FTAM
  Presentation Layer | Data |              Translation, Compression, Encryption/Decryption
  Session Layer |      Data |              Session Establishment, Synchronization,Dialog Controller
  Transport Layer |    Segments,Datagram | Segmentation, Flow Control, Error Control, TCP/UDP
  Network Layer |      Packets |           Logical Addressing, Routing, Traffic control, Fragmentation
  Data Link Layer |    Frames |            Physical Addressing, Flow control,Error control,Access control
  Physical Layer |     Bits |              Bit Synchronization,Bit rate control,Physical Topologies

**Layers and their uses –**\
![https://media.geeksforgeeks.org/wp-content/uploads/3-30.jpg](images//media/image15.jpg)



[***Manchester
Encoding***](https://www.geeksforgeeks.org/computer-network-manchester-encoding/):
When there is a long sequence of 0s and 1s, there is a problem at the
receiving end. The problem is that the synchronization is lost due to
lack of transmissions.

-   **NRZ-level encoding **: The polarity of signals changes when
    incoming siganl changes from ‘1’ to ‘0’ or from ‘0’ to ‘1’. It
    considers the first bit data as polarity change.

-   **NRZ-Inverted/ Differential encoding**:In this, the transitions at
    the beginning of bit interval is equal to 1 and if there is no
    transition at the beginning of bit interval is equal to 0.


**Network Layer**

[***Class Full Addressing
Table***](https://www.geeksforgeeks.org/ip-addressing-introduction-and-classful-addressing/):\
![https://media.geeksforgeeks.org/wp-content/uploads/1-45.jpg](images//media/image13.jpg)

[***IPv4 header
datagram***](https://www.geeksforgeeks.org/network-layer-introduction-ipv4/):\
![https://media.geeksforgeeks.org/wp-content/uploads/contentArticle-1.png](images//media/image21.png)

[***IP version 6 Header
Format***](https://www.geeksforgeeks.org/computer-network-internet-protocol-version-6-ipv6-header/)\
![https://media.geeksforgeeks.org/wp-content/uploads/ipv6-header.png](images//media/image4.png)

[***Internet Control Message
Protocol***](https://www.geeksforgeeks.org/internet-control-message-protocol-icmp/):
Since IP does not have a inbuilt mechanism for sending error and control
messages. It depends on Internet Control Message Protocol(ICMP) to
provide an error control.

1.  Source quench message

2.  Parameter problem

3.  Time exceeded message

4.  Destination un-reachable

 \
[***Difference between DVR and
LSR***](https://www.geeksforgeeks.org/computer-network-distance-vector-routing-vs-link-state-routing/)\
![https://media.geeksforgeeks.org/wp-content/uploads/4-18.jpg](images//media/image8.jpg)

[***Open shortest path first
(OSPF)***](https://www.geeksforgeeks.org/open-shortest-path-first-ospf-router-roles-configuration/):
Open shortest path first (OSPF) is a link-state routing protocol which
is used to find the best path between the source and the destination
router using its own SPF algorithm.\
Designated Router(DR) and Backup Designated Router(BDR) election takes
place in broadcast network or multi-access network.\
**Criteria for the election:**

1.  Router having the highest router priority will be declared as DR.

2.  If there is a tie in router priority then highest router will be
    considered. First, highest loopback address is considered. If no
    loopback is configured then the highest active IP address on the
    interface of the router is considered.

[***Routing Information
Protocol(RIP)***](https://www.geeksforgeeks.org/computer-network-routing-information-protocol-rip/):
is a dynamic routing protocol which uses hop count as a routing metric
to find the best path between the source and the destination network. It
is a distance vector routing protocol which has AD value 120 and works
on the application layer of OSI model. RIP uses port number 520.

**Hop Count**:

1.  Hop count is the number of routers occurring in between the source
    and destination network. The path with the lowest hop count is
    considered as the best route to reach a network and therefore
    placed in the routing table.

2.  The maximum hop count allowed for RIP is 15 and hop count of 16 is
    considered as network unreachable.



**Application Layer**

[***Domain Name
Server***](https://www.geeksforgeeks.org/dns-domain-name-server/): DNS
is a host name to IP address translation service. DNS is a distributed
database implemented in a hierarchy of name servers. It is an
application layer protocol for message exchange between clients and
servers.

[***Dynamic Host Configuration
Protocol(DHCP)***](https://www.geeksforgeeks.org/computer-network-dynamic-host-configuration-protocol-dhcp/) is
an application layer protocol which is used to provide:\
Subnet Mask (Option 1 – e.g., 255.255.255.0)\
Router Address (Option 3 – e.g., 192.168.1.1)\
DNS Address (Option 6 – e.g., 8.8.8.8)\
Vendor Class Identifier (Option 43 – e.g., ‘unifi’ = 192.168.1.9
##where unifi = controller)

[***Simple Network Management Protocol
(SNMP)***](https://www.geeksforgeeks.org/computer-network-simple-network-management-protocol-snmp/):
SNMP is an application layer protocol which uses UDP port number
161/162.SNMP is used to monitor network, detect network faults and
sometimes even used to configure remote devices.

[***Simple Mail Transfer Protocol
(SMTP)***](https://www.geeksforgeeks.org/simple-mail-transfer-protocol-smtp/):
SMTP is an application layer protocol. The client who wants to send the
mail opens a TCP connection to the SMTP server and then sends the mail
across the connection. The SMTP server is always on listening mode. As
soon as it listens for a TCP connection from any client, the SMTP
process initiates a connection on that port (25). After successfully
establishing the TCP connection the client process sends the mail
instantly.

[***File Transfer Protocol
(FTP)***](https://www.geeksforgeeks.org/computer-network-file-transfer-protocol-ftp/):
File Transfer Protocol(FTP) is an application layer protocol which moves
files between local and remote file systems. It runs on the top of TCP,
like HTTP. To transfer a file, 2 TCP connections are used by FTP in
parallel: control connection and data connection.


