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
| --- | --- | --- | --- | --- |--- | --- | --- | --- |
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
