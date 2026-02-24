# Wireless Networking

## Introduction

Wireless networking allows devices to connect to a network without physical cables, using
**radio frequency (RF)** signals. The most common wireless LAN technology is **Wi-Fi**,
based on the IEEE 802.11 family of standards.

Wireless networking operates at the **physical layer** and **data link layer** of the OSI
model.

## Wi-Fi Standards (IEEE 802.11)

| Standard    | Name       | Frequency       | Max Data Rate | Range (approx) | Year |
|-------------|------------|-----------------|---------------|-----------------|------|
| 802.11a     | Wi-Fi 1    | 5 GHz           | 54 Mbps       | ~35 m indoor    | 1999 |
| 802.11b     | Wi-Fi 2    | 2.4 GHz         | 11 Mbps       | ~38 m indoor    | 1999 |
| 802.11g     | Wi-Fi 3    | 2.4 GHz         | 54 Mbps       | ~38 m indoor    | 2003 |
| 802.11n     | Wi-Fi 4    | 2.4 / 5 GHz    | 600 Mbps      | ~70 m indoor    | 2009 |
| 802.11ac    | Wi-Fi 5    | 5 GHz           | 6.9 Gbps      | ~35 m indoor    | 2013 |
| 802.11ax    | Wi-Fi 6/6E | 2.4 / 5 / 6 GHz| 9.6 Gbps      | ~35 m indoor    | 2020 |
| 802.11be    | Wi-Fi 7    | 2.4 / 5 / 6 GHz| 46 Gbps       | ~35 m indoor    | 2024 |

## 2.4 GHz vs 5 GHz vs 6 GHz

| Feature        | 2.4 GHz              | 5 GHz               | 6 GHz               |
|----------------|----------------------|----------------------|----------------------|
| Range          | Longer               | Shorter              | Shortest             |
| Speed          | Lower                | Higher               | Highest              |
| Interference   | More (microwaves, Bluetooth) | Less          | Least                |
| Wall penetration | Better             | Worse                | Worst                |
| Channels       | 3 non-overlapping    | 25 non-overlapping   | 59 non-overlapping   |

## Wireless Network Architecture

```text
  Infrastructure Mode (most common)

  [Internet] ──── [Router] ──── [Access Point]
                                    │  │  │
                               ┌────┘  │  └────┐
                            Device A  Device B  Device C
                            (laptop)  (phone)   (tablet)

  Ad Hoc Mode (peer-to-peer)

  Device A ◄──────► Device B
      ▲                ▲
      │                │
      └───► Device C ◄─┘
```

### Key Components

- **Access Point (AP)** — Bridges wireless clients to the wired network.
- **Wireless Controller** — Centrally manages multiple APs in enterprise networks.
- **SSID** (Service Set Identifier) — The network name that clients see.
- **BSSID** — The MAC address of the access point's radio.
- **ESS** (Extended Service Set) — Multiple APs sharing the same SSID for seamless
  roaming.

## Wi-Fi Connection Process

```text
  Client                                  Access Point
    |                                          |
    |<-- 1. Beacon frame (SSID, rates) --------|  (AP advertises itself)
    |                                          |
    |--- 2. Probe Request -------------------->|  (client searches for network)
    |<-- 3. Probe Response --------------------|
    |                                          |
    |--- 4. Authentication Request ----------->|
    |<-- 5. Authentication Response -----------|
    |                                          |
    |--- 6. Association Request -------------->|
    |<-- 7. Association Response --------------|
    |                                          |
    |=== 8. 4-Way Handshake (WPA2/3) =========|  (derive encryption keys)
    |                                          |
    |=== Connected and encrypted ==============|
```

## Wireless Security Protocols

| Protocol | Year | Security Level | Notes                                   |
|----------|------|----------------|-----------------------------------------|
| WEP      | 1999 | Broken         | Uses RC4; can be cracked in minutes     |
| WPA      | 2003 | Weak           | TKIP-based; improved over WEP           |
| WPA2     | 2004 | Strong         | AES-CCMP; widely used; KRACK vulnerability found in 2017 |
| WPA3     | 2018 | Strongest      | SAE handshake; forward secrecy; protected management frames |

### WPA2 Modes

- **WPA2-Personal (PSK)** — Pre-Shared Key; all users share the same password.
  Suitable for home networks.
- **WPA2-Enterprise (802.1X)** — Each user authenticates individually via a RADIUS
  server. Used in corporate environments.

### WPA3 Improvements

- **SAE (Simultaneous Authentication of Equals)** — Replaces PSK with a more secure
  handshake resistant to offline dictionary attacks.
- **192-bit security suite** — For enterprise environments requiring higher security.
- **Opportunistic Wireless Encryption (OWE)** — Encrypts open (no password) networks.

## CSMA/CA (Carrier Sense Multiple Access / Collision Avoidance)

Wi-Fi uses CSMA/CA instead of CSMA/CD (used by Ethernet) because wireless devices
cannot detect collisions while transmitting.

```text
  1. Listen to the channel
  2. If busy → wait (random backoff)
  3. If free → wait DIFS period, then send
  4. Wait for ACK from receiver
  5. No ACK? → retransmit with longer backoff
```

The **hidden node problem** occurs when two clients can both reach the AP but cannot
hear each other. **RTS/CTS** (Request to Send / Clear to Send) mitigates this by
reserving the channel before transmission.

## Wireless Channels

### 2.4 GHz Band

Only three non-overlapping channels: **1**, **6**, and **11** (in most regions).
Adjacent APs should use different non-overlapping channels to avoid interference.

```text
  Channel:  1   2   3   4   5   6   7   8   9  10  11
            |===========|           |===========|
                        |===========|           |===========|
  Use:      1                   6                       11
```

### 5 GHz Band

Has many more non-overlapping channels (up to 25 depending on region), which reduces
co-channel interference significantly.

## Wireless Troubleshooting Tools

```bash
# Scan for nearby Wi-Fi networks (Linux)
nmcli device wifi list
# or
sudo iwlist wlan0 scan

# Show current wireless connection details
iwconfig wlan0

# Monitor mode and packet capture
sudo airmon-ng start wlan0
sudo airodump-ng wlan0mon

# Signal strength and channel analysis
wavemon
```

## Common Wireless Issues

| Issue                    | Cause                                   | Solution                              |
|--------------------------|-----------------------------------------|---------------------------------------|
| Slow speeds              | Interference, congestion, distance      | Change channel, move closer to AP     |
| Frequent disconnects     | Weak signal, driver issues              | Add AP, update drivers                |
| No connection            | Wrong password, MAC filtering           | Verify credentials, check AP config   |
| Limited range            | Physical obstacles, low TX power        | Add APs or repeaters, reposition AP   |
| High latency             | Channel congestion, too many clients    | Use 5 GHz, add APs, enable QoS       |
