'''
*********description*********
The client part of this UDP socket program implemented simple congestion control and 
reliability, and using connecting UDP socket. 
The server mode support simulate packet dropped in order to test the reliability 
algorithm of client mode.
'''

import random, socket, sys

MAX_RECV = 65535

# to listen on this port need administrator privileges in UNIX-like system 
PORT = 1060

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# running at server mode
if (2 <= len(sys.argv) <= 3) and sys.argv[1] == 'server':
	interface = sys.argv[2] if len(sys.argv) >2 else ''
	
