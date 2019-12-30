'''
*********description*********
get host name, get remote server ip address, convert dotted decimal notation strings to 
packed, fixed 4-bytes length hexadecimal notation strings (vice versa), 
query time from NTP server.....
'''

import socket
from binascii import hexlify

test_readable_ip = ['192.168.0.1', '8.8.8.8', '255.255.255.0']
test_server_name = 'www.facebook.com'
test_server_name_2 = 'www.vmofeuowlskqa.com'

