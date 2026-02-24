#!/usr/bin/env python3
"""
TCP Sliding Window Flow Control Simulator
==========================================
Simulates the sender-side TCP sliding window mechanism used for flow control.
The sliding window allows a sender to transmit multiple segments before needing
an acknowledgement, improving throughput over simple stop-and-wait protocols.

The window is defined by three pointers into the byte stream:
  - send_base: the oldest unacknowledged byte
  - next_seq:  the next byte to send
  - send_base + window_size: the upper edge of the window

Bytes between send_base and next_seq are "in flight" (sent, unACKed).
Bytes between next_seq and the window edge are "usable" (can send now).
When in-flight bytes equal the window size, the window is FULL and the
sender must wait for ACKs before sending more data.

Concepts demonstrated:
  * Sliding window mechanics and pointer advancement
  * Bytes in flight vs. usable window
  * Window-full condition (sender blocks)
  * Zero-window probing (receiver advertises rwnd=0)
  * Window scaling (large windows for high-BDP links)

Usage:
    python tcp_window_simulator.py                        # built-in demo
    python tcp_window_simulator.py --data-size 40 --window 8 --segment 4
    python tcp_window_simulator.py --window-scale 2       # window scaling demo
"""

import argparse
import random
import time
import sys

# ── visualisation helpers ──────────────────────────────────────────────

def render_window(send_base, next_seq, window_size, total, seg_size):
    """Return an ASCII picture of the current window state."""
    win_end = min(send_base + window_size, total)
    cols = min(total, 60)
    scale = max(1, total // cols)

    bar = []
    for i in range(0, total, scale):
        if i < send_base:
            bar.append("✓")          # acknowledged
        elif i < next_seq:
            bar.append("●")          # in flight
        elif i < win_end:
            bar.append("○")          # usable (can send)
        else:
            bar.append("─")          # outside window
    line = "".join(bar)

    in_flight = next_seq - send_base
    usable = max(0, win_end - next_seq)
    labels = (
        f"  [✓ ACKed] [● InFlight={in_flight}] "
        f"[○ Usable={usable}] [─ Outside]"
    )
    return f"  |{line}|\n{labels}"


def log(msg):
    print(f"  >> {msg}")

# ── core simulation ───────────────────────────────────────────────────

def simulate(data_size, window_size, segment_size, zero_window_at=None):
    """Run the sliding-window simulation and print each step."""
    send_base = 0
    next_seq = 0
    step = 0

    print(f"\n{'=' * 62}")
    print(f"  Data={data_size}B  Window={window_size}B  Segment={segment_size}B")
    print(f"{'=' * 62}\n")

    while send_base < data_size:
        step += 1
        effective_win = window_size

        # Simulate receiver advertising a zero window at a specific byte
        if zero_window_at is not None and send_base >= zero_window_at and step == 1 + zero_window_at // segment_size:
            effective_win = 0
            print(f"\n─── Step {step}: ZERO WINDOW advertised by receiver ───")
            log("Receiver buffer full — advertised rwnd = 0.")
            log("Sender pauses and starts zero-window probe timer.")
            print(render_window(send_base, next_seq, effective_win, data_size, segment_size))
            # After probe, window reopens
            effective_win = window_size
            log("Zero-window probe ACKed; window reopens.\n")

        print(f"─── Step {step} ───")

        # Send as many segments as the window allows
        win_end = min(send_base + effective_win, data_size)
        sent_this_round = 0
        while next_seq < win_end:
            send_amount = min(segment_size, win_end - next_seq)
            log(f"SEND seq={next_seq}–{next_seq + send_amount - 1}  ({send_amount}B)")
            next_seq += send_amount
            sent_this_round += send_amount

        in_flight = next_seq - send_base
        if in_flight >= effective_win and next_seq < data_size:
            log(f"Window FULL — {in_flight}B in flight, must wait for ACK.")

        print(render_window(send_base, next_seq, effective_win, data_size, segment_size))

        # Simulate ACKs: acknowledge 1–3 segments worth of data
        ack_bytes = min(segment_size * random.randint(1, 3), next_seq - send_base)
        new_base = send_base + ack_bytes
        log(f"ACK received: ack={new_base} (acknowledges {ack_bytes}B)")
        send_base = new_base

        print(render_window(send_base, next_seq, effective_win, data_size, segment_size))
        print()

    print("✔  All data acknowledged. Transfer complete.\n")


def window_scaling_demo(scale_factor):
    """Show how the Window Scale option multiplies the 16-bit field."""
    base_max = 65535
    scaled_max = base_max << scale_factor
    print(f"\n{'=' * 62}")
    print("  TCP Window Scaling (RFC 7323)")
    print(f"{'=' * 62}")
    print(f"  Base 16-bit max window : {base_max:>12,} bytes  ({base_max / 1024:.0f} KiB)")
    print(f"  Scale factor (shift)   : {scale_factor}")
    print(f"  Effective max window   : {scaled_max:>12,} bytes  ({scaled_max / 1024 / 1024:.1f} MiB)")
    print()
    log("Window Scale is negotiated in the SYN/SYN-ACK handshake.")
    log("Each side may choose a different scale factor (0-14).")
    log(f"With shift={scale_factor}, advertised value is multiplied by 2^{scale_factor}={1 << scale_factor}.")
    print()

    print("  Example header values → effective receive window:")
    for adv in (16384, 32768, 65535):
        eff = adv << scale_factor
        print(f"    advertised={adv:>5}  ×  2^{scale_factor} = {eff:>12,} bytes")
    print()

# ── entry point ───────────────────────────────────────────────────────

def build_parser():
    p = argparse.ArgumentParser(
        description="Simulate TCP sliding-window flow control."
    )
    p.add_argument("--data-size", type=int, default=0,
                   help="Total bytes to transfer (default: demo)")
    p.add_argument("--window", type=int, default=10,
                   help="Receiver window size in bytes (default: 10)")
    p.add_argument("--segment", type=int, default=2,
                   help="Max segment size in bytes (default: 2)")
    p.add_argument("--window-scale", type=int, default=None,
                   help="Run window-scaling demo with this shift count")
    p.add_argument("--seed", type=int, default=42,
                   help="Random seed for reproducibility")
    return p


def main():
    args = build_parser().parse_args()
    random.seed(args.seed)

    if args.window_scale is not None:
        window_scaling_demo(args.window_scale)
        return

    if args.data_size > 0:
        simulate(args.data_size, args.window, args.segment)
        return

    # ── built-in demo ──
    print("╔══════════════════════════════════════════════════════════╗")
    print("║       TCP Sliding Window — Educational Demo             ║")
    print("╚══════════════════════════════════════════════════════════╝")

    print("\n▸ Demo 1: Normal transfer  (20 B data, window=8, MSS=2)")
    simulate(data_size=20, window_size=8, segment_size=2)

    print("\n▸ Demo 2: Zero-window scenario")
    simulate(data_size=16, window_size=6, segment_size=2, zero_window_at=6)

    print("\n▸ Demo 3: Window scaling")
    window_scaling_demo(scale_factor=7)


if __name__ == "__main__":
    main()
