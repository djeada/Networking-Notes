# ip and ifconfig — Network Interface Configuration

`ip` and `ifconfig` are the primary tools for configuring and inspecting network interfaces on Linux. `ip` is the modern replacement for `ifconfig` and provides a unified interface for addresses, routes, neighbors (ARP), and links.

---

## Quick Comparison

| Task                         | `ip` (modern)                            | `ifconfig` (legacy)               |
|:-----------------------------|:-----------------------------------------|:----------------------------------|
| Show all interfaces          | `ip link show`                           | `ifconfig -a`                     |
| Show interface with IP       | `ip addr show`                           | `ifconfig`                        |
| Show a specific interface    | `ip addr show eth0`                      | `ifconfig eth0`                   |
| Bring interface up           | `ip link set eth0 up`                    | `ifconfig eth0 up`                |
| Bring interface down         | `ip link set eth0 down`                  | `ifconfig eth0 down`              |
| Set IP address               | `ip addr add 192.168.1.5/24 dev eth0`   | `ifconfig eth0 192.168.1.5 netmask 255.255.255.0` |
| Remove IP address            | `ip addr del 192.168.1.5/24 dev eth0`   | (not directly supported)          |
| Show routing table           | `ip route show`                          | `netstat -r` / `route -n`         |
| Add a route                  | `ip route add 10.0.0.0/8 via 192.168.1.1`| `route add -net 10.0.0.0/8 gw 192.168.1.1` |
| Show ARP table               | `ip neigh show`                          | `arp -n`                          |
| Set MAC address              | `ip link set eth0 address AA:BB:CC:DD:EE:FF` | `ifconfig eth0 hw ether AA:BB:CC:DD:EE:FF` |

---

## ip — Modern Network Configuration

The `ip` command is part of the `iproute2` package. Its sub-commands cover different aspects of networking:

| Sub-command  | Abbreviation | Purpose                                            |
|:-------------|:-------------|:---------------------------------------------------|
| `ip link`    | `ip l`       | Network interfaces (physical attributes)           |
| `ip addr`    | `ip a`       | IP addresses assigned to interfaces                |
| `ip route`   | `ip r`       | Routing table                                      |
| `ip neigh`   | `ip n`       | ARP / Neighbour table                              |
| `ip tunnel`  |              | Tunnels (GRE, IPIP, etc.)                         |
| `ip maddr`   |              | Multicast addresses                                |
| `ip rule`    |              | Policy routing rules                               |

---

## Viewing Interfaces and Addresses

```bash
# Show all interfaces and their link-layer state
ip link show

# Short form
ip l

# Show a specific interface
ip link show eth0

# Show all interfaces with their IP addresses
ip addr show
ip a               # shorthand

# Show a specific interface
ip addr show eth0
ip a show eth0
```

### Example Output

```text
$ ip addr show eth0
2: eth0: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc fq_codel state UP group default qlen 1000
    link/ether 52:54:00:ab:cd:ef brd ff:ff:ff:ff:ff:ff
    inet 192.168.1.5/24 brd 192.168.1.255 scope global dynamic eth0
       valid_lft 86340sec preferred_lft 86340sec
    inet6 fe80::5054:ff:feab:cdef/64 scope link
       valid_lft forever preferred_lft forever
```

| Field          | Meaning                                                         |
|:---------------|:----------------------------------------------------------------|
| `BROADCAST`    | Interface supports broadcast                                    |
| `MULTICAST`    | Interface supports multicast                                    |
| `UP`           | Interface is administratively enabled                           |
| `LOWER_UP`     | Physical link is up (cable connected)                           |
| `mtu 1500`     | Maximum Transmission Unit in bytes                              |
| `state UP`     | Operational state                                               |
| `link/ether`   | MAC (hardware) address                                          |
| `inet`         | IPv4 address with prefix length                                 |
| `inet6`        | IPv6 address                                                    |
| `scope global` | Address is globally routable                                    |
| `scope link`   | Address is only valid on this link (link-local)                 |
| `dynamic`      | Address was assigned via DHCP                                   |

---

## Managing Interfaces

```bash
# Bring an interface up
sudo ip link set eth0 up

# Bring an interface down
sudo ip link set eth0 down

# Change MTU
sudo ip link set eth0 mtu 9000

# Change MAC address (interface must be down first)
sudo ip link set eth0 down
sudo ip link set eth0 address AA:BB:CC:DD:EE:FF
sudo ip link set eth0 up
```

---

## Managing IP Addresses

