
## Internet Abstraction: Datagrams
- The internet provides the abstraction of **datagrams** for communication.
- **Reliability** is built on top of what the internet provides, explored more in later lectures.

### What is in a Datagram?
- "To" and "From" addresses:
  - IPv4: 32 bits (most common).
  - IPv6: 128 bits (emerged due to exhaustion of IPv4 addresses).
- Data payload (usually less than 1.5 KB).

### Datagram Delivery: Best-Effort
- Datagrams are delivered with "best effort", meaning:
  1. Delivered quickly (ideal).
  2. Delivered but with corrupted data.
  3. Delivered late or out of order.
  4. Delivered to or from the wrong address.
  5. Not delivered at all.
  6. Delivered with tampered data (maliciously).
  7. Delivered multiple times.
- This approach allows flexibility and minimal guarantees.



### Datagram Loop Prevention
- Datagrams have a **TTL (Time To Live)** field to prevent infinite looping.
- TTL is decremented at each router; if TTL=0, the datagram is dropped.
- **Traceroute** utilizes the TTL field to trace the path of a packet.


## Internet Datagram vs User Datagram
- **Internet Datagram**:
  - Conceptually travels machine to machine.
  - **IP** (Internet Protocol) is the protocol used here.
- **User Datagram**:
  - Conceptually travels from application to application.
  - **UDP** (User Datagram Protocol) is the protocol used here.

## Dot-Decimal Notation
- **IPv4 addresses**:
  - Composed of 32 bits or 4 bytes.
  - **Dot-decimal notation**: Represents each byte as a number separated by dots (e.g., `192.168.1.1`).

## Encapsulation and Layers
- **Encapsulation**:
  - Packets are like nested envelopes with headers of different layers.
- **Layers**:
  - Each layer communicates with its peer(s) at the same layer (e.g., routers talk to routers).
  - Layers care about specific headers in the nested envelopes.
  - Examples:
    - **Internet Datagram**: IP header + payload.
    - **User Datagram**: UDP header + payload (nested inside Internet Datagram).
    - **Application Data**: Nested inside user datagram.
- **Header Examination**:
  - Routers examine the IP header for destination addresses, checksum, and TTL.
  - OS Kernel examines user datagram header for port information.
  - Applications examine the data within the user datagram.

## Reliable Applications on Unreliable Datagram Service
- **Example**: DNS (Domain Name System) maps hostnames to IP addresses.
  - **Application Layer**: DNS
  - **Transport Layer**: UDP
  - **Internet Layer**: IP
