
#### Q. What mechanism does TCP employ to regulate the flow of data between sender and receiver?

* [x] Flow Control
* [ ] Checksum
* [ ] Sequence Numbers
* [ ] Port Numbering

#### Q. Which protocol is better suited for real-time applications such as video streaming or online gaming?

* [ ] TCP
* [x] UDP
* [ ] HTTP
* [ ] HTTPS

#### Q. Which of the following protocols is connectionless and does not ensure packet delivery?

* [ ] TCP
* [x] UDP
* [ ] FTP
* [ ] SMTP

#### Q. In which protocol are transmitted data units referred to as segments?

* [x] TCP
* [ ] UDP
* [ ] ICMP
* [ ] FTP

#### Q. What does the abbreviation UDP stand for?

* [ ] Universal Datagram Protocol
* [x] User Datagram Protocol
* [ ] Unified Data Packet
* [ ] Unicast Data Protocol

#### Q. Which protocol would you most likely choose for transferring a large file over the internet when data integrity is essential?

* [x] TCP
* [ ] UDP
* [ ] TFTP
* [ ] SNMP

#### Q. Which protocol guarantees reliable data delivery by setting up a connection before transmitting any data?

* [x] TCP
* [ ] UDP
* [ ] ICMP
* [ ] ARP

#### Q. Which of the following protocols relies on port 80 by default?

* [x] TCP
* [ ] UDP
* [ ] ICMP
* [ ] ARP

#### Q. What is the primary reason UDP is preferred over TCP for certain use cases?

* [x] Reduced overhead and faster data transmission
* [ ] Stronger security guarantees
* [ ] Reliable delivery of every packet
* [ ] Simpler implementation across all platforms

#### Q. Which protocol initiates a connection using a three-way handshake?

* [x] TCP
* [ ] UDP
* [ ] ICMP
* [ ] ARP

#### Q. Which of the following is a core characteristic of TCP?

* [ ] Connectionless communication
* [x] Guaranteed data delivery
* [ ] No flow control mechanisms
* [ ] No error-checking capabilities

#### Q. What is the main benefit of TCP compared to UDP?

* [ ] Speed
* [x] Reliability
* [ ] Lower latency
* [ ] Simplicity

#### Q. What is the purpose of the TCP window size?

* [x] It controls how much data a sender can transmit before needing an acknowledgment from the receiver
* [ ] It determines the maximum number of TCP connections a server can handle
* [ ] It specifies the size of each individual TCP segment
* [ ] It sets the timeout value for retransmitting lost packets

#### Q. Which well-known port number is typically used by DNS for queries?

* [x] Port 53
* [ ] Port 80
* [ ] Port 443
* [ ] Port 25

#### Q. What happens when a UDP packet is lost during transmission?

* [x] It is not retransmitted because UDP does not provide delivery guarantees
* [ ] The receiver automatically requests a retransmission from the sender
* [ ] The packet is buffered at the nearest router until the path recovers
* [ ] UDP converts the lost packet into a TCP segment for reliable retry

#### Q. What is the purpose of a TCP RST (reset) packet?

* [x] To abruptly terminate an existing connection or reject an unwanted connection attempt
* [ ] To request a retransmission of the most recent segment
* [ ] To acknowledge successful receipt of all outstanding data
* [ ] To negotiate a larger window size during the handshake

#### Q. How does the TCP header size compare to the UDP header size?

* [x] The TCP header is larger (typically 20 bytes or more) because it includes fields for sequencing, acknowledgment, and flow control, while the UDP header is fixed at 8 bytes
* [ ] Both headers are exactly the same size
* [ ] The UDP header is larger because it includes error-correction data
* [ ] TCP uses a variable-length header that is always smaller than UDP's
