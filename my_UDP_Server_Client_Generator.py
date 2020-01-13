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

allowed_IPs_white_list = ['127.0.0.1', '192.168.3.113']

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# running at server mode
# for example:
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
	
	'''
	client_request, address = s.recvfrom(MAX_RECV)
	if address[0] not in allowed_IPs_white_list:
			print '\n\t---receive data from a suspicious host,  exit ----'
			sys.exit(2)
			
	# we should receive the very first packet and retrieve its ID and reply client , 
	# then could start randomly reply/dropped logic
	previous_seq_num = int(client_request[0:5])
	print '\n\tThe client at', address, 'says:', repr(client_request)
	new_reply_msg = client_request[0:5] + "--------NEW server reply--------"
	s.sendto(new_reply_msg, address)
	'''
	
	while True:
		# keep receive data from client
		# here, "address" is a tuple like such----- ('192.168.3.113', 58713)
		client_request, address = s.recvfrom(MAX_RECV)
		
		# so we only perform security check against the 'IP' element in this tuple 
		if address[0] not in allowed_IPs_white_list:
			print '\n\t---receive data from a suspicious host,  exit ----'
			sys.exit(2)
				
		if random.randint(0, 1):
			'''
			result = random.choice(['new_reply', 'duplicate_reply'])
			if result == 'new_reply':
				print '\n\tThe client at', address, 'says:', repr(client_request)
				new_reply_msg = client_request[0:5] + "--------NEW server reply--------"
				s.sendto(new_reply_msg, address)
			else:
			'''	
			print '\n\treceive client message: ', repr(client_request)
			reply_to_client = client_request[0:5] + "--------Server Reply--------"
			print '\n\tNow reply client: ', repr(reply_to_client)	
			s.sendto(reply_to_client, address)
		
		
		# if generate number 0, then simulate we dropped packet due to network 
		# connectivity problem or congestion
		else:
			print '\n\tPretending to drop client request: --------', client_request
			
			# pause server for a period of time to simulate it is down entirely, 
			# adjust client reliability code correspondingly
			# this will pause arbitrary seconds, then keep receive data from client
			time.sleep(round(random.uniform(0.01, 0.20), 2)) 
			
		# save current client request ID before enter next iteration 
		# previous_seq_num = int(client_request[0:5])
		
# running at client mode
elif (len(sys.argv) == 3) and (sys.argv[1] == 'client'):
	
	# this is server's hostname
	hostname = sys.argv[2]
	s.connect((hostname, PORT))
	print '\n\t--------Client socket name is--------', s.getsockname()
	print '\n\t--------the PEER to which we connected to is: --------', s.getpeername()
	# 10 milliseconds
	local_delay = 0.01
	# internet_delay = 0.3
	resend = 0
	stay_under_max_delay = 0
	repeat = False
	seq_num = 0
	previous_seq_num = 0 
	
	# because first time the server always respond us without timeout, 
	# dropped or duplicated packet, so we can get packet successfully, 
	# and store current request ID for later used
	'''
	seq_num = random.randint(10000, 99999)
	
	previous_seq_num = seq_num
	msg = str(seq_num) + "--------NEW client message--------"
	s.send(msg)
	server_reply = s.recv(MAX_RECV)
	print '\n\tThe server reply as: ', repr(server_reply)
	'''
	while True:
		time.sleep(1)
		
		# when resend duplicate packet, using previously ID
		if repeat:
			duplicate_msg = str(previous_seq_num) + "--------DUPLICATED client message--------"
			s.send(duplicate_msg)
			print 'send to server: ', duplicate_msg
		else:
			# when sending new packet, generate new ID
			seq_num = random.randint(10000, 99999)
			msg = str(seq_num) + "--------NEW client message--------"
			s.send(msg)
			print 'send to server: ', msg
		
		print '\n\t--------Waiting up to', local_delay, 'seconds for a reply, the', resend, 'th resend--------'
		s.settimeout(local_delay)
		# s.settimeout(internet_delay)
		
		try:
			server_reply = s.recv(MAX_RECV)
		# we need to resend, so flag repeat
		except socket.timeout:
			
			repeat = True
			local_delay *= 2
			
			# if we resend over four times, stop increase waiting time or 
			# terminate process
			if local_delay > 0.16:
				local_delay = 0.16
				stay_under_max_delay += 1
				if stay_under_max_delay > 3:
					print "\n\t---------I think the server is down after %dth resend -_-!" % resend
					sys.exit(1)
					# raise RuntimeError('\n\t--------I think the server is down, after', resend, 'th resend------')
		     	resend += 1
			
				# raise RuntimeError('\n\t--------I think the server is down--------')
		except socket.error, err:
			print "\n\t-----Fail to receiving data:  %s-----" % err
			sys.exit(1) 
		
		except KeyboardInterrupt:
			print '\n\t--- handle user request for exiting ----'
			sys.exit(0) 
		# if server reply before current timeout value, exit loop, 
		# print message receiving from server	
		else:
			# upon receive duplicate packet, needn't handle
			if resend > 0 and server_reply[0:5] != str(seq_num):
				print '\n\tReceived duplicate reply: ", server_reply
				
			if resend <= 3:
				local_delay = 0.01
				print '\n\tGet reply before %d retries, now reset timeout to: %.2f seconds' % (resend, local_delay) 
			resend = 0
			stay_under_max_delay = 0
			
			# process reply only if it's not duplicate one
			print '\n\tThe UNIQUE server reply is: ', repr(server_reply)
			repeat = False
			
		# save current ID for possible later use	
		previous_seq_num = seq_num	
			
else:
    print >>sys.stderr, '\n\tusage:-------my_UDP_Server_Client_Generator.py server [ <interface> ]'
    print >>sys.stderr, '\tor:-------my_UDP_Server_Client_Generator.py client <host>'
    sys.exit(2)
	
	
