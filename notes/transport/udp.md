Header	Description
Time to Live (TTL)
	This field sets an expiry timer for the packet, so it doesn't clog up your network if it never manages to reach a host or escape!
Source Address	The IP address of the device that the packet is being sent from, so that data knows where to return to.
Destination Address	The device's IP address the packet is being sent to so that data knows where to travel next.
Source Port	This value is the port that is opened by the sender to send the UDP packet from. This value is randomly chosen (out of the ports from 0-65535 that aren't already in use at the time).
Destination Port	This value is the port number that an application or service is running on the remote host (the one receiving the data); for example, a webserver running on port 80. Unlike the source port, this value is not chosen at random.
Data	This header is where data, i.e. bytes of a file that is being transmitted, is stored.
