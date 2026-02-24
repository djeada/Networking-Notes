"""
Port Information Lookup
========================
A comprehensive reference tool that maps well-known port numbers to their
service names and descriptions.  Ports are categorised by IANA range:

    • Well-known ports  :   0 – 1 023   (assigned by IANA, require root)
    • Registered ports  :   1 024 – 49 151   (registered with IANA)
    • Dynamic/private   :   49 152 – 65 535  (ephemeral / temporary)

Features:
    • Look up a single port for its service and description.
    • List all ports in a given IANA category.
    • Search ports by keyword in the service name or description.
    • Interactive or CLI mode via argparse.

Usage examples:
    python port_info_lookup.py --port 443
    python port_info_lookup.py --category well-known
    python port_info_lookup.py --search mail
    python port_info_lookup.py --range 80 100
"""

import argparse


# ---------------------------------------------------------------------------
# Port database
# Each key is a port number; value is (service_name, description).
# ---------------------------------------------------------------------------
PORT_DB: dict[int, tuple[str, str]] = {
    # Well-known ports (0–1023)
    7:    ("Echo", "Echo Protocol — returns data sent to it"),
    20:   ("FTP-DATA", "File Transfer Protocol — data channel"),
    21:   ("FTP", "File Transfer Protocol — control channel"),
    22:   ("SSH", "Secure Shell — encrypted remote access"),
    23:   ("Telnet", "Telnet — unencrypted remote login (insecure)"),
    25:   ("SMTP", "Simple Mail Transfer Protocol — email routing"),
    53:   ("DNS", "Domain Name System — name resolution"),
    67:   ("DHCP-Server", "DHCP server — IP address assignment"),
    68:   ("DHCP-Client", "DHCP client — IP address request"),
    69:   ("TFTP", "Trivial File Transfer Protocol"),
    80:   ("HTTP", "Hypertext Transfer Protocol — web traffic"),
    88:   ("Kerberos", "Kerberos authentication system"),
    110:  ("POP3", "Post Office Protocol v3 — email retrieval"),
    119:  ("NNTP", "Network News Transfer Protocol — Usenet"),
    123:  ("NTP", "Network Time Protocol — clock sync"),
    135:  ("MS-RPC", "Microsoft Remote Procedure Call"),
    137:  ("NetBIOS-NS", "NetBIOS Name Service"),
    138:  ("NetBIOS-DGM", "NetBIOS Datagram Service"),
    139:  ("NetBIOS-SSN", "NetBIOS Session Service"),
    143:  ("IMAP", "Internet Message Access Protocol — email management"),
    161:  ("SNMP", "Simple Network Management Protocol — monitoring"),
    162:  ("SNMP-TRAP", "SNMP Trap — asynchronous alerts"),
    179:  ("BGP", "Border Gateway Protocol — inter-AS routing"),
    389:  ("LDAP", "Lightweight Directory Access Protocol"),
    443:  ("HTTPS", "HTTP over TLS — encrypted web traffic"),
    445:  ("SMB", "Server Message Block — file/printer sharing"),
    465:  ("SMTPS", "SMTP over TLS (legacy implicit TLS)"),
    500:  ("IKE", "Internet Key Exchange — IPsec key negotiation"),
    514:  ("Syslog", "Syslog — centralized log collection"),
    520:  ("RIP", "Routing Information Protocol"),
    587:  ("Submission", "Email message submission (STARTTLS)"),
    636:  ("LDAPS", "LDAP over TLS — encrypted directory services"),
    993:  ("IMAPS", "IMAP over TLS — encrypted email access"),
    995:  ("POP3S", "POP3 over TLS — encrypted email retrieval"),
    # Registered ports (1024–49151)
    1080: ("SOCKS", "SOCKS proxy protocol"),
    1433: ("MSSQL", "Microsoft SQL Server"),
    1521: ("Oracle-DB", "Oracle Database listener"),
    1723: ("PPTP", "Point-to-Point Tunneling Protocol"),
    2049: ("NFS", "Network File System"),
    3306: ("MySQL", "MySQL / MariaDB database"),
    3389: ("RDP", "Remote Desktop Protocol"),
    5060: ("SIP", "Session Initiation Protocol (VoIP signalling)"),
    5432: ("PostgreSQL", "PostgreSQL database"),
    5900: ("VNC", "Virtual Network Computing — remote desktop"),
    6379: ("Redis", "Redis in-memory data store"),
    8080: ("HTTP-Alt", "Alternate HTTP (proxies / dev servers)"),
    8443: ("HTTPS-Alt", "Alternate HTTPS"),
    9200: ("Elasticsearch", "Elasticsearch REST API"),
    27017: ("MongoDB", "MongoDB database"),
}


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def port_category(port: int) -> str:
    """Return the IANA category name for a port number."""
    if 0 <= port <= 1023:
        return "Well-known"
    if 1024 <= port <= 49151:
        return "Registered"
    if 49152 <= port <= 65535:
        return "Dynamic/Private"
    return "Invalid"


