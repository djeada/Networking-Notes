#!/usr/bin/env python3
"""WHOIS Lookup Tool — Educational Networking Script

Performs basic WHOIS lookups by connecting directly to WHOIS servers on
port 43 using raw TCP sockets.  This demonstrates how the WHOIS protocol
works at a low level:

  1. Open a TCP connection to the WHOIS server (default: whois.iana.org).
  2. Send the query domain followed by CRLF.
  3. Read the full response until the server closes the connection.

The script also shows how to follow referrals — many top-level WHOIS
servers point to a registrar-specific WHOIS server for detailed records.

Usage:
    python whois_lookup.py example.com
    python whois_lookup.py --server whois.verisign-grs.com example.com
"""

import argparse
import re
import socket
import sys

# Default WHOIS servers per TLD (a small educational subset)
TLD_WHOIS_SERVERS = {
    "com": "whois.verisign-grs.com",
    "net": "whois.verisign-grs.com",
    "org": "whois.pir.org",
    "io":  "whois.nic.io",
    "dev": "whois.nic.google",
    "edu": "whois.educause.edu",
}

IANA_WHOIS = "whois.iana.org"
WHOIS_PORT = 43
RECV_SIZE = 4096
TIMEOUT = 10  # seconds


def whois_query(server: str, domain: str) -> str:
    """Send a WHOIS query and return the raw response text.

    Protocol details (RFC 3912):
      • Client opens TCP to server:43
      • Client sends the query string + CR LF
      • Server replies with free-form text and closes the connection
    """
    print(f"\n  → Connecting to {server}:{WHOIS_PORT} …")
    # Create a TCP socket (AF_INET = IPv4, SOCK_STREAM = TCP)
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.settimeout(TIMEOUT)
        sock.connect((server, WHOIS_PORT))

        # Send the query terminated by CR LF as per RFC 3912
        query = domain + "\r\n"
        sock.sendall(query.encode("ascii"))
        print(f"  → Sent query: {domain!r}")

        # Read the response until the server closes the connection
        chunks = []
        while True:
            try:
                data = sock.recv(RECV_SIZE)
                if not data:
                    break
                chunks.append(data)
            except socket.timeout:
                break

    response = b"".join(chunks).decode("utf-8", errors="replace")
    print(f"  ← Received {len(response)} bytes from {server}")
    return response


def find_referral(response: str) -> str | None:
    """Look for a referral WHOIS server in the response.

    Many TLD WHOIS servers include a line like:
        Registrar WHOIS Server: whois.registrar.example
    or
        refer: whois.registrar.example
    """
    patterns = [
        r"(?i)registrar\s+whois\s+server\s*:\s*(\S+)",
        r"(?i)refer\s*:\s*(\S+)",
        r"(?i)whois\s+server\s*:\s*(\S+)",
    ]
    for pat in patterns:
        match = re.search(pat, response)
        if match:
            return match.group(1).strip().rstrip(".")
    return None


def choose_server(domain: str) -> str:
    """Pick a reasonable starting WHOIS server for the domain's TLD."""
    tld = domain.rsplit(".", 1)[-1].lower()
    return TLD_WHOIS_SERVERS.get(tld, IANA_WHOIS)


def lookup(domain: str, server: str | None = None, follow_referrals: bool = True) -> None:
    """Perform a full WHOIS lookup, optionally following one referral."""
    if server is None:
        server = choose_server(domain)

    print(f"\n{'=' * 60}")
    print(f" WHOIS Lookup for: {domain}")
    print(f" Server          : {server}")
    print(f"{'=' * 60}")

    response = whois_query(server, domain)
    print("\n── Response ──\n")
    print(response)

    # Attempt to follow a referral for more detail
    if follow_referrals:
        referral = find_referral(response)
        if referral and referral.lower() != server.lower():
            print(f"\n  📎 Referral found → {referral}")
            print("     Following referral for detailed record …")
            detail = whois_query(referral, domain)
            print("\n── Detailed Response ──\n")
            print(detail)
        else:
            print("  (no referral found)")


def run_demo() -> None:
    """Offline demo showing what a WHOIS exchange looks like."""
    print("=" * 60)
    print(" WHOIS Lookup — Offline Demo")
    print("=" * 60)
    print()
    print("  The WHOIS protocol (RFC 3912) is one of the simplest")
    print("  Internet protocols:")
    print()
    print("    1. Client opens TCP connection to server port 43.")
    print("    2. Client sends the query (domain name) + CR LF.")
    print("    3. Server sends back free-form text with registration")
    print("       details and closes the connection.")
    print()
    print("  Example exchange:")
    print()
    print("    Client → whois.verisign-grs.com:43")
    print('    Client sends: "example.com\\r\\n"')
    print("    Server responds:")
    print("    ─────────────────────────────────────")

    sample = """\
   Domain Name: EXAMPLE.COM
   Registry Domain ID: 2336799_DOMAIN_COM-VRSN
   Registrar WHOIS Server: whois.iana.org
   Updated Date: 2024-08-14T07:01:34Z
   Creation Date: 1995-08-14T04:00:00Z
   Registry Expiry Date: 2025-08-13T04:00:00Z
   Registrar: RESERVED-Internet Assigned Numbers Authority
   Domain Status: clientDeleteProhibited
   Name Server: A.IANA-SERVERS.NET
   Name Server: B.IANA-SERVERS.NET"""

    for line in sample.splitlines():
        print(f"    {line}")

    print("    ─────────────────────────────────────")
    print()
    print("  To perform a real lookup, run:")
    print("    python whois_lookup.py example.com")
    print()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Perform WHOIS lookups using raw sockets (port 43).",
    )
    parser.add_argument("domain", nargs="?", help="Domain name to look up, e.g. example.com")
    parser.add_argument(
        "--server", default=None,
        help="WHOIS server to query (auto-detected from TLD if omitted).",
    )
    parser.add_argument(
        "--no-follow", action="store_true",
        help="Do not follow referral servers.",
    )
    args = parser.parse_args()

    if args.domain is None:
        run_demo()
        sys.exit(0)

    try:
        lookup(args.domain, server=args.server, follow_referrals=not args.no_follow)
    except socket.gaierror as exc:
        print(f"\n  ✖ DNS resolution failed for WHOIS server: {exc}", file=sys.stderr)
        sys.exit(1)
    except socket.timeout:
        print("\n  ✖ Connection timed out.", file=sys.stderr)
        sys.exit(1)
    except OSError as exc:
        print(f"\n  ✖ Network error: {exc}", file=sys.stderr)
        sys.exit(1)
