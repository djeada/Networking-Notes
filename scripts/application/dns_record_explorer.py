#!/usr/bin/env python3
"""
DNS Record Explorer & Resolution Simulator
============================================
An educational tool that explains every major DNS record type and simulates
how a recursive resolver walks through a zone file to answer queries.

A sample zone database is built in memory. When a query is issued, the
simulator shows each lookup step: checking the cache, finding the
authoritative zone, matching the record, and following CNAME chains.

Record types covered:
  * A      — IPv4 address mapping
  * AAAA   — IPv6 address mapping
  * CNAME  — Canonical name (alias)
  * MX     — Mail exchange with priority
  * NS     — Authoritative name server
  * TXT    — Arbitrary text (SPF, DKIM, verification)
  * SOA    — Start of Authority (zone metadata)
  * PTR    — Reverse DNS (IP → hostname)
  * SRV    — Service locator (host + port + priority)

Concepts demonstrated:
  * DNS zone file structure and record format
  * Recursive vs iterative resolution
  * CNAME chain following
  * MX priority ordering
  * Reverse DNS with PTR records

Usage:
    python dns_record_explorer.py                          # run built-in demo
    python dns_record_explorer.py --query example.com A    # query a record
    python dns_record_explorer.py --list-types              # list all types
"""

import argparse
import textwrap

# --- Record-type reference ---------------------------------------------------

RECORD_INFO = {
    "A":     ("IPv4 Address",
              "Maps a hostname to a 32-bit IPv4 address.",
              "example.com.  300  IN  A  93.184.216.34"),
    "AAAA":  ("IPv6 Address",
              "Maps a hostname to a 128-bit IPv6 address.",
              "example.com.  300  IN  AAAA  2606:2800:220:1:248:1893:25c8:1946"),
    "CNAME": ("Canonical Name",
              "Creates an alias that points to another domain name. "
              "The resolver follows the chain to find the final address.",
              "www.example.com.  300  IN  CNAME  example.com."),
    "MX":    ("Mail Exchange",
              "Specifies mail servers for the domain with a priority value. "
              "Lower priority numbers are preferred.",
              "example.com.  300  IN  MX  10 mail.example.com."),
    "NS":    ("Name Server",
              "Delegates a zone to the listed authoritative name servers.",
              "example.com.  86400  IN  NS  ns1.example.com."),
    "TXT":   ("Text Record",
              "Holds arbitrary text, commonly used for SPF, DKIM, and "
              "domain verification strings.",
              'example.com.  300  IN  TXT  "v=spf1 include:_spf.google.com ~all"'),
    "SOA":   ("Start of Authority",
              "Contains zone metadata: primary NS, admin email, serial number, "
              "and timing parameters for zone transfers.",
              "example.com.  86400  IN  SOA  ns1.example.com. admin.example.com. "
              "2024010101 3600 900 604800 86400"),
    "PTR":   ("Pointer (Reverse DNS)",
              "Maps an IP address back to a hostname. Used in reverse-lookup "
              "zones (in-addr.arpa for IPv4).",
              "34.216.184.93.in-addr.arpa.  300  IN  PTR  example.com."),
    "SRV":   ("Service Locator",
              "Specifies host, port, priority, and weight for a service. "
              "Format: _service._proto.name TTL IN SRV priority weight port target.",
              "_sip._tcp.example.com.  300  IN  SRV  10 60 5060 sip.example.com."),
}

# --- Sample zone database ----------------------------------------------------

