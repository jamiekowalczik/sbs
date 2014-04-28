#!/usr/bin/env python
import time
import sys
import getopt
import os
import RPi.GPIO as GPIO
import pydb
import raspi
import sbs

GPIO.setwarnings(False)

def main(argv):
    try:
        opts, args = getopt.getopt(sys.argv[1:],"h",["help"])
    except getopt.GetoptError, err:
        #print "Error parsing options "
	print err
        sys.exit(1)

    for opt, arg in opts:
        if opt == "-h":
            print ""
	    print ""
            sys.exit(0)

    temphumid = sbs.getTempHumidityLoop(4)
    temp = temphumid.split("|")[0]
    humid = temphumid.split("|")[1]

    solar = raspi.getAnalogData(1,0)

    imgtime = time.strftime("%Y-%m-%d_%H_%M_%S")
    #os.system("wget -q -O /var/www/images/garden/"+imgtime+".jpg --user=myadminuseraccount --password=myadminuseraccountspassword http://mycameraipaddressorhostname/img/snapshot.cgi")
    
    depth = raspi.getAnalogData(0,0)
    buckettemp = sbs.read_temp()

    print "Time:",imgtime 
    print "Humidity:",humid
    print "Temperature:",temp
    print "Solar:",solar
    print "Bucket Depth:",depth
    print "Bucket Temperature:",buckettemp
    #logsql(str(temp),str(humid),solar,imgtime)

def logsql(temp,humid,solar,imgtime):
    pydb.runSQL("insert into `gpio`.`weather` (`temp`,`humid`,`solar`,`imgtime`,`timestamp`) values ('"+temp+"','"+humid+"','"+solar+"','"+imgtime+"','"+time.strftime("%Y-%m-%d %H:%M:%S")+"');")

if __name__ == "__main__":
    main(sys.argv[1:])
