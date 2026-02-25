# Port Forwarding

**Port forwarding** is a NAT technique that redirects incoming network traffic from a specific port on a router's public IP address to a specific device and port on the private network. Without port forwarding, devices behind a NAT router are unreachable from the internet.

---

## How Port Forwarding Works

```text
  Internet                          Router                       Private Network
  +------------+              +------------------+           +---------------------+
  |            |   request    | Public IP         |  forward  | 192.168.1.10        |
  | Client     |------------->| 82.62.51.70:80   |---------->| :80 (Web Server)    |
  | (anywhere) |              |                   |           +---------------------+
  |            |   request    |                   |  forward  | 192.168.1.20        |
  |            |------------->| 82.62.51.70:2222 |---------->| :22 (SSH Server)    |
  |            |              |                   |           +---------------------+
  |            |   request    |                   |  forward  | 192.168.1.30        |
  |            |------------->| 82.62.51.70:25565|---------->| :25565 (Game Server)|
  +------------+              +------------------+           +---------------------+
                              (Port forwarding rules
                               configured here)
```

Consider a web server at `192.168.1.10:80` on a private network. Only devices on the same network can reach it (an **intranet**). By adding a port forwarding rule on the router, external clients can access the web server via the router's public IP `82.62.51.70:80`. The router forwards incoming traffic on port 80 to `192.168.1.10:80`.

Port forwarding is configured at the **router** of a network.

---

## Use Cases

- **Hosting web servers**: Make a local web application accessible from the internet.
- **Gaming**: Host game servers that friends can connect to remotely.
- **Remote access**: Enable SSH or Remote Desktop connections to an internal machine.
- **Security cameras**: Access IP camera feeds from outside the local network.
- **File sharing**: Run FTP or other file-sharing services reachable externally.

---

## Setup Process

1. **Assign a static IP** to the target device (or use a DHCP reservation) so its address does not change.
2. **Log in to the router's** administration interface (typically at `192.168.1.1` or `192.168.0.1`).
3. **Navigate to the port forwarding section** (may be called "Virtual Servers", "NAT", or "Port Forwarding").
4. **Create a rule** specifying:
   - **External port**: The port on the public IP that receives traffic.
   - **Internal IP**: The private IP of the target device.
   - **Internal port**: The port the target device is listening on.
   - **Protocol**: TCP, UDP, or both.
5. **Save and apply** the configuration.
6. **Test** by connecting from an external network to the router's public IP and specified port.

---

## Port Forwarding vs Firewall

It is easy to confuse port forwarding with firewall behavior. They serve different purposes:

| Feature            | Port Forwarding                                  | Firewall                                          |
|--------------------|--------------------------------------------------|---------------------------------------------------|
| **Function**       | Opens and redirects specific ports to internal devices | Determines whether traffic is allowed or blocked |
| **Scope**          | Defines where traffic goes                       | Defines whether traffic can flow at all           |
| **Interaction**    | Port forwarding opens the path                   | Firewall rules may still block forwarded traffic  |

A port can be forwarded but still blocked by a firewall. Both must be configured for external access to work.

---

## Security Considerations

- **Minimize exposed ports**: Only forward the ports you actually need.
- **Use non-standard ports**: Forwarding SSH on port 2222 instead of 22 reduces automated scanning hits (security through obscurity — not a substitute for strong authentication).
- **Keep services updated**: Any service exposed to the internet must be patched and maintained.
- **Use strong authentication**: Ensure forwarded services require strong passwords or key-based authentication.
- **Monitor logs**: Watch for unauthorized access attempts on forwarded ports.
- **Consider alternatives**: A VPN may be safer than port forwarding for remote access, as it avoids exposing individual services directly.
