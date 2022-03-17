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

**What are layers in OSI model?**

1.  Physical Layer Converts data bit into an electrical impulse.

2.  Data Link Layer Data packet will be encoded and decoded into bits.

3.  Network Layer Transfer of datagrams from one to another.

4.  Transport Layer Responsible for Data transfer from one to another.

5.  Session Layer Manage and control signals between computers.

6.  Presentation Layer Transform data into application layer format.

7.  Application Layer An end user will interact with the Application
    layer.

The model is a theoretical stack of seven layers that can be used as a
reference to

help understand how networks operate. The model was introduced to
standardize networks in a way that allowed multi vendor systems. Prior
to this, you would only be able to have a one vendor network because the
devices from one vendor couldn't communicate with others. It is worth
nothing that we dont actually use the OSI model, we use something called
the TCP/IP model. The concepts are exactly the same. the layers are
slightly

different.

Layers

**Layer1: Physical layer**

carries data across physical hardware.

User: ethernet cables.

Examples:

-are all the cables plugged in?

-Is the network card functioning?

-Could it be a faulty cable?

**Layer 2: Data Link layer**

At this layer, the physical addresses are added to the data. This is
source and

destination mac addresses.

Switches operate at this layer

Example:

-Maybe the switch has gone bad?

**Layer 3: Network layer**

The network layer handles ip addressing and routing. At this layer, the
source

and destination IP addresses are added.

Routers operate at this layer

Example:

-Is the router functioning?

-Do i have the right IP address?

**Layer 4: Transport layer**

This layer adds transport protocols such as TCP/UDP, and adds
source/destination

port numbers.

Example:

-Could the internet card be functional?

**Layer 5: Session layer**

this layer is responsible for establishing and terminating connections
between devices.

Example:

-Are you connecting to the correct address?

**Layer 6: Presentation layer**

This layer formats the data in a way the receiving application can
understand it. This

layer can also encrypt and decrypt data if needed

Example:

-Are you reading the data in the same order that you wrote it?

**Layer 7: Application layer**

This layer is where the application and user communicates

Applications used here such as SMTP, if you're sending an email for
example.

Example:

-Is the application erroring out?

**What is Stop-and-Wait Protocol?**\
In Stop and wait protocol, a sender after sending a frame waits for an
acknowledgment of the frame and sends the next frame only when
acknowledgment of the frame has received.

**What is Piggybacking?**\
Piggybacking is used in bi-directional data transmission in the network
layer (OSI model). The idea is to improve efficiency piggyback
acknowledgment (of the received data) on the data frame (to be sent)
instead of sending a separate frame.

