#!/usr/bin/python
'''
this is why we can't have nice things.  Also, where
we hide our functions.
'''
import gwdglobals
import pcapy
import ConfigParser
#import os.path
from netaddr import IPNetwork, IPAddress
from connected import Connected
from remote import Remote
from router import Router


def eth_addr(a):
    b = '%.2x:%.2x:%.2x:%.2x:%.2x:%.2x' % (ord(a[0]) , ord(a[1]) , ord(a[2]), ord(a[3]), ord(a[4]) , ord(a[5]))
    return b

def createNode(ip, mac):
    subnet = gwdglobals.subnet
    if ipInSubnet(ip,subnet):
        print ip, ' is in subnet ' , subnet
        mac = Connected(ip, mac)
    else:
        ip = Remote(ip)
        print ip, ' is not in subnet ' , subnet

def ipInSubnet(ipaddr, subnet):
    if IPAddress(ipaddr) in IPNetwork(subnet):
        messagebody = 'IP: ' + ipaddr + ' Subnet: ' + subnet
        firemessage('1017',messagebody)
        return True
    else:
        return False

def printoutput():
    outfile = gwdglobals.outlog
    insidehost = ''
    gateway = ''
    if not outfile == '':
        f = open(outfile,'a')
        f.write('Routes: inside, outside, gateway, observed direction:\n')
        for h in gwdglobals.routes:
            f.write(str(h))
        f.write('Connected Nodes:\n')
        for i in gwdglobals.connected_nodes:
            f.write(i.mac + ' ' + i.ip + '\n')
        f.write('Remote Nodes:\n')
        for j in gwdglobals.connected_nodes:
            f.write(j.ip + '\n')
        f.write('Routers:\n')
        for k in gwdglobals.routers:
            f.write(k.mac + '\n')
            if any(m.mac == k.mac for m in gwdglobals.connected_nodes):
                routerIP = [connNode for connNode in gwdglobals.connected_nodes if connNode.mac == k.mac]
                f.write(k.mac + ' ' + routerIP[0].ip)
        return()
    print 'Routes: inside, outside, gateway, observed direction'
    for i in gwdglobals.routes:
        print i
    print 'Connected Nodes: '
    for j in gwdglobals.connected_nodes:
        print  j.mac , ' ' , j.ip
    print 'Remote Nodes:'
    for k in gwdglobals.remote_nodes:
        print k.ip
    print 'Routers:'
    for l in gwdglobals.routers:
        print l.mac
        if any(m.mac == l.mac for m in gwdglobals.connected_nodes):
            routerIP = [connNode for connNode in gwdglobals.connected_nodes if connNode.mac == l.mac]
            print l.mac , ' ' , routerIP[0].ip

def write_circos():
    outfile = gwdglobals.circos_report
    outmatrix = []
    router_labels = []
    host_labels = []
# Create the gateway labels
    for l in gwdglobals.routers:
        if any(m.mac == l.mac for m in gwdglobals.connected_nodes):
            routerIP = [connNode for connNode in gwdglobals.connected_nodes if connNode.mac == l.mac]
            router_labels.append(routerIP[0].ip)

# Now, node labels
    for o in gwdglobals.connected_nodes:
        if any(x[0] == o.mac for x in gwdglobals.routes):
            host_labels.append(o.ip)

# Build tabular data structure:
# Write header
    f = open(outfile,'w+')
    f.truncate()
    f = open(outfile,'a')
    topline = 'data'
    headercolors = 'data'
    for i in router_labels:
        if i in gwdglobals.gateway_whitelist :
            headercolors = headercolors + ' 100,100,100'
        else:
            headercolors = headercolors + ' 200,100,100'
        topline = topline + ' GW_' + str(i)
    topline = topline.replace('.','_').replace(':','_')
    f.write('#Please visit http://mkweb.bcgsc.ca/tableviewer/visualize to generate this graphic the easy way.\n')
    f.write('#Here is a hint: Row with Column Colors...\n')
    f.write(headercolors + '\n')
    f.write(topline + '\n')
    for y in gwdglobals.connected_nodes:
        line = y.ip
        for i in gwdglobals.routers:
            line = line + ' ' + count_routers(y.mac,i.mac)
        line = 'IP_' + line.replace('.','_').replace(':','_').replace(' 0',' -')
        f.write(line + '\n')
    f.close()


