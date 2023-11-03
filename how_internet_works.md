What happens when someone vists a website?
First their machine asks the website's server for a copy of a website.
Information is send with virtual envlopes known as packets.
The envolopes include ip addresses of senders and recievers. 
Information is send trough physical copper wires. It first passes local networks and is forwarded further.
Then they travel with fiber optic cabels located deep in the ocean.

* you type it in, and your ISP uses a Domain Name System (DNS) to turn it to an IP addresss.
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

8. 
