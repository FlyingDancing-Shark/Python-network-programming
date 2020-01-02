'''
*********description*********
The client part of this UDP socket program implemented simple congestion control and 
reliability, and using connecting UDP socket. 
The server mode support simulate packet dropped in order to test the reliability 
algorithm of client mode.
'''

import random, socket, sys, time

MAX_RECV = 65535

# to listen on this port need administrator privileges in UNIX-like system 
PORT = 1060

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# running at server mode
# for example ：
# python my_UDP_Server_Client_Generator.py server 
# argv[0] = my_UDP_Server_Client_Generator.py
# argv[1] = server 
# argv[2] = ''  , also support specify as a host name of server ,such as "shayi1983-PC"
if (2 <= len(sys.argv) <= 3) and (sys.argv[1] == 'server'):
	interface = sys.argv[2] if len(sys.argv) > 2 else ''
	s.bind((interface, PORT))
	
	# getsockname() return IP address(string object) of the interface 
	# and port(integer object) as a tuple
	print '\n\t--------Listening at--------\n\t', s.getsockname()
	
	while True:
		# keep receive data from client
		data, address = s.recvfrom(MAX_RECV)
		
		# 
		if random.randint(0, 1):
			print '\n\tThe client at', address, 'says:', repr(data)
			s.sendto('--------Your data was %d bytes--------' % len(data), address)
		
	
		# if generate number 0, then simulate we dropped packet due to network 
		# connectivity problem or congestion
		else:
			print '\n\tPretending to drop packet send from client--------', address
			
			# pause server for a period of time to simulate it is down entirely, 
			# adjust client reliability code correspondingly
			# this will pause arbitrary seconds, then keep receive data from client
			# if not random.randint(0, 1):
				# time.sleep(random.randint(5, 15)) 

# running at client mode
elif (len(sys.argv) == 3) and (sys.argv[1] == 'client'):
	
	# this is server's hostname
	hostname = sys.argv[2]
	s.connect((hostname, PORT))
	print '\n\t--------Client socket name is--------', s.getsockname()
	
	# 
	local_delay = 0.01
	# internet_delay = 0.3
	
	while True:
		s.send('--------This is another client message--------') 
		print '\n\t--------Waiting up to', local_delay, 'seconds for a reply--------'
		s.settimeout(local_delay)
		# s.settimeout(internet_delay)
		
		try:
			data = s.recv(MAX_RECV)
		except socket.timeout:
			local_delay *= 2
			if local_delay > 0.08:
				# local_delay = 0.08
				
				raise RuntimeError('\n\t--------I think the server is down--------')
		except socket.error, err:
			print "\n\t-----Fail to receiving data:  %s-----" % err
			sys.exit(1) 
			
		# if server reply before current timeout value, exit loop, 
		# print message receiving from server	
		else:
			break
	
	# if we put this print into "else" block, and comment "break“，then we can test 
	# along with "time.sleep(random.randint(5, 15))"
	print '\n\tThe server says: ', repr(data)

else:
    print >>sys.stderr, '\n\tusage:-------my_UDP_Server_Client_Generator.py server [ <interface> ]'
    print >>sys.stderr, '\tor:-------my_UDP_Server_Client_Generator.py client <host>'
    sys.exit(2)
	
	
