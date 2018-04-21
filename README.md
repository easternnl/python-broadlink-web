# python-broadlink-web
Webinterface between Broadlink RM* device and home automation software such as Domoticz

This is a small webserver and load the broadlink library at startup. It can take upto 5 seconds to load the library, which means that if you execute a script from the commandline it will always take 5 seconds before the command is send.

The webserver send the commands almost immediately.


# dependencies
Python 2.7.x (tested with 2.7.14)

Broadlink 0.8 (https://github.com/mjg59/python-broadlink)

# Startup

# Configuration
Use the file irconfig.py to adjust the IR commands you want to use. The tool IrScrutinizer ( https://github.com/bengtmartensson/harctoolboxbundle/releases/tag/Version-1.4.1 ) can be used to generate the IR codes for your device. 

Also have a look at http://www.remotecentral.com/cgi-bin/codes/onkyo/ (in my case Onkyo)

Use the file broadlinkconfig.py to setup your Broadlink device:

#!/usr/bin/env python
type = 0x2737    # take a look here to find your device type https://github.com/mjg59/python-broadlink/blob/master/protocol.md
host = "192.168.1.1"
mac = "abcdabcd"

For safety reason you can block your Broadlink device in your router if you don't use the functionaly to use it when out of range of your local Wifi.

# Usage
Browse to http://[servername]:[port]/ and it will display all your commands in a list. Click one of the commands to execute with the Broadlink device.
