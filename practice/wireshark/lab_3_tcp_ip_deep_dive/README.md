# Lab 3: TCP/IP Deep Dive

## Objective

Analyze a complete TCP connection and explain key IP and TCP header fields.

## Protocol Flow Diagram

```text
Client                               Server
  | ---- SYN -----------------------> |
  | <--- SYN, ACK ------------------- |
  | ---- ACK -----------------------> |
  | ======= Data transfer ========    |
  | ---- FIN -----------------------> |
  | <--- ACK / FIN ------------------ |
  | ---- ACK -----------------------> |
```

## Steps

1. Apply `tcp` filter.
2. Locate a full session (handshake + data + teardown).
3. Inspect and note:
   - IP: source, destination, TTL, total length
   - TCP: sequence, acknowledgment, window size, flags
4. Use **Follow -> TCP Stream** on the session.
5. Apply `tcp.analysis.retransmission` and check if retransmits exist.

## Explanation Targets

- Why sequence and acknowledgment numbers advance.
- How window size relates to flow control.
- Why FIN packets appear at the end of clean session closure.

## Exact Commands to Generate a Full TCP Session

### Terminal A

```bash
cd /home/runner/work/Networking-Notes/Networking-Notes
python3 scripts/transport/tcp_server.py -b 127.0.0.1 -p 9999
```

### Terminal B

```bash
cd /home/runner/work/Networking-Notes/Networking-Notes
python3 scripts/transport/tcp_client.py -s 127.0.0.1 -p 9999 -m "first payload"
python3 scripts/transport/tcp_client.py -s 127.0.0.1 -p 9999 -m "second payload"
python3 scripts/transport/tcp_client.py -s 127.0.0.1 -p 9999 -m "third payload"
```

### Wireshark filters to apply in order

```text
tcp
tcp.port == 9999
tcp.flags.syn == 1 or tcp.flags.fin == 1
```