**Differences between Hub, Switch and Router?**

  Hub | Switch | Router
  --- | --- | ---
  Physical Layer Device | Data Link Layer Device | Network Layer Device
  Simply repeats signal to all ports | Doesn’t simply repeat, but filters content by MAC or LAN address | Routes data based on IP address
  Connects devices within a single LAN | Can connect multiple sub-LANs within a single LAN | Connect multiple LANS and WANS together.
  [*Collision domain*](https://en.wikipedia.org/wiki/Collision_domain) of all hosts connected through Hub remains one. i.e., if signal sent by any two devices can collide.   Switch divides collision domain, but [*broadcast domain*](https://en.wikipedia.org/wiki/Broadcast_domain)of connected devices remains same.   It divides both collision and broadcast domains,
                                                                                                                                                                                                                                                                                                                            

See [*network
devices*](http://quiz.geeksforgeeks.org/network-devices-hub-repeater-bridge-switch-router-gateways/) for
more details.

**What happens when you type a URL in the web browser?**\
A URL may contain a request to HTML, image file or any other type.

1.  If the content of the typed URL is in the cache and fresh, then
    display the content.

2.  Else find the IP address for the domain so that a TCP connection can
    be set up. Browser does a DNS lookup.

3.  Browser needs to know the IP address for a URL so that it can set up
    a TCP connection.  This is why browser needs DNS service. The
    browser first looks for URL-IP mapping browser cache, then in OS
    cache. If all caches are empty, then it makes a recursive query to
    the local DNS server.   The local DNS server provides the IP
    address.

4.  Browser sets up a TCP connection using three-way handshake.

5.  Browser sends a HTTP request.

6.  Server has a web server like Apache, IIS running that handles
    incoming HTTP request and sends an HTTP response.

7.  Browser receives the HTTP response and renders the content.

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

**How does DNS work?**

**Domain :**

There are various kinds of DOMAIN :

1.  Generic domain : .com(commercial) .edu(educational) .mil(military)
    .org(non profit organization) .net(similar to commercial) all
    these are generic domain.

2.  Country domain .in (india) .us .uk

3.  Inverse domain if we want to know what is the domain name of the
    website. Ip to domain name mapping.So DNS can provide both the
    mapping for example to find the ip addresses of geeksforgeeks.org
    then we have to type nslookup www.geeksforgeeks.org.

**Hierarchy of Name Servers**

**Root name servers** – It is contacted by name servers that can not
resolve the name. It contacts authoritative name server if name mapping
is not known. It then gets the mapping and return the IP address to the
host.

**Top level server** – It is responsible for com, org, edu etc and all
top level country domains like uk, fr, ca, in etc. They have info about
authoritative domain servers and know names and IP addresses of each
authoritative name server for the second level domains.

**Authoritative name servers** This is organization’s DNS server,
providing authoritative hostName to IP mapping for organization servers.
It can be maintained by organization or service provider. In order to
reach cse.dtu.in we have to ask the root DNS server, then it will point
out to the top level domain server and then to authoritative domain name
server which actually contains the IP address. So the authoritative
domain server will return the associative ip address.

**Domain Name Server**

![DNS_3](images//media/image16.png)

The client machine sends a request to the local name server, which , if
root does not find the address in its database, sends a request to the
root name server, which in turn, will route the query to an intermediate
or authoritative name server. The root name server can also contain some
hostName to IP address mappings . The intermediate nae server always
knows who the authoritative name server is. So finally the IP address is
returned to the local name server which in turn returns the IP address
to the host.

**Recursive Resolution** –\
Here, client requires the Local Server to give either the requested
mapping or an error message. A DNS Query is generated by the application
program to the resolver to fetch the destination IP Address. The Query
is then forward to the local DNS Server. If it knows the IP Address, it
sends a response to the resolver. Assuming, it does not know the IP
Address, it sends the query to the root name server.\
The root name server contains information of about at least one server
of Top Level Domain. The query is then sent to the respective Top-Level
Domain server. If it contains the mapping, the response is sent back to
the root server and then to host’s local server. If it doesn’t contain
the mapping, it should contain the IP Address of destination’s local DNS
Server. The local DNS server knows the destination host’s IP Address.
The information is then sent back to the top-level domain server, then
to the root server and then to the host’s Local DNS Server and finally
to the host.\
![](images//media/image10.jpg)

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

**Physical Layer**

[***Network
Topologies:***](https://www.geeksforgeeks.org/network-topologies-computer-networks/)

-   **Mesh Topology:**\
    In mesh topology, every device is connected to another device via
    particular channel.If suppose, N number of devices are connected
    with each other, then total number of links required to connect
    NC~2~.

-   **Bus Topology:**\
    Bus topology is a network type in which every computer and network
    device is connected to single cable. If N devices are connected,
    then the number of cables required 1 which is known as backbone
    cable and N drop lines are required.

-   **Star Topology:**\
    In star topology, all the devices are connected to a single hub
    through a cable. If N devices are connected to each other, then
    the no. of cables required N.

-   **Ring Topology:**\
    In this topology, it forms a ring connecting a devices with its
    exactly two neighboring devices.

[***Transmission
Modes:***](https://www.geeksforgeeks.org/transmission-modes-computer-networks/)

-   **Simplex Mode**: the communication is unidirectional, as on a
    one-way street.Only one of the two devices on a link can transmit,
    the other can only receive.

-   **Half-duplex Mode**: each station can both transmit and receive,
    but not at the same time.

-   **Full-duplex Mode**: both stations can transmit and receive
    simultaneously.

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

**Data Link Layer**

1.  **Flow Control**\
    N = Sender’s Window Size. (in SR both sender and receiver window
    are same)\
    a = T~p~ /T~t~

![https://media.geeksforgeeks.org/wp-content/uploads/2-40.jpg](images//media/image5.jpg)

1.  Sequence No. >= (Sender’s Window Size) + (Reciever’s Window Size
    )

2.  Efficiency in TDM(polling) = T~t~ / (T~poll~ + T~t~)

3.  In CSMA/CD, T~t~ >= 2*T~p~\
    Hence, min frame length = 2*T~p~*B

4.  In CSMA/CD, Efficiency = 1/(1 + 6.44a)

5.  [***Back-off Algorithm for
    CSMA/CD***](https://www.geeksforgeeks.org/back-off-algorithm-csmacd/)\
    Waiting time = back–off time\
    Let n = collision number or re-transmission serial number.\
    Then, Waiting time = K * T~slot~\
    where K = \[0, 2<sup>n</sup> – 1 \]

6.  N = No. of stations\
    Early Token Reinsertion : Efficiency = 1/(1 + a/N)\
    Delayed Token Reinsertion : Efficiency = 1/(1 + (N+1)a/N)

7.  Pure Aloha Efficiency = 18.4 %\
    Slotted Aloha Efficiency = 36.8%

8.  [***Maximum data rate (channel capacity) for noiseless and noisy
    channels***](https://www.geeksforgeeks.org/computer-network-maximum-data-rate-channel-capacity-noiseless-noisy-channels/)

    -   **Noiseless Channel : Nyquist Bit Rate**\
        BitRate = 2 * Bandwidth * log2(L)\
        where,L is the number of signal levels used to represent data.

    -   **Noisy Channel : Shannon Capacity**\
        Capacity = bandwidth * log2(1 + SNR)\
        where, SNR is the signal-to-noise ratio

 

9.  **Error Control**

    -   [***Hamming
        Code***](https://www.geeksforgeeks.org/computer-network-hamming-code/):
        is a set of error-correction codes that can be used to detect
        and correct the errors that can occur when the data is moved
        or stored from the sender to the receiver.\
        **Redundant bits:**\
        2^r^ ≥ m + r + 1\
        where, r = redundant bit, m = data bit

    -   [***Framing in
        DLL***](https://www.geeksforgeeks.org/computer-network-framing-data-link-layer/):
        It provides a way for a sender to transmit a set of bits that
        are meaningful to the receiver.\
        **Character/Byte Stuffing:** Used when frames consist of
        character. If data contains ED then, byte is stuffed into data
        to diffentiate it from ED.\
        **Bit stuffing**: Sender stuffs a bit to break the pattern
        i.e. here appends a 0 in data = 0111**0**1.

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

**Transport Layer**

[***TCP
header***](https://www.geeksforgeeks.org/tcp-services-and-segment-structure/)\
![https://media.geeksforgeeks.org/wp-content/uploads/TCPSegmentHeader-1.png](images//media/image12.png)

[***In TCP congestion control
Algorithm***](https://www.geeksforgeeks.org/computer-network-tcp-congestion-control/)\
When Time Out Occurs Algorithm Enters Slow Start Phase\
When 3 Duplicate occurs algorithm enters congestion avoidance phase

[***TCP 3-Way Handshake
Process***](https://www.geeksforgeeks.org/computer-network-tcp-3-way-handshake-process/)\
**Step 1 (SYN)** : In the first step, client wants to establish a
connection with server, so it sends a segment with SYN(Synchronize
Sequence Number) which informs server that client is likely to start
communication and with what sequence number it starts segments with\
**Step 2 (SYN + ACK)**: Server responds to the client request with
SYN-ACK signal bits set. Acknowledgement(ACK) signifies the response of
segment it received and SYN signifies with what sequence number it is
likely to start the segments with\
**Step 3 (ACK)** : In the final part client acknowledges the response of
server and they both establish a reliable connection with which they
will start eh actual data transfer.\
 

[***UDP header***](https://www.geeksforgeeks.org/gate-cs-notes-gq/)\
![https://media.geeksforgeeks.org/wp-content/uploads/UDP-header.png](images//media/image7.png)

Refer the [*Differences between TCP and
UDP*](https://www.geeksforgeeks.org/differences-between-tcp-and-udp/)

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

[***Hypertext Transfer Protocol
(HTTP)***](https://www.geeksforgeeks.org/http-non-persistent-persistent-connection/):
is an application-level protocol that uses TCP as an underlying
transport and typically runs on port 80. HTTP is a stateless protocol
i.e. server maintains no information about past client requests.

**Network Security**

For Symmetric Key : n*(n-1)/2 keys are required.\
For Public Key : 2*n key are required ( each node will have private and
public key).

[***RSA Algorithm in
Cryptography***](https://www.geeksforgeeks.org/rsa-algorithm-using-multiple-precision-arithmetic-library/)\
\
![Rsa Example](images//media/image9.png)

[***Deffie Hellman Key
Exchange***](https://www.geeksforgeeks.org/implementation-diffie-hellman-algorithm/)\
R1 = g<sup>x</sup> mod p\
R2 = g<sup>y</sup> mod q\
Both will have same key = g<sup>xy</sup> mod p
