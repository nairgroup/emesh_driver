#This routine is to be used on a Raspberry Pi to
#gather observational data from an Arduino via the I2C bus

#++++++++++++++++++++++++++++++++++++++++++++++++++++++
#List of I2C write values and what they return
#++++++++++++++++++++++++++++++++++++++++++++++++++++++
# 1 - Returns Temperature from the BMP sensor
# 2 - Returns Temperature from the SHT1X Sensor
# 3 - Returns Relative Humidity from the SHT1X Sensor
# 4 - Returns Pressure from the BMP Sensor
# 5 - Returns Wind Direction from the Anemometer
# 6 - Returns Wind Speed from the Anemometer
# 7 - Returns Rain from the Tipping Rain Gauge
# 8 - Returns the Time from the Arduino's Clock Chip
#++++++++++++++++++++++++++++++++++++++++++++++++++++++
#++++++++++++++++++++++++++++++++++++++++++++++++++++++

#Importing necessary modules
import numpy
import smbus
import time
import RPi.GPIO as GPIO

#Defining GPIO parameters
GPIO.setmode(GPIO.BOARD)
GPIO.setup(7, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

#Defining I2C parameters
bus = smbus.SMBus(1)
arduino_address = 0x04

#I2C functions
def write_signal(obsv):
	bus.write_byte(arduino_address, obsv)
	return -1
	
def read_signal():
	value = bus.read_byte(arduino_address)
	return value

#Getting observations
def pull_obs(obsv):
	write_signal(obsv)
	nels = read_signal()
	data_bytes = numpy.zeros(nels)
	
	#Setting number of bytes in a single value
	if obsv == 1:
		nbytes = 2
	
	#Reading data bytes from arduino
	for i in range(nels):
		data_bytes[i] = read_signal()
	
	#Recombining bytes into values
	data = numpy.zeros(nels/nbytes)
	for i in range(len(data)):
		data[i] = (float(data_bytes[i*2])
			+float(data_bytes[i*2+1]/100.0)
	print(data)
	return data

#Telling R. Pi to wait for Arduino's signal before pulling obs
try:
	GPIO.wait_for_edge(7, GPIO.RISING)
	bmptmp_bytes = pull_obs(1)
	print(bmptmp_bytes)
	
	
	#Write observations to files
	
except KeyboardInterrupt:
	GPIO.cleanup()
	
GPIO.cleanup
