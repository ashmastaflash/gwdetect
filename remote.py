#!/usr/bin/python
from networknode import NetworkNode
class Remote(NetworkNode):
    def __init__(self, ip_addr):
        self.ip = ip_addr
