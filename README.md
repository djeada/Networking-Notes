# Networking
Notes on networking.

TODO:
* http://mw.home.amu.edu.pl/zajecia/BAD2016/BAD.html
* https://www.youtube.com/c/PracticalNetworking
* https://www.youtube.com/watch?v=X8RxRr7KNl8&list=PLSNNzog5eydtb5wyH2UtK09L9MsW9Hufq&ab_channel=SunnyClassroom
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


<h1>Lecture x</h1>

PART 1: RELIABILITY FROM UNRELIABILITY
Ref: slides from Sept 22

Slide 1: What the Internet provides

We want to get clear on the key, basic abstraction that the Internet provides. 

When we're talking about the Internet, we're talking about a global system of interconnected networks, each of which is made up of routers and links between them, and with a shared agreement to use certain protocols -- in particular, the Internet protocol (IP). The key abstraction that the Internet provides is best-effort delivery of datagrams. That's it. 

You can think of the network stack (allowing your machine to connect to the Internet) on a given machine as offering two basic functions: 
"Do your best to send this data to this destination"
"Check for any incoming data that was destined to me." 

Slide 2: What most users want. 

This bare-bones, potentially unreliable network is… not what most applications want. 
If you want to send an email, do you want (A) a guarantee that it'll get delivered? Or (B) a soft commitment that "maybe some or all of it will get there in some order"? (Probably A.) 

This is a key principle in this course: we want to build abstractions to provide reliability on top of the fundamental abstraction that the Internet offers us. 

Slide 3: reliability

If we want to implement reliability, it's a good idea to get clear about what the technical definition of reliability is. 

Aside: when we're talking about "abstractions" and "modules", we're talking about object-oriented programming and modular software design. If these terms aren't familiar to you, we recommend doing some web searches or posting on Ed. 

Slide 4: "The Big Question"

We jumped between slides 3 and 4, facilitating a group discussion to try to come up with some design ideas for providing reliability on top of an underlying, unreliable network.

We want to be really clear that the below are examples of the class's ideas -- not a documentation of what's done in practice! There's no right or wrong answer to this, and we came up with a few. However, we expect you to be able to reason about how you would implement core functionality over networks, so we encourage you to think about the below examples. 

For what's done in practice -- scroll down. 

Example 1: a DNS application 
We used the model of a "client" and "server." A client has a question, which it sends to a server; the server sends back an answer. 
We used the example of the Domain Name System (DNS) protocol -- a tool for looking up the IP address of a given website. 
Here, the client's question would be: "What's the 32-bit IP address for cs144.keithw.org ?" 
The server would answer, "cs144.keithw.org is mapped to 104.196.238.229."
How could we implement this (reliably) over the (unreliable) Internet? 
Idea 1: Retransmission with timeout 
If the client doesn't receive a reply within [x] ms, it sends the request again
This could protect against datagram loss (either the request or response) 
Idea 1.5: Retransmission with timeout + give up after [n] attempts
After [n] retransmissions, deliver an error message to user
Idea 2: Add some kind of validating information to protect against corruption 
Sender puts validating information in the datagram's header. The receiver recalculates this; if the values don't match, receiver the datagram. (Would be like the datagram never arrived.) 
Sum of all bytes?
Hash? 

Example 2: banking 
Client wants to send a request to their banking server: "Transfer $200 from my bank account to Keith's bank account." 
We encounter a new problem here: What if the request is delivered twice?
How could this happen? 
The client implemented retransmission with timeout as described above and sent the request again, but somehow both got delivered to the server. 
Something went wrong in the underlying network and the datagram got duplicated.
Server gets: 
 "Transfer $200 from my bank account to Keith's bank account." 
 "Transfer $200 from my bank account to Keith's bank account." 
Server transfers $400 total to Keith's bank account (yikes!) 

Aside: We didn't encounter this problem above in example #1. If the request or response got duplicated for a website to IP address mapping, there was no real negative impact. 

What's the difference in the "transfer $200 case?" 

Important terminology: an operation is idempotent if it doesn't matter how many times the operation occurs -- you get the same result. 
"Transfer $200 is not idempotent" -- there is a meaningful difference to some state in the real world if this happens multiple times 
"Give me this website's IP address" is idempotent -- there's no meaningful impact if this happens multiple times. 

