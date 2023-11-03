
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
