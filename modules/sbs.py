#!/usr/bin/python
# Filename: sbs.py

import time
import sys
import pydb
import raspi
import subprocess
import re

REDPIN = 27
YELLOWPIN = 22
GREENPIN = 17
FILLVALVEPIN = 24
EMPTYVALVEPIN = 23

EMPTYVAL = 865
FULLVAL = 840

def fillBucket(pin):
    try:
        bucketFull = False
        while (bucketFull == False):
            andata = raspi.getAnalogData(int(pin),0)
            if (float(andata) > EMPTYVAL):
                changeLightStatus(GREENPIN)
                switchFillValve(0)
                print "EMPTY, filling... "+andata
            elif (float(andata) < FULLVAL):
                changeLightStatus(REDPIN)
                switchFillValve(1)
                print "FULL, stop filling! "+andata
                bucketFull = True
            else:
                changeLightStatus(YELLOWPIN)
                switchFillValve(0)
                print "Filling... "+andata
            time.sleep(1)
    except KeyboardInterrupt:
        switchFillValve(1)
        sys.exit(2)

def emptyBucket(pin):
    try:
        bucketEmpty = False
        while (bucketEmpty == False):
            andata = raspi.getAnalogData(int(pin),0)
            if (float(andata) > EMPTYVAL):
                changeLightStatus(GREENPIN)
                time.sleep(5)
                switchEmptyValve(1)
                print "EMPTY, waiting 10 seconds then closing valve!... "+andata
                bucketEmpty = True
            elif (float(andata) < FULLVAL):
                changeLightStatus(REDPIN)
                switchEmptyValve(0)
                print "FULL, Emptying! "+andata
            else:
                changeLightStatus(YELLOWPIN)
                switchEmptyValve(0)
                print "Emptying... "+andata
            time.sleep(1)
    except KeyboardInterrupt:
        switchEmptyValve(1)
        sys.exit(2)

def changeLightStatus(pinOn):
    # Turn all pins off
    pydb.runSQL("update `gpio`.`pinStatus` set pinStatus = '0' WHERE pinNumber = '"+str(REDPIN)+"';")
    pydb.runSQL("update `gpio`.`pinStatus` set pinStatus = '0' WHERE pinNumber = '"+str(YELLOWPIN)+"';")
    pydb.runSQL("update `gpio`.`pinStatus` set pinStatus = '0' WHERE pinNumber = '"+str(GREENPIN)+"';")

    # Turn on pin
    pydb.runSQL("update `gpio`.`pinStatus` set pinStatus = '1' WHERE pinNumber = '"+str(pinOn)+"';")

def switchFillValve(pinStatus):
    #pinStatus = 0 is open, pinStatus = 1 is closed
    pydb.runSQL("update `gpio`.`pinStatus` set pinStatus = '"+str(pinStatus)+"' WHERE pinNumber = '"+str(FILLVALVEPIN)+"';")

def switchEmptyValve(pinStatus):
    #print "running sql "+str(pinStatus)+"  "+str(EMPTYVALVEPIN)
    #pinStatus = 0 is open, pinStatus = 1 is closed
    pydb.runSQL("update `gpio`.`pinStatus` set pinStatus = '"+str(pinStatus)+"' WHERE pinNumber = '"+str(EMPTYVALVEPIN)+"';")

def getTempHumidity(pin):
   try:
      output = subprocess.check_output(["/root/sbs/exe/Adafruit_DHT", "11", str(pin)]);
      #print output
      matches = re.search("Temp =\s+([0-9.]+)", output)
      temp = float(matches.group(1))
      # conver from C to F
      ftemp = 9.0/5.0 * temp + 32
      # search for humidity printout
      matches = re.search("Hum =\s+([0-9.]+)", output)
      humidity = float(matches.group(1))
      return str(ftemp)+"|"+str(humidity)
   except Exception, err:
      return ""

def getTempHumidityLoop(pin):
    matches = ""
    try:
        while len(matches) <= 0:
           #print matches
           matches = getTempHumidity(pin)
    except Exception, err:
        print err
        sys.exit(1)

    ftemp = matches.split("|")[0]
    humidity = matches.split("|")[1]

    #print "Temperature: %.1f F" % ftemp
    #print "Humidity:    %.1f %%" % humidity
    return str(ftemp)+"|"+str(humidity)

def blinkLED(pin,st):
    pydb.runSQL("update `gpio`.`pinStatus` set pinStatus = '1' WHERE pinNumber = '"+str(pin)+"';")
    time.sleep(st)
    pydb.runSQL("update `gpio`.`pinStatus` set pinStatus = '0' WHERE pinNumber = '"+str(pin)+"';")
    time.sleep(st)
    return

def turnLEDOn(pin,st):
    pydb.runSQL("update `gpio`.`pinStatus` set pinStatus = '1' WHERE pinNumber = '"+str(pin)+"';")
    time.sleep(st)
    return

def turnLEDOff(pin,st):
    pydb.runSQL("update `gpio`.`pinStatus` set pinStatus = '0' WHERE pinNumber = '"+str(pin)+"';")
    time.sleep(st)
    return
