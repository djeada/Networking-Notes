#!/usr/bin/env python3
"""
NAT / PAT Simulator
====================
Simulates Network Address Translation (NAT) with Port Address Translation
(PAT / NAPT).  This is a pure educational simulation — no actual packets are
sent.

Concepts demonstrated:
* **Static NAT** — one-to-one mapping of private to public IP.
* **Dynamic NAT** — private IPs are mapped to a pool of public IPs on demand.
* **PAT (Port Address Translation)** — many private IPs share a single public
  IP, distinguished by unique source-port numbers (also called NAPT or
  "overloaded NAT").

The simulator maintains an internal translation table and prints each step so
you can observe exactly how the mappings are created and used.

Usage:
    python nat_simulator.py          # runs the built-in demo scenario
"""

import random
import sys
from collections import OrderedDict


class PATSimulator:
    """Simulate Port Address Translation (many-to-one NAT).

    All private-side connections are translated to a single public IP with
    unique port numbers.
    """

    def __init__(self, public_ip: str, port_start: int = 10000, port_end: int = 65535):
        self.public_ip = public_ip
        self._next_port = port_start
        self._port_end = port_end
        # Translation table: (private_ip, private_port) -> (public_ip, public_port)
        self._table: OrderedDict[tuple, tuple] = OrderedDict()
        # Reverse lookup for incoming replies
        self._reverse: dict[tuple, tuple] = {}

    def _allocate_port(self) -> int:
        """Allocate the next available public-side port number."""
        if self._next_port > self._port_end:
            raise RuntimeError("PAT port pool exhausted")
        port = self._next_port
        self._next_port += 1
        return port

    # -- Outbound (LAN → WAN) -----------------------------------------------
    def translate_outbound(self, src_ip: str, src_port: int,
                           dst_ip: str, dst_port: int) -> dict:
        """Translate an outbound packet from a private host.

        Returns a dict describing the original and translated packet.
        """
        key = (src_ip, src_port)

        # Re-use existing mapping if one exists
        if key in self._table:
            pub_ip, pub_port = self._table[key]
            reused = True
        else:
            pub_port = self._allocate_port()
            pub_ip = self.public_ip
            self._table[key] = (pub_ip, pub_port)
            self._reverse[(pub_ip, pub_port)] = key
            reused = False

        return {
            "direction": "outbound",
            "original": {
                "src": f"{src_ip}:{src_port}",
                "dst": f"{dst_ip}:{dst_port}",
            },
            "translated": {
                "src": f"{pub_ip}:{pub_port}",
                "dst": f"{dst_ip}:{dst_port}",
            },
            "mapping_reused": reused,
        }

    # -- Inbound (WAN → LAN) ------------------------------------------------
    def translate_inbound(self, src_ip: str, src_port: int,
                          dst_ip: str, dst_port: int) -> dict:
        """Translate an inbound reply back to the original private host."""
        key = (dst_ip, dst_port)
        if key not in self._reverse:
            return {
                "direction": "inbound",
                "original": {
                    "src": f"{src_ip}:{src_port}",
                    "dst": f"{dst_ip}:{dst_port}",
                },
                "translated": None,
                "error": "No matching NAT entry — packet dropped",
            }

        priv_ip, priv_port = self._reverse[key]
        return {
            "direction": "inbound",
            "original": {
                "src": f"{src_ip}:{src_port}",
                "dst": f"{dst_ip}:{dst_port}",
            },
            "translated": {
                "src": f"{src_ip}:{src_port}",
                "dst": f"{priv_ip}:{priv_port}",
            },
            "mapping_reused": True,
        }

    def print_table(self) -> None:
        """Print the current NAT translation table."""
        print("  ┌──────────────────────────┬──────────────────────────┐")
        print("  │  Private Side             │  Public Side             │")
        print("  ├──────────────────────────┼──────────────────────────┤")
        if not self._table:
            print("  │  (empty)                 │  (empty)                 │")
        for (priv_ip, priv_port), (pub_ip, pub_port) in self._table.items():
            priv = f"{priv_ip}:{priv_port}"
            pub = f"{pub_ip}:{pub_port}"
            print(f"  │  {priv:<24s}│  {pub:<24s}│")
        print("  └──────────────────────────┴──────────────────────────┘")


