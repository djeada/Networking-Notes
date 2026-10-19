# Networking Notes

This repository is a comprehensive collection of notes, guides, and resources on various networking topics. It is designed to serve as a valuable reference for students, professionals, and anyone interested in learning more about networking concepts and technologies.

## Start Here

1. Learn the [TCP/IP model](notes/networking_basics/tcp_ip.md), [IP addressing](notes/network/ip_address.md), and [subnetting](notes/network/subnetting.md).
2. Follow a packet through [ARP](notes/data_link/arp.md), [IP](notes/application/ip_protocol.md), [TCP](notes/transport/tcp.md), [DNS](notes/application/dns.md), and [HTTP](notes/application/http.md).
3. Try the [ping](practice/ping/README.md), [DNS lookup](practice/nslookup_dig/README.md), and [Wireshark](practice/wireshark/README.md) labs, then check your understanding with the quizzes below.

The [Python scripts](scripts/README.md) require **Python 3.10 or later** and use the standard library. These examples run offline from the repository root:

```bash
python3 scripts/network/subnet_calculator.py 192.0.2.10/31
python3 scripts/network/cidr_to_hosts.py 2001:db8::/64
```

## Table of Contents

### Networking Basics
- [OSI Model](notes/networking_basics/osi.md)
- [TCP/IP Model](notes/networking_basics/tcp_ip.md)
- [Protocols](notes/networking_basics/protocols.md)
- [Ports](notes/networking_basics/ports.md)
- [Communication Between Devices](notes/networking_basics/communication_between_devices.md)
- [Cryptography Algorithms](notes/networking_basics/cryptography_algorithms.md)

### Physical Layer
- [Network Topologies](notes/physical/network_topologies.md)
- [Physical Devices](notes/physical/physical_devices.md)
- [Cables](notes/physical/cables.md)
- [Modes of Transmission](notes/physical/modes_of_transmission.md)
- [Wireless Networking](notes/physical/wireless_networking.md)
- [Cisco IOS](notes/physical/cisco_ios.md)

### Data Link Layer
- [Data Link Layer](notes/data_link/data_link_layer.md)
- [Ethernet](notes/data_link/ethernet.md)
- [Packet Switching](notes/data_link/packet_switching.md)
- [ARP](notes/data_link/arp.md)

### Network Layer
- [IP Addresses](notes/network/ip_address.md)
- [IP Protocol](notes/application/ip_protocol.md)
- [Subnetting](notes/network/subnetting.md)
- [NAT](notes/network/nat.md)
- [Datagrams](notes/network/datagrams.md)
- [Traceroute](notes/network/traceroute.md)
- [Port Forwarding](notes/network/port_forwarding.md)
- [Configuring Routers](notes/network/configuring_routers.md)
- [Routing Protocols](notes/network/routing_protocols.md)

### Transport Layer
- [TCP](notes/transport/tcp.md)
- [UDP](notes/transport/udp.md)
- [TCP vs UDP Comparison](notes/transport/tcp_udp_comparison.md)

### Application Layer
- [DNS](notes/application/dns.md)
- [HTTP](notes/application/http.md)
- [DHCP](notes/application/dhcp.md)
- [SSH](notes/application/ssh.md)
- [FTP](notes/application/ftp.md)
- [TLS/SSL](notes/application/tls_ssl.md)
- [SMTP and Email](notes/application/smtp_and_email.md)
- [Stateless vs Stateful](notes/application/stateless_vs_stateful.md)

### Internet
- [How the Internet Works](notes/internet/how_internet_works.md)
- [ISP](notes/internet/isp.md)
- [LAN and WAN](notes/internet/lan_and_wan.md)

### Other Topics
- [Firewall](notes/other/firewall.md)
- [IDS and IPS](notes/other/ids_and_ips.md)
- [VPN](notes/other/vpn.md)
- [VLAN](notes/other/vlan.md)
- [Proxy Servers](notes/other/proxy_servers.md)
- [Load Balancing](notes/other/load_balancing.md)
- [Network Troubleshooting](notes/other/network_troubleshooting.md)

### Practice
- [ping](practice/ping/README.md)
- [Traceroute](practice/traceroute/README.md)
- [DNS Lookup Tools (nslookup, dig, host)](practice/nslookup_dig/README.md)
- [Network Connections (netstat, ss)](practice/netstat_ss/README.md)
- [tcpdump](practice/tcpdump/README.md)
- [curl](practice/curl/README.md)
- [Netcat (nc)](practice/netcat/README.md)
- [iptables and nftables](practice/iptables/README.md)
- [Wireshark Labs](practice/wireshark/README.md)
- [nmap](practice/nmap/README.md)
- [SSH](practice/ssh/README.md)
- [ip and ifconfig](practice/ip_ifconfig/README.md)

### Scripts
- [Python Networking Scripts](scripts/README.md) — 60 educational Python scripts covering networking concepts

### Quizzes
- [OSI and Networking Basics](quizzes/osi_and_networking_basics.md)
- [Network Topologies and Physical Layer](quizzes/network_topologies_and_physical_layer.md)
- [TCP/UDP](quizzes/tcp_udp.md)
- [IP Addressing](quizzes/ip_addressing.md)
- [Subnetting and NAT](quizzes/subnetting_and_nat.md)
- [DNS and DHCP](quizzes/dns_dhcp.md)
- [HTTP and Web Protocols](quizzes/http_and_web_protocols.md)
- [Routing and Switching](quizzes/routing_and_switching.md)
- [Firewall, IDS, and IPS](quizzes/firewall_ids_and_ips.md)
- [VPN, Proxy, and Load Balancing](quizzes/vpn_proxy_and_load_balancing.md)

Quiz answers are marked with checked boxes. Try answering each question before reading the options marked as correct.

## Questions

- How does the internet work?
- What happens when you hit enter after typing a URL?
- What happens when you search for a phrase on Google?
- How does a messaging application like WhatsApp work?

## References

- [Computer Networking Full Course](https://www.youtube.com/watch?v=PhjHXeMNpp8)
- [Practical Networking](https://www.youtube.com/c/PracticalNetworking)
- [Sunny Classroom Networking Playlist](https://www.youtube.com/watch?v=X8RxRr7KNl8&list=PLSNNzog5eydtb5wyH2UtK09L9MsW9Hufq)
- [Neso Academy Computer Networks](https://www.youtube.com/watch?v=VwN91x5i25g&list=PLBlnK6fEyqRgMCUAG0XRw78UA8qnv6jEx)
- [DevOps Guide - Networking](https://github.com/Tikam02/DevOps-Guide/tree/master/Networking)

## Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Use primary sources, such as RFCs and official tool documentation, when correcting protocol behavior. Keep related notes, scripts, and quiz answers consistent. Run the offline checks from the repository root before submitting a change:

```bash
python3 -m unittest discover -s tests -v
python3 -m compileall -q scripts tests
```

## License

[MIT](LICENSE)
