#!/usr/bin/env python3
"""
Network Protocol Analyzer
===========================
Looks up common network protocols and displays detailed information
including OSI layer, port numbers, connection orientation, typical use
cases, and related protocols.

The built-in database covers ~20 widely-used protocols across all seven
layers of the OSI model, making this a quick reference tool for study
and troubleshooting.

Concepts demonstrated:
  * OSI model layer classification
  * Well-known port numbers (0-1023) and registered ports
  * Connection-oriented (TCP) vs connectionless (UDP) transport
  * Protocol relationships and encapsulation

Usage:
    python network_protocol_analyzer.py                 # run demo
    python network_protocol_analyzer.py --protocol HTTP
    python network_protocol_analyzer.py --port 443
    python network_protocol_analyzer.py --layer 4
    python network_protocol_analyzer.py --list
"""

import argparse
import sys

OSI_LAYERS = {
    1: "Physical",
    2: "Data Link",
    3: "Network",
    4: "Transport",
    5: "Session",
    6: "Presentation",
    7: "Application",
}

# Each entry: name, osi_layer, port(s), transport, conn_oriented, description, use_cases, related
PROTOCOLS = [
    {"name": "HTTP", "layer": 7, "ports": [80], "transport": "TCP",
     "conn_oriented": True,
     "desc": "HyperText Transfer Protocol — transfers web pages and API data.",
     "uses": ["Web browsing", "REST APIs", "File downloads"],
     "related": ["HTTPS", "HTTP/2", "TCP"]},
    {"name": "HTTPS", "layer": 7, "ports": [443], "transport": "TCP",
     "conn_oriented": True,
     "desc": "HTTP over TLS — encrypts web traffic for confidentiality and integrity.",
     "uses": ["Secure web browsing", "Online banking", "E-commerce"],
     "related": ["HTTP", "TLS", "TCP"]},
    {"name": "DNS", "layer": 7, "ports": [53], "transport": "UDP/TCP",
     "conn_oriented": False,
     "desc": "Domain Name System — resolves hostnames to IP addresses.",
     "uses": ["Name resolution", "Service discovery", "Mail routing (MX)"],
     "related": ["DNSSEC", "mDNS", "LLMNR"]},
    {"name": "DHCP", "layer": 7, "ports": [67, 68], "transport": "UDP",
     "conn_oriented": False,
     "desc": "Dynamic Host Configuration Protocol — auto-assigns IP configuration.",
     "uses": ["IP address assignment", "Network booting (PXE)", "Option distribution"],
     "related": ["BOOTP", "DHCPv6", "ARP"]},
    {"name": "FTP", "layer": 7, "ports": [20, 21], "transport": "TCP",
     "conn_oriented": True,
     "desc": "File Transfer Protocol — transfers files between client and server.",
     "uses": ["File uploads/downloads", "Website deployment", "Backup"],
     "related": ["SFTP", "FTPS", "TFTP"]},
    {"name": "SSH", "layer": 7, "ports": [22], "transport": "TCP",
     "conn_oriented": True,
     "desc": "Secure Shell — encrypted remote login and command execution.",
     "uses": ["Remote administration", "Secure tunnelling", "SCP/SFTP file transfer"],
     "related": ["Telnet", "SCP", "SFTP"]},
    {"name": "Telnet", "layer": 7, "ports": [23], "transport": "TCP",
     "conn_oriented": True,
     "desc": "Unencrypted remote terminal protocol (largely replaced by SSH).",
     "uses": ["Legacy device management", "Network equipment CLI"],
     "related": ["SSH"]},
    {"name": "SMTP", "layer": 7, "ports": [25, 587], "transport": "TCP",
     "conn_oriented": True,
     "desc": "Simple Mail Transfer Protocol — sends email between servers.",
     "uses": ["Email delivery", "Mailing lists"],
     "related": ["POP3", "IMAP", "MIME"]},
    {"name": "POP3", "layer": 7, "ports": [110, 995], "transport": "TCP",
     "conn_oriented": True,
     "desc": "Post Office Protocol v3 — retrieves email from a mail server.",
     "uses": ["Email retrieval", "Offline email access"],
     "related": ["IMAP", "SMTP"]},
    {"name": "IMAP", "layer": 7, "ports": [143, 993], "transport": "TCP",
     "conn_oriented": True,
     "desc": "Internet Message Access Protocol — manages email on the server.",
     "uses": ["Synced email across devices", "Server-side search"],
     "related": ["POP3", "SMTP"]},
    {"name": "SNMP", "layer": 7, "ports": [161, 162], "transport": "UDP",
     "conn_oriented": False,
     "desc": "Simple Network Management Protocol — monitors and manages devices.",
     "uses": ["Network monitoring", "Device configuration", "Alerting (traps)"],
     "related": ["Syslog", "NetFlow"]},
    {"name": "NTP", "layer": 7, "ports": [123], "transport": "UDP",
     "conn_oriented": False,
     "desc": "Network Time Protocol — synchronises clocks across a network.",
     "uses": ["Time synchronisation", "Log correlation", "Authentication tokens"],
     "related": ["PTP", "SNTP"]},
    {"name": "TLS", "layer": 6, "ports": [], "transport": "TCP",
     "conn_oriented": True,
     "desc": "Transport Layer Security — provides encryption for upper-layer protocols.",
     "uses": ["HTTPS encryption", "Email encryption", "VPN tunnels"],
     "related": ["SSL", "HTTPS", "DTLS"]},
    {"name": "TCP", "layer": 4, "ports": [], "transport": "—",
     "conn_oriented": True,
     "desc": "Transmission Control Protocol — reliable, ordered byte-stream delivery.",
     "uses": ["Web traffic", "Email", "File transfers"],
     "related": ["UDP", "SCTP", "IP"]},
    {"name": "UDP", "layer": 4, "ports": [], "transport": "—",
     "conn_oriented": False,
     "desc": "User Datagram Protocol — lightweight, best-effort datagram delivery.",
     "uses": ["DNS queries", "Video streaming", "VoIP", "Gaming"],
     "related": ["TCP", "SCTP", "IP"]},
    {"name": "ICMP", "layer": 3, "ports": [], "transport": "—",
     "conn_oriented": False,
     "desc": "Internet Control Message Protocol — diagnostics and error reporting.",
     "uses": ["ping", "traceroute", "Destination Unreachable messages"],
     "related": ["ICMPv6", "IP"]},
    {"name": "IP", "layer": 3, "ports": [], "transport": "—",
     "conn_oriented": False,
     "desc": "Internet Protocol — routes datagrams across interconnected networks.",
     "uses": ["Packet routing", "Addressing", "Fragmentation"],
     "related": ["IPv6", "ICMP", "ARP"]},
    {"name": "ARP", "layer": 2, "ports": [], "transport": "—",
     "conn_oriented": False,
     "desc": "Address Resolution Protocol — maps IPv4 addresses to MAC addresses.",
     "uses": ["Local delivery", "Proxy ARP", "Gratuitous ARP"],
     "related": ["NDP", "RARP", "IP"]},
    {"name": "STP", "layer": 2, "ports": [], "transport": "—",
     "conn_oriented": False,
     "desc": "Spanning Tree Protocol — prevents loops in switched Ethernet networks.",
     "uses": ["Loop prevention", "Redundant link management"],
     "related": ["RSTP", "MSTP"]},
    {"name": "Ethernet", "layer": 2, "ports": [], "transport": "—",
     "conn_oriented": False,
     "desc": "IEEE 802.3 — dominant LAN technology for frame-based data delivery.",
     "uses": ["LAN connectivity", "Data centre interconnect"],
     "related": ["Wi-Fi (802.11)", "ARP", "VLAN (802.1Q)"]},
]

