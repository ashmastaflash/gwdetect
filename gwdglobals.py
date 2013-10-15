#!/usr/bin/python
'''
Globals go in this file
'''
def globinit():
    usage_text = 'gwdetect.py -i <interface> -f <inputfile> -l <logfile> -x <xmloutfile> -s <subnet in 0.0.0.0/0 notation>'
    global interface
    global infile
    global outlog
    global outxml
    global subnet
    global src_maclist
    global dst_maclist
    global src_iplist
    global dst_iplist
    global srcdest_sets
    global master_ip_list
    global master_mac_list
    global sourcetype
    interface = ''
    infile = ''
    outlog = ''
    outxml = ''
    subnet = ''
    src_maclist = []
    dst_maclist = []
    src_iplist = []
    dst_iplist = []
    srcdest_sets = []
    master_ip_list = []
    master_mac_list = []
