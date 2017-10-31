'''
Created on 17 set 2017

@author: willy
'''

import socket
from .soilmoisture import SoilMoisture

class MoisturePiServer(object):
    '''
    classdocs
    '''

    def __init__(self, address = "0.0.0.0", port = 6000):
        self.hydro = SoilMoisture()
        self.address = (address, port)
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        
    def start(self):
        self.sock.bind(self.address)
        print("Listening on " + str(self.address))

        while True:
            try:
                (payload, client_address) = self.sock.recvfrom(1024)
                command = str(payload, "UTF8")
            
                print("Data received: [" + str(len(command)) + "] " + 
                    command + " from " + str(client_address))
            
                resp = self.parse(command)
                self.sock.sendto(bytes  (resp, "UTF8"), client_address)
            except KeyboardInterrupt:
                return
    
    def parse(self, command):
        req = str(command).upper()
        if (req == "RAW?"):
            resp = str(self.hydro.readData())
        elif (req == "PERC?"):
            resp = str(self.hydro.getPerc())
        elif (req == "MIN?"):
            resp = str(self.hydro.getMin())
        elif(req == "MAX?"):
            resp = str(self.hydro.getMax())
        else:
            resp = "UNKNOWN REQUEST " + req
            print("Unrecognized command ", req)
        
        print(resp)
        return resp
    
    def stop(self):
        self.hydro.cleanup()
        self.sock.close()
        
