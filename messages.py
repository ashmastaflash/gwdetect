#!/usr/bin/python
'''
This file contains all log messages,
called by logmsg object
1=ERROR
2=INFO
3=DEBUG
'''


'''
Messagecode, level, message
'''



messagelist = [['1000' , 2 , 'Configuration Verification Successful!'],
            ['1001' , 1 , 'Configuration verification FAILED!'],
            ['1010' , 2 , 'New node discovered in protected network'],
            ['1011' , 3 , 'New node discovered in remote network'],
            ['1012' , 2 , 'New router discovered'],
            ['1013' , 3 , 'New inbound route discovered'],
            ['1014' , 3 , 'New outbound route discovered'],
            ['1015' , 3 , 'Inbound route reconciled to complete route'],
            ['1016' , 3 , 'Outbound route reconciled to complete route'],
            ['1017' , 3 , 'Local subnet match found!'],
            ['1018' , 3 , 'Local existence check'],
            ['1019' , 3 , 'Remote existence check'],
            ['1020' , 3 , 'Router existence check '],
            ['1021' , 3 , 'Router already exists '],
            ['1022' , 3 , 'Local MAC address already exists '],
            ['1023' , 3 , 'MAC does not have attribute ip_addr (does not exist) '],
            ['1024' , 1 , 'Attempt to locate empty router! ']]


