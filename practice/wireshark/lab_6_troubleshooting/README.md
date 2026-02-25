# Lab 6: Troubleshooting Scenarios

## Objective

Diagnose common network issues using packet evidence instead of assumptions.

## Troubleshooting Workflow

```text
Symptom -> Hypothesis -> Filter -> Evidence -> Conclusion
```

## Scenario A: High Latency

- Generate repeated ping traffic.
- Filter: `icmp`
- Compare request/reply timing patterns.

## Scenario B: Connection Reset

- Trigger a failed connection.
- Filter: `tcp.flags.reset == 1`
- Identify which side sent RST and at what stage.

## Scenario C: Packet Loss Symptoms

- Filter: `tcp.analysis.retransmission`
- Correlate retransmissions with reduced application responsiveness.

## Scenario D: DNS Delays

- Filter: `dns`
- Check for delayed responses or repeated queries.

## Deliverable

For each scenario, record:

- observed symptom in packets
- likely cause
- next diagnostic command/tool to run

## Exact Reproduction Commands

Run these while capturing packets in Wireshark.

### Scenario A (ICMP timing baseline)

```bash
ping -c 20 8.8.8.8
```

### Scenario B (RST / refused connection)

```bash
python3 - <<'PY'
import socket
s = socket.socket()
s.settimeout(2)
try:
    s.connect(("127.0.0.1", 65000))
except OSError as e:
    print("Expected failure:", e)
finally:
    s.close()
PY
```

Expected: connection refused; filter with `tcp.flags.reset == 1`.

### Scenario C (retransmission-like behavior via unreachable host)

```bash
python3 - <<'PY'
import socket
s = socket.socket()
s.settimeout(5)
try:
    s.connect(("10.255.255.1", 81))
except OSError as e:
    print("Expected timeout/failure:", e)
finally:
    s.close()
PY
```

Expected: timeout/SYN retries on many networks; inspect with `tcp` and `tcp.analysis.retransmission`.

### Scenario D (DNS request bursts)

```bash
cd /home/runner/work/Networking-Notes/Networking-Notes
for d in example.com github.com openai.com wikipedia.org; do
  python3 scripts/application/dns_lookup.py "$d" --all
done
```
