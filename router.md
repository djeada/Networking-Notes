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
