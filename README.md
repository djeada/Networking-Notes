# Networking
Notes on networking.

TODO:
* http://mw.home.amu.edu.pl/zajecia/BAD2016/BAD.html
* https://www.youtube.com/c/PracticalNetworking
* https://www.youtube.com/watch?v=X8RxRr7KNl8&list=PLSNNzog5eydtb5wyH2UtK09L9MsW9Hufq&ab_channel=SunnyClassroom
* https://github.com/Tikam02/DevOps-Guide/tree/master/Networking
* https://github.com/Tikam02/DevOps-Guide/tree/master/Networking

<h1>LAN</h1>
LAN is made up of devices that are linked together via switches and access points.
If PC 1 and PC 6 are connected via a network, the computer breaks the data down into little pieces called packets and transmits it to the switch.
The switch then examines the contents of the packet, determines the package's destination, and transmits it to the dest, in this instance PC6. 
<h2>Switch</h2>
A switch can be used to link many computers in a network.
To link all of the computers to the switch, we can utilize copper wires or faster fiber optic connections.
Copper cables are classified into two types: CAT-5 and CAT-6.
No wirless connection.
Category 6 allows for faster transmission of data.
Switches are used to build a LAN network.
The switch has ports on it that are known as LAN ports. 

<h2>Access points</h2>

A device with functions similar to swtich. Uses wirless connection.

<h1>The internet</h1>

The internet connects all of the LANs and forms a network.
A home router is essential; it is essentially a router and a switch combined.
This generally has an access point capability, allowing us to connect to it wirelessly.


So why can't there be just one router that all home routers link to?
To begin with, the primary router must have millions of ports so that each device may connect to it.
However, the primary issue is that one router will have to handle all of the load, making it a single point of failure.
In this situation, if there is a single problem with the router, the entire internet will break at the same moment.
Long cables would also be necessary. 

These internet-connection cables are even put down on the ocean floor!
If one of these cables fails, the internet on that continent may go down.
These are all fiber optic lines since the data transfer speed is extremely fast.

Assume that a computer in India has to deliver a packet to a computer in Mexico.
First, the router receives this packet and forwards it to another router through wires.
This router now has a plethora of possibilities for forwarding this packet.
It uses something called a routing table to select the best one. 

<h2>How do devices connect to the internet?</h2>
A switch is sufficient to create a LAN.
How, though, do devices connect to the internet?
We utilize something called a router for this.
The switch is connected to the router via a copper cable.
To connect to the internet, however, we utilize a wire provided by the ISP (internet service provider) for a fee.
To transmit a packet to the internet, the computer first sends it to the switch, which then sends it to the router, which finally functions as a gateway to the internet.

Every home or apartment will have a LAN.
The router allows us to connect the computer to another computer anywhere in the globe.
In other words, the router facilitates the connection between distinct LANS. 

<h2>The internet is a network of networks.</h2>
Assume YouTube wants to give you data when you send it a request.
It will accomplish this by sending data packets to you through the internet.
Streaming refers to the process of delivering data in pieces.
When we request this packet from YouTube, we are actually talking with high-powered computers known as servers on YouTube.
To avoid a single point of failure, multiple YouTube servers are dispersed throughout the world. 

<h1>WAN(Wide area network)</h1>

This is used to link two LANs.
You may be asking what the distinction is between this and the internet.
The major distinction is one of privacy.

Assume one LAN network, which is an office, wishes to transfer data to another LAN network; if they do so over the internet, the data can be abused because the internet is open to the public.
As a result, if they are in a LAN, only those local computers will be able to access the data, and if they are in a WAN, only the two linked LAN networks will be able to access the data since it is private.
VPN is the most widely used WAN network technique (virtual private network).
VPN tunneling creates a tunnel for data transfer in a public network while simultaneously providing privacy and security.
Before transmitting your data packets, it encrypts them.
VPNs are commonly used to get access to restricted websites. 

<h2>What is the biggest WAN in the world?</h2>

The internet itself is the world's largest WAN.
However, there is a distinction between a WAN connection between two offices and the internet.
The internet is open to the public and is owned by everyone on the planet.


A LAN is more secure than a WAN because a LAN never travels via the internet, but a WAN, even with a VPN, does. 

<h2>Public and Private WAN</h2>

In a private WAN, you can purchase a line directly from your ISP and utilize it to link networks.
This is more secure, but it is more expensive, especially across long distances.
As a result, most businesses prefer Public WANS.


Switches are used to establish a LAN, and routers are used to build a WAN.
A switch cannot be used to build a WAN. 

