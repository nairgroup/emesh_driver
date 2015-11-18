#Library imports
import Adafruit_BMP.BMP085 as BMP085 #For use with the BMP185 pressure sensor
import RPi.GPIO as GPIO #For use with GPIO pins
import sht1x.Sht1x as SHT1x #For use with the SHT1x series of temperature sensors
#from AM2315 import AM2315 #For use with am2315 temperature sensor

#Setting GPIO mode
GPIO.setmode(GPIO.BCM)

#Defining save file name
savefile = "metobs.txt"

#Setting pins to be used with each instrument
sht1x_datapin = 11
sht1x_clkpin = 7

windspd_pin = 23
#winddir_pin = 0 #This is an analog signal and needs to be run thorugh an A->D converter


#Variable initialization
windspd_count = 0

#Defining interrupts for wind measurements
GPIO.setup(windspd_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)

def windspd_detection():
	windspd_count = windspd_count + 1
	
GPIO.add_event_detect(windspd_pin, GPIO.FALLING, callback=windspd_detection)
#-----------------BEGIN MAIN LOOP------------------------
while (1):
	
	#Reading from the BMP sensor
	bmp = BMP085.BMP085()
	bmp_temp = bmp.read_temperature()
	bmp_pres = bmp.read_pressure()
	
	print "bmp temp is: ", bmp_temp
	print "bmp pres is: ", bmp_pres
	
	#Reading from the AM2315
	
	
	#Reading from the SHT1x
	sht1x=SHT1x(sht1x_datapin, sht1x_clkpin, SHT1x.GPIO_BCM)
	
	sht1x_temp = sht1x.read_temperature_C()
	sht1x_rh = sht1x.read_humidity()
	
	#Write to the data file
	lun = open(savefile, 'w')
	lun.write("I made a file!")
	lun.close()
	
#----------------------END MAIN LOOP------------------------
