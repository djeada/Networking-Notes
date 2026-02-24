# nmap — Network Mapper

`nmap` (Network Mapper) is an open-source tool for network exploration and security auditing. It can discover hosts on a network, identify open ports, determine services and their versions, detect the operating system, and run scripted vulnerability checks.

> **Legal note:** Only run `nmap` against systems you own or have explicit written permission to scan. Unauthorized scanning is illegal in many jurisdictions.

---

## How nmap Works

nmap sends specially crafted packets and analyses the responses to determine:
- Which hosts are alive (host discovery)
- Which ports are open, closed, or filtered (port scanning)
- What services and versions are running (service detection)
- What operating system is running (OS fingerprinting)

```text
  nmap                            Target Host
    │                                  │
    │──── Probe packet (TCP SYN) ─────>│
    │                                  │
    │<─── SYN-ACK (port open) ─────────│   Port is OPEN
    │──── RST ─────────────────────────>│
    │
    │──── Probe packet (TCP SYN) ─────>│
    │<─── RST-ACK (port closed) ───────│   Port is CLOSED
    │
    │──── Probe packet (TCP SYN) ─────>│   (no response)
    │                  timeout          │   Port is FILTERED
```

---

## Basic Usage

```bash
nmap 192.168.1.1                  # Scan a single host
nmap 192.168.1.0/24               # Scan an entire subnet
nmap 192.168.1.1-50               # Scan a range of IPs
nmap scanme.nmap.org              # Scan by hostname (nmap's own test server)
nmap -iL targets.txt              # Read targets from a file
```

---

## Host Discovery

```bash
nmap -sn 192.168.1.0/24          # Ping scan — discover live hosts (no port scan)
nmap -Pn 192.168.1.1             # Skip ping, assume host is up (useful if ICMP is blocked)
nmap -PS80,443 192.168.1.0/24    # TCP SYN ping on ports 80 and 443
nmap -PA80 192.168.1.0/24        # TCP ACK ping
nmap -PR 192.168.1.0/24          # ARP ping (LAN only — most reliable on local network)
```

---

## Port Scanning Techniques

| Technique  | Option | Description                                                              |
|:-----------|:-------|:-------------------------------------------------------------------------|
| TCP SYN    | `-sS`  | (Default with root) Half-open scan — fast and stealthy; does not complete handshake |
| TCP Connect| `-sT`  | Full TCP handshake — used when root is not available                     |
| UDP scan   | `-sU`  | Scans UDP ports — slower; identifies DNS (53), DHCP (67/68), SNMP (161) |
| TCP ACK    | `-sA`  | Maps firewall rules — determines if ports are filtered or unfiltered     |
| Null scan  | `-sN`  | Sends no flags — can bypass some firewalls                               |
| FIN scan   | `-sF`  | Sends only FIN flag                                                      |
| Xmas scan  | `-sX`  | Sends FIN, PSH, and URG flags                                            |

```bash
sudo nmap -sS 192.168.1.1        # SYN scan (requires root/admin)
nmap -sT 192.168.1.1             # TCP connect scan (no root needed)
sudo nmap -sU -p 53,67,161 192.168.1.1  # UDP scan on specific ports
```

---

## Specifying Ports

```bash
nmap -p 22 192.168.1.1           # Single port
nmap -p 22,80,443 192.168.1.1    # Multiple ports
nmap -p 1-1024 192.168.1.1       # Port range
nmap -p- 192.168.1.1             # All 65535 ports
nmap --top-ports 100 192.168.1.1 # Top 100 most common ports
nmap -F 192.168.1.1              # Fast scan (top 100 ports)
```

---

## Service and Version Detection

```bash
nmap -sV 192.168.1.1             # Detect service versions
nmap -sV --version-intensity 9 192.168.1.1  # Aggressive version detection
```

Example output:
```text
PORT    STATE SERVICE VERSION
22/tcp  open  ssh     OpenSSH 8.9p1 Ubuntu 3ubuntu0.6
80/tcp  open  http    nginx 1.22.0
443/tcp open  ssl/http nginx 1.22.0
3306/tcp open mysql   MySQL 8.0.35
```

---

## OS Detection

```bash
sudo nmap -O 192.168.1.1         # OS fingerprinting (requires root)
sudo nmap -O --osscan-guess 192.168.1.1  # Guess OS even if not confident
```

---

## Aggressive Scan

The `-A` flag enables OS detection, version detection, script scanning, and traceroute in one command:

```bash
sudo nmap -A 192.168.1.1
```

---

## Nmap Scripting Engine (NSE)

NSE allows nmap to run Lua scripts for advanced detection, vulnerability checking, and exploitation testing.

```bash
nmap --script=default 192.168.1.1                   # Run default scripts
nmap --script=http-title 192.168.1.1                # Grab HTTP page titles
nmap --script=banner 192.168.1.1                    # Grab service banners
nmap --script=vuln 192.168.1.1                      # Check for known vulnerabilities
nmap --script=ssl-cert 192.168.1.1 -p 443           # Retrieve SSL certificate info
nmap --script=smb-vuln-ms17-010 192.168.1.1         # Check for EternalBlue (MS17-010)
nmap --script=ssh-brute 192.168.1.1                 # SSH brute-force (authorized use only)
```

Script categories: `auth`, `broadcast`, `brute`, `default`, `discovery`, `dos`, `exploit`, `fuzzer`, `intrusive`, `malware`, `safe`, `version`, `vuln`.

---

## Controlling Timing

Faster scans are noisier and may miss results; slower scans are stealthier and more accurate.

| Template | Option | Description                                 |
|:---------|:-------|:--------------------------------------------|
| Paranoid | `-T0`  | Very slow; evades IDS                       |
| Sneaky   | `-T1`  | Slow; avoids some detection                 |
| Polite   | `-T2`  | Slower than default; less bandwidth usage   |
| Normal   | `-T3`  | Default                                     |
| Aggressive| `-T4` | Faster; assumes reliable network            |
| Insane   | `-T5`  | Very fast; may miss results on slow networks|

```bash
nmap -T4 -p- 192.168.1.1        # Fast full port scan
nmap -T2 --scan-delay 500ms 192.168.1.1  # Slow and polite
```

---

## Output Formats

```bash
nmap -oN output.txt 192.168.1.1     # Normal (human-readable) output
nmap -oX output.xml 192.168.1.1     # XML output (for tools like Metasploit)
nmap -oG output.gnmap 192.168.1.1   # Grepable output
nmap -oA output 192.168.1.1         # Save in all three formats
```

---

## Example: Full Network Reconnaissance

```bash
# Step 1: Discover live hosts
sudo nmap -sn 192.168.1.0/24 -oG hosts.txt

# Step 2: Port scan all live hosts with service detection
sudo nmap -sS -sV -p- -T4 -iL hosts.txt -oA full_scan

# Step 3: Run default vulnerability scripts against findings
sudo nmap --script=vuln -iL hosts.txt -p 22,80,443,3306
```

---

## Port State Reference

| State       | Meaning                                                                         |
|:------------|:--------------------------------------------------------------------------------|
| `open`      | A service is actively accepting connections on this port                        |
| `closed`    | Port is accessible but no service is listening                                  |
| `filtered`  | Firewall or filter is blocking probes; nmap cannot determine if open or closed  |
| `unfiltered`| Port is accessible; nmap cannot determine if open or closed (ACK scan result)  |
| `open\|filtered` | Either open or filtered; nmap cannot distinguish (UDP, FIN, Null, Xmas) |
| `closed\|filtered` | Either closed or filtered (IP ID idle scan)                           |
