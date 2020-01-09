'''
*********description*********
this python program implement most functionality similar to the Netcat using multi-thread 
worker, including file upload, command execution remotely,  reverse back door shell, 
I plan to add some more robust features in the future,such as disable OS firewall rule, 
terminate anti-virus process.....
'''

import sys
import socket
import getopt
import threading
import subprocess

# these global used to record command-line option specified by users
listen			    = False
command			    = False
upload			    = False
execute			    = ""
PyNetCat_server 	= ""
upload_file_path 	= ""
server_port         = 0


def print_usage():
	
  	sys.exit(0)
	

def main():
	
	global listen
	global server_port
	global execute
	global command
	global upload_file_path
	global PyNetCat_server
	
	print "[*********] NetCat rewrite with Python [**************]"
	
	# sys.argv[0] = PyNetcat_Utility_Knife.py
	# sys.argv[1] =
	# sys.argv[2] = 
	if not len(sys.argv[1:]):
		print_usage()
	
	try:
		opts, args = getopt.getopt(sys.argv[1:], "hle:P:p:cu",\
			["help", "listen", "execute", "target", "port", "command", "upload"])
	except getopt.GetoptError as err:
		print str(err)
		print_usage()
	
	# here, "o" is command-line option (i.e., specify by user as -u or --upload), 
	#       "a" its value (i.e., specify by user as c:\\target.exe)
	# however, some option did not require associated value, so we just switch global status
	for o, a in opts:
		if o in ("-h", "--help"):
			print_usage()
		elif o in ("-l", "--listen"):
			listen  = True
		elif o in ("-e", "--execute")"
			execute = a
		elif o in ("-c", "--commandshell"):
			command = True
		elif o in ("-u", "--upload"):
			upload_file_path = a
		elif o in ("-t", "--target"):
			PyNetCat_server = a
		elif o in ("-p", "--port"):
			server_port = int(a)
		else:
			assert False, "Fail To Parsing Option, please check your typo"
			
	# running an PyNetCat client mode
	if not listen and len(target) and server_port > 0:
		
		# block to waiting user input until hit a new line, then send it to PyNetCat server
		buffer = sys.stdin.read()
		send_to_server(buffer)

	if listen:
		server_loop()
	
main()		


def send_to_server(buffer):
	
	client_side = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	
	try:
		client_side.connect((PyNetCat_server, server_port))
		if len(buffer):
			client_side.send(buffer)
		
		# read user input -> send to PyNetCat server -> receive and print response -> read user input .......repeat forever
		while True:
			
			recv_len = 1
			response = ""
			
			while recv_len:
				data = client_side.recv(4096)
				recv_len = len(data)
				response += data
				
				if recv_len < 4096:
					break
				
			print response,
			
			buffer = raw_input("")
			buffer += "\n"
			
			client_side.send(buffer)
			
	except:
		print "[***]Exception ! Exiting....."
		client_side.close()
	
	
def server_loop():
	
	
