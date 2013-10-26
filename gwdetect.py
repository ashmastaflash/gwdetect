#!/usr/bin/python
'''
 gwdetect gateway detection tool
 Identifies gateways in use, as observed on the wire
 or from a pcap file
'''
import socket
from struct import *
import datetime
import pcapy
import sys
import getopt
import syslog
import os.path
import gwdglobals
from netaddr import IPNetwork, IPAddress
from  messages import *
from parse import parse_pcap , parse_payload
from gwdfunctions import printoutput , validateinput , firemessage

def main(argv):
    gwdglobals.globinit()
    messagebody = ''
    try:
        opts, args = getopt.getopt(argv, "hi:f:l:x:s:",["interface=","infile=","outlog=","outxml=","subnet="])
    except getopt.GetoptError:
        print usage_text
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print usage_text
            sys.exit()
        elif opt in ("-i", "--interface"):
            gwdglobals.interface = arg
        elif opt in ("-f", "--infile"):
            gwdglobals.infile = arg
        elif opt in ("-l", "--outlog"):
            gwdglobals.outlog = arg
        elif opt in ("-x", "--outxml"):
            gwdglobals.outxml = arg
        elif opt in ("-s", "--subnet"):
            gwdglobals.subnet = arg
    print 'Input file: ', gwdglobals.infile
    print 'Output log file: ', gwdglobals.outlog
    print 'Interface: ', gwdglobals.interface
    print 'XML output file: ', gwdglobals.outxml
    if validateinput() == True:
        messagebody = 'Source type is: ' + gwdglobals.sourcetype
        firemessage('1000',messagebody)
        if gwdglobals.sourcetype == 'file':
            parse_pcap(gwdglobals.infile)
            printoutput()
        else:
            print 'Interface capture is currently unsupported.'
            sys.exit()
    else:
        print gwdglobals.usage_text
        sys.exit(2)

if __name__ == "__main__":
    main(sys.argv[1:])