Back to the example and back to the discussion -- how do we design for reliability that works when operations are not idempotent? 
Idea 1: The client could know something about the state on the server, and could make its request as specific and application-based as possible. The server could then know how to decode the message and not apply an action if it doesn't make sense. 
Example: "I now have $400; please transfer $200 from my bank account to Keith." 
If the server notices that the client doesn't have $400 in their bank account, it could avoid taking the action. 
Idea 2: A sender could number its messages, and the server could ignore duplicate numbers. 
Example: My message 0 is: "Please transfer $200 from my bank account to Keith."
The server would have to remember that it had already received "message 0" from the client. If it received another message 0, it could conclude that this is a duplicate and ignore it. 

Lots of other things to think about here -- More robust security? Is this general enough? And so on. For right now, we left this discussion here. 

A main takeaway from this discussion is: 
The fundamental abstraction of the Internet is unreliable, best-effort delivery of datagrams
Most applications want reliability 
We have to design abstractions on top of the Internet to get reliability
A core goal of this class is to demystify the Internet. 
You can and should think about how functionality on the Internet is designed, and how it could be done differently! 
Everything that makes the Internet work was just designed by some random people. 
It's not that special or deep, and you can and should engage with the ideas! 

[Back to Keith] - Let's talk about transferring a reliable stream of bytes over the Internet

A byte stream is an ordered sequence of bytes that has some beginning, can last arbitrarily long, and (at some point) has an ending. 
Note: the byte stream object can have limited internal storage ("capacity"), which is written to and read from. The stream can be arbitrarily long as the number of bytes that have been written in but not removed does not exceed the memory of the internal object at any given time. 

Example: say that a client wants to transfer "ABCDEF" to the server. Say that this is broken up into two messages / packets: the first contains "ABC" and the second contains "DEF."
Given what the Internet provides, sending "ABC" and then sending "DEF" is not enough -- a lot could go wrong! 
Server could get DEFABC (if DEF arrived first), or ABCABC (if ABC was duplicated), or any number of other combinations! 
What can we do? -- number each byte in the sequence
Client would send: 
"Bytes 0-2 of the stream are ABC"
"Bytes 3-5 of the stream are DEF"
"The stream ends at byte 6" 
The server could use these sequence numbers to reverse-engineer the order of the byte stream and discard duplicate messages!
The server / receiver would need space to store information -- 
The last sequence number received
Bytes + sequence numbers that were received but can't be written yet, because it's still waiting on previous sequence numbers to arrive
E.g., if "DEF" arrives first, server has to cache DEF until ABC arrives in order to write to the byte stream in order


Slide: TCP in a nutshell

TCP (transmission control protocol) is the protocol used to create a reliable byte stream on top of the unreliable Internet. 
In practice, it uses sequence numbers to do this (as described above - byte by byte)
In practice, the initial sequence number is randomly chosen -- not 0. 
It also uses checksums (basically, a sum of all of the bytes in a packet) to protect against random errors introduced by the network 
You'll learn a lot about TCP in this class :) 

Some applications that need additional reliability will implement additional features on top of TCP. (example: HTTPS uses encryption over TCP, some file transfer applications will send a file and then validate the hash of the file, etc.) 






PART 2: IP headers + UDP headers
No slides for this part 

Context: RFC = "request for comments"
RFCs are managed by an Internet standards body (IETF)
Collects comments on how people think the Internet should work 
Using these comments, publishes standards -- agreed-upon rules for the protocols machines use so that they can communicate over the Internet
Machines need to agree upon the format of packets - shared language

Displayed: structure of an IP header
https://datatracker.ietf.org/doc/html/rfc791
Scroll down to the ASCII drawing of the IP datagram, which lists the fields in an IP header 

Header = at the beginning of an IP datagram with the information that routers and computers need to know

