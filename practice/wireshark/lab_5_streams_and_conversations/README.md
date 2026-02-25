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

## Exact Commands for Multiple Concurrent Flows

### Terminal A (servers)

```bash
cd /home/runner/work/Networking-Notes/Networking-Notes
python3 scripts/transport/tcp_server.py -b 127.0.0.1 -p 9999
```

Open another shell for UDP server:

```bash
cd /home/runner/work/Networking-Notes/Networking-Notes
python3 scripts/transport/udp_server.py -b 127.0.0.1 -p 9998
```

### Terminal B (traffic burst script)

```bash
cd /home/runner/work/Networking-Notes/Networking-Notes
for i in 1 2 3 4 5; do
  python3 scripts/transport/tcp_client.py -s 127.0.0.1 -p 9999 -m "tcp stream $i"
  python3 scripts/transport/udp_client.py -s 127.0.0.1 -p 9998 -m "udp stream $i"
done
```

Then in Wireshark, sort **Statistics -> Conversations** by packet count and inspect top flows.
