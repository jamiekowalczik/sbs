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
    result = pydb.runSQL("SELECT * FROM task WHERE taskStatus = 1");
    for row in result:
        if (str(row['taskName']) == "Empty"):
            print "Empty Bucket"
            pydb.runSQL("UPDATE task set taskStatus = '2' WHERE taskID = "+str(row['taskID']))
            sbs.emptyBucket(row['taskID'])
        if (str(row['taskName']) == "Fill"):
            print "Fill Bucket"
            pydb.runSQL("UPDATE task set taskStatus = '2' WHERE taskID = "+str(row['taskID']))
            sbs.fillBucket(row['taskID'])
    time.sleep(1)

