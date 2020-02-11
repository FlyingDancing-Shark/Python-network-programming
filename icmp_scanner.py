"""
description

"""

from ctypes import *
import os
import socket
import sys
import struct
import threading
import time

# pip install netaddr
from netaddr import IPNetwork, IPAddress


listen_address =  "192.168.3.113"
scan_subnet = "192.168.3.0/24"
magic_message = "SHAYI1983"


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

###################### END OF CLASS IP_hdr definition #############################

class ICMP_hdr(Structure):

    _fields_ = [
        ("type",            c_ubyte),
        ("code",            c_ubyte),
        ("checksum",        c_ushort),
        ("unused",          c_ushort),
        ("next_hop_mtu",    c_ushort)
    ]


    def __new__(self, socket_buffer):
        return self.from_buffer_copy(socket_buffer)

    # this line can NOT be omitted, otherwise,
    # we can't instantiated an ICMP header object!
    def __init__(self, socket_buffer):
        pass

###################### END OF CLASS ICMP_hdr definition ###########################

def udp_sender(subnet, magic_string):

    # this guarantee that the worker thread won't emit host detection packets too 
    # fast that main sniffer thread can't display to user with each alive host 
    # in a timely manner.
    time.sleep(5)
    sender = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    for ip in IPNetwork(subnet):
        try:
            sender.sendto(magic_string, ("%s" % ip,65212))
        except:
            pass
###################### END OF udp_sender definition ###################

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

worker_thread = threading.Thread(target=udp_sender, args=(scan_subnet, magic_message))
worker_thread.start()


try:

    while True:

        raw_packet = sniffer.recvfrom(65535)[0]
        ip_header = IP_hdr(raw_packet[0:20])
        print "Protocol: %s %s ---> %s" % (ip_header.protocol, ip_header.src_address, ip_header.dst_address)

        if  ip_header.protocol == "ICMP":
            offset = ip_header.ihl * 4
            icmp_packet = raw_packet[offset:offset + sizeof(ICMP_hdr)]
            icmp_header = ICMP_hdr(icmp_packet)

            if icmp_header.code == 3 and icmp_header.type == 3:
                if IPAddress(ip_header.src_address) in IPNetwork(scan_subnet):
                    if raw_packet[len(raw_packet) - len(magic_message):] == magic_message:
                        print "Host UP !!! ---> %s" % ip_header.src_address


except KeyboardInterrupt:
    if os.name == "nt":
        sniffer.ioctl(socket.SIO_RCVALL, socket.RCVALL_OFF)
        print "\n\tturn OFF promiscuous mode of network adapter....."
    sys.exit(0)
    
    
