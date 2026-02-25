#!/usr/bin/env python3
"""
VLAN Tag Simulator (IEEE 802.1Q)
=================================
Simulates how IEEE 802.1Q VLAN tagging works on Ethernet frames within a
multi-switch network. Demonstrates the core data-link-layer mechanism that
allows a single physical network to be partitioned into isolated broadcast
domains.

Concepts demonstrated:
* 802.1Q tag insertion: a 4-byte header (TPID 0x8100 + TCI) is inserted
  between the source MAC and the EtherType of an Ethernet frame.
* Access ports: connect end-hosts; frames arrive untagged, the switch adds
  the port's configured VLAN ID on ingress and strips it on egress.
* Trunk ports: carry frames for multiple VLANs between switches; frames
  remain tagged while traversing the trunk link.
* VLAN isolation: hosts on different VLANs share the same physical cable
  but cannot communicate at Layer 2 without a router (inter-VLAN routing).

Usage:
    python vlan_tag_simulator.py                    # runs built-in demo
    python vlan_tag_simulator.py --vlans 10 20 30   # custom VLAN IDs
"""

import argparse
import textwrap
from dataclasses import dataclass, field
from typing import Dict, List, Optional


@dataclass
class EthernetFrame:
    src_mac: str
    dst_mac: str
    ethertype: str = "0x0800"
    payload: str = ""
    vlan_tag: Optional[int] = None

    def __str__(self):
        tag = f"  802.1Q Tag: VLAN {self.vlan_tag}" if self.vlan_tag else "  (untagged)"
        return (f"[Frame {self.src_mac} -> {self.dst_mac} | "
                f"EtherType={self.ethertype}{' | VLAN=' + str(self.vlan_tag) if self.vlan_tag else ''}]")

    def tagged_repr(self):
        if self.vlan_tag is None:
            return f"|{self.dst_mac}|{self.src_mac}|{self.ethertype}|{self.payload}|"
        return (f"|{self.dst_mac}|{self.src_mac}|0x8100|VLAN={self.vlan_tag}|"
                f"{self.ethertype}|{self.payload}|")


@dataclass
class SwitchPort:
    name: str
    mode: str  # "access" or "trunk"
    vlan: int = 1  # access VLAN (only meaningful for access ports)
    allowed_vlans: List[int] = field(default_factory=lambda: [1])
    connected_host: Optional[str] = None


class Switch:
    def __init__(self, name: str, ports: List[SwitchPort]):
        self.name = name
        self.ports = {p.name: p for p in ports}
        self.mac_table: Dict[str, str] = {}

    def receive_frame(self, port_name: str, frame: EthernetFrame) -> List[tuple]:
        """Process an incoming frame; return list of (port_name, frame) to forward."""
        port = self.ports[port_name]
        results = []
        print(f"\n  [{self.name}] Received {frame} on port {port_name} ({port.mode})")

        # Ingress: tag if access port
        if port.mode == "access":
            if frame.vlan_tag is not None:
                print(f"    ⚠  Access port received tagged frame — dropping.")
                return []
            frame.vlan_tag = port.vlan
            print(f"    → Ingress: tagged frame with VLAN {port.vlan}")
        else:
            if frame.vlan_tag is None:
                frame.vlan_tag = 1  # native VLAN
                print(f"    → Trunk ingress: untagged → native VLAN 1")
            elif frame.vlan_tag not in port.allowed_vlans:
                print(f"    ⚠  VLAN {frame.vlan_tag} not allowed on trunk — dropping.")
                return []
            else:
                print(f"    → Trunk ingress: VLAN {frame.vlan_tag} allowed")

        # Learn source MAC
        self.mac_table[frame.src_mac] = port_name
        print(f"    → MAC table learn: {frame.src_mac} on {port_name}")

        # Forwarding decision
        if frame.dst_mac in self.mac_table:
            out_port_name = self.mac_table[frame.dst_mac]
            out_port = self.ports[out_port_name]
            print(f"    → Unicast forward to {out_port_name}")
            out_frame = self._egress(out_port, frame)
            if out_frame:
                results.append((out_port_name, out_frame))
        else:
            print(f"    → Flooding to all ports in VLAN {frame.vlan_tag}")
            for pn, p in self.ports.items():
                if pn == port_name:
                    continue
                if p.mode == "access" and p.vlan != frame.vlan_tag:
                    continue
                if p.mode == "trunk" and frame.vlan_tag not in p.allowed_vlans:
                    continue
                out_frame = self._egress(p, frame)
                if out_frame:
                    results.append((pn, out_frame))

        return results

    def _egress(self, port: SwitchPort, frame: EthernetFrame) -> Optional[EthernetFrame]:
        out = EthernetFrame(frame.src_mac, frame.dst_mac, frame.ethertype,
                            frame.payload, frame.vlan_tag)
        if port.mode == "access":
            print(f"    → Egress {port.name}: stripping tag, delivering untagged")
            out.vlan_tag = None
        else:
            print(f"    → Egress {port.name}: keeping VLAN tag {out.vlan_tag} (trunk)")
        return out


