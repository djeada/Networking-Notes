"""
Protocol Identifier
====================
Given a port number or protocol name, identifies the protocol details.
Contains a curated dictionary of common network protocols with their port
numbers, transport type (TCP/UDP/both), and a brief description.

Supports two lookup modes:
    • By port number  → returns all protocols registered on that port.
    • By name/keyword → returns protocols whose name matches the query.

Usage examples (command-line):
    python protocol_identifier.py --port 443
    python protocol_identifier.py --name dns
    python protocol_identifier.py --list
"""

import argparse
from typing import Optional


# ---------------------------------------------------------------------------
# Protocol database
# Each entry: (port, transport, full_name, description)
# ---------------------------------------------------------------------------
PROTOCOLS: list[dict] = [
    {"port": 20, "transport": "TCP", "name": "FTP-DATA",
     "description": "File Transfer Protocol — data channel"},
    {"port": 21, "transport": "TCP", "name": "FTP",
     "description": "File Transfer Protocol — control/command channel"},
    {"port": 22, "transport": "TCP", "name": "SSH",
     "description": "Secure Shell — encrypted remote login and command execution"},
    {"port": 23, "transport": "TCP", "name": "Telnet",
     "description": "Telnet — unencrypted remote login (legacy, insecure)"},
    {"port": 25, "transport": "TCP", "name": "SMTP",
     "description": "Simple Mail Transfer Protocol — sending email"},
    {"port": 53, "transport": "TCP/UDP", "name": "DNS",
     "description": "Domain Name System — resolves domain names to IP addresses"},
    {"port": 67, "transport": "UDP", "name": "DHCP-Server",
     "description": "Dynamic Host Configuration Protocol — server listening port"},
    {"port": 68, "transport": "UDP", "name": "DHCP-Client",
     "description": "Dynamic Host Configuration Protocol — client listening port"},
    {"port": 69, "transport": "UDP", "name": "TFTP",
     "description": "Trivial File Transfer Protocol — simple, no-auth file transfer"},
    {"port": 80, "transport": "TCP", "name": "HTTP",
     "description": "Hypertext Transfer Protocol — unencrypted web traffic"},
    {"port": 110, "transport": "TCP", "name": "POP3",
     "description": "Post Office Protocol v3 — retrieving email from a server"},
    {"port": 119, "transport": "TCP", "name": "NNTP",
     "description": "Network News Transfer Protocol — Usenet newsgroups"},
    {"port": 123, "transport": "UDP", "name": "NTP",
     "description": "Network Time Protocol — clock synchronization"},
    {"port": 143, "transport": "TCP", "name": "IMAP",
     "description": "Internet Message Access Protocol — managing email on a server"},
    {"port": 161, "transport": "UDP", "name": "SNMP",
     "description": "Simple Network Management Protocol — network device monitoring"},
    {"port": 162, "transport": "UDP", "name": "SNMP-TRAP",
     "description": "SNMP Trap — asynchronous notifications from agents"},
    {"port": 389, "transport": "TCP/UDP", "name": "LDAP",
     "description": "Lightweight Directory Access Protocol — directory services"},
    {"port": 443, "transport": "TCP", "name": "HTTPS",
     "description": "HTTP over TLS/SSL — encrypted web traffic"},
    {"port": 445, "transport": "TCP", "name": "SMB",
     "description": "Server Message Block — Windows file/printer sharing"},
    {"port": 465, "transport": "TCP", "name": "SMTPS",
     "description": "SMTP over TLS/SSL — encrypted email submission (legacy)"},
    {"port": 514, "transport": "UDP", "name": "Syslog",
     "description": "Syslog — centralized logging protocol"},
    {"port": 587, "transport": "TCP", "name": "SMTP-Submission",
     "description": "SMTP message submission with STARTTLS support"},
    {"port": 636, "transport": "TCP", "name": "LDAPS",
     "description": "LDAP over TLS/SSL — encrypted directory services"},
    {"port": 993, "transport": "TCP", "name": "IMAPS",
     "description": "IMAP over TLS/SSL — encrypted email access"},
    {"port": 995, "transport": "TCP", "name": "POP3S",
     "description": "POP3 over TLS/SSL — encrypted email retrieval"},
    {"port": 1433, "transport": "TCP", "name": "MSSQL",
     "description": "Microsoft SQL Server default listening port"},
    {"port": 1521, "transport": "TCP", "name": "Oracle-DB",
     "description": "Oracle Database default listener port"},
    {"port": 3306, "transport": "TCP", "name": "MySQL",
     "description": "MySQL / MariaDB default listening port"},
    {"port": 3389, "transport": "TCP/UDP", "name": "RDP",
     "description": "Remote Desktop Protocol — Windows remote desktop"},
    {"port": 5432, "transport": "TCP", "name": "PostgreSQL",
     "description": "PostgreSQL database default listening port"},
    {"port": 5900, "transport": "TCP", "name": "VNC",
     "description": "Virtual Network Computing — remote desktop sharing"},
    {"port": 8080, "transport": "TCP", "name": "HTTP-Alt",
     "description": "Alternate HTTP port often used for proxies / dev servers"},
    {"port": 8443, "transport": "TCP", "name": "HTTPS-Alt",
     "description": "Alternate HTTPS port"},
]


