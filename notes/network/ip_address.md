# Notes on IP Address: Understanding How it Works and its Limitations

## Overview
- An **IP address** is a unique numerical identifier for devices on a network.
- Not unique to a user or computer, but to a Network Interface Card (NIC).
- A device can have multiple NICs and thus, multiple IP addresses.

## Dynamic Nature of IP Addresses
- IP addresses can change based on the network connection.
- Switching networks (e.g., home Wi-Fi to public network) leads to a new IP address assignment.
- **Dynamic Host Configuration Protocol (DHCP)** temporarily assigns IP addresses.
- DHCP ensures networks do not exhaust IP addresses as devices connect and disconnect.

## Limitations of IP Addresses as Identifiers
- IP addresses are not meant to be a unique identifier for a computer or user.
- Can help track activity but not comprehensive for identity or location.
- Designed to identify a device connected to a network.

## MAC Addresses and Limitations
- **MAC address**: A unique hardware identifier for a NIC.
- Limitations:
  - Can change if NIC is swapped.
  - Can be spoofed or randomly generated (e.g., by smartphones for security).
  - Typically don't extend beyond local network; web servers see IP and port, not MAC address.
  - Not a reliable method for global network identification.

## Challenges with IP Address Identification
- IP-based identification can break if IP address changes (e.g., rebooting, changing networks).
- A device can connect to multiple networks simultaneously.

## Alternative Identifiers
- To reliably identify a computer:
  - Use identifiers like the CPU's serial number.
  - Note that MAC addresses can be overwritten, and IP packets can be rerouted.

## Conclusion
- IP addresses are crucial but have limitations.
- Not unique identifiers for users/computers but for devices on a network.
- Important to understand limitations when using IP addresses for identification or tracking.
