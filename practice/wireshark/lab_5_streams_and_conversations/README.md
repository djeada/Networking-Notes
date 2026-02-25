# Lab 5: Streams, Conversations, and Advanced Filters

## Objective

Move from packet-level reading to flow-level reasoning using conversations and streams.

## Analysis Diagram

```text
Many packets -> grouped into conversations -> grouped into application behavior
```

## Steps

1. Open **Statistics -> Conversations** and sort by packet count.
2. Pick a high-volume conversation and inspect both endpoints.
3. Use **Follow TCP Stream** or **Follow UDP Stream**.
4. Apply targeted filters, e.g.:
   - `ip.addr == 192.168.1.10 and tcp.port == 443`
   - `tcp.flags.syn == 1 and tcp.flags.ack == 0`
5. Mark important packets and annotate what each indicates.

## Explanation Targets

- Which host initiated communication?
- Which flow dominates bandwidth?
- How stream context improves interpretation versus single packets.