# ---------------------------------------------------------------------------
# Lookup helpers
# ---------------------------------------------------------------------------

def lookup_by_port(port: int) -> list[dict]:
    """Return all protocol entries matching the given port number."""
    return [p for p in PROTOCOLS if p["port"] == port]


def lookup_by_name(name: str) -> list[dict]:
    """Return protocol entries whose name contains the query (case-insensitive)."""
    query = name.upper()
    return [p for p in PROTOCOLS if query in p["name"].upper()]


def format_entry(entry: dict) -> str:
    """Pretty-print a single protocol entry."""
    return (
        f"  Port {entry['port']:>5}  |  {entry['transport']:<7}  |  "
        f"{entry['name']:<16}  |  {entry['description']}"
    )


def print_results(results: list[dict], query_label: str) -> None:
    """Display results or a 'not found' message."""
    if results:
        print(f"\nResults for {query_label}:\n")
        for entry in results:
            print(format_entry(entry))
        print()
    else:
        print(f"\nNo protocols found for {query_label}.\n")


def list_all() -> None:
    """Print every protocol in the database, sorted by port number."""
    print("\nComplete protocol database:\n")
    for entry in sorted(PROTOCOLS, key=lambda e: e["port"]):
        print(format_entry(entry))
    print(f"\nTotal entries: {len(PROTOCOLS)}\n")


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Identify network protocols by port number or name.",
    )
    group = parser.add_mutually_exclusive_group()
    group.add_argument(
        "-p", "--port", type=int, metavar="PORT",
        help="Look up protocols by port number (e.g. 443)",
    )
    group.add_argument(
        "-n", "--name", type=str, metavar="NAME",
        help="Look up protocols by name/keyword (e.g. dns)",
    )
    group.add_argument(
        "-l", "--list", action="store_true",
        help="List every protocol in the database",
    )
    return parser


# ---------------------------------------------------------------------------
# Demo / entry point
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    parser = build_parser()
    args = parser.parse_args()

    if args.port is not None:
        results = lookup_by_port(args.port)
        print_results(results, f"port {args.port}")
    elif args.name is not None:
        results = lookup_by_name(args.name)
        print_results(results, f"name '{args.name}'")
    elif args.list:
        list_all()
    else:
        # No arguments — run a quick demo
        print("=" * 70)
        print("Protocol Identifier — Demo Mode")
        print("=" * 70)

        demo_ports = [22, 53, 80, 443, 3306]
        for port in demo_ports:
            results = lookup_by_port(port)
            print_results(results, f"port {port}")

        demo_names = ["smtp", "snmp"]
        for name in demo_names:
            results = lookup_by_name(name)
            print_results(results, f"name '{name}'")

        print("Tip: run with --help to see all options.\n")
