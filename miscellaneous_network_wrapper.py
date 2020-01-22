'''
*********description*********
get host name, get remote server ip address, convert dotted decimal notation strings to 
packed, fixed 4-bytes length hexadecimal notation strings (vice versa), 
query time from NTP server.....
'''

from binascii import hexlify
import random
import socket
import time

test_readable_ip = ['192.168.0.1', '8.8.8.8', '255.255.255.0']
test_server_name = 'www.facebook.com'
test_server_name_2 = 'www.vmofeuowlskqa.com'

# 3306 is the default port of MySQL, but it wouldn't be recognized by Python 
# "socket.getservbyport()" method.
test_port_range = [22, 25, 43, 69, 80, 123, 137, 138, 139, 443, 3389, 3306]
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
	print '[**ERROR**]:  %s' % (err_msg)

	
my_host_name = socket.gethostname()
my_local_ipaddr = socket.gethostbyname(my_host_name)

print '\nHost Name:   %s' % my_host_name
print 'Local IP Address:    %s' % my_local_ipaddr


try:
	print 'one IP address of Server %s:    %s' % (test_server_name, socket.gethostbyname(test_server_name))
	print 'one IP address of Server %s:    %s' % (test_server_name_2, socket.gethostbyname(test_server_name_2))
except socket.error, err_msg:
	print '[**ERROR**]%s:  %s' % (test_server_name_2, err_msg)


for ipaddr in test_readable_ip:
	Packed_ipaddr = socket.inet_aton(ipaddr)
	Unpacked_ipaddr = socket.inet_ntoa(Packed_ipaddr)
	
	print '\nIP: %s (length: %d bytes)  =====> (HEX notation) %s (length: %d bytes)'\
		%(Unpacked_ipaddr, len(Unpacked_ipaddr), hexlify(Packed_ipaddr), len(Packed_ipaddr))

def query_MTU():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) 
    s.connect(('168.95.192.1', 53)) 
    mtu = 65500
    while True:
        try:
            s.send('#' * mtu)
        except socket.error, err:
            print 'fail to send due to:\n  %s' % err
            print 'MTU is: %d' % (mtu - 1)
            break
        else:
            mtu += 1
    
    return (mtu - 1)


def check_sum(data):
	chksum = 0
        
        # "i" count from 0 to len(data) - 1
        for i in range(len(data)):
            
            # ord() compute an decimal value of a ASCII character 
            chksum += ord(data[i:i+1])
        return chksum
    
               
def gen_random64_bits():
    
    random_64bits = 0
    for i in range(64):
        sleep(3)
        # if False, skip this pass, don't perform bit-wise OR, entering next iteration (with "i" added by 1 ) 
        if random.randint(0, 1):
            random_64bits |= 1 << i
    	print 'generated random 64 bit number with hexadecimal format:  %0xd' % random_64bits
    	print 'generated random 64 bit number with decimal format: %d' % random_64bits
	
    print 'generated random 64 bit number with hexadecimal format:  %0xd' % random_64bits
    print 'generated random 64 bit number with decimal format: %d' % random_64bits
    return random_64bits
    

    
