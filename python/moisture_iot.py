'''
Created on 09 ago 2018

@author: william
'''

import sys
import requests
from time import sleep
from MoisturePi import SoilMoisture

if __name__ == '__main__':
    W_KEY = "5K6C8VV7KW7731CH"
    W_URL="https://api.thingspeak.com/update.json"
    R_KEY="HJY1S44I876R5FOE"
    R_URL="https://api.thingspeak.com/channels/554823/feeds.json"
    
    if(sys.argv[1] == "write"):
        moisture = SoilMoisture()
        moisture.readCalibration()
        
        try:
            while True:
                #GET https://api.thingspeak.com/update?api_key=5K6C8VV7KW7731CH&field1=0
                print("Sending data...")
                r = requests.get(W_URL, params={"api_key": W_KEY, "field1": moisture.readData(), "field2": moisture.getPerc()})
            
                print("Result: ", r.status_code)
                
                if r.status_code != 200:
                    print("Error: ", r.status_code)
            
                data = r.json()
                print(r.text)
                print(data["channel_id"], " - ", data["field1"], " - ", data["field2"])
                sleep(15.0)
                #print(data["field1"])
                #print(data["field2"])
        except KeyboardInterrupt:
            print("Done")
            moisture.cleanup()
            exit()
            
    elif(sys.argv[1] == "read"):
        #GET https://api.thingspeak.com/channels/554823/feeds.json?api_key=HJY1S44I876R5FOE&results=2
        r = requests.get(R_URL, params={"api_key": R_KEY, "results": 1})
        
        if r.status_code != 200:
            print("Error: ", r.status_code)
        
        data = r.json()
        #print(r.text)
        print(data["channel"]["id"], " - ", data["feeds"][0]["field1"], " - ", data["feeds"][0]["field2"])
