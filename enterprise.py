#!/usr/bin/python
from networknode import NetworkNode
class Enterprise(NetworkNode):
    def __init__(self, ip_addr):
        self.ip = ip_addr
        print '---Created Enterprise node with IP ' , ip_addr
