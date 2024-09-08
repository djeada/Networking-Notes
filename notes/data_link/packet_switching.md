# Notes on Packet Switching

## Background
- **Circuit Switching vs Packet Switching**
  - Traditional telephone networks used **circuit switching**.
  - **Packet switching** was a revolutionary idea for building networks.
  - Nowadays, even most telephone networks are built on packet-switched networks.

### Circuit Switching
- It involves creating a dedicated communication path between two points for the duration of their conversation.
  
### Packet Switching
- Involves breaking down data into small packets and sending them individually.
- Videos covering this topic can be found on YouTube under "module" videos (1-5, 3-2, 3-3) and Lecture 6 from last year.

#### Advantages of Packet Switching
- More efficient use of the network infrastructure.
- Better handling of network failures.
- Scalability.

## Mechanics of Packet Switching
- **Components of Delay**:
  1. **Serialization (Packetization) Delay**: Time taken to convert data into packets.
  2. **Propagation Delay**: Time taken for data to travel across a link.
  3. **Queueing Delay**: Time a packet spends waiting in a queue before being processed.

### Calculating Delays
- Formulas and examples are available in last year's videos and this year's lecture slides.
- Practicing calculations without queueing delay initially is recommended.

### Variability in Round Trip Time (RTT)
- **Round Trip Time (RTT)**: Time taken for a packet to travel from source to destination and back.
- **Ping**: A program to measure RTT.
- **Jitter**: Variability in RTT.
  - Packetization delay is usually fixed on wired links but variable on wireless links.
  - Propagation delay could be variable if the route changes.
  - Queueing delay is the most common source of variability.

### Switches
- **Store and forward**: Must receive the entire packet before forwarding.
- **Cut-through**: Sends out bits as it receives them.

## Terminology

### Throughput
- Refers to the amount of data moved successfully from one place to another in a given time period.
- One should be able to calculate the possible throughput from a source to a destination.

### Latency
- Refers to the time taken for a packet to travel from source to destination.
- Factors contributing to higher/lower latency should be understood.
- Industries like high-frequency trading and real-time calls (e.g., Zoom, multiplayer gaming) are sensitive to latency.

## Supplemental Material
- **History of Networks** (3-1): Additional context on the evolution of network technologies.



# CIRCUIT SWITCHING VS. PACKET SWITCHING

| Circuit Switching                             | Packet Switching                           |
|-----------------------------------------------|--------------------------------------------|
| ➔ Three phases: 1) connection establishment 2) data transfer 3) connection release | ➔ Data can be transmitted directly (no need for establishment). |
| ➔ Each data unit will have an entire path address. | ➔ Each data unit will have the destination address; the intermediate path is decided by routers. |
| ➔ Circuit Switching is not a store and forward technique. The packet simply bypasses the queue of the router. | ➔ Packet switching is a store & forward technique, where the packets are stored, and algorithms applied on the best path. |
| ➔ The transmission of the packet is done by the source. | ➔ The transmission of data is done not only by the source but also by intermediate routers. |
| ➔ The delay between the data unit is uniform or same. | ➔ The delay between the data unit is variable. |
| ➔ Resource reservation is a feature. | ➔ Resources are sharable. |
| ➔ Wastage of resources are more. | ➔ Wastage of resources is less. |
| ➔ Congestion can occur during the connection establishment phase. | ➔ Congestion can occur during the data transfer phase. |
| ➔ It is not a fault tolerant technique because the packets cannot be diverted to other paths if the link is broken. | ➔ It is a fault-tolerant technique because the data can be diverted via other paths if the link is broken. |
| ➔ Reliable, used for long messages. Circuit switching is slow. | ➔ Unreliable, used for short messages. Packet switching is fast. |