<h1>How does VPN tunnelling work?</h1>

The issue is, even if there is no physical tunnel linking the two LAN routers, the data may still be accessed.
However, the data is placed in a safe envelope, much like a letter, and is then encrypted so that it cannot be hacked or viewed.
Encapsulation is the process of putting data to be transferred into an envelope or another packet.

Do you believe that because the internet is a public network, the data you transmit to networks such as Amazon may be hacked?

To some extent, it cannot be hacked due to a feature known as end-to-end encryption.
Only the two communicating users will be able to see the data in this system. 

<h1>What is an ISP?</h1>

The internet is made up of several separate routers linked together.
These many ISPs link the routers of the world.
Specific routers can be controlled by each ISP.
ISPs are the corporations that provide us with access to the internet.
There are several ISPs throughout the world. 

<h2>Local ISP’S</h2>

Local ISPs are in charge of connecting LANS in their area.
These local internet service providers then link to the regional ISP.
As a result, we may argue that different local ISPs connect to form a regional ISP.
Local ISPs link locales such as neighborhoods, whereas Regional ISPs connect cities throughout a country.
As a result, regional and local ISPs constitute the country's network.
Global ISPs connect the networks of many nations.

It should be noted that some local ISPs can communicate with global ISPs without the need of regional ISPs.

Local ISPs are often smaller businesses that may desire a direct link with a global ISP in order to provide their consumers with a better experience. 

<h2>Peering</h2>

Assume a computer in Belgium wishes to connect to a website in India, but the website only has one server.
In this scenario, the user submits a request, and the packet travels via the local ISP, regional ISP, and global ISP to reach the website's server.
This website then delivers a response including all pertinent information.
Because these routes are never established, the request and answer may travel different paths.
A firm like Google is not the same as this random company.
It has servers all around the world to provide its clients with better speeds.
However, even Google experiences minor performance issues from time to time, which may dissatisfy its consumers.
Google, on the other hand, has an excellent answer for this.  This solution is peering.

Peering occurs when Google's servers create a direct link with our local ISPs, bypassing the requirement for ISP infrastructure. This also enhances security.

As a result, we may conclude that Google's rapid service speed is due to its dispersed servers and peering architecture.

We can also connect directly to a regional ISP for a quicker connection. 


<h1>Lecture x</h1>
These are notes taken by a CA during a lecture to supplement learning or act as one resource to catch up if you missed a class. (They are not a substitute for attending lectures if you are able to.) We encourage you to also talk with and share notes with each other in order to get multiple perspectives on the material! 

One other resource is each lecture's live discussion/question thread on Ed. 

--

Key topic: the whirlwind tour of how the internet works
Note: a lot of this stuff we will go into more during subsequent lectures

--

Some things we talked about: 
Reliability is an abstraction that we build on top of what the Internet provides. (Next lecture goes more into this.) 
The Internet provides one abstraction: DATAGRAMS

-- 

