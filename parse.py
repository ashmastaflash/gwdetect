#!/usr/bin/python
import pcapy
import socket
from struct import *
from gwdfunctions import eth_addr , createNode , disposition
import gwdglobals
import timeit


def time_parse_pcap(infile):
    reader = pcapy.open_offline(infile)
    while True:
        t = timeit.Timer()
        try:
            (header, payload) = reader.next()
            try:
                t.timeit(parse_payload(payload))
            except:
                pass
        except pcapyPcapError:
            break

def parse_pcap(infile):
    reader = pcapy.open_offline(infile)
    while True:
        try:
            (header, payload) = reader.next()
            parse_payload(payload)
        except pcapy.PcapError:
            break

def parse_payload(payload):
    eth_length = 14
    eth_header = payload[:eth_length]
    eth = unpack('!6s6sH', eth_header)
    eth_protocol = socket.ntohs(eth[2])
    mac_dest = eth_addr(payload[0:6])
    mac_src = eth_addr(payload[6:12])
    sip_unique = ''
    dip_unique = ''
    smac_unique = ''
    dmac_unique = ''
    #Carve out the IP header
    if eth_protocol == 8:
        ip_header = payload[eth_length:20+eth_length]
        iph = unpack('!BBHHHBBH4s4s' , ip_header)
        version_ihl = iph[0]
        version = version_ihl >> 4
        ihl = version_ihl & 0xF
        iph_length = ihl * 4
        ttl = iph[5]
        protocol = iph[6]
        ip_src = socket.inet_ntoa(iph[8])
        ip_dest = socket.inet_ntoa(iph[9])
# Send it along to its destiny
        disposition(ip_src,ip_dest,mac_src,mac_dest)
