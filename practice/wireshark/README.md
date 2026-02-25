# Wireshark Labs

This section provides a guided path for learning packet analysis with Wireshark.
The labs move from basic capture skills to troubleshooting and security-focused analysis.

## Big Picture

Wireshark is most effective when used as a workflow instead of a random packet browser:

```text
Generate Traffic -> Capture -> Filter -> Correlate Flows -> Explain Findings
```

Across these labs, you will repeatedly practice the same loop:

1. Trigger a known network action.
2. Capture a short packet trace.
3. Use display filters to isolate relevant traffic.
4. Explain protocol behavior from evidence in packet fields.

## Lab Map

- [Lab 1: Interface Setup and Wireshark Orientation](lab_1_interface_setup/README.md)
- [Lab 2: Basic Traffic Capture and Filters](lab_2_basic_capture/README.md)
- [Lab 3: TCP/IP Deep Dive](lab_3_tcp_ip_deep_dive/README.md)
- [Lab 4: UDP, DNS, and DHCP Analysis](lab_4_udp_dns_dhcp/README.md)
- [Lab 5: Streams, Conversations, and Advanced Filters](lab_5_streams_and_conversations/README.md)
- [Lab 6: Troubleshooting Scenarios](lab_6_troubleshooting/README.md)
- [Lab 7: Expert Tools, IO Graphs, and Flow Graphs](lab_7_advanced_features/README.md)
- [Lab 8: Security-Oriented Packet Analysis](lab_8_security_analysis/README.md)

## Recommended Setup

- Use a non-production environment when possible.
- Capture only traffic you are authorized to inspect.
- Save each trace with a descriptive filename, such as:
  - `lab3_tcp_handshake.pcapng`
  - `lab6_dns_timeout_case.pcapng`

## Baseline Commands (Run Before Labs)

Use these commands to create a predictable environment for all labs.

```bash
# 1) Go to repository root
cd /home/runner/work/Networking-Notes/Networking-Notes

# 2) Confirm Wireshark can capture on at least one interface
wireshark --version

# 3) (Optional, CLI check) list capture interfaces
dumpcap -D

# 4) Keep one terminal ready for traffic generators
python3 --version
```

If your system does not have `dumpcap`, use Wireshark GUI interface list instead.

## References

- [Wireshark Official Documentation](https://www.wireshark.org/docs/)
- [Display Filter Reference](https://www.wireshark.org/docs/dfref/)
- [Sample Captures](https://wiki.wireshark.org/SampleCaptures)
