# Cisco IOS

## Introduction

The **Cisco IOS (Internetwork Operating System)** is the operating system installed on the majority of Cisco networking devices, including routers and switches. It provides the command-line interface (CLI) used to configure, manage, and monitor Cisco equipment. Regardless of the device's size or type, IOS provides a consistent interface and feature set.

---

## IOS Boot Process

When a Cisco device is powered on, it goes through the following boot sequence:

```text
  +------------------+
  |  1. Power On     |
  +--------+---------+
           |
           v
  +------------------+
  |  2. POST         |  Power-On Self-Test: tests CPU, memory,
  |  (Hardware Test) |  and interfaces for basic functionality
  +--------+---------+
           |
           v
  +------------------+
  |  3. Load         |  Bootstrap program is loaded from ROM
  |  Bootstrap       |
  +--------+---------+
           |
           v
  +------------------+
  |  4. Locate IOS   |  Bootstrap locates IOS image:
  |  Image           |    1. Flash memory (default)
  +--------+---------+    2. TFTP server (if configured)
           |               3. ROM (fallback / ROMmon)
           v
  +------------------+
  |  5. Load IOS     |  IOS image is decompressed and loaded
  |  into RAM        |  into RAM
  +--------+---------+
           |
           v
  +------------------+
  |  6. Load Config  |  Startup-config is loaded from NVRAM.
  |  (startup-config)|  If none exists, device enters Setup Mode.
  +--------+---------+
           |
           v
  +------------------+
  |  7. CLI Ready    |  Device is operational and presents
  |  (User EXEC)     |  the User EXEC prompt
  +------------------+
```

---

## Access Methods

There are three primary ways to access the Cisco IOS CLI:

### Console Port

- **Type:** Out-of-band management (does not require network connectivity).
- **Connection:** A rollover (console) cable connects from the device's console port to a computer's serial or USB port.
- **Use Case:** Initial device setup, password recovery, and troubleshooting when the network is down.
- **Software:** Terminal emulator software (PuTTY, Tera Term, minicom) with settings: 9600 baud, 8 data bits, no parity, 1 stop bit, no flow control.

### SSH (Secure Shell)

- **Type:** In-band management (requires network connectivity and an IP address on the device).
- **Connection:** Encrypted remote access over the network (TCP port 22).
- **Use Case:** Secure day-to-day remote management of devices.
- **Prerequisites:** The device must have an IP address, an SSH server must be enabled, and RSA keys must be generated.
- **Recommendation:** Always use SSH over Telnet for security.

### Telnet

- **Type:** In-band management (requires network connectivity and an IP address).
- **Connection:** Unencrypted remote access over the network (TCP port 23).
- **Use Case:** Legacy environments only.
- **Warning:** Telnet transmits everything in **plain text**, including usernames, passwords, and commands. It should be avoided in favor of SSH.

---

## IOS Command Modes

Cisco IOS uses a hierarchical mode structure. Each mode provides a different set of commands and a different level of access.

### Mode Diagram

```text
  +---------------------+
  |    User EXEC        |  Prompt: Router>
  |    (Limited View)   |  Limited monitoring commands
  +----------+----------+
             |
             | enable
             v
  +---------------------+
  |  Privileged EXEC    |  Prompt: Router#
  |  (Full View)        |  All show/debug commands, save config
  +----------+----------+
             |
             | configure terminal
             v
  +---------------------+
  |  Global Config      |  Prompt: Router(config)#
  |  (Device-wide)      |  Change device-wide settings
  +----------+----------+
             |
             | interface, line, router, etc.
             v
  +---------------------+
  |  Sub-Config Modes   |  Prompt: Router(config-if)#
  |  (Interface, Line,  |          Router(config-line)#
  |   Router, etc.)     |          Router(config-router)#
  +---------------------+

  Navigation:
    exit       -> Go back one level
    end / Ctrl+Z -> Return directly to Privileged EXEC
    disable    -> Return from Privileged EXEC to User EXEC
```

### Mode Details

| Mode                | Prompt               | Access Command           | Purpose                             |
|---------------------|----------------------|--------------------------|-------------------------------------|
| User EXEC          | `Router>`            | (default on login)       | Basic monitoring (ping, show, etc.) |
| Privileged EXEC    | `Router#`            | `enable`                 | Full monitoring, save, restart      |
| Global Config      | `Router(config)#`    | `configure terminal`     | Device-wide configuration           |
| Interface Config   | `Router(config-if)#` | `interface <type/num>`   | Configure a specific interface      |
| Line Config        | `Router(config-line)#`| `line <type> <number>`  | Configure console, VTY, AUX lines   |

---

## Basic IOS Navigation Commands

| Command                   | Description                                      |
|---------------------------|--------------------------------------------------|
| `enable`                  | Enter Privileged EXEC mode                       |
| `disable`                 | Return to User EXEC mode                         |
| `configure terminal`      | Enter Global Configuration mode                  |
| `exit`                    | Go back one mode level                           |
| `end` or `Ctrl+Z`        | Return to Privileged EXEC from any config mode   |
| `?`                       | Display available commands in the current mode    |
| `command ?`               | Display options/arguments for a specific command  |
| `Tab`                     | Auto-complete a partial command                  |
| `no <command>`            | Negate or remove a configuration command          |
| `do <command>`            | Run a Privileged EXEC command from config mode    |
| `copy running-config startup-config` | Save the current configuration to NVRAM |
| `write memory`            | Save configuration (shortcut for copy run start) |

---

## IOS File System

Cisco devices store files across several types of memory:

| Memory Type | Purpose                                  | Persistence         |
|-------------|------------------------------------------|---------------------|
| **ROM**     | POST, bootstrap, ROMmon (minimal IOS)    | Permanent           |
| **Flash**   | Stores the IOS image file(s)             | Persistent          |
| **NVRAM**   | Stores the startup-config                | Persistent          |
| **RAM**     | Running-config, routing tables, buffers  | Lost on reboot      |

### Useful File System Commands

| Command                        | Description                              |
|--------------------------------|------------------------------------------|
| `show flash:`                  | List files stored in flash memory        |
| `show version`                 | Display IOS version and hardware info    |
| `dir flash:`                   | Directory listing of flash               |
| `copy flash: tftp:`            | Copy IOS image to a TFTP server          |
| `copy tftp: flash:`            | Copy IOS image from a TFTP server        |
| `delete flash:<filename>`      | Delete a file from flash                 |
| `erase startup-config`         | Erase the saved configuration in NVRAM   |

---

## Common Show Commands

| Command                          | Description                                         |
|----------------------------------|-----------------------------------------------------|
| `show running-config`            | Display the current active configuration in RAM     |
| `show startup-config`            | Display the saved configuration in NVRAM            |
| `show version`                   | IOS version, uptime, hardware, and boot image       |
| `show ip interface brief`        | Summary of all interfaces with IP and status        |
| `show interfaces`                | Detailed info for all interfaces                    |
| `show ip route`                  | Display the IP routing table                        |
| `show mac address-table`         | Display the switch MAC address table                |
| `show vlan brief`                | Display VLAN assignments on a switch                |
| `show arp`                       | Display the ARP table                               |
| `show cdp neighbors`             | Display directly connected Cisco devices            |
| `show clock`                     | Display the system clock                            |
| `show history`                   | Display command history for the current session     |
