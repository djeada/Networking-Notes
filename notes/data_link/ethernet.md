The Ethernet technology operates primarily at two layers of the OSI model:

    Data Link Layer (Layer 2):
        This layer is responsible for data transfer between network nodes within the same local area network (LAN). It involves the use of MAC addresses to identify nodes, the creation of Ethernet frames, and the forwarding of these frames within the network.

    Physical Layer (Layer 1):
        This layer deals with the physical connection between network nodes, including the electrical or optical properties of the transmission medium, and the speed at which data is transmitted over the network.
        
### 1. **Introduction to Ethernet Fundamentals**
   - **Objective**: Understand the basics of Ethernet technology and data forwarding in an Ethernet network.
   - **Topics Covered**:
     - Ethernet technology evolution and standards.
     - Ethernet specifics, such as MAC addresses and Ethernet frame structure.
     - The role of Ethernet switches and MAC address tables in forwarding frames.
     - Ethernet operation at the Data Link Layer and Physical Layer of the OSI model.

### 2. **Ethernet Technology Evolution**
   - **Historical Background**:
     - Introduced in the 1970s by Robert Metcalfe at Xerox Corporation, Palo Alto Research Center.
     - Formalized by the IEEE in the mid-1980s with the IEEE 802.3 standard.
   - **IEEE 802.3 Standard**:
     - Defines rules for configuring an Ethernet network.
     - Specifies interactions between Ethernet network elements.
     - Ensures compatibility between equipment and protocols from different vendors.

### 3. **Ethernet Performance and Adaptability**
   - **Throughput Evolution**:
     - Originally 10 Mbps, increased to 100 Mbps in the mid-1990s.
     - Currently supports up to 400 Gbps.
   - **Versatility**:
     - Suits various applications: home networks, corporate LANs, and data centers.
     - Supports unique requirements and protocols for different applications.
   - **Backward Compatibility**:
     - Ethernet has maintained backward compatibility while evolving to higher performance levels.

### 4. **Ethernet Node Identification: MAC Addresses**
   - **MAC Address**:
     - Unique identifier for network interfaces in a local network.
     - Assigned by the vendor and burned into the hardware.
   - **Structure of a MAC Address**:
     - 48 bits long, represented by 12 hexadecimal digits.
     - Consists of two halves:
       - **OUI (Organizationally Unique Identifier)**: First 6 digits.
       - **Serial Number**: Last 6 digits, assigned by the vendor.
   - **Vendor Registration**:
     - Vendors register with IEEE to be assigned an OUI.
   - **Identifying MAC Addresses**:
     - On Linux: Use the `ifconfig` command.
     - On Windows: Use the `ipconfig` command.

### 5. **Ethernet Frame Structure**
   - **Ethernet Frame Components**:
     - **Payload**: Protocol data unit received from the upper layer.
     - **Header**:
       - **Destination MAC Address**: Specifies the node for which the frame is intended.
       - **Source MAC Address**: Specifies the node sending the frame.
       - **Type/EtherType Field**: Indicates the upper layer protocol type (e.g., IPv4).
     - **Frame Check Sequence (FCS)**:
       - Added to the end of the frame.
       - Used to detect corrupted frames, which are typically dropped.
   - **Frame Size**:
     - Payload size ranges from 46 to 1,500 bytes.
     - Maximum Transmit Unit (MTU) defined as 1,500 bytes.
     - Frame size ranges from 64 to 1,518 bytes (including header and trailer).
     - **Jumbo Frames**: Payloads exceeding 1,500 bytes, not standard but supported by some vendors.

### 6. **Role of Ethernet Switches**
   - **Functionality**:
     - Connect Ethernet nodes with multiple ports.
     - Forward frames based on destination MAC addresses.
   - **MAC Address Tables**:
     - Store destination MAC address to exit port mappings.
     - Entries are dynamically learned and aged out after a defined time.
     - Static entries can be manually configured and are not aged out.
   - **Frame Forwarding**:
     - **Known Unicast Frames**: Forwarded based on matching MAC address table entries.
     - **Unknown Unicast Frames**: Flooded to all ports except the incoming port.
     - **Broadcast Frames**: Flooded to all nodes, identified by a MAC address with all bits set to one.
     - **Multicast Frames**: Traditionally flooded, identified by MAC addresses with the least significant bit of the first octet set to one.

### 7. **Ethernet in the OSI Model**
   - **Data Link Layer (Layer 2)**:
     - Responsible for data transfer over the physical medium.
     - Involves MAC addressing and Ethernet frame creation.
   - **Physical Layer (Layer 1)**:
     - Defines electrical or optical properties and transfer speed of the physical connection between network nodes.

### 8. **Switching vs. Routing**
   - **Layer 2 Switching**:
     - Operates at the Data Link Layer.
     - Forwarding based on MAC addresses.
   - **Layer 3 Routing**:
     - Operates at the Network Layer.
     - Forwarding based on IP addresses.
   - **Multi-layer Switching**:
     - Combines the functionality of switches and routers.
     - Provides flexibility in network design.
   - **Network Design Considerations**:
     - Whether to use Layer 2, Layer 3, or a combination depends on network requirements.

These notes provide a comprehensive overview of Ethernet fundamentals, covering its evolution, standards, operational layers, and how it functions within a network environment.