def count_routers(host_mac,rtr_mac):
    count = 0
    for i in gwdglobals.routes:
        if i[3] == 'confirmed' and i[0] == host_mac and i[2] == rtr_mac:
            count += 1
    return(str(count))


# Testing output...
    print 'Router Labels:'
    for p in router_labels:
        print p
    print 'Host Labels:'
    for q in host_labels:
        print q


def disposition(sip,dip,smac,dmac):
    mac_src = smac
    mac_dest = dmac
    ip_src = sip
    ip_dest = dip
    sip_local = ''
    dip_local = ''
    sip_unique = ''
    dip_unique = ''
    router = ''
    nodename = ''
    subnet = gwdglobals.subnet
    direction = 'indeterminite'
# Test if IPs exist in connected net, then determine if they are unique
# Determine if source IP is local
    if ipInSubnet(ip_src,subnet):
        sip_local = 1
    else:
        sip_local = 0
# If the source IP is local, determine if it is new
    if sip_local == 1:
        if not check_local_exists(mac_src):
            sip_unique = 1
        else:
            sip_unique = 0
# If the source IP is not local, determine if it is new
    elif sip_local == 0:
        if not check_remote_exists(ip_src):
            sip_unique = 1
        else:
            sip_unique = 0
    else:
        print 'Source IP is in Schrodinger box.  with the cat.'

# Determine if destination IP is local
    if ipInSubnet(ip_dest,subnet):
        dip_local = 1
    else:
        dip_local = 0
# If dest IP is local, determine if it is new
    if dip_local == 1:
        if not check_local_exists(mac_dest):
            dip_unique = 1
        else:
            dip_unique = 0
# If destinationIP is not local, determine if it is new
    elif dip_local == 0:
        if not check_remote_exists(ip_dest):
            dip_unique = 1
        else:
            dip_unique = 0
    else:
        print ' Destination IP is in Schrodinger box, playing with the cat.'

# If Create nodes if necessary
    if sip_unique == 1:
        if sip_local == 1:
            nodename = mac_src
            gwdglobals.connected_nodes.append(Connected(ip_src,mac_src))
            messagebody = 'IP: ' + ip_src + ' MAC: ' + mac_src
            firemessage('1010',messagebody)
        elif sip_local == 0:
            nodename = ip_src
            gwdglobals.remote_nodes.append(Remote(ip_src))
            messagebody = 'IP: ' + ip_src
            firemessage('1011',messagebody)
        else:
            print 'Failed node disposition, creation with source ' , mac_src , ' ' , ip_src
    if dip_unique == 1:
        if dip_local == 1:
            nodename = mac_dest
            gwdglobals.connected_nodes.append(Connected(ip_dest,mac_dest))
            messagebody = 'IP: ' + ip_dest + ' MAC: ' + mac_dest
            firemessage('1010',messagebody)
        elif dip_local == 0:
            nodename = ip_dest
            gwdglobals.remote_nodes.append(Remote(ip_dest))
            messagebody = 'IP: ' + ip_dest
            firemessage('1011',messagebody)
        else:
            print 'Failed node disposition, creation with destination ' , mac_dest , ' ' , ip_src
#Now we want to know if they are inbound or outbound
    if sip_local == 1 and dip_local == 1:
        router = 'Layer 2'
        return()
    if sip_local == 0 and dip_local == 0:
        router = 'Who Cares'
        return()
    if sip_local == 1 and dip_local == 0:
        direction = 'outbound'
    if sip_local == 0 and dip_local == 1:
        direction = 'inbound'
# Now, we determine router MAC address
    if direction == 'outbound':
        router = mac_dest
    if direction == 'inbound':
        router = mac_src
# Now, we create a router if none exists already...
    if not check_router_exists(router):
        rtrmac = router
        gwdglobals.routers.append(Router('undefined',rtrmac))
    else:
        if router == '':
            print 'Source: '+ mac_src + ':' + ip_src +' Destination: ' + mac_dest + ':' + ip_dest + 'EMPTY ROUTER'


