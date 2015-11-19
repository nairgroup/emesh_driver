#Library imports
import time
import Adafruit_BMP.BMP085 as BMP085 #For use with the BMP185 pressure sensor
import RPi.GPIO as GPIO #For use with GPIO pins
from sht1x.Sht1x import Sht1x as SHT1x #For use with the SHT1x series of temperature sensors

#Setting GPIO mode
GPIO.setmode(GPIO.BCM)

#Defining save file name
savefile = "metobs.txt"

#Defining time for loop delay
dt = 5 #seconds

#Declaring counter variables to be global
#These are used for wind and rain
global rain_count
global windspd_count

#Variable initialization
rain_count = 0
#windspd_count = 0

#Setting pins to be used with each instrument
sht1x_datapin = 11 #GPIO number
sht1x_clkpin = 7 #GPIO number
rain_pin = 25 #GPIO number

#Defining interrupt function for the rain bucket
def rain_detect(channel):
	rain_count = rain_count + 1
	return
GPIO.setup(rain_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.add_event_detect(rain_pin, GPIO.FALLING, callback=rain_detect, bouncetime=500)

#windspd_pin = 23
#winddir_pin = 0 #This is an analog signal and needs to be run thorugh an A->D converter

#Defining interrupts for wind measurements
#GPIO.setup(windspd_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)

#def windspd_detection():
#	windspd_count = windspd_count + 1
#	return

#GPIO.add_event_detect(windspd_pin, GPIO.FALLING, callback=windspd_detection)

#Creating object for sht1x themperature sensor
sht1x = SHT1x(sht1x_datapin, sht1x_clkpin, SHT1x.GPIO_BCM)

#Creating file header
lun = open(savefile, 'w')
lun.write("Header")
lun.write("\n")
lun.close()


#-----------------BEGIN MAIN LOOP------------------------
while (1):
	time.sleep(dt) 
	#Reading from the BMP sensor
	bmp = BMP085.BMP085()
	bmp_temp = bmp.read_temperature()
	bmp_pres = bmp.read_pressure()
	
	print "bmp temp is: ", bmp_temp
	print "bmp pres is: ", bmp_pres
	
	#Reading from the SHT1x
	sht1x_temp = sht1x.read_temperature_C()
	sht1x_rh = sht1x.read_humidity()
	
	print "sht1x temp is: ", sht1x_temp
	print "sht1x rh is: ", sht1x_rh
	
	#Determining rain rate
	rain_rate = (rain_count*0.2/dt)*3600 #rain rate in mm/hr
	
	print "rain count is: ", rain_count
	print "rain rate is: ", rain_rate
	
	#Write to the data file
	lun = open(savefile, 'a')
	lun.write("I made a file!")
	lun.write("\n")
	lun.close()
	
#----------------------END MAIN LOOP------------------------
