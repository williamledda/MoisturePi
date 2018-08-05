#!/bin/sh
cd /home/pi/MoisturePi/python;

#Uncomment the following line to activate virtualenv when used
. /home/pi/MoisturePi-env/bin/activate;
python3 ./moisture_server.py

#Uncomment the following line to deactivate virtualenv when used
deactivate

