#import sys
#import requests       #to use emoncms
from RPi import GPIO
#import math
#import string
from time import sleep
from Adafruit_ADS1x15 import ADS1115

class SoilMoisture:
    status = ""
    res_dict = {2/3: 6144, 1: 4096, 2: 2048, 4: 1024, 16: 256}
    
    def __init__(self):
        self.status = "Initializing"
        # Choose a gain of 1 for reading voltages from 0 to 4.09V.
        # Or pick a different gain to change the range of voltages that are read:
        #  - 2/3 = +/-6.144V
        #  -   1 = +/-4.096V
        #  -   2 = +/-2.048V
        #  -   4 = +/-1.024V
        #  -   8 = +/-0.512V
        #  -  16 = +/-0.256V
        # See table 3 in the ADS1015/ADS1115 datasheet for more info on gain.
        
        # Hygromter powerd by a GPIO line -> 3.3 
        # The ADC will be powered at 3.3 Vcc so it requires 1 to be precise
        self.gain = 1
        
        #Resolution is 16 bits so 2^16 = 65536
        #self.resolution = 65536
        #self.resmin =  -32768
        #self.resmax = 32767
        #self.gainV = 6.144
        
        #Compute resolution in volts according to gain
        self.resolution = self.res_dict[self.gain] / 32768 / 1000
        self.channel = 0
        
        #frequency. Not used for the moment
        self.data_rate = None  # 250 samples per second <- it was here

        #self.device = 0x01 #16-bit ADC ADS1115
        self.adc = ADS1115()

        #dry run
        self.raw = 0
        self.min = 0
        self.max = 0
        self.volts = 0
        
        #Configure GPIO mode and channels
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(18, GPIO.OUT, initial=GPIO.LOW)
        
        
        self.readCalibration()
        self.readData()
        
        self.status = "Idle"

    def readData(self):
        self.status = "Reading"
        #Power on the hygrometer
        #GPIO.output(18, GPIO.HIGH)
        #sleep(0.5)
        #Get the raw adc value
        self.raw = self.adc.read_adc(self.channel, gain=self.gain)
        #Power off the hygrometer
        #GPIO.output(18, GPIO.LOW)
        
        #self.volts = (self.raw * self.gainV) / self.resmax 
        self.volts = self.raw * self.resolution
        self.status = "Idle"
        return self.volts

    def calibMax(self, iterations, delay):
        self.status = "Calibrating MAX"
        sleep(delay)
        self.max = 0
        
        for i in range(1,iterations + 1):
            value = self.readData()
            print("[%02d] - %.3f"  % (i, value)) 
            #print "."
            self.max = self.max + value
            sleep(1)

        self.max = self.max / iterations
        self.status = "Idle"
        return self.max

    def calibMin(self, iterations, delay):
        self.status = "Calibrating MIN"
        sleep(delay)
        self.min = 0
        
        for i in range(1,iterations + 1):
            value = self.readData()
            print ("[%02d] - %.3f" % (i, value))
            #print "."
            self.min = self.min + value
            sleep(1)

        self.min = self.min / iterations
        self.status = "Idle"
        return self.min

    def getMax(self):
        return self.max

    def getMin(self):
        return self.min
    
    def getPerc(self):
        perc = ((self.volts - self.min)/(self.max - self.min))*100
        return 100 - perc
    
    def setCalibration(self, minV, maxV):
        self.min = minV
        self.max = maxV
        self.writeCalibration()
        

    def writeCalibration(self):
        # Write calibration file.
        out_file = open("calib.txt","w")
        out_file.write("%.3f,%.3f\n" %(self.min, self.max))
        out_file.close()

    def readCalibration(self):
        # Read calibration file.
        try:
            in_file = open("calib.txt","r")
            values = in_file.read().split(",")
            self.min = float(values[0])
            self.max = float(values[1])
            #print("%.3f %.3f" % (self.min, self.max))
            in_file.close()
        except(IOError):
            print("Calibration file deosn't exists")
            return False

        return True
    
    def cleanup(self):
        print("Cleaning up GPIO")
        GPIO.output(18, GPIO.LOW)
        GPIO.cleanup()
#hydro = SoilMoisture()    
#hydro.readCalibration()
#for i in range(30):
#    print(hydro.readData())
#    sleep(1)

