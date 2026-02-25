# Python Networking Scripts

A collection of 60 educational Python scripts that demonstrate networking concepts covered in this repository. All scripts use only the Python standard library — no external dependencies required.

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
| [mac_address_tool.py](networking_basics/mac_address_tool.py) | MAC address generator, validator, and analyzer with OUI lookup |
| [binary_ip_converter.py](networking_basics/binary_ip_converter.py) | Converts between binary, decimal, and hexadecimal IP representations |
| [network_protocol_analyzer.py](networking_basics/network_protocol_analyzer.py) | Protocol reference with OSI layer, ports, and use-case details |
| [encoding_demo.py](networking_basics/encoding_demo.py) | Demonstrates Base64, URL, hex, and ASCII/UTF-8 encoding schemes |
| [packet_header_parser.py](networking_basics/packet_header_parser.py) | Parses raw hex bytes of Ethernet, IPv4, TCP, UDP, and ICMP headers |

### Data Link Layer

| Script | Description |
|--------|-------------|
| [ethernet_frame_builder.py](data_link/ethernet_frame_builder.py) | Builds and parses Ethernet II frames with CRC-32 FCS |
| [crc_calculator.py](data_link/crc_calculator.py) | CRC-32 calculation with step-by-step polynomial division |
| [arp_spoof_detector.py](data_link/arp_spoof_detector.py) | Educational ARP spoof detection with MAC-flap and flood alerts |

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
| [routing_table_simulator.py](network/routing_table_simulator.py) | Simulates IP routing table lookups with longest-prefix match |
| [ipv6_address_tool.py](network/ipv6_address_tool.py) | IPv6 address expansion, compression, and type classification |
| [packet_fragmentation_sim.py](network/packet_fragmentation_sim.py) | Simulates IPv4 packet fragmentation and reassembly |
| [subnet_overlap_checker.py](network/subnet_overlap_checker.py) | Checks if CIDR subnets overlap with address range visualization |
| [ttl_analyzer.py](network/ttl_analyzer.py) | Analyzes TTL values to estimate OS and hop count |

### Transport Layer

| Script | Description |
|--------|-------------|
| [tcp_client.py](transport/tcp_client.py) | Simple TCP client for sending messages |
| [tcp_server.py](transport/tcp_server.py) | Simple TCP echo server |
| [udp_client.py](transport/udp_client.py) | Simple UDP client demonstrating connectionless communication |
| [udp_server.py](transport/udp_server.py) | Simple UDP echo server |
| [tcp_handshake_simulator.py](transport/tcp_handshake_simulator.py) | Visualizes TCP 3-way handshake and connection teardown |
| [tcp_window_simulator.py](transport/tcp_window_simulator.py) | Simulates TCP sliding window flow control with ASCII visualization |
| [tcp_state_machine.py](transport/tcp_state_machine.py) | Simulates all 11 TCP states and their transitions |
| [port_multiplexer_demo.py](transport/port_multiplexer_demo.py) | Demonstrates transport layer port multiplexing and demultiplexing |

### Application Layer

| Script | Description |
|--------|-------------|
| [dns_lookup.py](application/dns_lookup.py) | Performs forward and reverse DNS lookups |
| [http_get_request.py](application/http_get_request.py) | Builds a raw HTTP GET request using sockets |
| [http_server.py](application/http_server.py) | Minimal HTTP server with educational logging |
| [url_parser.py](application/url_parser.py) | Parses and analyzes URL components |
| [ssl_certificate_checker.py](application/ssl_certificate_checker.py) | Checks SSL/TLS certificate details for HTTPS sites |
| [dhcp_simulator.py](application/dhcp_simulator.py) | Simulates the DHCP DORA process with lease management |
| [dns_record_explorer.py](application/dns_record_explorer.py) | DNS record type reference and resolution simulator |
| [http_header_analyzer.py](application/http_header_analyzer.py) | Analyzes HTTP request and response headers with explanations |
| [smtp_client_demo.py](application/smtp_client_demo.py) | Simulates an SMTP email sending conversation step by step |
| [ftp_client_demo.py](application/ftp_client_demo.py) | Simulates FTP sessions showing active and passive mode |

### Internet

| Script | Description |
|--------|-------------|
| [bandwidth_calculator.py](internet/bandwidth_calculator.py) | Calculates bandwidth, transfer time, and data size conversions |
| [download_speed_test.py](internet/download_speed_test.py) | Simple download speed estimation tool |
| [whois_lookup.py](internet/whois_lookup.py) | Performs WHOIS lookups using raw socket connections |
| [latency_calculator.py](internet/latency_calculator.py) | Calculates propagation, transmission, and queuing delays |
| [network_bandwidth_monitor.py](internet/network_bandwidth_monitor.py) | Monitors network interface throughput statistics |
| [ip_geolocation_lookup.py](internet/ip_geolocation_lookup.py) | Educational IP geolocation with built-in sample database |
| [traceroute_visualizer.py](internet/traceroute_visualizer.py) | ASCII visualization of traceroute network paths |

### Other Topics

| Script | Description |
|--------|-------------|
| [simple_firewall_simulator.py](other/simple_firewall_simulator.py) | Simulates packet-filtering firewall rule processing |
| [vpn_tunnel_simulator.py](other/vpn_tunnel_simulator.py) | Demonstrates VPN tunnel encapsulation and decapsulation |
| [packet_sniffer_demo.py](other/packet_sniffer_demo.py) | Parses sample Ethernet/IP/TCP packet bytes field by field |
| [network_chat_app.py](other/network_chat_app.py) | TCP-based chat application with server and client modes |
| [arp_table_viewer.py](other/arp_table_viewer.py) | Displays and explains the system ARP table |
| [vlan_tag_simulator.py](other/vlan_tag_simulator.py) | Simulates IEEE 802.1Q VLAN tagging across switches |
| [load_balancer_simulator.py](other/load_balancer_simulator.py) | Compares Round Robin, Weighted, Least Connections, and IP Hash algorithms |
| [ids_rule_matcher.py](other/ids_rule_matcher.py) | Signature-based Intrusion Detection System rule matching |
| [proxy_server_demo.py](other/proxy_server_demo.py) | Simulates forward and reverse proxy behavior with caching |
| [dns_cache_simulator.py](other/dns_cache_simulator.py) | DNS resolver cache simulation with TTL-based expiry |

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
