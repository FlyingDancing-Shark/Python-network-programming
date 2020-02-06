"""
description
this program implemented a simple sniffer using raw socket,
the packets it captured include IP header and anything above the L3,
the "IP_hdr" class serve as an IP header parser and container for storage ourselves
human-readable IP header fields format that parsed from raw packets..........
"""

from ctypes import *
import os
import socket
import sys
import struct

host_address =  "192.168.3.113"


class IP_hdr(Structure):

    _fields_ = [
        ("ihl", c_ubyte,  4),      ("version", c_ubyte,  4),  ("tos", c_ubyte),
        ("len", c_ushort),         ("id", c_ushort),          ("offset", c_ushort),
        ("ttl", c_ubyte),          ("protocol_num", c_ubyte), ("sum", c_ushort),
        ("src", c_ulong),          ("dst", c_ulong)
    ]

    def __new__(self, socket_buffer=None):
        return self.from_buffer_copy(socket_buffer)


    def __init__(self, socket_buffer=None):

        self.protocol_map = {1:"ICMP", 6:"TCP", 17:"UDP"}
        self.src_address = socket.inet_ntoa(struct.pack("<L", self.src))
        self.dst_address = socket.inet_ntoa(struct.pack("<L", self.dst))

        try:
            self.protocol = self.protocol_map[self.protocol_num]
        except:
            self.protocol = str(self.protocol_num)

###################### END OF CLASS IP_hdr #################################

if os.name == 'nt':
    socket_protocol = socket.IPPROTO_IP
else:
    socket_protocol = socket.IPPROTO_ICMP

sniffer = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket_protocol)
sniffer.bind((host_address, 0))
sniffer.setsockopt(socket.IPPROTO_IP, socket.IP_HDRINCL, 1)

if os.name == 'nt':
    sniffer.ioctl(socket.SIO_RCVALL, socket.RCVALL_ON)
    print "\n\tturn ON promiscuous mode of network adapter....."

try:

    while True:

        raw_packet = sniffer.recvfrom(65535)[0]
        ip_header = IP_hdr(raw_packet[0:20])
        print "Protocol: %s %s ---> %s" % (ip_header.protocol, ip_header.src_address, ip_header.dst_address)

except KeyboardInterrupt:
    if os.name == "nt":
        sniffer.ioctl(socket.SIO_RCVALL, socket.RCVALL_OFF)
        print "\n\tturn OFF promiscuous mode of network adapter....."
    sys.exit(0)
