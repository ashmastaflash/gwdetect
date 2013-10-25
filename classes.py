#!/usr/bin/python
'''
Class definitions go here
'''

class NetworkNode:
    ip_addr = ''
    def __init__(self):
        print 'Calling NetworkNode constructor.  If this is happening then something is wrong'

class Connected(NetworkNode):
    def __init__(self, ip_addr, mac_addr):
        self.mac = mac_addr
        self.ip = ip_addr

class Router(NetworkNode):
    mac_addr = ''
    def __init__(self, ip_addr, mac_addr):
        self.mac = mac_addr
        self.ip = ip_addr

class Remote(NetworkNode):
    def __init__(self, ip_addr):
        self.ip = ip_addr

class Enterprise(NetworkNode):
    def __init__(self, ip_addr):
        self.ip = ip_addr
        print '---Created Enterprise node with IP ' , ip_addr

class Path:
    def __init__(self, Connected, Remote, Router, route_direction):
        self.local = Connected
        self.remote = Remote
        self.router = Router
        self.direction = route_direction
