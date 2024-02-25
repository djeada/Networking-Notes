
# Understanding Subnet Masks and Network Addressing

- **Purpose of Subnet Mask**: Determines which part of the 32-bit IP address is the network address, indicating the first 'n' bits as the network address.
- **Function**: Helps in identifying whether a destination IP is on the same subnet or not.

## Working with Subnet Masks
- **On the Same Subnet**:
  - If the destination IP is on the same subnet, the packet is passed to the link layer code for delivery within the subnet.
- **On a Different Subnet**:
  - If the destination IP is not on the same subnet, the packet is sent to the gateway.

## Binary Representation
- **IP Address in Binary**: Example: 192.168.1.100 = `11000000101010000000000101100100` in binary.
- **Subnet Mask in Binary**: In a /24 subnet, subnet mask = `11111111111111111111111100000000`.
- **Bitwise AND Operation**: Used to determine the network address.
  - Example: `11000000101010000000000101100100` (IP Address) AND `11111111111111111111111100000000` (Subnet Mask) = `11000000101010000000000100000000` (Network Address).
  - Human-readable format: Network address is 192.168.1.0.

## Subnetting Example
- **Large Network Example**: 10.0.0.0/8 with 16,777,216 IPs.
- **Home Network Example**: 192.168.1.1/24.
  - **Reason for /24**: Typically, homes do not need 16 million addresses.
  - **Subnet Size**: /24 subnet allows 256 - 2 addresses (254 usable IPs).
    - First address (e.g., 192.168.1.0) is the network address.
    - Last address (e.g., 192.168.1.255) is the broadcast address.
- **Separate Subnets**: Different subnets (e.g., 192.168.2.0/24) may not have routes to each other, thus remaining isolated.


* decimal
* binary
* octet (a group of 8, in this case 8 binary numbers)
* IPV4 (4 sets of octets)

* Classes distinguishable by first octet.
* D-E for private network (not on the internet).
* C is the most common on the internet.

| Class | Range |
| --- | --- |
| A | 0.0.0.0 - 127.0.0.0 |
| B | 128.0.0.0 - 191.0.0.0 |
| C | 192.0.0.0 - 223.0.0.0 |
| D | 224.0.0.0 - 239.0.0.0 |
| E | 240.0.0.0 - 255.0.0.0 |

Class A: Each ip gets 16,777,214 Hosts.

You get the network ID 192.168.4.0/24

Now you have to create 3 subnetworks. One for office, one for front desk, one for storage. Each network gets network ID, subnet mask, host id range, # of usable hosts, brodcast id.

| Subnet      | 1   | 2   | 4   | 8   | 16  | 32  | 64  | 128 | 256 |
| --- | --- | --- | --- | --- |--- | --- | --- | --- | --- |
| Host        | 256 | 128 | 64  | 32  | 16  | 8   | 4   | 2   | 1   | 
| Subnet Mask | /24 | /25 | /26 | /27 | /28 | /29 | /30 | /31 | /32 |

We are looking for 3 subnets. There is no 3. But there is 4: (4, 64, /26).

Total host id is 64 (including host id and broadcast id).

| Network ID | Subnet Mask | Host ID Range | # of Usable Hosts | Broadcast ID |
| --- | --- | --- | --- | --- |
| 192.168.4.0 | /26 | 192.168.4.1 - 192.168.4.62 | 64 - 2 = 62 | 192.168.4.63 |
| 192.168.4.64 | /26 | 192.168.4.65 - 192.168.4.126 | 64 - 2 = 62 | 192.168.4.127 |
| 192.168.4.128 | /26 | 192.168.4.129 - 192.168.4.190 | 64 - 2 = 62 | 192.168.4.191 |
| 192.168.4.192 | /26 | 192.168.4.193 - 192.168.4.254 | 64 - 2 = 62 | 192.168.4.255 |

Example
Adres A: 192.168.10.32
Mask: 255.255.255.0

Adres B: 192.168.10.67
Mask: 255.255.255.0

* They are in the same network.
* Network adress is 192.168.10.0
* Broadcast adress is 192.168.10.255
* There are 254 hosts in the network.
