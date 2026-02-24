# Python Networking Scripts

A collection of 30 educational Python scripts that demonstrate networking concepts covered in this repository. All scripts use only the Python standard library — no external dependencies required.

## Requirements

- Python 3.6 or later

## Scripts

### Networking Basics

| Script | Description |
|--------|-------------|
| [osi_model_simulator.py](networking_basics/osi_model_simulator.py) | Simulates data encapsulation and decapsulation through the 7 OSI layers |
| [protocol_identifier.py](networking_basics/protocol_identifier.py) | Looks up protocol details by port number or name |
| [port_scanner.py](networking_basics/port_scanner.py) | Basic TCP port scanner with service identification |
| [port_info_lookup.py](networking_basics/port_info_lookup.py) | Comprehensive well-known port reference and lookup tool |
| [checksum_calculator.py](networking_basics/checksum_calculator.py) | Demonstrates the Internet checksum algorithm (RFC 1071) step by step |

### Network Layer

| Script | Description |
|--------|-------------|
| [ip_address_validator.py](network/ip_address_validator.py) | Validates and classifies IPv4 and IPv6 addresses |
| [subnet_calculator.py](network/subnet_calculator.py) | Calculates subnet details with binary math breakdown |
| [cidr_to_hosts.py](network/cidr_to_hosts.py) | Converts CIDR notation to detailed host information |
| [ip_class_identifier.py](network/ip_class_identifier.py) | Identifies IPv4 address class (A through E) with default masks |
| [nat_simulator.py](network/nat_simulator.py) | Simulates Network Address Translation with port mapping |
| [traceroute_sim.py](network/traceroute_sim.py) | Simulates TTL-based traceroute route discovery |
| [network_interface_info.py](network/network_interface_info.py) | Displays local network interface information |

### Transport Layer

| Script | Description |
|--------|-------------|
| [tcp_client.py](transport/tcp_client.py) | Simple TCP client for sending messages |
| [tcp_server.py](transport/tcp_server.py) | Simple TCP echo server |
| [udp_client.py](transport/udp_client.py) | Simple UDP client demonstrating connectionless communication |
| [udp_server.py](transport/udp_server.py) | Simple UDP echo server |
| [tcp_handshake_simulator.py](transport/tcp_handshake_simulator.py) | Visualizes TCP 3-way handshake and connection teardown |

### Application Layer

| Script | Description |
|--------|-------------|
| [dns_lookup.py](application/dns_lookup.py) | Performs forward and reverse DNS lookups |
| [http_get_request.py](application/http_get_request.py) | Builds a raw HTTP GET request using sockets |
| [http_server.py](application/http_server.py) | Minimal HTTP server with educational logging |
| [url_parser.py](application/url_parser.py) | Parses and analyzes URL components |
| [ssl_certificate_checker.py](application/ssl_certificate_checker.py) | Checks SSL/TLS certificate details for HTTPS sites |

### Internet

| Script | Description |
|--------|-------------|
| [bandwidth_calculator.py](internet/bandwidth_calculator.py) | Calculates bandwidth, transfer time, and data size conversions |
| [download_speed_test.py](internet/download_speed_test.py) | Simple download speed estimation tool |
| [whois_lookup.py](internet/whois_lookup.py) | Performs WHOIS lookups using raw socket connections |

### Other Topics

| Script | Description |
|--------|-------------|
| [simple_firewall_simulator.py](other/simple_firewall_simulator.py) | Simulates packet-filtering firewall rule processing |
| [vpn_tunnel_simulator.py](other/vpn_tunnel_simulator.py) | Demonstrates VPN tunnel encapsulation and decapsulation |
| [packet_sniffer_demo.py](other/packet_sniffer_demo.py) | Parses sample Ethernet/IP/TCP packet bytes field by field |
| [network_chat_app.py](other/network_chat_app.py) | TCP-based chat application with server and client modes |
| [arp_table_viewer.py](other/arp_table_viewer.py) | Displays and explains the system ARP table |

## Usage

Each script can be run directly with Python:

```bash
python3 scripts/networking_basics/osi_model_simulator.py
python3 scripts/network/subnet_calculator.py
python3 scripts/transport/tcp_handshake_simulator.py
```

Many scripts support command-line arguments. Use `--help` to see available options:

```bash
python3 scripts/network/subnet_calculator.py --help
python3 scripts/networking_basics/port_scanner.py --help
```

Scripts that require a server and client (TCP/UDP) should be run in separate terminals:

```bash
# Terminal 1
python3 scripts/transport/tcp_server.py

# Terminal 2
python3 scripts/transport/tcp_client.py
```
