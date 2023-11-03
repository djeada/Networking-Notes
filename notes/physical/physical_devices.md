# Differences between Hub, Switch, and Router

Understanding the differences between a **Hub**, **Switch**, and **Router** is essential for grasping network functionalities.

## **Hub**
- **Layer**: Physical Layer Device.
- **Functionality**: Hubs simply repeat the signal to all ports.
- **Connection**: Connects devices within a single Local Area Network (LAN).
- **Collision Domain**: The [collision domain](https://en.wikipedia.org/wiki/Collision_domain) of all hosts connected through a Hub remains one, i.e., signals sent by any two devices can collide.

## **Switch**
- **Layer**: Data Link Layer Device.
- **Functionality**: Switches don't just repeat but filter content by Media Access Control (MAC) or LAN address.
- **Connection**: Can connect multiple sub-LANs within a single LAN.
- **Domains**:
  - **Collision Domain**: Switch divides the collision domain.
  - **Broadcast Domain**: The [broadcast domain](https://en.wikipedia.org/wiki/Broadcast_domain) of connected devices remains the same.

## **Router**
- **Layer**: Network Layer Device.
- **Functionality**: Routers direct data based on IP address.
- **Connection**: Connect multiple LANs and Wide Area Networks (WANs) together.
- **Domains**: Routers divide both collision and broadcast domains.

## **Summary**
- **Hub**: A basic repeater that doesn't filter or differentiate signals, leading to possible collisions.
- **Switch**: An intelligent device that filters and directs data within a LAN, reducing collisions.
- **Router**: A more advanced device that directs data between different networks and divides both collision and broadcast domains.
