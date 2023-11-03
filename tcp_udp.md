
## UDP Protocol
- In the IP packet payload, an identifier (port) is included to identify the target application.
- **UDP Header** contains a destination port number, telling the machine which program to forward the packet to.
- **OS** maintains a mapping of port numbers and protocols to open sockets.

### UDP: Client vs Server
- **Client UDP Socket**: OS chooses a unique port number when connecting to a remote server.
- **Server UDP Socket**: You choose a socket, bind to it, and then listen for incoming packets addressed to the IP address + port combo.
- Clients need to know the server socket's IP address + port combo to address packets correctly.

## Transport Layer
- Understanding of the **transport layer** (part of the 4-layer network model) is crucial.
- Key differences between **TCP** and **UDP** should be understood.

## Overview
- **TCP** provides a reliable byte stream over an unreliable Internet.
- Utilizes **sequence numbers** to order bytes and ensure data integrity.
- Uses **checksums** to protect against errors introduced by the network.

## TCP vs. UDP
- Both are transport layer protocols.
- **TCP** is more reliable; **UDP** is faster but less reliable.

## TCP Header
- Contains information such as sequence numbers, SYN, ACK, and window size.

## TCP Connection Process
1. **SYN (Synchronize)**
   - Initiates a byte stream.
   - First packet in the byte stream sets the SYN bit.
2. **ACK (Acknowledgment)**
   - Indicates the next expected sequence number.
3. **Window Size**
   - Specifies how many bytes a sender is willing to receive at once.
4. **FIN (Finished)**
   - Indicates the end of the byte stream.

## Example TCP Connection
### Keith -> Student
- **Sequence number**: 0 (initial)
- **Data**: "Hello."
- **SYN**: Set (start of byte stream)
- **Window size**: 1000 (bytes willing to receive at once)

### Student -> Keith
- **Sequence number**: 5000 (initial)
- **SYN**: Set (start of byte stream)
- **Data**: "Hi!"
- **ACK**: 7 (next expected sequence number from Keith)
- **Window size**: 100 (bytes willing to receive at once)

### Notes
- **SYN** occupies a sequence number.
- **ACK 7** means: received data up to sequence number 6; expecting 7 next.
- Sequence numbers: 1 = H, 2 = E, 3 = L, 4 = L, 5 = O, 6 = ., 7 = expected next.

### Ending the Connection
#### Keith -> Student
- **Sequence number**: 7
- **Data**: "Bye"
- **FIN**: Set (end of byte stream)
- **ACK**: 5004 (next expected sequence number from Student)
- **Window**: 1000

#### Student -> Keith
- **Sequence number**: 5004
- **Data**: "Where?"
- **ACK**: 11 (next expected sequence number from Keith)
- **Window**: 100

#### Keith -> Student
- **Sequence number**: 11
- **Data**: ""
- **ACK**: 5011 (next expected sequence number from Student)
- **Window**: 1000

#### Student -> Keith
- **Sequence number**: 5011
- **Data**: "CU"
- **FIN**: Set (end of byte stream)
- **ACK**: 11 (next expected sequence number from Keith)
- **Window**: 500

## Additional Features
- Some applications implement additional features over TCP for extra reliability.
  - **Example**: HTTPS uses encryption over TCP; file transfer applications validate file hashes.

