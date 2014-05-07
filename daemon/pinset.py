#!/usr/bin/env python
import time
import os
import subprocess
import RPi.GPIO as GPIO
import pydb
import sbs
import threading
import itertools

GPIO.setmode(GPIO.BCM)

while True:
    result = pydb.runSQL("SELECT * FROM sbs")
    for row in result:
        pinNumber = int(row['sbsFillPin'])
        pinStatus = True if int(row['sbsFillPinStatus']) == 1 else False
        GPIO.setup(pinNumber, GPIO.OUT)
        GPIO.output(pinNumber, pinStatus)

        pinNumber = int(row['sbsEmptyPin'])
        pinStatus = True if int(row['sbsEmptyPinStatus']) == 1 else False
        GPIO.setup(pinNumber, GPIO.OUT)
        GPIO.output(pinNumber, pinStatus)
    time.sleep(1)
