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

my_host_name = socket.gethostname()
my_local_ipaddr = socket.gethostbyname(my_host_name)

print 'Host Name:   %s' % my_host_name
print 'Local IP Address:    %s' % my_local_ipaddr


try:
	print 'one IP address of Server:    %s' % socket.gethostbyname(test_server_name)
except socket.err, err_msg:
	print 'error meassage from %s:  %s' % (test_server_name, err_msg)


for ipaddr in test_readable_ip:
	Packed_ipaddr = socket.inet_aton(ipaddr)
	Unpacked_ipaddr = socket.inet_ntoa(Packed_ipaddr)
	
	print 'IP: %s (length: %d bytes)  =====> (hexadecimal notation) %s (length: %d bytes)'\
		%(len(Unpacked_ipaddr), Unpacked_ipaddr, hexlify(Packed_ipaddr), len(Packed_ipaddr))
