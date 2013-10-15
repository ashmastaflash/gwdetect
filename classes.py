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
        mac = mac_addr
        ip = ip_addr
        print 'Created ConnectedNode with IP ' , ip_addr , ' and MAC ' , mac_addr

class Router(NetworkNode):
    mac_addr = ''
    def __init__(self, ip_addr, mac_addr):
        mac = mac_addr
        ip = ip_addr
        print 'Created Rotuer with IP ' , ip_addr , ' and MAC ' , mac_addr

class Remote(NetworkNode):
    def __init__(self, ip_addr):
        ip = ip_addr
        print 'Created Remote node with IP ' , ip_addr

class Enterprise(NetworkNode):
    def __init__(self, ip_addr):
        ip = ip_addr
        print 'Created Enterprise node with IP ' , ip_addr

class Path:
    def __init__(self, Connected, Remote, Router, route_direction):
        local = Connected
        remote = Remote
        router = Router
        direction = route_direction
