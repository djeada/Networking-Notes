"""
Basic TCP Port Scanner
======================
A simple, educational TCP port scanner that attempts to connect to specified
ports on a target host using Python's ``socket`` module.

Features:
    • Scans a user-defined range of TCP ports on any reachable host.
    • Uses a configurable connection timeout (default 0.5 s).
    • Maps open ports to well-known service names where possible.
    • Displays a summary of open ports when finished.

Usage examples:
    python port_scanner.py localhost
    python port_scanner.py 192.168.1.1 -s 20 -e 100
    python port_scanner.py example.com -s 80 -e 443 -t 1.0

⚠  Only scan hosts you own or have explicit permission to scan.
   Unauthorized port scanning may violate laws or network policies.
"""

import argparse
import socket
import time


# ---------------------------------------------------------------------------
# Well-known ports → service name mapping (subset)
# ---------------------------------------------------------------------------
WELL_KNOWN_PORTS: dict[int, str] = {
    20: "FTP-DATA",
    21: "FTP",
    22: "SSH",
    23: "Telnet",
    25: "SMTP",
    53: "DNS",
    80: "HTTP",
    110: "POP3",
    119: "NNTP",
    123: "NTP",
    143: "IMAP",
    161: "SNMP",
    389: "LDAP",
    443: "HTTPS",
    445: "SMB",
    465: "SMTPS",
    514: "Syslog",
    587: "SMTP-Submission",
    636: "LDAPS",
    993: "IMAPS",
    995: "POP3S",
    1433: "MSSQL",
    1521: "Oracle-DB",
    3306: "MySQL",
    3389: "RDP",
    5432: "PostgreSQL",
    5900: "VNC",
    8080: "HTTP-Alt",
    8443: "HTTPS-Alt",
}


def service_name(port: int) -> str:
    """Return the service name for a port, or 'Unknown'."""
    return WELL_KNOWN_PORTS.get(port, "Unknown")


# ---------------------------------------------------------------------------
# Scanner
# ---------------------------------------------------------------------------

def scan_port(host: str, port: int, timeout: float = 0.5) -> bool:
    """
    Try to open a TCP connection to *host*:*port*.

    Returns True if the port is open (connection succeeded), False otherwise.
    """
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.settimeout(timeout)
            # connect_ex returns 0 on success, an error indicator otherwise
            result = sock.connect_ex((host, port))
            return result == 0
    except (socket.gaierror, OSError):
        return False


def scan_range(host: str, start: int, end: int,
               timeout: float = 0.5) -> list[int]:
    """
    Scan TCP ports from *start* to *end* (inclusive) on *host*.

    Returns a sorted list of open port numbers.
    """
    open_ports: list[int] = []
    total = end - start + 1

    print(f"\nScanning {host} — ports {start}–{end} ({total} ports) …\n")
    t0 = time.time()

    for port in range(start, end + 1):
        if scan_port(host, port, timeout):
            svc = service_name(port)
            print(f"  [OPEN] port {port:>5}  ({svc})")
            open_ports.append(port)

    elapsed = time.time() - t0
    print(f"\nScan complete in {elapsed:.2f} s — "
          f"{len(open_ports)} open port(s) found.\n")
    return open_ports


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Basic TCP port scanner (educational use only).",
    )
    parser.add_argument(
        "host",
        help="Target hostname or IP address (e.g. localhost, 192.168.1.1)",
    )
    parser.add_argument(
        "-s", "--start", type=int, default=1, metavar="PORT",
        help="First port in scan range (default: 1)",
    )
    parser.add_argument(
        "-e", "--end", type=int, default=1024, metavar="PORT",
        help="Last port in scan range (default: 1024)",
    )
    parser.add_argument(
        "-t", "--timeout", type=float, default=0.5, metavar="SEC",
        help="Connection timeout in seconds (default: 0.5)",
    )
    return parser


# ---------------------------------------------------------------------------
# Demo / entry point
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    parser = build_parser()
    args = parser.parse_args()

    if args.start < 1 or args.end > 65535 or args.start > args.end:
        parser.error("Port range must be between 1 and 65535, "
                     "and start must be ≤ end.")

    print("=" * 60)
    print("  TCP Port Scanner — Educational Tool")
    print("=" * 60)
    print(f"  Target  : {args.host}")
    print(f"  Ports   : {args.start}–{args.end}")
    print(f"  Timeout : {args.timeout} s")

    open_ports = scan_range(args.host, args.start, args.end, args.timeout)

    if open_ports:
        print("Summary of open ports:")
        print("-" * 40)
        for p in open_ports:
            print(f"  {p:>5}  —  {service_name(p)}")
        print("-" * 40)
    else:
        print("No open ports detected in the given range.")
