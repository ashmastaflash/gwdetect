#!/usr/bin/python
'''
 gwdetect gateway detection tool
 Identifies gateways in use, as observed on the wire
 or from a pcap file
'''
import socket
from struct import *
import datetime
import time
import pcapy
import sys
import getopt
import syslog
import os.path
import gwdglobals
import ConfigParser
from netaddr import IPNetwork, IPAddress
from  messages import *
#from parse import parse_pcap , parse_payload
from gwdfunctions import printoutput , firemessage , write_circos , parse_config_file
from validate import validateinput
from gwdbackbone import backbone

def main(argv):
    gwdglobals.globinit()
    messagebody = ''
    try:
        opts, args = getopt.getopt(argv, "hi:f:l:C:s:c:",["interface=","infile=","outlog=","circosfile=","subnet=","configfile="])
    except getopt.GetoptError:
        print gwdglobals.usage_text
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print usage_text
            sys.exit()
        elif opt in ("-c","--configfile"):
            gwdglobals.configfile = arg
            parse_config_file()
        elif opt in ("-i", "--interface"):
            gwdglobals.interface = arg
        elif opt in ("-f", "--infile"):
            gwdglobals.infile = arg
        elif opt in ("-l", "--outlog"):
            gwdglobals.outlog = arg
        elif opt in ("-C", "--circosfile"):
            gwdglobals.circos_report = arg
        elif opt in ("-s", "--subnet"):
            gwdglobals.subnet = arg
    print 'Input file: ', gwdglobals.infile
    print 'Output log file: ', gwdglobals.outlog
    print 'Interface: ', gwdglobals.interface
    print 'Circos output file: ', gwdglobals.circos_report
    if validateinput() == True:
        messagebody = 'Source type is: ' + gwdglobals.sourcetype
        firemessage('1000',messagebody)
        backbone()
    else:
        print gwdglobals.usage_text
        sys.exit(2)

if __name__ == "__main__":
    main(sys.argv[1:])
