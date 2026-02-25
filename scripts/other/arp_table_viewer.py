#!/usr/bin/env python3
"""ARP Table Viewer — Educational Networking Script

Displays and explains the system's ARP (Address Resolution Protocol) table.

  • On **Linux**, reads directly from /proc/net/arp (a virtual file
    exported by the kernel).
  • On **other platforms** (macOS, Windows), falls back to parsing the
    output of the ``arp`` command via subprocess.

For each entry the script explains what each field means and why ARP is
essential for mapping Layer-3 (IP) addresses to Layer-2 (MAC) addresses
on a local network.

Usage:
    python arp_table_viewer.py           # show current ARP table
    python arp_table_viewer.py --demo    # show a sample table with explanations
"""

from __future__ import annotations

import argparse
import os
import platform
import subprocess
import sys
import textwrap

# ── ARP entry representation ────────────────────────────────────────────

# ARP hardware-type flags from the Linux kernel (include/uapi/linux/if_arp.h)
HW_TYPES = {
    "0x1": "Ethernet (10 Mbps)",
    "0x6": "IEEE 802 (Token Ring)",
    "0xF": "Frame Relay",
}

# ARP flags bitmask (Linux /proc/net/arp)
ARP_FLAGS = {
    0x0: "incomplete",
    0x2: "complete (C)",
    0x4: "permanent (P)",
    0x6: "complete + permanent",
}


def explain_arp() -> None:
    """Print a short educational primer on ARP."""
    print(textwrap.dedent("""\
    ── What is ARP? ──────────────────────────────────────────────────

      ARP (Address Resolution Protocol, RFC 826) maps a Layer-3 address
      (IPv4) to a Layer-2 address (MAC) on a local network segment.

      When host A wants to send a packet to host B on the same subnet:
        1. A checks its ARP cache for B's MAC address.
        2. If not found, A broadcasts an ARP Request:
             "Who has 192.168.1.5?  Tell 192.168.1.100"
        3. B replies with an ARP Reply (unicast):
             "192.168.1.5 is at aa:bb:cc:dd:ee:ff"
        4. A caches the mapping and sends the Ethernet frame.

      The ARP table (cache) stores recent mappings so the host does not
      need to broadcast for every single packet.

      Fields in the ARP table:
        • IP address   — the Layer-3 address
        • HW type      — usually 0x1 (Ethernet)
        • Flags        — 0x2 = complete, 0x0 = incomplete (no reply yet)
        • HW address   — the Layer-2 (MAC) address
        • Mask         — (rarely used) subnet mask for proxy ARP
        • Device       — the network interface this entry is on
    """))


# ── Platform-specific readers ────────────────────────────────────────────

def read_proc_arp() -> list[dict]:
    """Read /proc/net/arp on Linux and return a list of entries."""
    entries = []
    with open("/proc/net/arp") as f:
        header = f.readline()  # skip header
        for line in f:
            parts = line.split()
            if len(parts) < 6:
                continue
            entries.append({
                "ip":      parts[0],
                "hw_type": parts[1],
                "flags":   parts[2],
                "mac":     parts[3],
                "mask":    parts[4],
                "device":  parts[5],
            })
    return entries


def read_arp_command() -> list[dict]:
    """Run the 'arp -a' command and parse output (macOS / Windows / fallback)."""
    try:
        result = subprocess.run(
            ["arp", "-a"],
            capture_output=True, text=True, timeout=5,
        )
    except FileNotFoundError:
        print("  ⚠  'arp' command not found on this system.", file=sys.stderr)
        return []

    entries = []
    for line in result.stdout.splitlines():
        # Typical macOS/Linux format: host (ip) at mac on iface ...
        # Typical Windows format varies — best effort parsing
        line = line.strip()
        if not line or line.startswith("Address") or line.startswith("Interface"):
            continue
        parts = line.split()
        ip = mac = device = "?"
        for i, p in enumerate(parts):
            if p.startswith("(") and p.endswith(")"):
                ip = p.strip("()")
            elif ":" in p and len(p) >= 11:
                mac = p
            elif p == "on" and i + 1 < len(parts):
                device = parts[i + 1]
        # Fallback for Windows-style output
        if ip == "?" and len(parts) >= 3:
            ip = parts[0]
            mac = parts[1]
            device = parts[2] if len(parts) > 2 else "?"
        if ip != "?":
            entries.append({
                "ip":      ip,
                "hw_type": "0x1",
                "flags":   "0x2",
                "mac":     mac,
                "mask":    "*",
                "device":  device,
            })
    return entries


