# Reasons for Protocols

Protocols are essential in network communication for several reasons:

- **Identified Sender and Receiver**: Ensuring the correct source and destination.
- **Common Language and Grammar**: Ensuring that the message is understood by both parties.
- **Speed and Timing of Delivery**: Ensuring timely and ordered delivery of data.
- **Confirmation or Acknowledgement Requirements**: Ensuring that the message has been received and understood.

## Characteristics of Network Communication Protocols

Network communication protocols share the following characteristics:

- **Message Encoding**: How the message is encoded for transmission.
- **Message Formatting and Encapsulation**: How the message is structured and packaged.
- **Message Size**: The size constraints of the message.
- **Message Timing**: The speed and order in which messages are sent and received.
- **Message Delivery Options**: How the message can be delivered (unicast, multicast, broadcast, etc.).

## Protocol Interaction

### **HTTP (Hypertext Transfer Protocol)**
- **Role**: An application protocol regulating interaction between a webserver and a webclient.
- **Dependency**: Relies on other protocols for message transmission between client and server.

### **TCP (Transmission Control Protocol)**
- **Role**: Controls individual conversations and breaks down HTTP messages into smaller chunks (segments).
- **Management**: Manages the size and rate of message exchange between server and clients.

### **IP (Internet Protocol)**
- **Role**: Encapsulates TCP segments into packets, assigns IPs, and delivers them to the destination.

### **Ethernet**
- **Role**: Handles Data Link communication and physical transfer over the network medium.

## TCP/IP Protocol Suite

### **Application Layer**
- **Name System**
  - **DNS** (Domain Name System)
- **Host Config**
  - **BOOTP** (Bootstrap Protocol)
  - **DHCP** (Dynamic Host Configuration Protocol)
- **Email**
  - **SMTP** (Simple Mail Transfer Protocol)
  - **POP** (Post Office Protocol)
  - **IMAP** (Internet Message Access Protocol)
- **File Transfer**
  - **FTP** (File Transfer Protocol)
  - **TFTP** (Trivial File Transfer Protocol)
- **Web**
  - **HTTP** (Hypertext Transfer Protocol)

### **Transport Layer**
- **UDP** (User Datagram Protocol)
- **TCP** (Transmission Control Protocol)

### **Internet Layer**
- **IP** (Internet Protocol)
- **NAT** (Network Address Translation)
- **IP Support**
  - **ICMP** (Internet Control Message Protocol)
- **Routing Protocols**
  - **OSPF** (Open Shortest Path First)
  - **EIGRP** (Enhanced Interior Gateway Routing Protocol)

### **Network Access Layer**
- **ARP** (Address Resolution Protocol)
- **PPP** (Point to Point Protocol)
- **Ethernet**
- **Interface Drivers**


**Transport Layer**

[***TCP
header***](https://www.geeksforgeeks.org/tcp-services-and-segment-structure/)\
![https://media.geeksforgeeks.org/wp-content/uploads/TCPSegmentHeader-1.png](images/media/image12.png)

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
![https://media.geeksforgeeks.org/wp-content/uploads/UDP-header.png](images/media/image7.png)

Refer the [*Differences between TCP and
UDP*](https://www.geeksforgeeks.org/differences-between-tcp-and-udp/)
    