Here are the important fields we want you to know: 
Version: 4 or 6 (usually 4) – what IP version are we using
Note: the diagram we looked at shows an IPv4 header
It’s important that the version goes first so that a receiver knows how to interpret the rest of the header
IHL = length of the IP header 
Total length = length of entire datagram 
Time to live = how many more times the datagram should get forward before it's dropped
This is meant to prevent infinite looping in a network 
Protocol – what is contained within the datagram?
Codes for ICMP, UDP, TCP, etc. 
Tells your machine how to interpret the contents after the IP header
Checksum 
Source address – IP address of who’s sending it (32-bit for IPv4)
Destination address – IP address of who’s receiving it (32-bit for IPv4)

After the header: the bytes/data you want to send. We call this the "IP payload" or the "payload of an IP packet." 

DEMO: Wireshark 

Wireshark is an application that lets you actually observe the datagrams being sent and received on your machine over the Internet. 

We filtered for packets with a particular IP address (given by Keith): 


Image: screenshot of Wireshark filter box, with `ip.dst == 171.64.65.14` filter applied. This filters for IP packets with destination IP address 171.64.65.14. 

We then pinged that IP address from a terminal window

Image: screenshot of a terminal line, with `ping 171.64.65.14` displayed.

We then examined the packets being sent by Wireshark. In particular, we examined the IP header to observe all of the fields in action! (You should do this!) 


Introducing: "ports"  

Context: multiplexing refers to sharing some scarce resource with some technique. 

Keith has said that IP addresses are a way to "multiplex" the scarce resource of the Internet -- multiple machines can communicate over the Internet, because routers know how to deliver packets based on their destination address. 

But an IP address just identifies a machine. How does a machine know which application or program to deliver the packet to? 
For example, if you're streaming a movie and checking your email, how does your operating system know which application an incoming packet is destined for? How does it avoid scrambling up your email data with your movie data? 

Key point: we need another layer of multiplexing -- we need to "share" the resource of limited IP address(es) on a given machine. Multiple programs/applications should be able to use the Internet at the same time. 

The general idea of doing this is: in the payload of the IP packet, include some identifier that uniquely identifies a target application on the destination machine. 

UDP is one protocol that uses "ports" to do this
https://datatracker.ietf.org/doc/html/rfc768

Key idea: 
Machine references the protocol field in the IP header to figure out how to interpret subsequent bytes in the packet. 
There's a nested header after the IP header -- the UDP header -- which contains a destination port number. 
The machine examines the destination port number and figures out which program to forward the packet to based on it. 
OS stores a mapping based on port numbers and protocols to open sockets! 

So: 
IP address = destination machine = allows the datagram to be delivered over the Internet
UDP port = destination socket/application/program on the destination machine = allows the data to be delivered to the correct application 

Notes: 
TCP also uses ports! 
A port is not a physical thing -- it's just a number that is assigned to keep applications separate from each other. 

Demo: writing a program
We ran the client program, then examined packets being sent in Wireshark.  
We then started the client program and the server program, both on localhost. 

Notes:
For a client UDP socket: the OS will choose a unique port number for the socket when you "connect" to a remote server 
For a server UDP socket: you choose a socket, then "bind" to it -- this creates an address (IP address + port number) for the socket. 
The server then "listens" for incoming packets addressed to this IP address + port. 
It's the client's responsibility to know the server socket's IP address + port combo and address packets to it accordingly. 


Note: You should, broadly, understand the concept of the "transport layer" (using the language of the 4-layer network model), and you should understand the key differences between TCP and UDP. 

<h1>Lecture x</h1>

Aside - "Internet datagram" vs. "User datagram"
An Internet datagram (conceptually) travels machine to machine
IP is the protocol here
A "user datagram" (conceptually) travels from application to application
UDP is a protocol here 

Aside - we write numerical IPv4 addresses in "dot-decimal notation"
Each IPv4 address is 32 bits = 4 bytes 
Dot decimal notation = just taking each of the four bytes (groups of 8 bits) from the raw, "on-wire", numerical representation; then writing them as numbers, with dots between them

Back to the structure of a datagram

