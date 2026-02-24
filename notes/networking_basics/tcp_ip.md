## Network Stack: Abstraction and Layering
- **Byte stream**: A sequence of bytes that can be written to and read from.
- The internet allows building abstractions over others, forming a **network stack**.
- **4-layer Internet Model**:
  1. **Link Layer**: Ethernet, WiFi, etc.
  2. **Network Layer**: IP.
  3. **Transport Layer**: TCP, UDP.
  4. **Application Layer**: HTTP, FTP, etc.
- Layers are isolated and communicate with their corresponding layers at the destination host.
- **7-layer OSI model** exists but hasn't been covered yet.
The TCP/IP Model
----- 

| Name | Description |
|:----:|:----|
| Application | Represents data to the user, plus encoding and dialog control |
| Transport | Supports communications between various devices across diverse networks |
| Internet | Determines the best path through the network |
| Network Access | Controls the hardware devices and media that make up the network |