def lookup_port(port: int) -> None:
    """Print information about a single port."""
    cat = port_category(port)
    entry = PORT_DB.get(port)
    if entry:
        name, desc = entry
        print(f"\n  Port  : {port}")
        print(f"  Range : {cat}")
        print(f"  Service: {name}")
        print(f"  Info   : {desc}\n")
    else:
        print(f"\n  Port {port} ({cat} range) — no entry in database.\n")


def list_category(category: str) -> None:
    """List all database entries in the given category."""
    ranges = {
        "well-known": (0, 1023),
        "registered": (1024, 49151),
        "dynamic":    (49152, 65535),
    }
    key = category.lower()
    if key not in ranges:
        print(f"Unknown category '{category}'. "
              "Choose: well-known, registered, dynamic.")
        return

    lo, hi = ranges[key]
    entries = {p: v for p, v in PORT_DB.items() if lo <= p <= hi}

    print(f"\n{category.title()} ports ({lo}–{hi}): "
          f"{len(entries)} entries\n")
    for port in sorted(entries):
        name, desc = entries[port]
        print(f"  {port:>5}  {name:<18}  {desc}")
    print()


def search_ports(keyword: str) -> None:
    """Search service names and descriptions for a keyword."""
    kw = keyword.lower()
    results = {
        p: v for p, v in PORT_DB.items()
        if kw in v[0].lower() or kw in v[1].lower()
    }
    if results:
        print(f"\nSearch results for '{keyword}' "
              f"({len(results)} match(es)):\n")
        for port in sorted(results):
            name, desc = results[port]
            print(f"  {port:>5}  {name:<18}  {desc}")
        print()
    else:
        print(f"\nNo matches for '{keyword}'.\n")


def show_range(start: int, end: int) -> None:
    """Show all known ports in the given numeric range."""
    entries = {p: v for p, v in PORT_DB.items() if start <= p <= end}
    if entries:
        print(f"\nPorts {start}–{end} ({len(entries)} known):\n")
        for port in sorted(entries):
            name, desc = entries[port]
            cat = port_category(port)
            print(f"  {port:>5}  [{cat:<12}]  {name:<18}  {desc}")
        print()
    else:
        print(f"\nNo known ports in range {start}–{end}.\n")


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Look up well-known port information.",
    )
    group = parser.add_mutually_exclusive_group()
    group.add_argument(
        "-p", "--port", type=int, metavar="PORT",
        help="Look up a specific port number",
    )
    group.add_argument(
        "-c", "--category", type=str, metavar="CAT",
        choices=["well-known", "registered", "dynamic"],
        help="List ports in category: well-known, registered, dynamic",
    )
    group.add_argument(
        "-s", "--search", type=str, metavar="KEYWORD",
        help="Search ports by keyword",
    )
    group.add_argument(
        "-r", "--range", type=int, nargs=2, metavar=("START", "END"),
        help="Show known ports in a numeric range",
    )
    return parser


# ---------------------------------------------------------------------------
# Demo / entry point
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    parser = build_parser()
    args = parser.parse_args()

    if args.port is not None:
        lookup_port(args.port)
    elif args.category:
        list_category(args.category)
    elif args.search:
        search_ports(args.search)
    elif args.range:
        show_range(args.range[0], args.range[1])
    else:
        # No arguments — run a demo
        print("=" * 60)
        print("  Port Information Lookup — Demo")
        print("=" * 60)

        print("\n--- Single port lookup ---")
        for p in (22, 80, 443, 3306, 50000):
            lookup_port(p)

        print("--- Category listing: well-known (first 10) ---")
        wk = {p: v for p, v in PORT_DB.items() if 0 <= p <= 1023}
        for port in sorted(wk)[:10]:
            name, desc = wk[port]
            print(f"  {port:>5}  {name:<18}  {desc}")
        print(f"  … and {len(wk) - 10} more.\n")

        print("--- Keyword search: 'mail' ---")
        search_ports("mail")

        print("Tip: run with --help to see all options.\n")