# Depending on direction, we create routes
# Routes will be consolidated if inverse routes
# of opposite directions exist.  The inbound and outbound
# routes will be replaced by confirmed when both directions
# have been observed

    if direction == 'outbound':
        if check_route_exists(mac_src,ip_dest,router,'confirmed'):
            return()
        if check_route_exists(mac_src,ip_dest,router,'outbound'):
            return()
        if check_route_exists(mac_src,ip_dest,router,'inbound'):
            gwdglobals.routes.remove([mac_src,ip_dest,router,'inbound'])
            gwdglobals.routes.append([mac_src,ip_dest,router,'confirmed'])
            messagebody = 'Inside: ' + mac_src + ' Outside: ' + ip_dest + \
                    ' Router: ' + router
            firemessage('1015',messagebody)
            return()
        else:
            gwdglobals.routes.append([mac_src,ip_dest,router,'outbound'])
            messagebody = 'Inside: ' + mac_src + ' Outside: ' + ip_dest + \
                    ' Router: ' + router
            firemessage('1014',messagebody)
            return()
    if direction == 'inbound':
        if check_route_exists(mac_dest,ip_src,router,'confirmed'):
            return()
        if check_route_exists(mac_dest,ip_src,router,'inbound'):
            return()
        if check_route_exists(mac_dest,ip_src,router,'outbound'):
            gwdglobals.routes.remove([mac_dest,ip_src,router,'outbound'])
            gwdglobals.routes.append([mac_dest,ip_src,router,'confirmed'])
            messagebody = 'Inside: ' + mac_dest + ' Outside: ' + ip_src + \
                    ' Router: ' + router
            firemessage(1016,messagebody)
            return()
        else:
            gwdglobals.routes.append([mac_dest,ip_src,router,'inbound'])
            messagebody = 'Inside: ' + mac_dest + ' Outside: ' + ip_src + \
                    ' Router: ' + router
            firemessage('1015',messagebody)
            return()


def check_ip_is_local(ipaddress):
    subnet = gwdglobals.subnet
    if ipInSubnet(ipaddress,subnet):
        return True
    else:
        return False

def check_local_exists(macaddress):
    firemessage('1018',macaddress)
    if any(x.mac == macaddress for x in gwdglobals.connected_nodes):
        firemessage('1022',macaddress)
        return True
    else:
        firemessage('1023',macaddress)
        return False

def check_remote_exists(ipaddress):
    firemessage('1019',ipaddress)
    if any(x.ip == ipaddress for x in gwdglobals.remote_nodes):
        return True
    else:
        return False

def check_router_exists(macaddress):
    if macaddress == '':
        firemessage('1024',macaddress)
        return True
    firemessage('1020',macaddress)
    if any(x.mac == macaddress for x in gwdglobals.routers):
        firemessage('1021',macaddress)
        return True
    else:
        firemessage('1012',macaddress)
        return False

def check_route_exists(inner,outer,rtr,direction):
    if [inner,outer,rtr,direction] in gwdglobals.routes:
        return True
    else:
        return False

def firemessage(code , message):
    messages = gwdglobals.messages
    level = gwdglobals.debuglevel
    leveltext = ''
    if not gwdglobals.outlog == '':
        outlog = gwdglobals.outlog
        f=open(outlog,'a')
        if any(i[0] == code for i in messages):
            messagematch = [messages for messages in messages if messages[0] == code]
            if messagematch[0][1] <= level:
                if messagematch[0][1] == 1:
                    leveltext = 'ERROR'
                elif messagematch[0][1] == 2:
                    leveltext = 'INFO'
                elif messagematch[0][1] == 3:
                    leveltext = 'DEBUG'
                else:
                    f.write('Undefined Message Alert Level!!\n')
                f.write(leveltext + ':' + code + ' ' + messagematch[0][2] + message + '\n')
                return()
    elif any(i[0] == code for i in messages):
        messagematch = [messages for messages in messages if messages[0] == code]
        if messagematch[0][1] <= level :
            if messagematch[0][1] == 1:
                leveltext = 'ERROR'
            elif messagematch[0][1] == 2:
                leveltext = 'INFO'
            elif messagematch[0][1] == 3:
                leveltext = 'DEBUG'
            else:
                print 'Undefined message alert level!!'
            print leveltext + ':' + code , ' ' + messagematch[0][2] ,  message
            return()

def parse_config_file():
    config = ConfigParser.RawConfigParser(allow_no_value=True)
    config.read(gwdglobals.configfile)
    gwdglobals.infile = config.get("Input","filename")
    gwdglobals.interface = config.get("Input","interface")
    gwdglobals.gateway_whitelist = config.get("Filter","whitelist_gateways")
    gwdglobals.subnet = config.get("Filter","protected_subnet")
    gwdglobals.circos_report = config.get("Output","circos_report")



