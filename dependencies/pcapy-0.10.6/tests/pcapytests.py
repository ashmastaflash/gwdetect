## Copyright (c) 2003 CORE Security Technologies
##
## This software is provided under under a slightly modified version
## of the Apache Software License. See the accompanying LICENSE file
## for more information.
##
## $Id: test.py 21 2003-10-23 20:00:54Z jkohen $
import pcapy
import sys
import unittest

class TestPcapy(unittest.TestCase):
    _96PINGS = '96pings.pcap'
    def testPacketHeaderRefCount(self):
        """#1:when next() creates a pkthdr it make one extra reference"""
        class _Simple: pass
        #r = pcapy.open_live("en1", 65000, 0, 1000)
        r = pcapy.open_offline(TestPcapy._96PINGS)
        #get one & check its refcount
        self.assertEqual( sys.getrefcount(r.next()[0]),
                          sys.getrefcount(_Simple()) )

suite = unittest.TestLoader().loadTestsFromTestCase(TestPcapy)
unittest.TextTestRunner(verbosity=2).run(suite)
