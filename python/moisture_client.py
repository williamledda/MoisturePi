'''
Created on 17 set 2017

@author: willy
'''
import socket
import sys

if __name__ == '__main__':
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
    
    if(MESSAGE == "RAW?" or MESSAGE == "PERC?"):
        print("{:.2f}".format(float(payload)))
    else:
        print("Response: ", str(payload, "UTF8"))
    exit()
    