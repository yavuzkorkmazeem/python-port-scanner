#!/bin/python3

import sys #allows us to enter command line argument ,among other things
import socket 
from datetime import datetime

#define our target
if len(sys.argv) == 2:
	target = socket.gethostbyname(sys.argv[1]) #translate a host name to IPV4
else:
	print("Invalid amount of arguments.")
	print("syntax : python3 scanner.py <ip>")
	sys.exit()

#add a pretty banner
print ("-"*50)
print("scanning target"+target)
print("Time started: "+str(datetime.now()))	
print("-"*50)

try:
	for port in range(50,85):
		s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)	
		socket.setdefaulttimeout(1) #is a float
		result = s.connect_ex((target,port)) #returns error indicator
		print("port {} is being checked".format(port))
		if result ==0:
			print("port {} is open".format(port))
			s.close()
except KeyboardInterrupt :
	print('\n exiting from the program')
	sys.exit()

except socket.gaierror :
	print("the host couldn't be resolved")
	sys.exit()
	
except socket.error :
	print("couldn't connect to the server")
	sys.exit()
