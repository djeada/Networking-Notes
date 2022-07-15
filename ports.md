## Many connections on a single port

This depends in part on your operating system.

There is however no limit on a specific port. There is a limit on the number of concurrent connections however, typically limited by the number of file descriptors the kernel supports (eg 2048).

The thing to remember is that a TCP connection is unique and a connection is a pair of end points (local and remote IP address and port) so it doesn't matter if 1000 connections connect to the same port on a server because the connections are all still unique because the other end is different.

The other limit to be aware of is that a machine can only make about 64K outbound connections or the kernel limit on connections, whichever is lower. That's because port is an unsigned 16 bit number (0-65535) and each outbound connection uses one of those ports.

You can extend this by giving a machine additional IP addresses. Each IP address is another address space of 64K addresses.

* More than you can handle on a single box for performance reasons
* More than you need on a single box because your load balancers will distribute them amongst several for availability reasons anyway
