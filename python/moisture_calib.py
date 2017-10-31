'''
Created on 20 ago 2017

@author: willy
'''
from MoisturePi import SoilMoisture

if __name__ == '__main__':
    hydro = SoilMoisture()
    print("Starting Max calibration...")
    hydro.calibMax(10, 10)
    print("Starting Min calibration...")
    hydro.calibMin(10, 20)
    print("Calibration completed. Writing values...")
    hydro.writeCalibration()
    
    hydro.cleanup()