_BY_NAME = {p["name"].upper(): p for p in PROTOCOLS}


def print_protocol(p: dict) -> None:
    layer_name = OSI_LAYERS.get(p["layer"], "?")
    ports_str = ", ".join(str(x) for x in p["ports"]) if p["ports"] else "N/A"
    conn = "Yes (reliable, ordered)" if p["conn_oriented"] else "No (best-effort)"

    print(f"  Protocol       : {p['name']}")
    print(f"  OSI Layer      : {p['layer']} — {layer_name}")
    print(f"  Well-known port: {ports_str}")
    print(f"  Transport      : {p['transport']}")
    print(f"  Conn-oriented  : {conn}")
    print(f"  Description    : {p['desc']}")
    print(f"  Typical uses   : {', '.join(p['uses'])}")
    print(f"  Related        : {', '.join(p['related'])}")


def lookup_by_name(name: str) -> None:
    p = _BY_NAME.get(name.upper())
    if p:
        print_protocol(p)
    else:
        print(f"  [!] Protocol '{name}' not found. Use --list to see available protocols.")


def lookup_by_port(port: int) -> None:
    matches = [p for p in PROTOCOLS if port in p["ports"]]
    if not matches:
        print(f"  [!] No protocol found for port {port}.")
        return
    for i, p in enumerate(matches):
        if i > 0:
            print()
        print_protocol(p)


