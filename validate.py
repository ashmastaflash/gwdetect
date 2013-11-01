#!/usr/bin/python
import gwdglobals
import pcapy
import os.path

def validateinput():
    if not validate_device():
        print 'Device validation failed.  Check your config.'
        return 2
    if not validate_file():
        print 'File validation failed.  Check your config.'
        return 2
    if gwdglobals.interface == '' and gwdglobals.infile == '':
        print 'Must define input, either interface or file!'
    elif gwdglobals.interface != '' and gwdglobals.infile != '':
        print 'Cannot process two input sources!'
        return 2
    elif gwdglobals.outlog == '':
        print 'No output file defined!'
        return 2
    elif gwdglobals.outfile == '':
        print 'No output XML file defined!'
        return 2
    elif gwdglobals.subnet == '':
        print 'No subnet defined!'
        return 2
    else:
        return True

def validate_file():
    if gwdglobals.infile == '':
        print 'No input file defined, moving on...'
    elif os.path.isfile(gwdglobals.infile):
        gwdglobals.sourcetype = 'file'
        print 'Input file exists, moving on...'
        return True
    else:
        print 'Input file ' , gwdglobals.infile , ' does not exist!'
        return 2

def validate_outfile():
    return True

def validate_outformat():
    if gwdglobals.outformat == 'circos':
        return True

def validate_device():
    if gwdglobals.interface == '':
        print 'No interface selected'
        return True
    else:
        try:
            devices = pcapy.findalldevs()
        except:
            print 'pcapy can not find any devices - try sudo'
            return False
        if gwdglobals.interface in devices:
            gwdglobals.sourcetype = 'interface'
            print 'Interface verified: ' + gwdglobals.interface
        else:
            print 'Configured interface does not exist.  Available interfaces: ' , devices
            return False