def build_demo_topology(vlans: List[int]):
    """Two switches connected by a trunk, each with access ports."""
    v1, v2 = vlans[0], vlans[1] if len(vlans) > 1 else vlans[0]
    sw1_ports = [
        SwitchPort("Fa0/1", "access", v1, connected_host="HostA"),
        SwitchPort("Fa0/2", "access", v2, connected_host="HostB"),
        SwitchPort("Gi0/1", "trunk", allowed_vlans=vlans),
    ]
    sw2_ports = [
        SwitchPort("Fa0/1", "access", v1, connected_host="HostC"),
        SwitchPort("Fa0/2", "access", v2, connected_host="HostD"),
        SwitchPort("Gi0/1", "trunk", allowed_vlans=vlans),
    ]
    return Switch("SW1", sw1_ports), Switch("SW2", sw2_ports)


def demo(vlans: List[int]):
    print("=" * 65)
    print("  IEEE 802.1Q VLAN Tagging Simulator")
    print("=" * 65)
    print(f"\nVLANs in use: {vlans}")
    sw1, sw2 = build_demo_topology(vlans)
    v1, v2 = vlans[0], vlans[1] if len(vlans) > 1 else vlans[0]

    topology = textwrap.dedent(f"""\
    Topology
    --------
       [HostA]---(Fa0/1 VLAN {v1})---[SW1]---(Gi0/1 trunk)---[SW2]---(Fa0/1 VLAN {v1})---[HostC]
       [HostB]---(Fa0/2 VLAN {v2})---[SW1]                    [SW2]---(Fa0/2 VLAN {v2})---[HostD]
    """)
    print(topology)

    scenarios = [
        ("Same VLAN, same switch",
         "Fa0/1", sw1,
         EthernetFrame("AA:AA:AA:00:00:01", "FF:FF:FF:FF:FF:FF",
                        payload="ARP Who has 10.0.10.2?")),
        ("Same VLAN, across trunk",
         "Fa0/1", sw1,
         EthernetFrame("AA:AA:AA:00:00:01", "CC:CC:CC:00:00:01",
                        payload="ICMP Echo to HostC")),
        ("Different VLAN — should be isolated",
         "Fa0/1", sw1,
         EthernetFrame("AA:AA:AA:00:00:01", "BB:BB:BB:00:00:01",
                        payload="Attempt to reach HostB on VLAN " + str(v2))),
        ("Cross-switch trunk relay",
         "Gi0/1", sw2,
         EthernetFrame("AA:AA:AA:00:00:01", "CC:CC:CC:00:00:01",
                        payload="Data via trunk", vlan_tag=v1)),
    ]

    for i, (title, port, switch, frame) in enumerate(scenarios, 1):
        print(f"\n{'─' * 65}")
        print(f"  Scenario {i}: {title}")
        print(f"{'─' * 65}")
        print(f"  Original frame: {frame.tagged_repr()}")
        forwarded = switch.receive_frame(port, frame)
        if not forwarded:
            print("  Result: frame was dropped (VLAN isolation in effect).")
        for pname, fwd_frame in forwarded:
            print(f"  → Delivered on {pname}: {fwd_frame.tagged_repr()}")

    print(f"\n{'=' * 65}")
    print("  Key takeaway: VLANs create separate broadcast domains on the")
    print("  same physical infrastructure. Trunk links carry multiple VLANs")
    print("  using 802.1Q tags; access ports strip tags for end-hosts.")
    print("=" * 65)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="IEEE 802.1Q VLAN tagging simulator")
    parser.add_argument("--vlans", nargs="+", type=int, default=[10, 20],
                        help="VLAN IDs to simulate (default: 10 20)")
    args = parser.parse_args()
    demo(args.vlans)
