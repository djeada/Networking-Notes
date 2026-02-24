#!/usr/bin/env python3
"""
DNS Lookup Tool
===============
Performs DNS lookups using Python's socket module.

DNS (Domain Name System) translates human-readable hostnames (e.g., example.com)
into IP addresses (e.g., 93.184.216.34) that computers use to communicate.

This script demonstrates:
  - Forward lookup: hostname -> IP address(es)
  - Reverse lookup: IP address -> hostname
  - Retrieving address info (simulating different record types)

Usage:
    python dns_lookup.py example.com
    python dns_lookup.py --reverse 93.184.216.34
    python dns_lookup.py example.com --all
"""

import argparse
import socket
import sys


def forward_lookup(hostname):
    """Resolve a hostname to its IP address(es).

    This is the most common DNS operation — converting a domain name
    to the IP address a client needs to connect to.
    """
    print(f"\n--- Forward DNS Lookup for '{hostname}' ---")
    try:
        # gethostbyname returns a single IPv4 address
        ip = socket.gethostbyname(hostname)
        print(f"  Primary IP (A record): {ip}")
    except socket.gaierror as e:
        print(f"  Error resolving hostname: {e}")
        return

    try:
        # gethostbyname_ex returns (hostname, aliases, ip_list)
        canonical, aliases, ip_list = socket.gethostbyname_ex(hostname)
        print(f"  Canonical name: {canonical}")
        if aliases:
            print(f"  Aliases (CNAME): {', '.join(aliases)}")
        if len(ip_list) > 1:
            print(f"  All IPs: {', '.join(ip_list)}")
    except socket.gaierror:
        pass


def reverse_lookup(ip_address):
    """Resolve an IP address back to a hostname (PTR record equivalent).

    Reverse DNS maps an IP address to a domain name — the opposite of a
    forward lookup. Not all IPs have reverse DNS entries configured.
    """
    print(f"\n--- Reverse DNS Lookup for '{ip_address}' ---")
    try:
        hostname, aliases, _ = socket.gethostbyaddr(ip_address)
        print(f"  Hostname: {hostname}")
        if aliases:
            print(f"  Aliases: {', '.join(aliases)}")
    except socket.herror as e:
        print(f"  Reverse lookup failed: {e}")
    except socket.gaierror as e:
        print(f"  Invalid address: {e}")


def address_info_lookup(hostname, port=80):
    """Use getaddrinfo to retrieve detailed address information.

    getaddrinfo is the modern way to resolve hostnames. It supports both
    IPv4 and IPv6, and returns results suitable for creating sockets.

    Each result is a tuple: (family, type, proto, canonname, sockaddr)
      - family:   AF_INET (IPv4) or AF_INET6 (IPv6)
      - type:     SOCK_STREAM (TCP) or SOCK_DGRAM (UDP)
      - proto:    protocol number (6=TCP, 17=UDP)
      - sockaddr: (ip, port) for IPv4; (ip, port, flow, scope) for IPv6
    """
    print(f"\n--- Address Info for '{hostname}' (port {port}) ---")

    family_names = {
        socket.AF_INET: "IPv4",
        socket.AF_INET6: "IPv6",
    }
    type_names = {
        socket.SOCK_STREAM: "TCP (SOCK_STREAM)",
        socket.SOCK_DGRAM: "UDP (SOCK_DGRAM)",
    }

    try:
        results = socket.getaddrinfo(hostname, port)
        seen = set()
        for family, socktype, proto, canonname, sockaddr in results:
            key = (family, socktype, sockaddr)
            if key in seen:
                continue
            seen.add(key)

            fam = family_names.get(family, str(family))
            styp = type_names.get(socktype, str(socktype))
            addr = sockaddr[0]
            print(f"  {fam:5s} | {styp:20s} | {addr}")
    except socket.gaierror as e:
        print(f"  Lookup failed: {e}")


def main():
    parser = argparse.ArgumentParser(
        description="DNS Lookup Tool — resolve hostnames and IP addresses."
    )
    parser.add_argument(
        "target",
        help="Hostname or IP address to look up",
    )
    parser.add_argument(
        "--reverse", "-r",
        action="store_true",
        help="Perform a reverse lookup (IP -> hostname)",
    )
    parser.add_argument(
        "--all", "-a",
        action="store_true",
        help="Show detailed address info (IPv4/IPv6, TCP/UDP)",
    )
    args = parser.parse_args()

    if args.reverse:
        reverse_lookup(args.target)
    else:
        forward_lookup(args.target)
        if args.all:
            address_info_lookup(args.target)


if __name__ == "__main__":
    # If no arguments provided, run a quick demo
    if len(sys.argv) == 1:
        print("=" * 55)
        print("  DNS Lookup Tool — Educational Demo")
        print("=" * 55)
        print("\nDNS is the internet's phone book. It maps domain names")
        print("to IP addresses so browsers and apps know where to connect.\n")

        demo_host = "example.com"
        forward_lookup(demo_host)
        address_info_lookup(demo_host)

        # Reverse lookup on the resolved IP
        try:
            ip = socket.gethostbyname(demo_host)
            reverse_lookup(ip)
        except socket.gaierror:
            pass

        print("\n--- Usage ---")
        print("  python dns_lookup.py example.com")
        print("  python dns_lookup.py --reverse 93.184.216.34")
        print("  python dns_lookup.py example.com --all")
    else:
        main()
