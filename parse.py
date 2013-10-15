#!/usr/bin/python
import pcapy
import socket
from struct import *
from gwdfunctions import eth_addr , createNode
import gwdglobals

def parse_pcap(infile):
    reader = pcapy.open_offline(infile)
    while True:
        try:
            (header, payload) = reader.next()
            parse_payload(payload)
        except pcapy.PcapError:
            break

def parse_payload(payload):
    #Slice up the header
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
        #print 'Source: ' + mac_src + ' ' + str(ip_src) + ' Destination: ' + mac_dest + ' ' + str(ip_dest)
        if mac_src not in gwdglobals.src_maclist:
            smac_unique = 1
            gwdglobals.src_maclist.append(mac_src)
        if mac_dest not in gwdglobals.dst_maclist:
            dmac_unique = 1
            gwdglobals.dst_maclist.append(mac_dest)
        if ip_src not in gwdglobals.src_iplist:
            sip_unique = 1
            gwdglobals.src_iplist.append(ip_src)
        if ip_dest not in gwdglobals.dst_iplist:
            dip_unique = 1
            gwdglobals.dst_iplist.append(ip_dest)
            if mac_src + '-' + ip_src + '-' + mac_dest + '-' + ip_dest not in gwdglobals.srcdest_sets:
                gwdglobals.srcdest_sets.append(mac_src + '-' + ip_src + '-' + mac_dest + '-' + ip_dest)
            if mac_src not in gwdglobals.master_mac_list:
                gwdglobals.master_mac_list.append(mac_src)
            if mac_dest not in gwdglobals.master_mac_list:
                gwdglobals.master_mac_list.append(mac_dest)
            if ip_src not in gwdglobals.master_ip_list:
                createNode(ip_src, mac_src)
            if ip_dest not in gwdglobals.master_ip_list:
                createNode(ip_dest, mac_dest)


