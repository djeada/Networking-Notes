#!/usr/bin/env python3
"""
DHCP DORA Process Simulator
=============================
Simulates the Dynamic Host Configuration Protocol (DHCP) four-step process
that clients use to obtain network configuration from a server:

  1. DISCOVER - Client broadcasts a request for any available DHCP server.
  2. OFFER    - Server responds with an available IP and configuration.
  3. REQUEST  - Client formally requests the offered IP address.
  4. ACKNOWLEDGE - Server confirms the lease and sends final parameters.

The simulator maintains a lease table tracking assigned addresses, lease
durations, and client identifiers (MAC addresses). When the address pool
is exhausted, new clients are refused with a NACK.

Concepts demonstrated:
  * DHCP DORA handshake and packet flow
  * IP address pool management and lease tracking
  * Network parameters: subnet mask, default gateway, DNS server
  * Lease expiration and renewal mechanics
  * Broadcast vs unicast communication in DHCP

Usage:
    python dhcp_simulator.py                        # run built-in demo
    python dhcp_simulator.py --clients 10           # simulate 10 clients
    python dhcp_simulator.py --pool-start 10.0.0.50 --pool-size 5
"""

import argparse
import random
import time
from datetime import datetime, timedelta


class DHCPServer:
    """Simulates a DHCP server with an address pool and lease table."""

    def __init__(self, pool_start, pool_size, subnet_mask="255.255.255.0",
                 gateway="192.168.1.1", dns_server="8.8.8.8", lease_time=3600):
        octets = list(map(int, pool_start.split(".")))
        self.pool = []
        for i in range(pool_size):
            ip = f"{octets[0]}.{octets[1]}.{octets[2]}.{octets[3] + i}"
            self.pool.append(ip)
        self.available = list(self.pool)
        self.leases = {}
        self.subnet_mask = subnet_mask
        self.gateway = gateway
        self.dns_server = dns_server
        self.lease_time = lease_time
        self.transaction_id = 0

    def _next_xid(self):
        self.transaction_id += 1
        return f"0x{self.transaction_id:08X}"

    def handle_discover(self, client_mac):
        """Process DHCPDISCOVER and return an offer or None."""
        xid = self._next_xid()
        print(f"\n{'='*60}")
        print(f"  [DISCOVER] Client {client_mac} broadcasts DHCPDISCOVER")
        print(f"    Transaction ID : {xid}")
        print(f"    Src IP: 0.0.0.0  →  Dst IP: 255.255.255.255")
        print(f"    \"I need an IP address! Is any DHCP server out there?\"")

        if not self.available:
            print(f"  [SERVER]   No addresses available — ignoring discover.")
            return None
        offered_ip = self.available[0]
        return {"xid": xid, "offered_ip": offered_ip, "client_mac": client_mac}

    def handle_offer(self, discover_result):
        """Send DHCPOFFER to the client."""
        ip = discover_result["offered_ip"]
        mac = discover_result["client_mac"]
        xid = discover_result["xid"]
        print(f"\n  [OFFER]    Server offers {ip} to {mac}")
        print(f"    Transaction ID : {xid}")
        print(f"    Offered IP     : {ip}")
        print(f"    Subnet Mask    : {self.subnet_mask}")
        print(f"    Default Gateway: {self.gateway}")
        print(f"    DNS Server     : {self.dns_server}")
        print(f"    Lease Time     : {self.lease_time}s")
        print(f"    \"Here's an address you can use!\"")
        return discover_result

    def handle_request(self, offer_result):
        """Process DHCPREQUEST from the client."""
        ip = offer_result["offered_ip"]
        mac = offer_result["client_mac"]
        xid = offer_result["xid"]
        print(f"\n  [REQUEST]  Client {mac} requests {ip}")
        print(f"    Transaction ID : {xid}")
        print(f"    Src IP: 0.0.0.0  →  Dst IP: 255.255.255.255")
        print(f"    Requested IP   : {ip}")
        print(f"    \"I'd like to use {ip}, please confirm!\"")
        return offer_result

    def handle_acknowledge(self, request_result):
        """Send DHCPACK and commit the lease."""
        ip = request_result["offered_ip"]
        mac = request_result["client_mac"]
        xid = request_result["xid"]

        if ip not in self.available:
            print(f"\n  [NACK]     Server NACK — {ip} no longer available!")
            return False

        self.available.remove(ip)
        now = datetime.now()
        self.leases[ip] = {
            "client_mac": mac,
            "lease_start": now,
            "lease_end": now + timedelta(seconds=self.lease_time),
            "xid": xid,
        }
        print(f"\n  [ACK]      Server acknowledges {ip} → {mac}")
        print(f"    Transaction ID : {xid}")
        print(f"    Assigned IP    : {ip}")
        print(f"    Lease Start    : {now:%H:%M:%S}")
        print(f"    Lease Expires  : {self.leases[ip]['lease_end']:%H:%M:%S}")
        print(f"    \"You're all set! Welcome to the network.\"")
        return True

    def run_dora(self, client_mac):
        """Execute the full DORA sequence for a single client."""
        disc = self.handle_discover(client_mac)
        if disc is None:
            return False
        offer = self.handle_offer(disc)
        req = self.handle_request(offer)
        return self.handle_acknowledge(req)

    def print_lease_table(self):
        """Pretty-print the current lease table."""
        print(f"\n{'='*60}")
        print("  DHCP Lease Table")
        print(f"  {'IP Address':<16} {'MAC Address':<20} {'Expires':<12}")
        print(f"  {'-'*16} {'-'*20} {'-'*12}")
        for ip, info in self.leases.items():
            print(f"  {ip:<16} {info['client_mac']:<20} "
                  f"{info['lease_end']:%H:%M:%S}")
        print(f"  Available addresses: {len(self.available)}/{len(self.pool)}")
        print(f"{'='*60}")


def random_mac():
    """Generate a random MAC address string."""
    return ":".join(f"{random.randint(0, 255):02x}" for _ in range(6))


def demo():
    """Run the built-in demo with 4 clients."""
    run_simulation(num_clients=4, pool_start="192.168.1.100", pool_size=5)


def run_simulation(num_clients, pool_start, pool_size):
    print("╔══════════════════════════════════════════════════════════╗")
    print("║            DHCP DORA Process Simulator                  ║")
    print("╚══════════════════════════════════════════════════════════╝")
    print(f"\n  Server pool : {pool_start} — {pool_size} addresses")
    print(f"  Clients     : {num_clients}\n")

    server = DHCPServer(pool_start, pool_size)
    macs = [random_mac() for _ in range(num_clients)]

    for mac in macs:
        server.run_dora(mac)

    server.print_lease_table()


def main():
    parser = argparse.ArgumentParser(description="DHCP DORA Process Simulator")
    parser.add_argument("--clients", type=int, default=0,
                        help="Number of clients to simulate (0 = demo mode)")
    parser.add_argument("--pool-start", default="192.168.1.100",
                        help="First IP in the DHCP pool")
    parser.add_argument("--pool-size", type=int, default=5,
                        help="Number of IPs in the pool")
    args = parser.parse_args()

    if args.clients == 0:
        demo()
    else:
        run_simulation(args.clients, args.pool_start, args.pool_size)


if __name__ == "__main__":
    main()