# ---------------------------------------------------------------------------
# Display helpers
# ---------------------------------------------------------------------------

def print_packet(result: dict, step: int) -> None:
    """Print a single translation step in a readable format."""
    d = "→ OUTBOUND →" if result["direction"] == "outbound" else "← INBOUND ←"
    print(f"\n  Step {step}  ({d})")
    orig = result["original"]
    print(f"    Original packet : {orig['src']}  →  {orig['dst']}")
    if result.get("translated"):
        trans = result["translated"]
        print(f"    Translated to   : {trans['src']}  →  {trans['dst']}")
        if result.get("mapping_reused"):
            print("    (existing mapping reused)")
        else:
            print("    (new mapping created)")
    else:
        print(f"    ✗ {result.get('error', 'Translation failed')}")


# ---------------------------------------------------------------------------
# Demo scenario
# ---------------------------------------------------------------------------

def run_demo() -> None:
    """Run an educational NAT/PAT demonstration."""
    print("=" * 62)
    print("  NAT / PAT Simulator — Educational Demo")
    print("=" * 62)
    print()
    print("  Scenario:")
    print("    Three private hosts share a single public IP via PAT.")
    print("    Private network : 192.168.1.0/24")
    print("    Public IP       : 203.0.113.1")
    print("    Remote server   : 93.184.216.34 (example.com)")
    print()

    nat = PATSimulator(public_ip="203.0.113.1")

    # --- Outbound traffic from three internal hosts -----------------------
    outbound_packets = [
        ("192.168.1.10", 12345, "93.184.216.34", 80),
        ("192.168.1.20", 54321, "93.184.216.34", 443),
        ("192.168.1.10", 12346, "93.184.216.34", 80),
        ("192.168.1.30", 22222, "93.184.216.34", 80),
        # Retransmit from .10 — should reuse existing mapping
        ("192.168.1.10", 12345, "93.184.216.34", 80),
    ]

    step = 0
    print("-" * 62)
    print("  Phase 1: Outbound packets (LAN → Internet)")
    print("-" * 62)
    for src_ip, src_port, dst_ip, dst_port in outbound_packets:
        step += 1
        result = nat.translate_outbound(src_ip, src_port, dst_ip, dst_port)
        print_packet(result, step)

    print()
    print("-" * 62)
    print("  Current NAT Translation Table")
    print("-" * 62)
    nat.print_table()

    # --- Inbound reply traffic --------------------------------------------
    print()
    print("-" * 62)
    print("  Phase 2: Inbound reply packets (Internet → LAN)")
    print("-" * 62)

    inbound_packets = [
        # Reply from server to the first mapping
        ("93.184.216.34", 80, "203.0.113.1", 10000),
        # Reply to the second mapping
        ("93.184.216.34", 443, "203.0.113.1", 10001),
        # Unsolicited inbound — no mapping exists
        ("93.184.216.34", 80, "203.0.113.1", 55555),
    ]

    for src_ip, src_port, dst_ip, dst_port in inbound_packets:
        step += 1
        result = nat.translate_inbound(src_ip, src_port, dst_ip, dst_port)
        print_packet(result, step)

    print()
    print("-" * 62)
    print("  Key Takeaways")
    print("-" * 62)
    print("  • PAT allows many private hosts to share one public IP.")
    print("  • Each connection is uniquely identified by the public port.")
    print("  • Inbound packets without a matching table entry are dropped,")
    print("    providing a basic layer of security (stateful filtering).")
    print("  • This is why home routers need 'port forwarding' rules for")
    print("    inbound services — there's no pre-existing NAT mapping.")
    print()


def main():
    run_demo()


if __name__ == "__main__":
    main()
