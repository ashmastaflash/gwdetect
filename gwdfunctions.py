#!/usr/bin/python
'''
this is why we can't have nice things.  Also, where
we hide our functions.
'''
import gwdglobals
import pcapy
import os.path
from netaddr import IPNetwork, IPAddress
from classes import *

def eth_addr(a):
    b = '%.2x:%.2x:%.2x:%.2x:%.2x:%.2x' % (ord(a[0]) , ord(a[1]) , ord(a[2]), ord(a[3]), ord(a[4]) , ord(a[5]))
    return b

def createNode(ip, mac):
    subnet = gwdglobals.subnet
    if ipInSubnet(ip,subnet):
        print ip, ' is in subnet ' , subnet
        ip = Connected(ip, mac)
    else:
        ip = Remote(ip)
        print ip, ' is not in subnet ' , subnet

def ipInSubnet(ipaddr, subnet):
    if IPAddress(ipaddr) in IPNetwork(subnet):
        print 'Match! ', ipaddr , ' exists in subnet ' , subnet
        return True
    else:
        return False

def printoutput():
    print 'Unique source MAC addresses: ' ,  gwdglobals.src_maclist
    print 'Unique destination MAC addresses: ' , gwdglobals.dst_maclist
    print 'Unique source IP addresses: ' , gwdglobals.src_iplist
    print 'Unique destination IP addresses: ' , gwdglobals.dst_iplist
    print 'Unique source/destination sets'
    for i in gwdglobals.srcdest_sets:
        print i
    for j in gwdglobals.master_ip_list:
        print j


def validateinput():
    global sourcetype
    sourcetype = ''
    devices = pcapy.findalldevs()
    if gwdglobals.interface in devices:
        gwdglobals.sourcetype = 'interface'
        print 'Interface verified: ', gwdglobals.interface
    elif gwdglobals.interface == '':
        print 'No interface selected, moving on...'
    else:
        print 'Configured interface does not exist'
        print 'Available devices: ', devices
        return 2
    if gwdglobals.infile == '':
        print 'No input file defined, moving on...'
    elif os.path.isfile(gwdglobals.infile):
        gwdglobals.sourcetype = 'file'
        print 'Input file exists, moving on...'
    else:
        print 'Input file does not exist!'
        return 2
    if gwdglobals.interface == '' and gwdglobals.infile == '':
        print 'Must define input, either interface or file!'
    elif gwdglobals.interface != '' and gwdglobals.infile != '':
        print 'Cannot process two input sources!'
        return 2
    elif gwdglobals.outlog == '':
        print 'No output file defined!'
        return 2
    elif gwdglobals.outxml == '':
        print 'No output XML file defined!'
        return 2
    elif gwdglobals.subnet == '':
        print 'No subnet defined!'
        return 2
    else:
        return True

