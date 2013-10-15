#!/usr/bin/python
'''
This file contains all log message handling
functions for gwdetect.py
'''

def messagehandler(msgcode, srcip, srcmac, dstip, dstmac, custom_string):
    if msgcode == 1000:
        print 'INFO:1000 Configuration verification successful!'
        if msgcode == 1001:
            print 'ERROR:1001 Configuration verification FAILED! ' , custom_string
        elif msgcode == 1010:
            print 'INFO:1010 New IP address discovered in PROTECTED network: ' , srcip
        elif msgcode == 1011:
            print 'INFO:1011 New IP address discovered in REMOTE network: ' , srcip
        elif msgcode == 1012:
            print 'INFO:1013 New MAC address discovered in PROTECTED network: ' , srcmac
        elif msgcode == 1013:
            print 'INFO:1013 New INBOUND route discovered: ', srcip , ' inbound to ' , dstip , ' via gateway ' , custom_string
        elif msgcode == 1014:
            print 'INFO:1014 New OUTBOUND route discovered: ' ,  srcip , ' outbound to ' , dstip , ' via gateway ' , custom_string

