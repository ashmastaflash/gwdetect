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
from parse import parse_pcap , parse_payload
from gwdfunctions import printoutput , firemessage , write_circos , parse_config_file
from validate import validateinput

def main(argv):
    gwdglobals.globinit()
    messagebody = ''
    try:
        opts, args = getopt.getopt(argv, "hi:f:l:o:r:s:c:",["interface=","infile=","outlog=","reportfile=","subnet=","configfile="])
    except getopt.GetoptError:
        print usage_text
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
        elif opt in ("-r", "--reportfile"):
            gwdglobals.outfile = arg
        elif opt in ("-s", "--subnet"):
            gwdglobals.subnet = arg
    print 'Input file: ', gwdglobals.infile
    print 'Output log file: ', gwdglobals.outlog
    print 'Interface: ', gwdglobals.interface
    print 'Output report file: ', gwdglobals.outfile
    if validateinput() == True:
        messagebody = 'Source type is: ' + gwdglobals.sourcetype
        firemessage('1000',messagebody)
        if gwdglobals.sourcetype == 'file':
            print 'Parsing input file, please wait.  Time is now: ' + datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S')
            parse_pcap(gwdglobals.infile)
            printoutput()
            if not gwdglobals.circos_report == '':
                write_circos()
            print 'Finished.  Time is now: ' + datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S')
        else:
            print 'Interface capture is currently unsupported.'
            sys.exit()
    else:
        print gwdglobals.usage_text
        sys.exit(2)

if __name__ == "__main__":
    main(sys.argv[1:])
