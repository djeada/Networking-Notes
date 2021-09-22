# networking
notes on networking

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
