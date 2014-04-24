#!/usr/bin/python
# Filename: raspi.py

import RPi.GPIO as GPIO

GPIO.setwarnings(False)

def getAnalogData(pin, DEBUG):
    GPIO.setmode(GPIO.BCM)
    try:
        # change these as desired - they're the pins connected from the
        # SPI port on the ADC to the Cobbler
        #SPICLK = 18
        SPICLK = 11
        #SPIMISO = 23
        SPIMISO = 9
        #SPIMOSI = 24
        SPIMOSI = 10
        #SPICS = 25
        SPICS = 8

        # set up the SPI interface pins
        GPIO.setup(SPIMOSI, GPIO.OUT)
        GPIO.setup(SPIMISO, GPIO.IN)
        GPIO.setup(SPICLK, GPIO.OUT)
        GPIO.setup(SPICS, GPIO.OUT)

        sensor_adc = pin;

        # read the analog pin
        trim_sensval = readadc(sensor_adc, SPICLK, SPIMOSI, SPIMISO, SPICS)

        if DEBUG:
            print "trim_sensval:", trim_sensval
        return str(trim_sensval)
        sens_val = trim_sensval / 10.24     # convert 10bit adc0 (0-1024) trim pot read into 0-100 volume level
        sens_val = round(sens_val)          # round out decimal value
        sens_val = int(sens_val)            # cast volume as integer

        #print str(sens_val)
        return str(sens_val)

        if DEBUG:
            print "sens_val", sens_val
    except Exception, err:
        print err
        sys.exit(1)

# read SPI data from MCP3008 chip, 8 possible adc's (0 thru 7)
def readadc(adcnum, clockpin, mosipin, misopin, cspin):
    GPIO.setmode(GPIO.BCM)
    try:
        if ((adcnum > 7) or (adcnum < 0)):
                return -1
        GPIO.output(cspin, True)

        GPIO.output(clockpin, False)  # start clock low
        GPIO.output(cspin, False)     # bring CS low

        commandout = adcnum
        commandout |= 0x18  # start bit + single-ended bit
        commandout <<= 3    # we only need to send 5 bits here
        for i in range(5):
                if (commandout & 0x80):
                        GPIO.output(mosipin, True)
                else:
                        GPIO.output(mosipin, False)
                commandout <<= 1
                GPIO.output(clockpin, True)
                GPIO.output(clockpin, False)

        adcout = 0
        # read in one empty bit, one null bit and 10 ADC bits
        for i in range(12):
                GPIO.output(clockpin, True)
                GPIO.output(clockpin, False)
                adcout <<= 1
                if (GPIO.input(misopin)):
                        adcout |= 0x1

        GPIO.output(cspin, True)

        adcout >>= 1       # first bit is 'null' so drop it
        return adcout
    except Exception, err:
	print err
	sys.exit(1)

