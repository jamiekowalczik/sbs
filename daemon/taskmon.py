#!/usr/bin/env python
import time
import os
import subprocess
import RPi.GPIO as GPIO
import pydb
import sbs

GPIO.setmode(GPIO.BCM)

FILLBUCKETID = 99 
EMPTYBUCKETID = 98 

while True:
    result = pydb.runSQL("select * from pinStatus where pinGroup = 'sbs' and pinNumber > 90 and pinStatus = 1");
    for row in result:
        if (int(row[1]) == EMPTYBUCKETID and int(row[2]) == 1):
           print "Empty Bucket"
           pydb.runSQL("update `gpio`.`pinStatus` set pinStatus = '0' WHERE pinNumber = '"+str(EMPTYBUCKETID)+"';")
	   sbs.emptyBucket(0)
        if (int(row[1]) == FILLBUCKETID and int(row[2]) == 1):
           print "Fill Bucket"
           pydb.runSQL("update `gpio`.`pinStatus` set pinStatus = '0' WHERE pinNumber = '"+str(FILLBUCKETID)+"';")
	   sbs.fillBucket(0)
    time.sleep(1)
##############