# Network Topologies

## Introduction

A **network topology** defines how devices (nodes) in a network are arranged and connected. There are two categories of topology:

- **Physical Topology** — The actual physical layout of cables and devices.
- **Logical Topology** — The way data flows through the network, regardless of the physical layout.

Understanding topologies is critical for designing networks that meet requirements for cost, reliability, scalability, and performance.

---

## 1. Mesh Topology

### Explanation

In a **Mesh Topology**, every device on the network is connected to every other device. This creates multiple pathways for data to travel, enhancing reliability and redundancy.

### Characteristics

- **Robustness:** If one link fails, data can take an alternate path.
- **Expensive to Cable:** A large number of cables and I/O ports are required.
- **Complex to Implement:** Best suited for smaller networks or critical backbone connections.
- **High Redundancy:** No single point of failure.

### Links Calculation

If there are N devices, the total number of links required is:

    Links = N * (N - 1) / 2

For example, 4 devices require 4 * 3 / 2 = 6 links. Each device needs (N - 1) ports.

### Diagram

```text
        [A]------------------[B]
        /|\                  /|
       / | \                / |
      /  |  \              /  |
     /   |   \            /   |
    /    |    \          /    |
  [C]----+-----\-------[D]   |
    \    |      \        |   |
     \   |       \       |  /
      \  |        \      | /
       \ |         \     |/
        [E]---------\---[F]
```

> In a full mesh with 6 devices: Links = 6 * 5 / 2 = 15

---

## 2. Bus Topology

### Explanation

In a **Bus Topology**, all devices share a single communication line or cable known as the **backbone**. Each device taps into the backbone via a drop line.

### Characteristics

- **Easy to Install:** Requires less cabling compared to mesh and star topologies.
- **Cost-Effective:** Economical for small networks.
- **Limited Data Traffic:** If multiple devices transmit simultaneously, data collisions occur.
- **Single Point of Failure:** If the backbone cable fails, the entire network goes down.
- **Terminators Required:** Both ends of the backbone must be terminated to prevent signal reflection.

### Links Calculation

If N devices are connected, only 1 backbone cable and N drop lines are required.

### Diagram

```text
  Terminator                                              Terminator
      |                                                       |
      |====[A]========[B]========[C]========[D]========[E]====|
             |          |          |          |          |
          Drop Line  Drop Line  Drop Line  Drop Line  Drop Line

  Signal Direction --->
  <--- Signal Direction (bidirectional)
```

---

## 3. Star Topology

### Explanation

In a **Star Topology**, all devices are connected to a central device (hub, switch, or router). All communication passes through the central node.

### Characteristics

- **Easy to Install and Manage:** Adding or removing devices is simple.
- **Centralized Monitoring:** The central device can monitor all traffic.
- **Single Point of Failure:** If the central device fails, the whole network is inoperable.
- **Easy Troubleshooting:** A failed link only affects one device.

### Links Calculation

If N devices are connected, then N cables are required (one per device to the central hub).

### Diagram

```text
            [A]         [B]
              \         /
               \       /
                \     /
                 \   /
              [HUB/SWITCH]
                 / | \
                /  |  \
               /   |   \
              /    |    \
            [C]   [D]   [E]
```

---

## 4. Ring Topology

### Explanation

In a **Ring Topology**, each device is connected to exactly two other devices, forming a closed loop. Data travels in one direction (unidirectional) or both directions (dual ring).

### Characteristics

- **Predictable Routing:** Data passes through each node sequentially.
- **Easy to Install:** Each device is linked only to its immediate neighbors.
- **Low Collision:** Only one device transmits at a time using a token.
- **Difficult Troubleshooting:** A single device failure can disrupt the entire ring (unless dual ring is used).

### Diagram

```text
  Unidirectional Ring:              Dual Ring (Bidirectional):

        [A]                              [A]
       /   \                            // \\
      /     \                          //   \\
    [E]     [B]                      [E]     [B]
     |       |                        ||     ||
     |       |                        ||     ||
    [D]     [C]                      [D]     [C]
       \   /                           \\  //
        \ /                             \\//
        [F]                              [F]

  ---> Token direction           ---> and <--- both directions
```

---

## 5. Tree (Hierarchical) Topology

### Explanation

A **Tree Topology** combines characteristics of star and bus topologies. It has a hierarchical structure with a root node at the top, and all other nodes arranged in levels below it.

### Characteristics

- **Scalable:** Easy to add new branches and devices.
- **Hierarchical Management:** Network management mirrors organizational structure.
- **Dependent on Root:** If the root node or backbone fails, large sections of the network go down.
- **Used in WANs:** Common in large enterprise and wide area networks.

### Diagram

```text
                      [Root Switch]
                       /         \
                      /           \
              [Switch A]        [Switch B]
              /   |   \          /   |   \
             /    |    \        /    |    \
           [A1] [A2]  [A3]   [B1] [B2]  [B3]
                  |                  |
               [Switch C]        [Switch D]
               /       \         /       \
             [C1]     [C2]     [D1]     [D2]
```

---

## 6. Hybrid Topology

### Explanation

A **Hybrid Topology** is a combination of two or more different topologies. Most real-world enterprise networks use hybrid topologies to leverage the strengths of each individual topology.

### Characteristics

- **Flexible:** Can be designed to meet specific needs.
- **Scalable:** Different segments can use different topologies.
- **Complex:** More difficult to design and manage.
- **Expensive:** Combines costs from multiple topology types.

### Diagram

```text
          Star Segment                   Ring Segment
          -----------                    ------------
         [A]   [B]                         [R1]
           \   /                          /    \
         [Switch 1]---Backbone---[Switch 2]    [R2]
           / \                          \    /
         [C] [D]                         [R3]
                  \                  /
                   \                /
                  [Router]----------
                     |
                     |
              [Switch 3]
              /    |    \
            [E]  [F]   [G]
            Bus/Star Segment
```

---

## Comparison Table

| Topology   | Cost       | Reliability     | Scalability | Ease of Troubleshooting |
|------------|------------|-----------------|-------------|-------------------------|
| Mesh       | Very High  | Very High       | Poor        | Easy (redundant paths)  |
| Bus        | Very Low   | Low             | Poor        | Difficult               |
| Star       | Moderate   | Moderate        | Good        | Easy                    |
| Ring       | Low        | Low to Moderate | Poor        | Difficult               |
| Tree       | Moderate   | Moderate        | Very Good   | Moderate                |
| Hybrid     | High       | High            | Very Good   | Moderate to Difficult   |

