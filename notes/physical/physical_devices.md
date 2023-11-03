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

<h2>Switch</h2>
A switch can be used to link many computers in a network.
To link all of the computers to the switch, we can utilize copper wires or faster fiber optic connections.
Copper cables are classified into two types: CAT-5 and CAT-6.
No wirless connection.
Category 6 allows for faster transmission of data.
Switches are used to build a LAN network.
The switch has ports on it that are known as LAN ports. 

<h2>Access points</h2>

A device with functions similar to swtich. Uses wirless connection.
