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
