#!/usr/bin/python3

#
#
# 9th Nov '19
#
# A simple python script to poll the status of a gateway & set LED's appropiately
# Uses the TTN url combined with the gateway ID
#
# Note: required modules:
# sudo apt-get install rpi.gpio
#
# Must be run as sudo (to control pins)
#
#

import RPi.GPIO as GPIO
import time
import json
from urllib.request import Request, urlopen
from urllib.error import URLError, HTTPError

#Define LED's
red_LED = 23
green_LED = 24

#Enter the gateway to monitor below
baseURL = 'http://noc.thethingsnetwork.org:8085/api/v2/gateways/eui-b827ebfffe87bd11'
gateway_timeout = 5 * 60    # Presume gateway not connected if this time exceeded
gateway_status = 0          # up = 1, down = 2, dont_know = 3

# How long to wait (in seconds) between checks (at least 30 sec?)
FREQUENCY_SECONDS = 90

#Setup pins
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(23,GPIO.OUT)
GPIO.setup(24,GPIO.OUT)

#start loop
while True:

    try:
        response = urlopen(baseURL)
    except HTTPError as e:
        print('The server couldn\'t fulfill the request.')
        print('Error code: ', e.code)
        # Gateway may be down but not certain.. set both LED's
        gateway_status = 3
    except URLError as e:
        print('We failed to reach the TTN server.')
        print('Reason: ', e.reason)
        #Presume gateway unable to reach network so indicate gateway down
        gateway_status = 2
    else:
        print('Success: ', response.status, response.reason)
        data = json.loads(response.read().decode("utf-8"))
        # Convert time to number & convert to seconds
        gateway_time = int(data['time']) / 1000000000
        print(gateway_time)
        tn = time.time()
        print(tn)
        print (tn - gateway_time)
        if ((tn - gateway_time) < gateway_timeout):
            gateway_status = 1
        else:
            gateway_status = 2

    if gateway_status == 1:
        # Up
        print ('Gateway up')
        GPIO.output(green_LED,GPIO.HIGH)
        GPIO.output(red_LED,GPIO.LOW)
        time.sleep(FREQUENCY_SECONDS)
    if gateway_status == 2:
        # Down
        print ('Gateway down')
        GPIO.output(green_LED,GPIO.LOW)
        # Flash red LED
        for n in range(0,(FREQUENCY_SECONDS * 2) ):
            GPIO.output(red_LED,GPIO.HIGH)
            time.sleep(0.5)
            GPIO.output(red_LED,GPIO.LOW)
            time.sleep(0.5)
    if gateway_status == 3:
        # Don't know
        print ('Gateway... don\'t know!')
        # Alterate LED's
        for n in range(0,(FREQUENCY_SECONDS * 2) ):
            GPIO.output(red_LED,GPIO.HIGH)
            GPIO.output(green_LED,GPIO.LOW)
            time. sleep(0.5)
            GPIO.output(red_LED,GPIO.LOW)
            GPIO.output(green_LED,GPIO.HIGH)
            time. sleep(0.5)
