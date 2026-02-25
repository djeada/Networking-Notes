# Lab 8: Security-Oriented Packet Analysis

## Objective

Practice first-pass security triage by identifying suspicious communication patterns.

## Triage Model

```text
Unexpected endpoint + unusual rate + suspicious protocol usage = investigate deeper
```

## Steps

1. Identify external IPs with notable packet volume.
2. Inspect for suspicious patterns:
   - frequent DNS lookups to many domains
   - repeated failed connection attempts
   - cleartext protocols carrying sensitive data
3. Use protocol filters (`dns`, `http`, `ftp`, `telnet`, `tcp.flags.reset == 1`).
4. Document findings with timestamp, source, destination, and rationale.

## Boundaries and Ethics

- Capture only authorized traffic.
- Treat packet payloads as potentially sensitive data.
- Escalate incidents according to organizational policy.

## Exact Commands for Security-Triage Practice Traffic

### Terminal A (capture baseline services)

Run in separate terminals:

```bash
cd /home/runner/work/Networking-Notes/Networking-Notes
python3 scripts/transport/tcp_server.py -b 127.0.0.1 -p 9999
```

```bash
cd /home/runner/work/Networking-Notes/Networking-Notes
python3 scripts/transport/udp_server.py -b 127.0.0.1 -p 9998
```

### Terminal B (generate mixed normal + suspicious-looking patterns)

```bash
cd /home/runner/work/Networking-Notes/Networking-Notes

# 1) Burst DNS lookups (volume anomaly simulation)
for d in example.com github.com gitlab.com cloudflare.com openai.com; do
  python3 scripts/application/dns_lookup.py "$d" --all
done

# 2) Repeated failed TCP connections (failure pattern simulation)
python3 - <<'PY'
import socket
for _ in range(20):
    s = socket.socket()
    s.settimeout(0.5)
    try:
        s.connect(("127.0.0.1", 65000))
    except OSError:
        pass
    finally:
        s.close()
PY

# 3) Legitimate local TCP/UDP traffic for contrast
python3 scripts/transport/tcp_client.py -s 127.0.0.1 -p 9999 -m "baseline tcp"
python3 scripts/transport/udp_client.py -s 127.0.0.1 -p 9998 -m "baseline udp"
```

### Suggested filters for this lab

- `dns`
- `tcp.flags.reset == 1`
- `tcp.port == 9999 or udp.port == 9998`