Key principle: encapsulation
Think of packets as nested envelopes
Think of abstractions (fundamental "services" on the Internet) as "layers"
Each "layer" talks to peer(s) at the same layer. 
Routers talk to routers; machines talk to machines; applications talk to applications
Each "layer" cares about the header of one of the nested envelopes
An Internet datagram (IP header + payload) = one envelope
Inside the Internet datagram, you might have a user datagram (e.g., UDP header + payload). This is like a "nested envelope" -- another "envelope", which is also the payload of an Internet datagram. 
Inside the user datagram, you might have application data
Routers on the Internet examine the IP header
E.g.: destination addresses (where to send), checksum (to check for possible data corruption), and TTL (to decrement) 
The kernel (OS) on a machine examines the user datagram header, which is encapsulated in the Internet datagram 
E.g., examine port to decide which application to forward to
An application examines data that's in the user datagram 


High-level: We want to talk about how to build reliable applications on top of an unreliable datagram service (the Internet)

There are a lot of different ways to do this, and it depends on what you want to do. Let's talk about one specific service: DNS (the service that maps / resolves host names to IP addresses)

In other words, we talked about our first "application layer implementation" -- of DNS 
Application layer, here: "DNS"
Transport layer, here: "UDP"
Internet layer, here: "IP"

First step: how do we use DNS? 
We can call a library function to get a mapping from a host name to a 32-bit, numerical IP address. (Keith wrote a program that calls this library function.) 
We say that this "resolves" a hostname to an IP address. 
The numerical IP address is what we actually need to connect to some destination / send packets to a destination -- hostnames are just for human readability

How does DNS work?

How does DNS work from the client side? 
A DNS request is a request for a hostname to IP address mapping
E.g., "Please tell me the IP address for tiktok.com"
A client sends a DNS request to a DNS server 
There is a file called `etc/resolve.conf`, which lists the IP addresses for DNS servers you can send requests to
The DNS request is encapsulated in a user datagram, which is encapsulated in an IP datagram
Common terminology: "DNS runs over UDP" -- meaning, DNS is an application/service that uses UDP as its transport protocol
We ran Keith's program while capturing packets on Wireshark and observed the packets that were sent and received!
Side note: we noted that "destination port 53" is what the machine put in the UDP header (port) to signify that this is a DNS request. Port 53 is a port that is assigned to the DNS service. 

A big part of this: how do names get assigned? 
Who stores the name -> IP address mappings? 
E.g., stanford.edu
Answer: there is a hierarchical "tree" of both control (giving out names) and storing information (hierarchical, distributed database) 
This hierarchy that starts at the "root" -- the empty string
This was created by the US government
The US government then delegated responsibility for different categories of names to different authorities
For example, some nonprofit holds ".edu" addresses, and gives them out to educational institutions. 
Think of every website name as having multiple parts:
"stanford.edu." has three parts:
"" (root)
There is an implicit "." + "" (empty string) at the end of every website address -- implicitly, every name starts at the root. If we want to be rigorous in writing out names, we add a "." at the end to be extra clear about this. 
edu
stanford
puffer.stanford.edu. has four parts: 
Root ("")
Edu
Stanford
Puffer 

Different authorities manage different parts of the name space.
These authorities control name servers that can either tell you a name / IP address mapping or can tell you which name server you should ask for that mapping 
For example: 
Some name servers have information about and control ".edu" addresses
Those name servers might not have the information for "puffer.stanford.edu.", but they would be able to tell us what server has the information for all ".stanford.edu." addresses. 

We used the command "dig" to perform a recursive lookup through the distributed DNS database (name servers) for the IP address of "puffer.stanford.edu."
From the command line: dig puffer.stanford.edu @[IP address of DNS name server, starting at a root name server] 
This allows us to examine the hierarchy of the distributed database in practice 
First, we asked the root name server for "puffer.stanford.edu."
The root name server said, "we don't know anything about "puffer.stanford.edu.", but we do know the IP addresses of the name servers that have information about names with ".edu" suffixes 
Then, we asked one of those ".edu" servers for the IP address of "puffer.stanford.edu."
This server said, "we don't know anything about "puffer.stanford.edu.", but we do know the IP addresses of the servers that have information about names with "stanford.edu" suffixes
So, we asked one of those servers, and we got the IP address of "puffer.stanford.edu."

Key point: 
There is a recursive process for looking up IP addresses in this distributed database 
There's a hierarchy of control and lookup -- first root, then suffix (.edu, .com, .ly, etc.), then moving to the left in the name 

