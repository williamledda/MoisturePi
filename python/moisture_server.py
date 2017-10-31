'''
Created on 29 ott 2017

@author: willy
'''

from MoisturePi import MoisturePiServer

if __name__ == '__main__':
    server = MoisturePiServer()
    server.start()
    pass
    server.stop()
    exit()