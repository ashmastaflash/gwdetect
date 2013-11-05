#!/usr/bin/python
# This will contain the backbone,
# It will be run by MAIN and will
# handle the high-level decision-making
# in the application.

import gwdglobals
import datetime
import time
from parse import time_parse_pcap , parse_pcap , parse_payload
from gwdfunctions import printoutput , firemessage , write_circos , parse_config_file

def backbone():
    if gwdglobals.sourcetype == 'file':
        if  gwdglobals.timedebug == 'True':
            print 'Parsing input file, collecting timing metrics'
            time_parse_pcap(gwdglobals.infile)
        else:
            print 'Parsing input file, please wait.  Time is now: ' + datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S')
            parse_pcap(gwdglobals.infile)
        printoutput()
        if not gwdglobals.circos_report == '':
            write_circos()
            print 'Finished.  Time is now: ' + datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S')
    else:
        print 'Interface capture is currently unsupported.'
        sys.exit()