In practice, what usually happens when your machine makes a DNS request:
Your machine doesn't do the whole process outlined above 
Your machine asks a DNS server to resolve a name 
Note: the DNS server might be on your machine too, or it might not. 
The DNS server does the work of recursively contacting name servers for you -- performing the lookup in the distributed database, as described above -- then sends the result back to your computer 
Note: the DNS server will also have a cache
DNS replies have an "expiration date" associated -- e.g., "this name to IP address mapping is valid for this amount of time". The DNS server will then cache that reply for that amount of time. 
Before performing the whole lookup, the DNS server will check its cache. It may be able to send a response to your computer right away without contacting any name servers. 

If you're confused about how DNS works, there are lots of resources online (for example, this website has a diagram of the DNS tree / hierarchy). There were also great questions + answers in the "Live Lecture Discussion Thread! Sep 29" post on Ed. 


In response to a question -- it's worth noting that when we're talking about "layers" on the Internet (Interned, transport, application, etc.) -- these layers aren't really "real". They're descriptive, and they're meant to offer abstractions that are conceptually helpful. 

A common model of the Internet is the "7-layer OSI model." This is conceptually helpful, but it also breaks down sometimes. (For example, if you're using a VPN, you might have another IP header in your packet somewhere.) 


We moved on to talk a bit about TCP
UDP is one transport layer 
TCP is a different transport layer 
What's in the TCP header 
What the process is for TCP (SYN, ACK, SYN/ACK, sequence numbers, etc.) 

We acted out an example TCP connection 
Keith exchanged "packets" with a student

Keith -> student


Sequence number: 0
This is the initial sequence number that Keith is assigning to the byte stream from him to the student. E.g., Keith is telling the student that the first sequence number of his byte stream is 0. 
Keith sends some data: "Hello." 
This is encapsulated in the TCP packet -- after the TCP header
Keith sets the SYN bit. 
SYN = synchronize
This is how you start each byte stream in a TCP connection
This means: "This is the first packet in my byte stream to you" 
Window size: 1000
How many bytes Keith is willing to receive from the student in future packets at the same time
Student -> Keith 


Student sends a packet 


Sequence number: 5000
Student decides to start their byte stream at sequence number 5,000
SYN bit is set 
Student is also initiating a byte stream in the other direction, so they need to set a SYN bit 
Student sends some data: "Hi!" 
This is encapsulated in the TCP packet 


ACK = 7
"ACK" = acknowledgment; indicates the next sequence number that the student is willing to receive from Keith.

Implicitly, this means, "I've received data from you up to sequence number 6; the next sequence number I'm expecting is 7". 
 
A tricky thing: SYN occupies a sequence number. (e.g., sequence number 0 corresponds to the SYN bit that was set in the packet that Keith sent.) 

Byte 0 = SYN (SYN occupies a sequence number!) 
1 = H, 2 = E, 3 = L, 4 = L, 5 = 0, 6 = .
Next we're expecting = sequence number 7
Window size: 100
This is how much data the student is willing to receive from Keith at one time 
Keith sends a packet back -- decides to end the connection 


Sequence number: 7


The first sequence number of the data in this packet 
Data: "Bye"


FIN bit is set 
Fin = finished
Keith sets this bit to indicate: "I'm finished sending bytes" / "this is the last packet in the byte stream from me to you" 
ACK: 5,004
5,004 is the next sequence number Keith would like to receive from the student 
Window: 1,000
Keith re-affirms that his window size is 1,000 
Student -> Keith


Sequence number: 5,004
The first sequence number of the data in this packet
Data: "Where?" 


ACK: 11
Note: we count sequence numbers by - every byte of data + SYN occupies a sequence number + FIN occupies a sequence number
Window: 100


Keith sends a packet


Seqno: 11
Still sends a seqno, even though he's sending no data (and can't -- since he's finished his byte stream) 
Data = ""
No data - Keith has no data to send, but Keith needs to send an acknowledgment -- so he sends a packet
ACK = 5011


Window = 1000


Student sends a packet


Seqno = 5011


Data = "CU"


FIN 
Student ends their byte stream 
ACK: 11


Window = 500

<h1>Lecture x</h1>
Packet switching

These "module" videos from last year, which are on YouTube, cover what we covered in lecture today: 
1-5: The Principle of Packet Switching 
3-2: What is Packet Switching? 
3-3: End-to-End delay (the math-y part of this lecture)
Lecture 6 from last year (CS144 Canvas site -> Panopto Course Videos -> L6) also contains material that heavily overlaps with today's and Wednesday's lecture 
Supplemental, not really covered in lecture:
3-1: History of Networks


Background: circuit switching vs. packet switching 
This is well-covered in the videos above

You should understand: 
What circuit switching is
The telephone network, which was a circuit-switched network, was the major precedent for the Internet when it was first being started up
Packet switching was a revolutionary idea at the time 
Side note -- now: circuit switching is uncommon - even most telephone networks are built on top of packet switched networks. 

Packet switching:
These are covered in the videos above, and key notes on packet switching are in the lecture slides from this year. 

You should understand:
We recommend referring to lecture slides for these, with additional explanations in videos 
What packet switching is 
How packet switching is different from circuit switching
Fundamental advantages of packet switching 

The mechanics of packet switching
AKA: "let's do some math"

You should understand: 
There are three components that go into the delay of sending a packet. You should be able to name and describe each of them. 
Serialization (also called packetization) delay
Propagation delay
Queueing delay 
How can you calculate each of them? 
You should know formulas and be able to solve problems. The videos from last year and the lecture slides from this year have examples. 
From a basic network, you should be able to use the above to calculate end-to-end delay from some source to some destination through some switches. You should be able to do this on networks without queueing delay and networks with queueing delay. 
Example from lecture slides: A -> S1 -> S2 -> S3 -> B, where S_i are switches. We'll do more calculations on Wednesday. 
We recommend starting with calculations without queueing delay -- just examining packetization and propagation delay. Once you feel comfortable with that, add in consideration of the variable queueing delay. 
You should be able to reason a bit about what might increase/decrease each of these delays. 

Related to reasoning about delays, we also talked about: 
Where does variability in round trip time come from?
Background: 
Round trip time (RTT) = source -> destination -> source = time between when you send a request and when you receive the response 
We ran `pings` to a destination and observed variability in round trip time. 
Ping is a program that sends an "ICMP echo request," which is a way of asking some destination, "please reply with the same payload". The destination will reply with an "ICMP echo reply." 
Key point: ping will then report the total round trip time between the source and destination (time from when it sent the echo request to when it received the matching echo reply). 
Variability in round trip time is sometimes called "jitter". 
On a wired link, we consider packetization delay to be generally fixed
On a wireless link, packetization delay depends on the quality of the link, which is likely to be variable (e.g., how far away / close to a router you are)
Total propagation delay could be variable if your route changes (e.g., a link breaks) 
Queueing delay is the most common source of variability -- it depends on congestion

Terminology: 
"Throughput" 
For many of the Internet applications we care about, this is what we care about. 
You should be able to calculate the throughput that's possible from a source to a destination. 
"Latency"
You should be able to reason about: what contributes to higher/lower latency? 
Who cares about latency? 
High-frequency trading (a few milliseconds = lots of $$) 
Maybe a real-time call (e.g., Zoom, multiplayer gaming)


Notes: 

The difference between "propagation delay" and "packetization delay" is sometimes subtle. Propagation delay is how long it takes for data to travel across a link once it's on the wire (point A to point B). Packetization delay is how long it takes for data to be written to (encoded onto) the wire (i.e., translate bits into voltage in a physical medium). 

You don't need to know the details of the physical layer of the Internet (yet), but you should generally know that bits need to get translated into something that can be sent over a physical link (could be wireless, fiber optic wire, satellite, or some other type of link). This "serialization" work takes time (packetization/serialization delay). It also takes time for the signals to travel across the physical link (propagation delay). 

There are a few different kinds of switches:
"Store and forward" - must receive the whole packet before it starts sending bits out along the next link (forwarding) 
"Cut-through" - sends out bits as it receives them 
Unless we state explicitly otherwise, we'll be referring to store-and-forward switches

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
