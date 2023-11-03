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

## Recommended Resources
- Last year's module videos on YouTube and Lecture 6 on CS144 Canvas site.
- Current year's lecture slides for additional explanations and examples.

