'''
Created on 17 set 2017

@author: willy
'''
import socket
import time
import sys

#UDP_IP = "127.0.0.1"
#UDP_PORT = 6000
#MESSAGE = "RAW?"

UDP_IP = sys.argv[1]
UDP_PORT = int(sys.argv[2])
MESSAGE = sys.argv[3]

#print("UDP target IP:", UDP_IP)
#print("UDP target port:", UDP_PORT)
#print("message:", MESSAGE)

sock = socket.socket(socket.AF_INET, # Internet
                     socket.SOCK_DGRAM) # UDP

sock.settimeout(5)

sock.sendto(bytes(MESSAGE, "UTF8"), (UDP_IP, UDP_PORT))
(payload, remote) = sock.recvfrom(1024)
print("{:.2f}".format(float(payload)))