def get_arp_entries() -> list[dict]:
    """Return the current ARP table using the best available method."""
    if platform.system() == "Linux" and os.path.exists("/proc/net/arp"):
        return read_proc_arp()
    return read_arp_command()


# ── Display ──────────────────────────────────────────────────────────────

def display_table(entries: list[dict]) -> None:
    """Pretty-print the ARP table with explanations."""
    if not entries:
        print("  (ARP table is empty or could not be read)\n")
        return

    header = (
        f"  {'IP Address':<18} {'MAC Address':<20} {'HW Type':<12} "
        f"{'Flags':<10} {'Device':<10}"
    )
    print(header)
    print("  " + "─" * (len(header) - 2))

    for e in entries:
        hw_desc = HW_TYPES.get(e["hw_type"], e["hw_type"])
        flag_int = int(e["flags"], 16) if e["flags"].startswith("0x") else 0
        flag_desc = ARP_FLAGS.get(flag_int, e["flags"])
        print(
            f"  {e['ip']:<18} {e['mac']:<20} {hw_desc:<12} "
            f"{flag_desc:<10} {e['device']:<10}"
        )

    print(f"\n  Total entries: {len(entries)}\n")


# ── Demo mode ────────────────────────────────────────────────────────────

SAMPLE_ENTRIES = [
    {"ip": "192.168.1.1",   "hw_type": "0x1", "flags": "0x2",
     "mac": "aa:bb:cc:dd:ee:01", "mask": "*", "device": "eth0"},
    {"ip": "192.168.1.50",  "hw_type": "0x1", "flags": "0x2",
     "mac": "aa:bb:cc:dd:ee:32", "mask": "*", "device": "eth0"},
    {"ip": "192.168.1.100", "hw_type": "0x1", "flags": "0x0",
     "mac": "00:00:00:00:00:00", "mask": "*", "device": "eth0"},
    {"ip": "10.0.0.1",      "hw_type": "0x1", "flags": "0x4",
     "mac": "02:42:ac:11:00:01", "mask": "*", "device": "docker0"},
]


def run_demo() -> None:
    print("=" * 60)
    print(" ARP Table Viewer — Demo Mode")
    print("=" * 60)
    explain_arp()

    print("── Sample ARP Table ──\n")
    display_table(SAMPLE_ENTRIES)

    print("  Explanation of sample entries:")
    print("    • 192.168.1.1   — the default gateway, fully resolved (complete).")
    print("    • 192.168.1.50  — another host, MAC address known.")
    print("    • 192.168.1.100 — incomplete entry: ARP request sent but no")
    print("                      reply received yet (MAC is all zeros).")
    print("    • 10.0.0.1      — permanent entry (e.g. Docker bridge),")
    print("                      will not expire from the cache.\n")


# ── Entry point ──────────────────────────────────────────────────────────

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Display and explain the ARP table.")
    parser.add_argument("--demo", action="store_true", help="Show a sample ARP table with explanations.")
    args = parser.parse_args()

    if args.demo:
        run_demo()
        sys.exit(0)

    print("=" * 60)
    print(" ARP Table Viewer")
    print("=" * 60)
    explain_arp()

    print("── Current ARP Table ──\n")
    entries = get_arp_entries()
    display_table(entries)
