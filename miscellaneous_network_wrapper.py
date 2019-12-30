'''
*********description*********
get host name, get remote server ip address, convert dotted decimal notation strings to 
packed, fixed 4-bytes length hexadecimal notation strings (vice versa), 
query time from NTP server.....
'''

import socket
import random
from binascii import hexlify

test_readable_ip = ['192.168.0.1', '8.8.8.8', '255.255.255.0']
test_server_name = 'www.facebook.com'
test_server_name_2 = 'www.vmofeuowlskqa.com'
test_port_range = [22, 25, 43, 69, 80, 123, 137, 138, 139, 443, 3306, 3389]
"""
for i in range(0, 11):
	port = random.randrange(0, 1024)
	test_port_range.append(port)
"""
try:
	for port_number in test_port_range:
		print "Port: %s => service name: %s" %\
			(port_number, socket.getservbyport(port_number))
except socket.error, err_msg:
	print 'Port Number Error:  %s' % (err_msg)

	
my_host_name = socket.gethostname()
my_local_ipaddr = socket.gethostbyname(my_host_name)

print '\nHost Name:   %s' % my_host_name
print 'Local IP Address:    %s' % my_local_ipaddr


try:
	print 'one IP address of Server %s:    %s' % (test_server_name, socket.gethostbyname(test_server_name))
except socket.error, err_msg:
	print '%s:  %s' % (test_server_name, err_msg)


for ipaddr in test_readable_ip:
	Packed_ipaddr = socket.inet_aton(ipaddr)
	Unpacked_ipaddr = socket.inet_ntoa(Packed_ipaddr)
	
	print '\nIP: %s (length: %d bytes)  =====> (HEX notation) %s (length: %d bytes)'\
		%(Unpacked_ipaddr, len(Unpacked_ipaddr), hexlify(Packed_ipaddr), len(Packed_ipaddr))


	
