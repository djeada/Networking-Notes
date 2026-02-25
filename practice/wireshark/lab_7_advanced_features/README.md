# Lab 7: Expert Tools, IO Graphs, and Flow Graphs

## Objective

Use Wireshark's advanced built-in analysis tools to detect patterns faster.

## Feature Overview

```text
Expert Info  -> protocol warnings/anomalies
IO Graphs    -> traffic rate trends over time
Flow Graph   -> sequence of packet exchanges
```

## Steps

1. Open **Analyze -> Expert Information** and review warnings/errors.
2. Open **Statistics -> I/O Graphs** and visualize packet rate spikes.
3. Open **Statistics -> Flow Graph** for a selected conversation.
4. Add or adjust coloring rules for protocols of interest.

## Explanation Targets

- Which anomalies are informational versus likely actionable?
- Do graph spikes correlate with specific protocols or hosts?
- How does the flow graph clarify request-response order?

## Exact Commands to Create Graph-Friendly Traffic

Run with Wireshark capture active:

```bash
cd /home/runner/work/Networking-Notes/Networking-Notes
python3 scripts/transport/tcp_server.py -b 127.0.0.1 -p 9999
```

In another terminal:

```bash
cd /home/runner/work/Networking-Notes/Networking-Notes
for i in $(seq 1 30); do
  python3 scripts/transport/tcp_client.py -s 127.0.0.1 -p 9999 -m "graph packet $i"
done
```

Now open:

1. **Analyze -> Expert Information**
2. **Statistics -> I/O Graphs** (add graph for `tcp.port == 9999`)
3. **Statistics -> Flow Graph** for one TCP conversation
