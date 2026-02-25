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
