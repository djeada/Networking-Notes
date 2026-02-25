
1. **What mechanism does TCP employ to regulate the flow of data between sender and receiver?**
   - Flow Control
   - Checksum
   - Sequence Numbers
   - Port Numbering

2. **Which protocol is better suited for real-time applications such as video streaming or online gaming?**
   - TCP
   - UDP
   - HTTP
   - HTTPS

3. **Which of the following protocols is connectionless and does not ensure packet delivery?**
   - TCP
   - UDP
   - FTP
   - SMTP

4. **In which protocol are transmitted data units referred to as segments?**
   - TCP
   - UDP
   - ICMP
   - FTP

5. **What does the abbreviation UDP stand for?**
   - Universal Datagram Protocol
   - User Datagram Protocol
   - Unified Data Packet
   - Unicast Data Protocol

6. **Which protocol would you most likely choose for transferring a large file over the internet when data integrity is essential?**
   - TCP
   - UDP
   - TFTP
   - SNMP

7. **Which protocol guarantees reliable data delivery by setting up a connection before transmitting any data?**
   - TCP
   - UDP
   - ICMP
   - ARP

8. **Which of the following protocols relies on port 80 by default?**
   - TCP
   - UDP
   - ICMP
   - ARP

9. **What is the primary reason UDP is preferred over TCP for certain use cases?**
   - Reduced overhead and faster data transmission
   - Stronger security guarantees
   - Reliable delivery of every packet
   - Simpler implementation across all platforms

10. **Which protocol initiates a connection using a three-way handshake?**
    - TCP
    - UDP
    - ICMP
    - ARP

11. **Which of the following is a core characteristic of TCP?**
    - Connectionless communication
    - Guaranteed data delivery
    - No flow control mechanisms
    - No error-checking capabilities

12. **What is the main benefit of TCP compared to UDP?**
    - Speed
    - Reliability
    - Lower latency
    - Simplicity

13. **What is the purpose of the TCP window size?**
    - It controls how much data a sender can transmit before needing an acknowledgment from the receiver
    - It determines the maximum number of TCP connections a server can handle
    - It specifies the size of each individual TCP segment
    - It sets the timeout value for retransmitting lost packets

14. **Which well-known port number is typically used by DNS for queries?**
    - Port 53
    - Port 80
    - Port 443
    - Port 25

15. **What happens when a UDP packet is lost during transmission?**
    - It is not retransmitted because UDP does not provide delivery guarantees
    - The receiver automatically requests a retransmission from the sender
    - The packet is buffered at the nearest router until the path recovers
    - UDP converts the lost packet into a TCP segment for reliable retry

16. **What is the purpose of a TCP RST (reset) packet?**
    - To abruptly terminate an existing connection or reject an unwanted connection attempt
    - To request a retransmission of the most recent segment
    - To acknowledge successful receipt of all outstanding data
    - To negotiate a larger window size during the handshake

17. **How does the TCP header size compare to the UDP header size?**
    - The TCP header is larger (typically 20 bytes or more) because it includes fields for sequencing, acknowledgment, and flow control, while the UDP header is fixed at 8 bytes
    - Both headers are exactly the same size
    - The UDP header is larger because it includes error-correction data
    - TCP uses a variable-length header that is always smaller than UDP's
