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
