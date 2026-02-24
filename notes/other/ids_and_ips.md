# IDS and IPS (Intrusion Detection and Prevention Systems)

## Introduction

Intrusion Detection Systems (IDS) and Intrusion Prevention Systems (IPS) are network
security technologies that monitor traffic for suspicious activity. While they share
many detection techniques, they differ in how they respond to threats.

- **IDS** — monitors traffic and generates **alerts** when suspicious activity is detected.
  It is a passive system that does not block traffic.
- **IPS** — monitors traffic and can **actively block or drop** malicious packets in
  real time. It sits inline with the traffic flow.

## IDS vs IPS

```text
  IDS (Passive — out of band)

  [Internet] ──────> [Router] ──────> [Firewall] ──────> [Switch] ──────> [Network]
                                                            │
                                                      (mirror/span)
                                                            │
                                                        ┌───▼───┐
                                                        │  IDS  │
                                                        │(alert)│
                                                        └───────┘

  IPS (Active — inline)

  [Internet] ──────> [Router] ──────> [Firewall] ──────> [IPS] ──────> [Network]
                                                          │
                                                    inspects and
                                                    blocks threats
```

## Comparison Table

| Feature              | IDS                                     | IPS                                      |
|----------------------|-----------------------------------------|------------------------------------------|
| **Position**         | Out-of-band (receives copy of traffic)  | Inline (traffic passes through it)       |
| **Action on threat** | Alerts administrators                   | Blocks or drops malicious traffic        |
| **Latency impact**   | None (passive monitoring)               | May add slight latency                   |
| **False positives**  | Alerts only — no disruption             | Can block legitimate traffic             |
| **Failure mode**     | Network continues if IDS fails          | Network may be disrupted if IPS fails    |
| **Use case**         | Visibility and forensics                | Active threat prevention                 |

## Detection Methods

Both IDS and IPS use similar techniques to identify threats:

### 1. Signature-Based Detection

Compares traffic against a database of known attack signatures (patterns).

- **Pros**: Very accurate for known attacks; low false-positive rate.
- **Cons**: Cannot detect new or zero-day attacks; requires regular signature updates.

### 2. Anomaly-Based Detection

Establishes a baseline of "normal" network behavior and flags deviations.

- **Pros**: Can detect previously unknown attacks.
- **Cons**: Higher false-positive rate; requires a training period to learn the baseline.

### 3. Policy-Based Detection

Triggers alerts when traffic violates administrator-defined policies (e.g., a host
connecting to a prohibited port).

- **Pros**: Tailored to organizational needs.
- **Cons**: Requires manual policy creation and maintenance.

## Types of IDS

### Network-Based IDS (NIDS)

Monitors traffic on a network segment by analyzing packets captured from a switch
mirror port or network tap.

- Sees traffic across the entire segment.
- Examples: **Snort**, **Suricata**, **Zeek** (formerly Bro).

### Host-Based IDS (HIDS)

Runs on individual hosts and monitors system logs, file integrity, and process
activity.

- Can detect attacks that NIDS might miss (e.g., local privilege escalation).
- Examples: **OSSEC**, **Tripwire**, **AIDE**.

## IDS / IPS Placement

Where you place these systems affects what they can detect:

```text
                    ┌──────────────┐
  [Internet] ──────>│   Firewall   │
                    └──────┬───────┘
                           │
                    ┌──────┴───────┐
                    │   IPS        │  ← blocks threats before they reach the network
                    └──────┬───────┘
                           │
                    ┌──────┴───────┐
                    │   Switch     │──────── (mirror port) ──────> [IDS]
                    └──────┬───────┘                          ← alerts on suspicious
                           │                                    internal traffic
                    [Internal Network]
```

- **Before the firewall**: Sees all external traffic, including what the firewall
  would drop. Useful for threat intelligence but very noisy.
- **After the firewall**: Monitors traffic that the firewall allowed through.
  This is the most common and practical placement.
- **On internal segments**: Detects lateral movement and insider threats.

## False Positives and False Negatives

| Term               | Definition                                                    |
|--------------------|---------------------------------------------------------------|
| **True Positive**  | Correctly identified malicious activity.                      |
| **False Positive** | Legitimate traffic incorrectly flagged as malicious.          |
| **True Negative**  | Correctly identified legitimate traffic.                      |
| **False Negative** | Malicious activity that was not detected.                     |

Tuning IDS/IPS rules is a balance between minimizing false positives (which cause alert
fatigue and may block legitimate traffic on an IPS) and minimizing false negatives
(which leave threats undetected).

## Common IDS/IPS Software

| Tool         | Type     | Description                                              |
|--------------|----------|----------------------------------------------------------|
| **Snort**    | NIDS/IPS | Open-source, signature-based, widely used.               |
| **Suricata** | NIDS/IPS | Open-source, multi-threaded, supports signature and anomaly detection. |
| **Zeek**     | NIDS     | Open-source, focuses on network analysis and logging.    |
| **OSSEC**    | HIDS     | Open-source, host-based, log analysis and file integrity. |
| **Fail2Ban** | HIPS     | Bans IPs based on log patterns (e.g., failed SSH logins). |