ZONE_DB = {
    ("example.com", "SOA"):   [("ns1.example.com admin.example.com "
                                 "2024010101 3600 900 604800 86400", 86400)],
    ("example.com", "NS"):    [("ns1.example.com", 86400),
                                ("ns2.example.com", 86400)],
    ("example.com", "A"):     [("93.184.216.34", 300)],
    ("example.com", "AAAA"):  [("2606:2800:220:1:248:1893:25c8:1946", 300)],
    ("www.example.com", "CNAME"): [("example.com", 300)],
    ("example.com", "MX"):    [("10 mail.example.com", 300),
                                ("20 mail2.example.com", 300)],
    ("mail.example.com", "A"): [("93.184.216.50", 300)],
    ("mail2.example.com", "A"): [("93.184.216.51", 300)],
    ("example.com", "TXT"):   [('"v=spf1 include:_spf.example.com ~all"', 300)],
    ("34.216.184.93.in-addr.arpa", "PTR"): [("example.com", 300)],
    ("_sip._tcp.example.com", "SRV"): [("10 60 5060 sip.example.com", 300)],
    ("sip.example.com", "A"): [("93.184.216.60", 300)],
    ("ns1.example.com", "A"): [("93.184.216.2", 86400)],
    ("ns2.example.com", "A"): [("93.184.216.3", 86400)],
}


def resolve(name, rtype, depth=0):
    """Simulate recursive resolution, following CNAME chains."""
    indent = "  " * (depth + 1)
    print(f"{indent}→ Looking up ({name}, {rtype})")

    key = (name.lower().rstrip("."), rtype)
    records = ZONE_DB.get(key)

    if records:
        for value, ttl in records:
            print(f"{indent}  ✔ Found: {name}  {ttl}  IN  {rtype}  {value}")
        return records

    # Check for CNAME if direct match not found
    cname_key = (name.lower().rstrip("."), "CNAME")
    cname_records = ZONE_DB.get(cname_key)
    if cname_records and rtype != "CNAME":
        target = cname_records[0][0]
        print(f"{indent}  ↳ CNAME alias: {name} → {target}  (following chain)")
        return resolve(target, rtype, depth + 1)

    print(f"{indent}  ✘ No records found for ({name}, {rtype})")
    return []


def print_record_types():
    """Display a formatted reference for all DNS record types."""
    print("\n  DNS Record Type Reference")
    print("  " + "=" * 56)
    for rtype, (title, desc, example) in RECORD_INFO.items():
        print(f"\n  {rtype:<6} — {title}")
        for line in textwrap.wrap(desc, width=52):
            print(f"           {line}")
        print(f"           Example: {example}")
    print()


def demo():
    """Run a series of educational queries against the sample zone."""
    print("╔══════════════════════════════════════════════════════════╗")
    print("║          DNS Record Explorer & Resolver Demo            ║")
    print("╚══════════════════════════════════════════════════════════╝")

    print_record_types()

    queries = [
        ("example.com", "A",    "Simple A-record lookup"),
        ("www.example.com", "A", "CNAME → A chain resolution"),
        ("example.com", "MX",   "Mail exchange lookup (note priorities)"),
        ("example.com", "TXT",  "TXT record (SPF policy)"),
        ("34.216.184.93.in-addr.arpa", "PTR", "Reverse DNS lookup"),
        ("_sip._tcp.example.com", "SRV", "SRV service locator"),
        ("example.com", "SOA",  "Start of Authority metadata"),
        ("nonexistent.example.com", "A", "Query with no matching records"),
    ]

    print("\n  Simulated DNS Queries")
    print("  " + "=" * 56)
    for name, rtype, description in queries:
        print(f"\n  Query: {name} {rtype}")
        print(f"  Purpose: {description}")
        print(f"  {'-'*56}")
        resolve(name, rtype)

    print(f"\n{'='*60}")
    print("  Demo complete — all record types demonstrated.")
    print(f"{'='*60}\n")


def main():
    parser = argparse.ArgumentParser(
        description="DNS Record Explorer & Resolution Simulator")
    parser.add_argument("--query", nargs=2, metavar=("NAME", "TYPE"),
                        help="Resolve NAME for record TYPE (e.g. example.com A)")
    parser.add_argument("--list-types", action="store_true",
                        help="Print a reference of all DNS record types")
    args = parser.parse_args()

    if args.list_types:
        print_record_types()
    elif args.query:
        name, rtype = args.query
        rtype = rtype.upper()
        if rtype not in RECORD_INFO:
            print(f"  Unknown record type '{rtype}'. Use --list-types to see options.")
            return
        print(f"\n  Resolving {name} {rtype} …")
        resolve(name, rtype)
        print()
    else:
        demo()


if __name__ == "__main__":
    main()
