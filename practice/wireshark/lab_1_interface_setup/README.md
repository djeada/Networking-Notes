# Lab 1: Interface Setup and Wireshark Orientation

## Objective

Set up Wireshark correctly, identify key UI components, and run your first controlled capture.

## Why This Matters

Before protocol analysis, you need confidence in capture source and packet navigation. Most beginner mistakes come from capturing on the wrong interface or misreading packet panes.

## Concept Diagram

```text
[Network Interface] --> [Packet List] --> [Packet Details] --> [Packet Bytes]
        where              what/when           how parsed           raw data
```

## Steps

1. Install Wireshark for your platform.
2. Launch Wireshark and identify your active interface (look for packet counters).
3. Start a 20-30 second capture and then stop.
4. Click a packet and inspect all three panes.
5. Use `Ctrl+F` (or Find Packet) to search for a protocol string like `TCP`.

## Expected Observations

- Packet list updates in real time.
- Packet details expand hierarchically by protocol layer.
- Packet bytes pane maps to selected protocol fields.

## Checks

- Can you explain the difference between a capture filter and a display filter?
- Can you identify source and destination MAC/IP addresses in one packet?
