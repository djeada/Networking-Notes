
The OSI Reference Model
----

| Layer | Description|
|:-------:|:------------|
| Application | Contains protocols used for process to process communications |
| Presentation | Provides for common representation of the data transferred between application layer services |
| Session | Provides services to the presentation layer to organize its dialogue and to manage data exchange |
| Transport | Defines services to segment, transfer and reassemble the data for individual communications between end devices |
| Network | Provides services to exchange individual pieces of data over the network between identified devices |
| Data Link | Describes methods for exchanging data frames between devices over a common media |
| Physical | Describes the mechanical, electrical, functional and procedural means to activate, maintain and deactivate physical connections for bit transmission to and from a network device |




# Notes on OSI Model Layers

## Overview
- **OSI Model**: A theoretical stack of seven layers for understanding network operations.
- Introduced to standardize networks and enable multi-vendor systems.
- While OSI model is a reference, **TCP/IP model** is more commonly used with similar concepts but slightly different layers.

## Layers in OSI Model

### **Layer 1: Physical Layer**
- **Function**: Converts data bits into electrical impulses.
- **Components**: Physical hardware, e.g., ethernet cables.
- **Examples**:
  - Are all cables plugged in?
  - Is the network card functioning?
  - Could it be a faulty cable?

### **Layer 2: Data Link Layer**
- **Function**: Encodes and decodes data packets into bits; adds physical addresses (MAC addresses).
- **Components**: Switches operate at this layer.
- **Examples**:
  - Maybe the switch has gone bad?

### **Layer 3: Network Layer**
- **Function**: Handles IP addressing, routing, and transfer of datagrams.
- **Components**: Routers operate at this layer.
- **Examples**:
  - Is the router functioning?
  - Do I have the right IP address?

### **Layer 4: Transport Layer**
- **Function**: Responsible for data transfer and adds transport protocols (TCP/UDP), source/destination port numbers.
- **Examples**:
  - Could the internet card be functional?

### **Layer 5: Session Layer**
- **Function**: Manages and controls signals; responsible for establishing and terminating connections between devices.
- **Examples**:
  - Are you connecting to the correct address?

### **Layer 6: Presentation Layer**
- **Function**: Transforms data into the application layer format; can encrypt and decrypt data if needed.
- **Examples**:
  - Are you reading the data in the same order that you wrote it?

### **Layer 7: Application Layer**
- **Function**: End users interact at this layer; involves application communication.
- **Components**: Applications like SMTP for email.
- **Examples**:
  - Is the application erroring out?

## Conclusion
- The OSI model is a reference tool to understand how different network components interact.
- Despite not being used explicitly, its concepts are reflected in the TCP/IP model.


