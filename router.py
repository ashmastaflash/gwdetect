#!/usr/bin/python
from networknode import NetworkNode
class Router(NetworkNode):
    mac_addr = ''
    def __init__(self, ip_addr, mac_addr):
        self.mac = mac_addr
        self.ip = ip_addr
