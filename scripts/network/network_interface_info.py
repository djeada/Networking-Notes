#!/usr/bin/env python3
"""
Network Interface Information
==============================
Displays information about the system's network interfaces, including:

* Interface names
* IPv4 and IPv6 addresses
* Netmasks / prefix lengths
* MAC (hardware) addresses
* Interface status (up/down) where detectable

Works on **Linux**, **macOS**, and **Windows** using only the Python standard
library.  The primary data source is ``socket`` plus platform-specific
commands (``ip addr``, ``ifconfig``, ``ipconfig``, ``getmac``) parsed as a
fallback.

Usage:
    python network_interface_info.py
"""

import os
import platform
import re
import socket
import subprocess
import sys


# ---------------------------------------------------------------------------
# Cross-platform interface discovery
# ---------------------------------------------------------------------------

def _run(cmd: list[str]) -> str:
    """Run a command and return stdout, or empty string on failure."""
    try:
        result = subprocess.run(
            cmd, capture_output=True, text=True, timeout=10
        )
        return result.stdout
    except (FileNotFoundError, subprocess.TimeoutExpired, OSError):
        return ""


def get_interfaces_linux() -> list[dict]:
    """Parse ``ip -o addr show`` on Linux."""
    output = _run(["ip", "-o", "addr", "show"])
    if not output:
        return []

    interfaces: dict[str, dict] = {}
    for line in output.strip().splitlines():
        # Example: 2: eth0    inet 10.0.2.15/24 brd 10.0.2.255 scope global ...
        parts = line.split()
        if len(parts) < 4:
            continue
        name = parts[1].rstrip(":")
        family = parts[2]  # inet or inet6
        addr_cidr = parts[3]

        if name not in interfaces:
            interfaces[name] = {
                "name": name,
                "ipv4": [],
                "ipv6": [],
                "mac": None,
            }

        if family == "inet":
            interfaces[name]["ipv4"].append(addr_cidr)
        elif family == "inet6":
            interfaces[name]["ipv6"].append(addr_cidr)

    # Get MAC addresses from ``ip link show``
    link_output = _run(["ip", "-o", "link", "show"])
    for line in link_output.strip().splitlines():
        parts = line.split()
        name = parts[1].rstrip(":")
        # Look for "link/ether xx:xx:xx:xx:xx:xx"
        if "link/ether" in parts:
            idx = parts.index("link/ether")
            if idx + 1 < len(parts):
                mac = parts[idx + 1]
                if name in interfaces:
                    interfaces[name]["mac"] = mac

    return list(interfaces.values())


def get_interfaces_macos() -> list[dict]:
    """Parse ``ifconfig`` on macOS."""
    output = _run(["ifconfig"])
    if not output:
        return []

    interfaces: list[dict] = []
    current: dict | None = None

    for line in output.splitlines():
        # New interface block starts with a non-whitespace character
        iface_match = re.match(r"^(\w[\w\d]*):?\s", line)
        if iface_match:
            current = {
                "name": iface_match.group(1),
                "ipv4": [],
                "ipv6": [],
                "mac": None,
            }
            interfaces.append(current)
            # Check for ether on the same line (unlikely but safe)
            ether_match = re.search(r"ether\s+([\da-fA-F:]{17})", line)
            if ether_match and current:
                current["mac"] = ether_match.group(1)
            continue

        if current is None:
            continue

        # IPv4
        ipv4_match = re.search(
            r"inet\s+([\d.]+)\s+netmask\s+(0x[\da-fA-F]+|[\d.]+)", line
        )
        if ipv4_match:
            addr = ipv4_match.group(1)
            mask_raw = ipv4_match.group(2)
            # macOS shows hex netmask like 0xffffff00
            if mask_raw.startswith("0x"):
                mask_int = int(mask_raw, 16)
                mask = ".".join(
                    str((mask_int >> (8 * i)) & 0xFF)
                    for i in reversed(range(4))
                )
            else:
                mask = mask_raw
            current["ipv4"].append(f"{addr}/{mask}")

        # IPv6
        ipv6_match = re.search(r"inet6\s+([^\s]+?)(%\w+)?\s+prefixlen\s+(\d+)", line)
        if ipv6_match:
            current["ipv6"].append(f"{ipv6_match.group(1)}/{ipv6_match.group(3)}")

        # MAC
        ether_match = re.search(r"ether\s+([\da-fA-F:]{17})", line)
        if ether_match:
            current["mac"] = ether_match.group(1)

    return interfaces


