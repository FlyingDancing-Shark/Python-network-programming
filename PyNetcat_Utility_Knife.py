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
PyNetCat_server = ""
upload_file_path = ""
port            = 0


def usage():
	print "[*********] NetCat rewrite with Python [**************]"
  	