def lookup_by_layer(layer: int) -> None:
    matches = [p for p in PROTOCOLS if p["layer"] == layer]
    if not matches:
        print(f"  [!] No protocols in database for layer {layer}.")
        return
    print(f"  OSI Layer {layer} — {OSI_LAYERS.get(layer, '?')}:")
    print(f"  {'Name':<10s} {'Ports':<14s} {'Transport':<10s} Connection-oriented")
    print(f"  {'----':<10s} {'-----':<14s} {'---------':<10s} -------------------")
    for p in matches:
        ports = ",".join(str(x) for x in p["ports"]) if p["ports"] else "—"
        conn = "Yes" if p["conn_oriented"] else "No"
        print(f"  {p['name']:<10s} {ports:<14s} {p['transport']:<10s} {conn}")


def list_all() -> None:
    print(f"  {'Protocol':<10s} {'Layer':<18s} {'Port(s)':<14s} {'Transport':<10s}")
    print(f"  {'--------':<10s} {'-----':<18s} {'-------':<14s} {'---------':<10s}")
    for p in PROTOCOLS:
        layer_str = f"{p['layer']} - {OSI_LAYERS[p['layer']]}"
        ports = ",".join(str(x) for x in p["ports"]) if p["ports"] else "—"
        print(f"  {p['name']:<10s} {layer_str:<18s} {ports:<14s} {p['transport']:<10s}")


def demo() -> None:
    print("=" * 62)
    print("  Network Protocol Analyzer — Demo Mode")
    print("=" * 62)

    print("\n— Full protocol list ——————————————————————")
    list_all()

    for name in ["HTTP", "DNS", "TCP", "ARP"]:
        print(f"\n— Detailed: {name} {'—' * (48 - len(name))}")
        lookup_by_name(name)

    print(f"\n— Lookup by port 443 ——————————————————————")
    lookup_by_port(443)

    print(f"\n— Protocols at Layer 4 ————————————————————")
    lookup_by_layer(4)

    print()


def main() -> None:
    parser = argparse.ArgumentParser(description="Look up network protocol information")
    parser.add_argument("--protocol", metavar="NAME", help="Protocol name (e.g. HTTP)")
    parser.add_argument("--port", metavar="N", type=int, help="Look up by port number")
    parser.add_argument("--layer", metavar="N", type=int, choices=range(1, 8), help="List protocols at OSI layer N")
    parser.add_argument("--list", action="store_true", help="List all protocols in the database")
    args = parser.parse_args()

    if not any([args.protocol, args.port, args.layer, args.list]):
        demo()
        return

    if args.list:
        list_all()
    if args.protocol:
        lookup_by_name(args.protocol)
    if args.port is not None:
        lookup_by_port(args.port)
    if args.layer is not None:
        lookup_by_layer(args.layer)


if __name__ == "__main__":
    main()
