#!/usr/bin/env python
import os
import subprocess
import time
import RPi.GPIO as GPIO
import MySQLdb
import pydb

GPIO.setwarnings(False)

GPIO.setmode(GPIO.BCM)

while True:
    result = pydb.runSQL("select * from pinStatus where pinGroup = 'sbs' AND pinID < 90")
    for row in result:
        pinNumber = int(row[1])
        pinStatus = True if int(row[2]) == 1 else False
        GPIO.setup(pinNumber, GPIO.OUT)
        GPIO.output(pinNumber, pinStatus)
    time.sleep(.5)
##############
