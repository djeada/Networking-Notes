#!/usr/bin/env python3
"""
Load Balancer Algorithm Simulator
===================================
Simulates the five most common server load-balancing algorithms used by
hardware appliances and software proxies (HAProxy, Nginx, AWS ALB, etc.).

Concepts demonstrated:
* Round Robin — each server gets the next request in cyclic order.
* Weighted Round Robin — servers receive requests proportional to a
  configured weight (e.g., a more powerful server gets more traffic).
* Least Connections — the request goes to the server currently handling
  the fewest active connections (favors lightly-loaded backends).
* IP Hash — the client's IP address is hashed to deterministically pin
  that client to a particular server (session affinity / sticky sessions).
* Random — each request is sent to a uniformly random server.

The demo sends a burst of requests through every algorithm and prints a
side-by-side comparison of how traffic is distributed.

Usage:
    python load_balancer_simulator.py                           # built-in demo
    python load_balancer_simulator.py --requests 200            # 200 requests
    python load_balancer_simulator.py --servers web1:3 web2:1   # custom weights
"""

import argparse
import hashlib
import random
from collections import defaultdict
from dataclasses import dataclass, field
from typing import Dict, List, Tuple


@dataclass
class Server:
    name: str
    weight: int = 1
    active_connections: int = 0

    def __repr__(self):
        return f"{self.name}(w={self.weight}, conn={self.active_connections})"


class LoadBalancer:
    def __init__(self, servers: List[Server]):
        self.servers = [Server(s.name, s.weight) for s in servers]
        self._rr_index = -1
        self._wrr_schedule: List[int] = []
        self._wrr_pos = -1
        self._build_wrr_schedule()

    def _build_wrr_schedule(self):
        for i, s in enumerate(self.servers):
            self._wrr_schedule.extend([i] * s.weight)

    def reset(self):
        for s in self.servers:
            s.active_connections = 0
        self._rr_index = -1
        self._wrr_pos = -1

    # --- Algorithms ---
    def round_robin(self, _client_ip: str = "") -> Server:
        self._rr_index = (self._rr_index + 1) % len(self.servers)
        srv = self.servers[self._rr_index]
        srv.active_connections += 1
        return srv

    def weighted_round_robin(self, _client_ip: str = "") -> Server:
        self._wrr_pos = (self._wrr_pos + 1) % len(self._wrr_schedule)
        srv = self.servers[self._wrr_schedule[self._wrr_pos]]
        srv.active_connections += 1
        return srv

    def least_connections(self, _client_ip: str = "") -> Server:
        srv = min(self.servers, key=lambda s: s.active_connections)
        srv.active_connections += 1
        return srv

    def ip_hash(self, client_ip: str) -> Server:
        h = int(hashlib.md5(client_ip.encode()).hexdigest(), 16)
        idx = h % len(self.servers)
        srv = self.servers[idx]
        srv.active_connections += 1
        return srv

    def random_choice(self, _client_ip: str = "") -> Server:
        srv = random.choice(self.servers)
        srv.active_connections += 1
        return srv


def generate_client_ips(n: int) -> List[str]:
    rng = random.Random(42)
    return [f"10.{rng.randint(0,255)}.{rng.randint(0,255)}.{rng.randint(1,254)}" for _ in range(n)]


def run_algorithm(lb: LoadBalancer, algo_name: str, algo_func, client_ips: List[str],
                  verbose: bool = False) -> Dict[str, int]:
    lb.reset()
    dist: Dict[str, int] = defaultdict(int)
    for i, ip in enumerate(client_ips):
        srv = algo_func(ip)
        dist[srv.name] += 1
        if verbose and i < 8:
            print(f"    Request {i+1:>3} from {ip:<16} → {srv.name}")
    if verbose and len(client_ips) > 8:
        print(f"    ... ({len(client_ips) - 8} more requests processed)")
    return dict(dist)


def print_bar(label: str, count: int, total: int, bar_width: int = 30):
    pct = count / total * 100
    filled = int(bar_width * count / total)
    bar = "█" * filled + "░" * (bar_width - filled)
    print(f"    {label:<10} {bar} {count:>4} ({pct:5.1f}%)")


def demo(server_specs: List[Tuple[str, int]], num_requests: int):
    print("=" * 65)
    print("  Load Balancer Algorithm Simulator")
    print("=" * 65)

    servers = [Server(name, weight) for name, weight in server_specs]
    print(f"\n  Backend servers:")
    for s in servers:
        print(f"    • {s.name}  (weight={s.weight})")
    print(f"  Total requests: {num_requests}\n")

    client_ips = generate_client_ips(num_requests)
    lb = LoadBalancer(servers)

    algorithms = [
        ("Round Robin", lb.round_robin,
         "Cycles through servers 1→2→3→1→2→3… regardless of load."),
        ("Weighted RR", lb.weighted_round_robin,
         "Like Round Robin but higher-weight servers get proportionally more turns."),
        ("Least Conn", lb.least_connections,
         "Always picks the server with the fewest active connections."),
        ("IP Hash", lb.ip_hash,
         "Hashes the client IP so the same client always reaches the same server."),
        ("Random", lb.random_choice,
         "Each request goes to a uniformly random server."),
    ]

    all_results = {}
    for algo_name, algo_func, description in algorithms:
        print(f"{'─' * 65}")
        print(f"  Algorithm: {algo_name}")
        print(f"  {description}")
        print()
        dist = run_algorithm(lb, algo_name, algo_func, client_ips, verbose=True)
        print(f"\n  Distribution:")
        for s in servers:
            count = dist.get(s.name, 0)
            print_bar(s.name, count, num_requests)
        all_results[algo_name] = dist
        print()

    # Comparison table
    print(f"{'═' * 65}")
    print("  Comparison Summary (requests per server)")
    print(f"{'═' * 65}")
    header = f"  {'Algorithm':<15}" + "".join(f"{s.name:>10}" for s in servers)
    print(header)
    print("  " + "─" * (15 + 10 * len(servers)))
    for algo_name, dist in all_results.items():
        row = f"  {algo_name:<15}" + "".join(f"{dist.get(s.name,0):>10}" for s in servers)
        print(row)

    print(f"\n{'═' * 65}")
    print("  Key takeaway: algorithm choice depends on the workload.")
    print("  • Round Robin is simplest but ignores server capacity.")
    print("  • Weighted RR accounts for heterogeneous hardware.")
    print("  • Least Connections adapts to real-time load.")
    print("  • IP Hash provides session affinity (sticky sessions).")
    print("=" * 65)


def parse_server(spec: str) -> Tuple[str, int]:
    if ":" in spec:
        name, weight = spec.rsplit(":", 1)
        return name, int(weight)
    return spec, 1


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Load balancer algorithm simulator")
    parser.add_argument("--requests", type=int, default=100,
                        help="Number of requests to simulate (default: 100)")
    parser.add_argument("--servers", nargs="+", default=["web1:3", "web2:2", "web3:1"],
                        help="Server specs as name:weight (default: web1:3 web2:2 web3:1)")
    parser.add_argument("--seed", type=int, default=42,
                        help="Random seed for reproducibility (default: 42)")
    args = parser.parse_args()
    random.seed(args.seed)
    specs = [parse_server(s) for s in args.servers]
    demo(specs, args.requests)
