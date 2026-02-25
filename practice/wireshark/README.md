# Wireshark Labs

Wireshark helps you understand network behavior by letting you inspect packets at every layer.
These labs are organized as separate exercises so you can practice one skill at a time.

## What You Will Learn

- Packet analysis across OSI/TCP-IP layers
- Protocol behavior (ARP, IP, ICMP, TCP, UDP, DNS, HTTP)
- Troubleshooting using filters, streams, and timing analysis
- Basic security-oriented packet inspection

---

## Lab 1: Install Wireshark and Explore the Interface

**Goal:** Get comfortable with Wireshark before capturing traffic.

1. Install Wireshark (`wireshark` package on Linux, official installer on macOS/Windows).
2. Open Wireshark and identify:
   - Interface list
   - Packet List pane
   - Packet Details pane
   - Packet Bytes pane
3. Start and stop a short capture on your active interface.
4. Open **Help → About** and note your Wireshark version.

**Focus topics:** interface selection, capture start/stop, packet view layout, basic navigation.

---

## Lab 2: Capture and Analyze Basic Traffic

**Goal:** Observe normal local traffic and practice display filters.

1. Start a live capture.
2. Generate traffic with common commands:
   - `ping 8.8.8.8`
   - open a website in your browser
3. Apply display filters:
   - `arp`
   - `icmp`
   - `tcp`
   - `udp`
4. Inspect one packet from each protocol and identify source/destination addresses.

**Focus topics:** live capture basics, protocol identification, display filters.

---

## Lab 3: Deep Dive into TCP/IP

**Goal:** Understand TCP connection setup/teardown and key IP/TCP fields.

1. Filter TCP traffic (`tcp`).
2. Find a complete TCP session and inspect:
   - Three-way handshake (`SYN`, `SYN, ACK`, `ACK`)
   - Session close (`FIN`, `ACK`)
3. In packet details, review:
   - IP TTL, total length, source/destination IP
   - TCP sequence/acknowledgment numbers
   - TCP window size and flags
4. Right-click a TCP packet and choose **Follow → TCP Stream**.

**Focus topics:** TCP state transitions, flow control basics, stream-level analysis.

---

## Lab 4: Study UDP and Supporting Protocols

**Goal:** Compare UDP behavior with TCP and inspect common UDP-based protocols.

1. Filter UDP traffic (`udp`).
2. Trigger DNS queries (`nslookup example.com` or browse a new domain).
3. Inspect DNS request/response packet pairs.
4. If available on your network, inspect DHCP packets (`bootp` filter).
5. Compare a UDP flow and a TCP flow:
   - no handshake in UDP
   - no retransmission logic in protocol headers

**Focus topics:** connectionless transport, DNS over UDP, protocol comparison.

---

## Lab 5: Advanced Packet Analysis

**Goal:** Move from packet-by-packet viewing to conversation-level analysis.

1. Use **Statistics → Conversations** to identify active flows.
2. Use **Follow TCP Stream** or **Follow UDP Stream**.
3. Apply advanced filters, for example:
   - `ip.addr == 192.168.1.10 and tcp.port == 443`
   - `tcp.flags.syn == 1 and tcp.flags.ack == 0`
4. Mark packets and add temporary comments for investigation notes.

**Focus topics:** stream reconstruction, conversations, precise filtering.

---

## Lab 6: Network Troubleshooting Scenarios

**Goal:** Use Wireshark to diagnose realistic network issues.

Run one scenario at a time and capture during the test:

1. **High latency:** run repeated pings and inspect RTT patterns (`icmp`).
2. **Connection failures:** filter `tcp.flags.reset == 1` and look for resets.
3. **Packet loss symptoms:** look for retransmissions (`tcp.analysis.retransmission`).
4. **Name resolution issues:** inspect failed or delayed DNS responses (`dns`).

**Focus topics:** symptom-to-packet correlation, root-cause clues in captures.

---

## Lab 7: Use Wireshark Advanced Features

**Goal:** Improve analysis speed using built-in visualization and expert tools.

1. Open **Analyze → Expert Information** and review warnings/errors.
2. Open **Statistics → I/O Graphs** to visualize traffic rates.
3. Open **Statistics → Flow Graph** for sequence-level communication view.
4. Customize coloring rules for key protocols (e.g., DNS, TCP errors, ICMP).

**Focus topics:** expert analysis, traffic visualization, workflow customization.

---

## Lab 8: Security-Focused Traffic Analysis

**Goal:** Build foundational packet analysis skills for security investigations.

1. Identify unexpected external IP communication.
2. Filter suspicious behavior examples:
   - unusually frequent DNS queries
   - repeated failed TCP connection attempts
   - cleartext protocol use (e.g., HTTP, FTP, Telnet)
3. Review packet payloads only where legally and ethically permitted.
4. Document findings: source, destination, protocol, timestamp, and reason for suspicion.

**Focus topics:** anomaly spotting, suspicious-pattern triage, evidence-oriented notes.

---

## Suggested Workflow for All Labs

1. Capture traffic for a short, defined time window.
2. Save the file (`.pcapng`) with a meaningful name.
3. Analyze with filters and statistics.
4. Write 3-5 findings after each lab (what happened, why it matters, what to check next).
