* It was created to solve the problem of limited number of ipv4 addresses.
* Previously each device got it's own PUBLIC ip address (connected with switch to default gateway).
* Another thing is security. IP of each device is public so can potentailly be accessed from anywhere.
* NAT is a process where a router translates one ip adress into another.

4 types of NAT:
* Static nat (SNAT)
* Dynamic nat (DNAT) (ip masquerading, private addresses are rotated)
* Port address translation (PAT)
* port forwarding (requests with one port can be translated to another port locally)

With PAT each host on the LAN is translated to the routers WAN-side public IP address, with a different port number.

