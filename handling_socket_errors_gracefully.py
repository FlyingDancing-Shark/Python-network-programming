'''
*********description*********
this is use as a client socket creation and connection (to server) error handling framework, 
we add try-except block in each of socket operation processes, you can use these  in your application logic
'''

import sys
import socket
import argparse

def main():
	
	parser = argparse.ArgumentParser(description='Elegant Socket Error Handling')
	parser.add_argument('--host', action="store", dest="host", required=False)
	parser.add_argument('--port', action="store", dest="port", type=int, required=False)
	parser.add_argument('--remotefile', action="store", dest="remotefile", required=False)
	given_args = parser.parse_args()
	
	host = given_args.host
	port = given_args.port
	remotefile = given_args.remotefile
	
	# we can alternatively wrap all these four "try-except" blocks into one,  
	# and repeatedly wait user input then send it to server, 
	# see another version "single_error_handling_of_socket.py"
	try:
		client_S = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	except socket.error, err:
		print "Fail to create socket:  %s" % err
		sys.exit(1)
	
	# by default, this will block our Python program until OS establish a connection
	# with remote server, we can set timeout (blocking until our specified time) 
	# then handling "socket.timeout" exception
	try:
		client_S.connect((host, port))
	except socket.gaierror, err:
		print "Address-related problem occur when connect to server:  %s" % err
		sys.exit(1)
	except socket.error, err:
		print "Fail to connecting to server:  %s" % err
		sys.exit(1)
		
	try:
		client_S.sendall("GET %s HTTP/1.0\r\n\r\n" % remotefile)
	except socket.error, err:
		print "Fail to sending data:  %s" % err
		sys.exit(1)
		
	while True:
		try:
			buffer = client_S.recv(2048)
		except socket.error, err:
			print "Fail to receiving data:  %s" % err
			sys.exit(1)
			
		if not len(buffer):
			break
		
		sys.stdout.write(buffer)
		
	
main()
	
	