```bash
# Add an IPv4 address
sudo ip addr add 192.168.1.10/24 dev eth0

# Add a second IP (alias)
sudo ip addr add 192.168.1.20/24 dev eth0

# Remove an IP address
sudo ip addr del 192.168.1.10/24 dev eth0

# Add an IPv6 address
sudo ip addr add 2001:db8::1/64 dev eth0

# Flush all addresses from an interface
sudo ip addr flush dev eth0
```

---

## Routing Table

```bash
# Show the routing table
ip route show
ip r                    # shorthand

# Show the route for a specific destination
ip route get 8.8.8.8

# Add a static route
sudo ip route add 10.0.0.0/8 via 192.168.1.1

# Add a route via a specific interface
sudo ip route add 192.168.2.0/24 dev eth1

# Delete a route
sudo ip route del 10.0.0.0/8

# Set / change the default gateway
sudo ip route add default via 192.168.1.1
sudo ip route del default
sudo ip route replace default via 192.168.1.254
```

### Example Routing Table

```text
$ ip route show
default via 192.168.1.1 dev eth0 proto dhcp src 192.168.1.5 metric 100
192.168.1.0/24 dev eth0 proto kernel scope link src 192.168.1.5
10.0.0.0/8 via 192.168.1.1 dev eth0
```

| Column          | Meaning                                                         |
|:----------------|:----------------------------------------------------------------|
| `default`       | Default gateway (matches all destinations not in other routes) |
| `via 192.168.1.1` | Next-hop router                                               |
| `dev eth0`      | Send via this interface                                         |
| `proto kernel`  | Route was installed by the kernel (auto-generated)             |
| `scope link`    | Destination is directly connected (no next hop needed)         |
| `metric 100`    | Route preference — lower metric is preferred                   |

---

## ARP / Neighbour Table

```bash
# Show ARP (IPv4 neighbor) table
ip neigh show
ip n

# Show IPv6 neighbors
ip -6 neigh show

# Add a static ARP entry
sudo ip neigh add 192.168.1.50 lladdr AA:BB:CC:DD:EE:FF dev eth0

# Delete an ARP entry
sudo ip neigh del 192.168.1.50 dev eth0

# Flush the ARP cache
sudo ip neigh flush dev eth0
```

---

## Making Changes Persistent

Changes made with `ip` commands are **temporary** and lost on reboot. To make them permanent:

### Debian/Ubuntu (netplan)

```yaml
# /etc/netplan/01-netcfg.yaml
network:
  version: 2
  ethernets:
    eth0:
      addresses:
        - 192.168.1.10/24
      routes:
        - to: default
          via: 192.168.1.1
      nameservers:
        addresses: [8.8.8.8, 8.8.4.4]
```

```bash
sudo netplan apply
```

### RHEL/CentOS/Fedora (NetworkManager)

```bash
nmcli con mod eth0 ipv4.addresses 192.168.1.10/24
nmcli con mod eth0 ipv4.gateway 192.168.1.1
nmcli con mod eth0 ipv4.method manual
nmcli con up eth0
```

---

## ifconfig — Legacy Reference

`ifconfig` is still found on many systems (especially macOS and older Linux). It is read-only on modern systems when `net-tools` is not installed.

```bash
# Show all interfaces
ifconfig -a
ifconfig           # only shows active interfaces

# Show a specific interface
ifconfig eth0

# Assign a static IP
sudo ifconfig eth0 192.168.1.10 netmask 255.255.255.0

# Bring interface up/down
sudo ifconfig eth0 up
sudo ifconfig eth0 down

# Set MTU
sudo ifconfig eth0 mtu 9000
```

### macOS Differences

```bash
# List all interfaces (macOS uses en0, en1, etc.)
ifconfig -a
ifconfig en0

# Add an IP alias
sudo ifconfig en0 alias 192.168.1.20 netmask 255.255.255.0

# Remove an alias
sudo ifconfig en0 -alias 192.168.1.20

# Flush DNS cache (macOS)
sudo dscacheutil -flushcache && sudo killall -HUP mDNSResponder
```

---

## Network Statistics

```bash
# Show interface statistics (TX/RX packets, errors, drops)
ip -s link show eth0

# Watch statistics in real time
watch -n 1 'ip -s link show eth0'

# Alternative: read from /proc
cat /proc/net/dev
```

Example:
```text
$ ip -s link show eth0
2: eth0: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 ...
    RX:  bytes   packets  errors dropped  missed   mcast
    123456789    987654       0       0       0       0
    TX:  bytes   packets  errors dropped carrier collsns
     98765432    876543       0       0       0       0
```
