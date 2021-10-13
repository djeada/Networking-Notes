Reasons for portocols:
An identified sender and receiver
Common language and grammar
Speed and timing of delivery
Confirmation or acknowledgement requirements

The following characteristics are shared by network communication protocols: 
Message encoding
Message Formatting and Encapsulation
Message size
Message Timing
Mesage Delivery Options

<h1>Protocol Interaction</h1>

HTTP: An application protocol that regulates the interaction between a webserver and a webclient.
HTTP is dependent on other protocols to control how messages are sent between the client and the server.

TCP: The transport protocol that controls individual conversations.
TCP breaks down HTTP messages into smaller chunks.
(Segments)
TCP is also in charge of managing the size and pace at which messages between the server and clients are exchanged.

IP: Encapsulates prepared TCP segments into packets, assigns the appropriate IP, and delivers them to the destination.

Ethernet: Data Link communication and physical transfer over network medium. 

<h1>TCP/IP Protocol Suite</h1>

Applictaion Layer
    Name System
        DNS - Domain Name System
    Host Config
        BOOTP - Bootstrap Protocol
        DHCP - Dynamic Host Configuration Protocol
    Email
        SMTP - Simple Mail Transfer Protocol
        POP - Post Office Protocol
        IMAP - Internet Message Access Protocol
    File Transfer
        FTP - File Transfer Protocol
        TFTP - Trivial File Transfer Protocol
    Web
        HTTP - Hypertext Transfer Protocol
Transport Layer
    UDP - User Datagram Protocol
    TCP - Transmission Control Protocol
Internet Layer
    IP - Internet Protocol
    NAT - Network Address Translation
    IP Support
        ICMP - Internet Control Message Protocol
    Routing Protocols
        OSPF - Open Shortest Path First
        EIGRP - Enhanced Interior Gateway Routing Protocol
Network Access Layer
    ARP - Address Resolution Protocol
    PPP - Point to Point Protocol
    Ethernet
    Interface Drivers
