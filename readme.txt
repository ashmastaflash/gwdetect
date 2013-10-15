gwdetect.py

This tool is designed to observe network behavior
and generate log events for anomalies.

Currently, only pcap processing is supported, with live network monitoring coming soon


This is what it does now:
From a pcap file
  Creates a list of observed unique MAC addresses
  Creates a list of observed IP addresses
  Creates a list of observed L2 paths

Future functionality:
  Configuration:
    File-based configuration

  XML output:
    Describing observed routes, focusing on onbound and outbound from target (connected) subnet
    Describing MAC to IP relationships for nodes discovered in connected subnet

  Whitelisting:
    Define permitted gateways
    Sample whitelist generation from observed traffic

  Filtering:
    Support multiple subnets
    Support VLAN filtering
    Support tracking enterprise nodes, outside of focus subnet

  Data handling:
    Better-looking output to stdout, log file, and/or syslog
    Garbage collection for old routes/external nodes after dumping snapshot to XML



This product includes software developed by CORE Security Technologies (http://www.coresecurity.com/)."
