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
#global windspd_count

#Variable initialization
rain_count = 0
#windspd_count = 0

#Setting pins to be used with each instrument
sht1x_datapin = 11 #GPIO number
sht1x_clkpin = 7 #GPIO number
rain_pin = 25 #GPIO number

#Defining interrupt function for the rain bucket
def rain_detect(channel):
	global rain_count
	rain_count = rain_count + 1
	return
GPIO.setup(rain_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.add_event_detect(rain_pin, GPIO.FALLING, callback=rain_detect, bouncetime=500)

#windspd_pin = 23
#winddir_pin = 0 #This is an analog signal and needs to be run thorugh an A->D converter

#Defining interrupts for wind measurements
#GPIO.setup(windspd_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)

#def windspd_detection():
#	global windspd_count = windspd_count + 1
#	return

#GPIO.add_event_detect(windspd_pin, GPIO.FALLING, callback=windspd_detection)

#Creating object for sht1x themperature sensor
sht1x = SHT1x(sht1x_datapin, sht1x_clkpin, SHT1x.GPIO_BCM)

#Creating file header
lun = open(savefile, 'w')
lun.write("Year", "\t", "Julian Day", "Hour", "\t", "Minute", "\t", "Second", "\t", 
	"Temp1 (K)", "Temp2 (K)", "\t", "Pressure (hPa)", "\t", "RH (%)", "\t",
	"WindDir (V)", "\t", "WindSpd", "\t", "Rain Rate (mm/hr)", "\t",
	"Year", "\t", "Julian Day", "\t", "Hour", "\t", "Minute", "\t", "Second")
lun.write("\n")
lun.close()


#-----------------BEGIN MAIN LOOP------------------------
while (1):
	time.sleep(dt)
	
	#Time of sensor read start
	year1 = time.strftime("%Y")
	day1 = time.strftime("%j")
	h1 = time.strftime("%H")
	m1 = time.strftime("%M")
	s1 = time.strftime("%S")
	
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
	
	#Determining Wind Speed and Wind Direction
	wind_dir = float('NaN')
	wind_spd = float('NaN')
	
	#Determining rain rate
	rain_rate = (rain_count*0.2/dt)*3600 #rain rate in mm/hr
	
	print "rain count is: ", rain_count
	print "rain rate is: ", rain_rate
	
	rain_count = 0
	
	
	#Time of sensor read end
	year2 = time.strftime("%Y")
	day2 = time.strftime("%j")
	h2 = time.strftime("%H")
	m2 = time.strftime("%M")
	s2 = time.strftime("%S")
	
	
	#Write to the data file
	lun = open(savefile, 'a')
	lun.write(year1, day1, h1, m1, s1, sht1x_temp, bmp_temp, bmp_pres, sht1x_rh,
		wind_dir, wind_spd, rain_rate, year2, day2, h2, m2, s2))
	lun.write("\n")
	lun.close()
	
#----------------------END MAIN LOOP------------------------