What is in a datagram?
"To" address of a computer (laptop, server, phone, etc) on the internet (fully specified)
Ipv4: addresses 32 bits (most common)
Ipv6: addresses 128 bits (because we ran out of IPv4 addresses…) 
"From" address (fully specified)
Some data to send (generally approx < 1.5 Kilobyte (= 1500 bytes)
Keith will defer question of why 1.5 Kilobytes

-- 

The Internet allows information to be sent between different computers
The datagram abstraction means "best effort delivery" 
What could happen to the datagram?
Option 1: delivered quickly (what we hope for)
Option 2: delivered, but with different text (corrupted)
Option 3: Delivered late (could be after other datagrams, in the wrong order)
Option 4: Delivered to the wrong address (or from address)
Option 5: NOT delivered
Option 6: Delivered, tampered text (maliciously!) 
Option 7: Delivered multiple times

Why is this "best-effort" idea helpful?
All of the hardware on the internet (routers, ethernet, etc) can provide this abstraction -- very few guarantees, as minimal as possible 
For example: would have later been much harder to build Wifi if datagram abstraction were reliable
Allows flexibility to implement stuff on top of it
For example: a service like Zoom might actually not want reliability 

--

How do packets find their way across the internet?
IP addresses! 
In ipv4, addresses are 32 bits; we have 2^32 unique addresses (~4 billion)
Side note: there are more than 4 billion addresses in the world (cellphone, chromecast, Apple Watch...); there's a thing called "private IP addresses" within local networks, but we're not there yet. 
You should have a rough idea of how to calculate the 32-bit number from the human-readable string notation
Example: 104.196.238.229 = first byte is 104 (in binary), second byte is 196, third byte is 248, and fourth byte is 229. Numerically, is: 104 * 256 ^ 3 + 196 * 256 ^ 2 + 238 * 256 + 229. 
You should know that IP addresses are based on the network you're in
Keith's address on his laptop comes from Stanford, not Lenovo. His IP address right now is in Stanford's network "address space". His IP address is different when he's at home. When he shows up at Stanford and opens his laptop, his computer needs to get a new address from Stanford, and Stanford only needs to have addresses for computers that are on. 
Look at this fun XKCD map which shows an (older) picture of which IPs belong to which organizations: https://xkcd.com/195/ 
You should know that IP addresses have a hierarchical structure
Addresses in the same network share a prefix -- in other words, start with some number of the same bits. This makes routing easier. 
For example: all addresses from 104.196.0.0-104.199.255.255 are owned by Google.
How do you get to own an IP address? Generally, from the network that owns them. 

--

An additional feature that the datagram abstraction provides: 
Datagrams won't loop infinitely in a network
IP headers have a TTL (time to live) field - number of "hops" it's allowed to take until it expires. Each router decrements this. 
If TTL value = 0, the router will drop the datagram and send a message back to the sender saying it's dropped. 
Cool hack: we can use this to implement "traceroute", an application that lets us figure out the path that our packet takes through a network. 
You should generally know how traceroute uses the TTL field in order to get the IP addresses of routers along a path. 
Generally, it involves setting the TTL of packets at 1, 2, 3, …, and examining the source IP address of the "time to live exceeded" error message that routers send back. 



One of the core services you can build on top of the datagram is the abstraction of the reliable byte stream
Byte stream: sequence of bytes, arbitrarily long, can be written to and read from.

Internet: we can build abstractions over other abstractions. We call this the network stack.
Each layer is meant to be isolated -- provides a clear, well-defined abstraction to the layer above it. You can individually build layers without worrying about how other layers are implemented.
Ex: You can build a website (application layer) over a TCP socket without worrying too much about how that socket is implemented -- just the methods and functionality that it provides. 
Ex: You can use IP over Ethernet or WiFi -- link layers that are implemented very differently, but provide the same interface and functionality
This made it easy to innovate - you could build new systems that relied on existing implementations of lower/other layers. 
Example: could build a web application without having to redesign TCP
Example: could build UDP over IP to provide a different service than TCP
Each layer at the source host will communicate with its "peer" at the destination host
TCP stack at host A communicates with TCP stack at host B
HTTP application at host A communicates with HTTP application at host B 
Network layers on hosts and routers examine IP headers to send, forward, and receive datagrams without worrying about whatever is encapsulated in them. 
The key thing you should understand here is the idea of abstraction / isolation and how it applies on the Internet. 
You should also understand the basic "4-layer Internet model": link layer, network layer, transport layer, and application layer 
You should also know that this model is meant to be descriptive, but it sometimes breaks down -- for example, Keith drew a diagram for an HTTPS application, which runs over TLS (encryption), which provides the abstraction of a secure byte stream. This is kind of an "extra layer." 
There's another model called the "7-layer OSI model", but it includes some stuff we haven't really covered yet. 


Q: How is it possible to hide address?
People use Web / HTTP Proxies:
Where, in the HTTP layer, you could proxy to another HTTP layer
Virtual private network:
At the datagram layer: make a request -- it becomes a datagram
Instead of directly sending datagram, take datagram and put it inside another datagram -- lots of nesting! 
Take cs155 :) 
Q: If multiple lines of communication go to one specific address, how does this address share specific interface across different lines of communication:
Great question!! For example: TCP serves different programs (Firefox, Chrome, Outlook, Safari). Each one of these programs has several byte streams. When a message is received, which program is it for? 
MULTIPLEXING: take one interface and make It look like many different interfaces. (We'll talk about this more in the next lectures.) 
VIRTUALIZATION: different VMs (virtual machines) on same computer (you don't have to know about this right now) 	



<h1>Questions</h1>

* how does internet work?
* what happens when you hit enter after typing a url?
* what happens when you search for a phrase on google?
* how does whatsapp work?

<h1>Linki</h1>
 * Bombal na gicie
 * https://www.youtube.com/watch?v=VwN91x5i25g&list=PLBlnK6fEyqRgMCUAG0XRw78UA8qnv6jEx
 * https://www.youtube.com/watch?v=L_6RmF3QQyo&t=447s
 * https://www.youtube.com/watch?v=kNKHM_isojI&t=934s

## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update tests as appropriate.

## License
[MIT](https://choosealicense.com/licenses/mit/)