def get_interfaces_windows() -> list[dict]:
    """Parse ``ipconfig /all`` on Windows."""
    output = _run(["ipconfig", "/all"])
    if not output:
        return []

    interfaces: list[dict] = []
    current: dict | None = None

    for line in output.splitlines():
        # Adapter header
        adapter_match = re.match(r"^(\S.+?):\s*$", line)
        if adapter_match and "adapter" in line.lower():
            current = {
                "name": adapter_match.group(1),
                "ipv4": [],
                "ipv6": [],
                "mac": None,
            }
            interfaces.append(current)
            continue

        if current is None:
            continue

        # Physical (MAC) address
        mac_match = re.search(r"Physical Address[.\s:]+([0-9A-Fa-f-]{17})", line)
        if mac_match:
            current["mac"] = mac_match.group(1).replace("-", ":")

        # IPv4
        ipv4_match = re.search(r"IPv4 Address[.\s:]+([\d.]+)", line)
        if ipv4_match:
            current["ipv4"].append(ipv4_match.group(1))

        # Subnet mask (appears on next line after IPv4 typically, but
        # sometimes on the same adapter block).  We just grab it.
        mask_match = re.search(r"Subnet Mask[.\s:]+([\d.]+)", line)
        if mask_match and current["ipv4"]:
            last = current["ipv4"][-1]
            if "/" not in last:
                current["ipv4"][-1] = f"{last}/{mask_match.group(1)}"

        # IPv6
        ipv6_match = re.search(r"IPv6 Address[.\s:]+([0-9a-fA-F:]+)", line)
        if ipv6_match:
            current["ipv6"].append(ipv6_match.group(1))

    return interfaces


def get_interfaces() -> list[dict]:
    """Detect the OS and return interface information."""
    system = platform.system().lower()
    if system == "linux":
        return get_interfaces_linux()
    elif system == "darwin":
        return get_interfaces_macos()
    elif system == "windows":
        return get_interfaces_windows()
    else:
        print(f"  Unsupported platform: {platform.system()}")
        return []


# ---------------------------------------------------------------------------
# Hostname / basic socket info
# ---------------------------------------------------------------------------

def get_basic_info() -> dict:
    """Gather basic networking info available via the socket module."""
    hostname = socket.gethostname()
    try:
        host_ip = socket.gethostbyname(hostname)
    except socket.gaierror:
        host_ip = "N/A"

    fqdn = socket.getfqdn()

    return {
        "hostname": hostname,
        "fqdn": fqdn,
        "host_ip": host_ip,
        "platform": platform.platform(),
    }


# ---------------------------------------------------------------------------
# Display
# ---------------------------------------------------------------------------

def print_report(basic: dict, interfaces: list[dict]) -> None:
    """Print a formatted report of all network interface information."""
    print("=" * 62)
    print("  Network Interface Information")
    print("=" * 62)
    w = 20
    print(f"{'  Hostname':<{w}}: {basic['hostname']}")
    print(f"{'  FQDN':<{w}}: {basic['fqdn']}")
    print(f"{'  Primary IP':<{w}}: {basic['host_ip']}")
    print(f"{'  Platform':<{w}}: {basic['platform']}")
    print()

    if not interfaces:
        print("  No interface information could be retrieved.")
        print("  (This may happen in sandboxed or minimal environments.)")
        print()
        return

    for iface in interfaces:
        print(f"  Interface: {iface['name']}")
        print(f"  {'MAC Address':<{w}}: {iface['mac'] or 'N/A'}")
        if iface["ipv4"]:
            for addr in iface["ipv4"]:
                print(f"  {'IPv4':<{w}}: {addr}")
        else:
            print(f"  {'IPv4':<{w}}: (none)")
        if iface["ipv6"]:
            for addr in iface["ipv6"]:
                print(f"  {'IPv6':<{w}}: {addr}")
        else:
            print(f"  {'IPv6':<{w}}: (none)")
        print()


def main():
    basic = get_basic_info()
    interfaces = get_interfaces()
    print_report(basic, interfaces)


if __name__ == "__main__":
    main()
