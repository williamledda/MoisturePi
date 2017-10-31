'''
Created on 20 ago 2017

@author: willy
'''
from sys import exit
from time import sleep
from MoisturePi import SoilMoisture

if __name__ == '__main__':
    hydro = SoilMoisture()
    
    hydro.readCalibration()
    
    while True:
        try:
            print(hydro.readData())
            sleep(1)
        except KeyboardInterrupt:
            print("Done")
            hydro.cleanup()
            exit()