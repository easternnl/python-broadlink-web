#!/usr/bin/env python
"""
Based on https://gist.githubusercontent.com/mdonkers/63e115cc0c79b4f6b8b3a6b797e485c7/raw/a6a1d090ac8549dac8f2bd607bd64925de997d40/server.py

Use this small app to control your broadlink device to send IR codes. This is based on the example of IrScrutinizer, the database with all the IR codes,
to send them to your device.
The downside of the IrScrutinizer is that each time a single Python script is launched the complete broadlink module needs to be loaded, which can take 
upto 5 seconds on a Raspberry.

This small app loads the module once, and presents an index page with all the commands registered in the ircodes.py and send the to the device configured
in the broadlinkconfig.py file

Enjoy the use of this small app.


This is used to enable fast loading of the Broadlink module to control IR-codes

Usage::
    ./broadlink-python-web.py [<port>]
    
    
Created by Eastern
"""
import logging
import broadlink
import SimpleHTTPServer
import SocketServer
import BaseHTTPServer
from SimpleHTTPServer import SimpleHTTPRequestHandler
import broadlinkconfig
import irconfig


def get_command_data(command_name, count):
    cmd = irconfig.commands[command_name]
    buffer = bytearray()
    buffer.append(cmd[0])
    repeat_only = len(cmd[1]) == 0 and len(cmd[3]) == 0
    buffer.append(count - 1 if repeat_only else 0)
    seq = cmd[2] if repeat_only else mk_sequence(cmd, count)
    buffer.append(len(seq) % 256)
    buffer.append(len(seq) / 256)
    return buffer + seq


def mk_sequence(cmd, count):
    no_repeats = count if len(cmd[1]) == 0 else count - 1
    data = cmd[1]
    for i in range(0, no_repeats):
        data = data + cmd[2]
    return data + cmd[3]


def auto_int(x):
    return int(x, 0)

#class S(BaseHTTPRequestHandler):
class S(SimpleHTTPRequestHandler):
    def _set_response(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()

    def do_GET(self):
        #logging.info("GET request,\nPath: %s\nHeaders:\n%s\n", str(self.path), str(self.headers))
        #logging.info("GET request Path: %s\n", str(self.path))
        self._set_response()
        #self.wfile.write("GET request for {}".format(self.path).encode('utf-8'))
        if self.path == "/" :
            self.wfile.write("Commands available to send to {} / {} / type: 0x{}: <br /><br />".format(broadlinkconfig.host,broadlinkconfig.mac,format(broadlinkconfig.type, '02x')).encode('utf-8'))
            for command in irconfig.commands:
                self.wfile.write("<a href=/{}>{}</a><br />".format(command, command).encode('utf-8'))
        else : 
             #self.wfile.write("command:".encode('utf-8'))
            command = self.path.replace('/','')
            #type = 0x2737
            #host = "192.168.1.1"
            #mac = bytearray.fromhex("abcdef")
            dev = broadlink.gendevice(broadlinkconfig.type, (broadlinkconfig.host, 80), bytearray.fromhex(broadlinkconfig.mac))
            dev.auth()
            payload = get_command_data(command, 1)
            dev.send_data(payload)
            self.wfile.write("command <b>{}</b> send<br />".format(command).encode('utf-8'))
            self.wfile.write("<br /><a href=/>Return to index</a>".encode('utf-8'))
            
        self.wfile.write("<br /><br />end of document".encode('utf-8'))    

    def do_POST(self):
        content_length = int(self.headers['Content-Length']) # <--- Gets the size of data
        post_data = self.rfile.read(content_length) # <--- Gets the data itself
        logging.info("POST request,\nPath: %s\nHeaders:\n%s\n\nBody:\n%s\n",
                str(self.path), str(self.headers), post_data.decode('utf-8'))

        self._set_response()
        self.wfile.write("POST request for {}".format(self.path).encode('utf-8'))

def run(server_class=BaseHTTPServer, handler_class=S, port=9191):
    logging.basicConfig(level=logging.INFO)
    server_address = ('', port)
    #httpd = server_class(server_address, handler_class)
    httpd = SocketServer.TCPServer(server_address, handler_class)
    logging.info('Starting httpd on %d...\n', port)
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        pass
    httpd.server_close()
    logging.info('Stopping httpd...\n')

if __name__ == '__main__':
    from sys import argv

    if len(argv) == 2:
        run(port=int(argv[1]))
    else:
        run()