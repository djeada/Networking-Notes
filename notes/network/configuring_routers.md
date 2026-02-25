# Configuring Routers

## Router Architecture Overview

```text
+-----------------------------------------------------------------------+
|                            Router                                     |
|                                                                       |
|   +----------+    +-------------+    +-----------+    +----------+    |
|   |   CPU    |    |   Memory    |    | Flash /   |    | Operating|    |
|   |          |    | (RAM/NVRAM) |    | Storage   |    | System   |    |
|   +----------+    +-------------+    +-----------+    +----------+    |
|                                                                       |
|   +---------+    +---------+    +---------+    +---------+            |
|   | WAN Port|    | LAN 1   |    | LAN 2   |    | LAN 3   |    ...    |
|   | (Public)|    |(Private)|    |(Private)|    |(Private)|            |
|   +----+----+    +----+----+    +----+----+    +----+----+            |
|        |              |              |              |                  |
+--------|--------------|--------------|--------------|------------------+
         |              |              |              |
     To ISP /       To internal devices (PCs, servers, APs)
     Internet
```

- **WAN port**: Connects to the ISP / public internet.
- **LAN ports**: Connect to devices on the private network.
- **CPU / Memory**: Processes routing decisions, NAT translations, and firewall rules.
- **Flash / NVRAM**: Stores the operating system (e.g., Cisco IOS) and configuration files.

---

## **Device Protection Methods**
Protecting your device from unwanted access can be achieved through several methods:

### **1. Limiting Privileged Mode Access**
- Restrict access to privileged exec mode.
- Example:
    ```bash
    Router> enable
    Router# conf terminal
    Router(config)# enable secret ultrasecretpassword
    Router(config)# exit
    ```

### **2. Restricting Console Access**
- Control access to the device via console.
- Example:
    ```bash
    Router> enable
    Router# conf terminal
    Router(config)# line console 0
    Router(config-line)# password ultrasecretpassword
    Router(config-line)# login
    Router(config-line)# exit
    ```

### **3. Restricting SSH / TTY Access**
- Limit access via SSH or TTY.
- Example:
    ```bash
    Router> enable
    Router# conf terminal
    Router(config)# line vty 0 15
    Router(config-line)# password ultrasecretpassword
    Router(config-line)# login
    ```

### **4. Encrypting Passwords**
- Encrypt plaintext passwords stored in configuration files.
- Example:
    ```bash
    Router> enable
    Router# conf terminal
    Router(config)# service password-encryption
    Router(config)# exit
    ```

### **5. Modifying Banners**
- Change the Message of the Day (MotD) to notify users.
- Example:
    ```bash
    Router> enable
    Router# conf terminal
    Router(config)# banner motd "Pls dont hack me!"
    ```

### **6. Managing Configurations**
- **Viewing Configurations**
    ```bash
    Router> enable
    Router# show running-config
    Router# show startup-config
    ```
- **Saving Configurations**
    ```bash
    Router> enable
    Router# copy running-config startup-config
    ```
- **Reloading Configurations**: Use `reload` command to revert to a saved state. Beware it momentarily turns off the device.
- **Deleting Configurations**: `delete startup-config` and `wipe` commands remove configurations.
- **Overriding Configurations**: If unsaved changes are made, revert to the old configuration.
    ```bash
    Router> enable
    Router# copy startup-config running-config
    ```

## **Router Traffic Differentiation**

### **1. User Construct**
- The user defines private and public networks.
- Rules and configurations are set accordingly.

### **2. Firewall and NAT**
- **Public Network**: ISP connected on one side.
- **Private Network**: Personal networks on the other side.
- **NAT and Firewall Rules**: Control inbound and outbound traffic.

### **3. WAN Port**
- Consumer hardware routers have a "wan" port to identify the public network.

### **4. Ports and Routing**
- Routers use ports to identify connections and route messages accordingly.

### **5. Experimentation**
- Using tools like pfSense in a virtual environment can aid in understanding routing and firewall concepts.

### **Conclusion**
- Effective device protection and correct router configurations ensure secure and efficient network communication.

---

## Basic Routing Concepts

### Static vs Dynamic Routing

Routers determine how to forward packets using a **routing table**. Routes can be configured manually (static) or learned automatically (dynamic).

| Feature            | Static Routing                             | Dynamic Routing                             |
|--------------------|--------------------------------------------|---------------------------------------------|
| **Configuration**  | Manually entered by an administrator       | Automatically learned via routing protocols  |
| **Adaptability**   | Does not adapt to network changes          | Adapts to topology changes automatically     |
| **Overhead**       | No protocol overhead                       | Uses CPU/bandwidth for route advertisements  |
| **Use Case**       | Small networks, default routes, stub networks | Large, complex, or frequently changing networks |
| **Protocols**      | N/A                                        | RIP, OSPF, EIGRP, BGP                       |
| **Security**       | More secure (no route advertisements)      | Routes can be poisoned if not secured        |

**Static route example (Cisco IOS)**:
```bash
Router> enable
Router# conf terminal
Router(config)# ip route 10.0.2.0 255.255.255.0 192.168.1.1
```

This tells the router: "To reach the `10.0.2.0/24` network, forward packets to the next-hop address `192.168.1.1`."

### How a Router Forwards a Packet

1. A packet arrives on an interface.
2. The router examines the **destination IP** in the packet header.
3. It looks up the destination in its **routing table** to find the best matching route.
4. The packet is forwarded out the appropriate interface toward the next hop.
5. If no route matches, the packet is sent to the **default route** (if configured) or dropped.
