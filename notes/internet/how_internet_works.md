What happens when someone visits a website?
First their machine asks the website's server for a copy of a website.
Information is sent with virtual envelopes known as packets.
The envelopes include IP addresses of senders and receivers. 
Information is sent through physical copper wires. It first passes local networks and is forwarded further.
Then they travel with fiber optic cables located deep in the ocean.

* you type it in, and your ISP uses a Domain Name System (DNS) to turn it to an IP address.
* a request is sent to that IP via HTTP
* the request hops from server to server till it reaches it destination
* the server sends css, html, js and resources
* the browser parses the info and draws images.



**What happens when you type a URL in the web browser?**\
A URL may contain a request to HTML, image file or any other type.

1.  If the content of the typed URL is in the cache and fresh, then
    display the content.

2.  Else find the IP address for the domain so that a TCP connection can
    be set up. Browser does a DNS lookup.

3.  Browser needs to know the IP address for a URL so that it can set up
    a TCP connection.  This is why browser needs DNS service. The
    browser first looks for URL-IP mapping browser cache, then in OS
    cache. If all caches are empty, then it makes a recursive query to
    the local DNS server.   The local DNS server provides the IP
    address.

4.  Browser sets up a TCP connection using three-way handshake.

5.  Browser sends a HTTP request.

6.  Server has a web server like Apache, IIS running that handles
    incoming HTTP request and sends an HTTP response.

7.  Browser receives the HTTP response and renders the content.
# How the Internet Works

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

## How Do Devices Connect to the Internet?
A switch is sufficient to create a LAN.
How, though, do devices connect to the internet?
We utilize something called a router for this.
The switch is connected to the router via a copper cable.
To connect to the internet, however, we utilize a wire provided by the ISP (internet service provider) for a fee.
To transmit a packet to the internet, the computer first sends it to the switch, which then sends it to the router, which finally functions as a gateway to the internet.

Every home or apartment will have a LAN.
The router allows us to connect the computer to another computer anywhere in the globe.
In other words, the router facilitates the connection between distinct LANS. 

## The Internet Is a Network of Networks
Assume YouTube wants to give you data when you send it a request.
It will accomplish this by sending data packets to you through the internet.
Streaming refers to the process of delivering data in pieces.
When we request this packet from YouTube, we are actually talking with high-powered computers known as servers on YouTube.
To avoid a single point of failure, multiple YouTube servers are dispersed throughout the world. 

