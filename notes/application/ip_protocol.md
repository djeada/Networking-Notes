
## IP Header
- Found at the beginning of an IP datagram, provides necessary information for routers and computers.
- Key fields in an **IPv4 header**:
  - **Version**: Indicates IP version (usually 4).
  - **IHL**: Length of the IP header.
  - **Total Length**: Length of the entire datagram.
  - **Time to Live (TTL)**: Limits the datagram's lifespan to prevent infinite looping.
  - **Protocol**: Specifies the type of data contained (ICMP, UDP, TCP, etc.).
  - **Checksum**: Ensures data integrity.
  - **Source Address**: Sender's IP address (32-bit for IPv4).
  - **Destination Address**: Receiver's IP address (32-bit for IPv4).
- The data sent after the header is referred to as the **IP payload**.
