There are several methods for protecting your device from unwanted access.
You can limit privileged mode access as well as the numerous ways to connect to the device.
Remember that passwords are kept in plain text.
Make careful to always encrypt these files.
Example of Privileged Exec Mode 

Router> enable
Router#
Router# conf terminal
Router(config)# enable secret ultrasecretpassword
Router(config)# exit
Router#

Restrict Console Access

Router> enable
Router#
Router# conf terminal
Router(config)# line console 0
Router(config-line)# password ultrasecretpassword
Router(config-line)# login
Router(config-line)# exit
Router(config)#

Restrict SSH / TTY Access

Router> enable
Router#
Router# conf terminal
Router(config)# line vty 0 15
Router(config-line)# password ultrasecretpassword
Router(config-line)# login
Router(config-line)#

Encrypt Passwords

Router> enable
Router#
Router# conf terminal
Router(config)# service password-encryption
Router(config)# exit

Change Banner / Message of the Day / MotD

Router> enable
Router#
Router# conf terminal
Router(config)# banner motd "Pls dont hack me!"

Viewing and Saving Running Configuration

View

Router> enable
Router#
Router# show running-config

Router> enable
Router#
Router# show startup-config

Save

Router> enable
Router#
Router# copy running-config startup-config

If you find yourself in an undesirable configuration state for whatever reason, you may always use the reload command.
However, be careful that this operation momentarily turns off the device, removing its network capabilities.
The same is true with the command delete startup-config.
However, the wipe command will remove whatever settings you made, such as passwords, hostnames, or motd's.


If you messed up but haven't saved yet, you can override the old configuration with the startup configuration.
Simply run: 

Router> enable
Router#
Router# copy startup-config running-config


<h1>How does a router differentiate traffick from the private network and from the ISP?</h1>
Ultimately it's a construct of the user. You decide "these are my private networks" and "these pubic networks over here are another network", and you setup the rules between them. Consider the case where you don't have internet. You have a home network, and so does your neighbor, and you run a cable between your houses. You may want to bridge the networks with no restrictions, may want to protect your network from theirs, and they may have a firewall/router protecting their network from yours.

Now, the most common way to do things is to have the ISP as the public network on one side of the firewall and NAT capabilities, and all your personal networks on the other side. You then use NAT and Firewall rules to permit most outbound traffic, some amount of internal traffic, and very limited inbound traffic from the public network. This is setup by you on more Enterprise devices, and comes setup as a default on most consumer devices so that grandma doesn't have to understand firewall rules to stay safe while looking up cooking recipes. In order to let the router know which network you consider "public", consumer hardware will have a "wan" port where you plug in your modem so the router knows that's the internet side. This is most important if your modem is also part router and provides an RFC1918 address to your router, your router wouldn't know whether that's really a private network or a pubic one without you telling it.

If you want to play around with routing and Firewall concepts, may I suggest setting up pfSense in a virtual environment at home and setting up some basic things. Make 2-3 VLANs, setup rules so machines on one can talk to machines on another, and you can play with things like NAT in both directions (yes, outbound NAT is a thing too, I use it for things like forcing all DNS traffic to a specific DNS server).

The router knows the difference between the cables. In router terminology they are called ports. The router knows for example that port 1 is connected to the outside world. It knows port 2 is connected to something else. It knows how to take a message from port 2 and route it to port 1 and vice versa.
