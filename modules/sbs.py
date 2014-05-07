#!/usr/bin/python
# Filename: sbs.py

import time
import sys
import pydb
import raspi
import subprocess
import re
import os
import glob
import numpy as np

REDPIN = 27
YELLOWPIN = 22
GREENPIN = 17
FILLVALVEPIN = 24
EMPTYVALVEPIN = 23

#EMPTYVAL = 865
EMPTYVAL = 790
#FULLVAL = 840
FULLVAL = 720

def read_temp_raw():
    base_dir = '/sys/bus/w1/devices/'
    device_folder = glob.glob(base_dir + '28*')[0]
    device_file = device_folder + '/w1_slave'
    catdata = subprocess.Popen(['cat',device_file], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    out,err = catdata.communicate()
    out_decode = out.decode('utf-8')
    lines = out_decode.split('\n')
    return lines

def read_temp():
    os.system('modprobe w1-gpio')
    os.system('modprobe w1-therm')

    lines = read_temp_raw()
    while lines[0].strip()[-3:] == 'YES':
        time.sleep(0.2)
        lines = read_temp_raw()
        equals_pos = lines[1].find('t=')
        if equals_pos != -1:
            temp_string = lines[1][equals_pos+2:]
            temp_c = float(temp_string) / 1000.0
            temp_f = temp_c * 9.0 / 5.0 + 32.0
            return str(temp_f)

def fillBucket(taskID):
    try:
        result = pydb.runSQL("SELECT * FROM task WHERE taskID = "+str(taskID)+" AND taskStatus = 2")
	sensorID = result[0]['taskSensorID']
	result = pydb.runSQL("SELECT * FROM sbs WHERE sbsID = "+str(sensorID))
        depthpin = result[0]['sbsDepthPin']
        bucketFull = False
        while (bucketFull == False):
            #andata = raspi.getAnalogData(int(depthpin),0)
	    result = pydb.runSQL("SELECT * FROM task WHERE taskID = "+str(taskID))
            taskStatus = result[0]['taskStatus']
	    val = 0
            arrayValues = []
            for x in range(0,5):
                val = raspi.getAnalogData(int(depthpin),0)
                arrayValues.append(int(val))
                time.sleep(.1)
                val = np.mean(arrayValues)

            andata = val

            if (float(andata) > EMPTYVAL):
                changeLightStatus(GREENPIN)
                switchFillValve(sensorID,0)
                print "EMPTY, filling... "+str(andata)
            elif (float(andata) < FULLVAL):
                changeLightStatus(REDPIN)
                pydb.runSQL("UPDATE task set taskStatus = '0', taskEndTime = NOW()  WHERE taskID = "+str(taskID))
                switchFillValve(sensorID,1)
                print "FULL, stop filling! "+str(andata)
                bucketFull = True
            elif (int(taskStatus) != 2):
                changeLightStatus(REDPIN)
                pydb.runSQL("UPDATE task set taskEndTime = NOW()  WHERE taskID = "+str(taskID))
                switchFillValve(sensorID,1)
                bucketFull = True
            else:
                changeLightStatus(YELLOWPIN)
                switchFillValve(sensorID,0)
                print "Filling... "+str(andata)
            time.sleep(1)
    except KeyboardInterrupt:
        switchFillValve(sensorID,1)
        sys.exit(2)

def emptyBucket(taskID):
    try:
        result = pydb.runSQL("SELECT * FROM task WHERE taskID = "+str(taskID)+" AND taskStatus = 2")
        sensorID = result[0]['taskSensorID']
        result = pydb.runSQL("SELECT * FROM sbs WHERE sbsID = "+str(sensorID))
        depthpin = result[0]['sbsDepthPin']
        print "depth pin: "+str(depthpin)
        bucketEmpty = False
        while (bucketEmpty == False):
            #andata = raspi.getAnalogData(int(depthpin),0)
            result = pydb.runSQL("SELECT * FROM task WHERE taskID = "+str(taskID))
            taskStatus = result[0]['taskStatus'] 
            val = 0
            arrayValues = []
            for x in range(0,5):
                val = raspi.getAnalogData(int(depthpin),0)
                arrayValues.append(int(val))
                time.sleep(.1)
                val = np.mean(arrayValues)

            andata = val

            if (float(andata) > EMPTYVAL):
		print "EMPTY, waiting 60 seconds then closing valve!... "+str(andata)
                changeLightStatus(GREENPIN)
                pydb.runSQL("UPDATE task set taskStatus = '0', taskEndTime = NOW() WHERE taskID = "+str(taskID))
                time.sleep(60)
                switchEmptyValve(sensorID,1)
                bucketEmpty = True
            elif (float(andata) < FULLVAL):
                changeLightStatus(REDPIN)
                switchEmptyValve(sensorID,0)
                print "FULL, Emptying! "+str(andata)
            elif (int(taskStatus) != 2):
                changeLightStatus(GREENPIN)
                pydb.runSQL("UPDATE task taskEndTime = NOW() WHERE taskID = "+str(taskID))
                switchEmptyValve(sensorID,1)
                bucketEmpty = True
            else:
                changeLightStatus(YELLOWPIN)
                switchEmptyValve(sensorID,0)
                print "Emptying... "+str(andata)
            time.sleep(1)
    except KeyboardInterrupt:
        switchEmptyValve(sensorID,1)
        sys.exit(2)

def changeLightStatus(pinOn):
    # Turn all pins off
    #pydb.runSQL("update `gpio`.`pinStatus` set pinStatus = '0' WHERE pinNumber = '"+str(REDPIN)+"';")
    #pydb.runSQL("update `gpio`.`pinStatus` set pinStatus = '0' WHERE pinNumber = '"+str(YELLOWPIN)+"';")
    #pydb.runSQL("update `gpio`.`pinStatus` set pinStatus = '0' WHERE pinNumber = '"+str(GREENPIN)+"';")
    raspi.setPin(int(REDPIN),0)
    raspi.setPin(int(YELLOWPIN),0)
    raspi.setPin(int(GREENPIN),0)

    # Turn on pin
    #pydb.runSQL("update `gpio`.`pinStatus` set pinStatus = '1' WHERE pinNumber = '"+str(pinOn)+"';")
    raspi.setPin(int(pinOn),1)

def switchFillValve(sensorID,pinStatus):
    #pinStatus = 0 is open, pinStatus = 1 is closed
    pydb.runSQL("update `sbs`.`sbs` set sbsFillPinStatus = '"+str(pinStatus)+"' WHERE sbsID = "+str(sensorID))
    #raspi.setPin(int(FILLVALVEPIN),int(pinStatus))

def switchEmptyValve(sensorID,pinStatus):
    #print "running sql "+str(pinStatus)+"  "+str(EMPTYVALVEPIN)
    #pinStatus = 0 is open, pinStatus = 1 is closed
    pydb.runSQL("update `sbs`.`sbs` set sbsEmptyPinStatus = '"+str(pinStatus)+"' WHERE sbsID = "+str(sensorID))
    #raspi.setPin(int(EMPTYVALVEPIN),int(pinStatus))

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
