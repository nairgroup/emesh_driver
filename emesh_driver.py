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
#This sets the temporal resolution of the measurements
dt = 5 #seconds

#Declaring counter variables to be global
#These are used for wind and rain
global rain_count
global windspd_count
global anem #For determining whether first or second anemoter rotation in a cycle
global vane #For determining whether wind vane has reutrned a signal in the current anenometer cycle
global wst1 #anemometer first detection time
global wst2 #anemomter second detection time
global wdt #Wind vane detection time

#Variable initialization
rain_count = 0
windspd_count = 0
dir_time = float('nan') #Cannot initialize to zero because 0 corresponds to a direction
a = 0
v = 0
wst1 = 0
wst2 = 0
wdt = 0

#Setting pins to be used with each instrument
sht1x_datapin = 19 #GPIO number
sht1x_clkpin = 26 #GPIO number
rain_pin = 25 #GPIO number
windspd_pin = 23 #GPIO number
winddir_pin = 24 #GPIO number

#Defining interrupt function for the rain bucket
def rain_detect(channel):
	global rain_count
	rain_count = rain_count + 1
	return

#Defining interrupt function for anemomter
def windspd_detect(channel):
	global windspd_count
	global anem
	global vane
	global wst1
	global wst2
	windspd_count +=1
	if anem and vane:
		wst2 = time.time()
		anem = 0
		vane = 0
	else:
		anem = 1
		wst1 = time.time()
		
def winddir_detect(channel):
	global vane
	global wdt
	wdt = time.time()
	if anem:
		vane = 1
	
	

GPIO.setup(rain_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.add_event_detect(rain_pin, GPIO.FALLING, callback=rain_detect, bouncetime=500)

GPIO.setup(windspd_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.add_event_detect(windspd_pin, GPIO.FALLING, callback=windspd_detect, bouncetime=10)

GPIO.setup(winddir_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.add_event_detect(winddir_pin, GPIO.RISING, callback=winddir_detect, bouncetime=10)


#Creating object for sht1x themperature sensor
sht1x = SHT1x(sht1x_datapin, sht1x_clkpin, SHT1x.GPIO_BCM)

#Creating file header
lun = open(savefile, 'w')
lun.write("Year \t Julian Day \t Hour \t Minute \t \Second \t Temp1 (K) \t Temp2 (K) \t Pressure (hPa) \t RH (%) \t" \
	"Wind Direction (V) \t Wind Speed (m/s) \t Rain Rate (mm/hr) \t Year \t Julian Day \t Hour \t Minute \t Second \n")
lun.close()


#-----------------BEGIN MAIN LOOP------------------------
try:

	while (1):
		
		#Wind Calculations
		#dir_time calculation is in the if statements to prevent it from running in calm conditions
		wrps = windspd_count/dt #Should change dt to a value based on the actual loop runtime
		if (wrps >= 0.010) and (wrps < 3.229 ):
			wind_spd = (-0.1095*wrps**2 +2.9318*wrps-0.1412)*0.48037
			dir_time = (wtd-wts1)/(wts2-wts1)
		elif (wrps >= 3.230) and (wrps < 54.362):
			wind_spd = (0.0052*wrps**2+2.1980*wrps+1.1091)*0.48037
			dir_time = (wtd-wts1)/(wts2-wts1)
		elif (wrps >= 54.362) and (wrps < 66.332):
			wind_spd = (0.1104*wrps**2-9.5685*wrps+329.87)*0.48037
			dir_time = (wtd-wts1)/(wts2-wts1)
		elif (wrps >= 66.332):
			wind_spd = 999 #Most likely a tornado
			dir_time = (wtd-wts1)/(wts2-wts1)
		elif (windspd_count < 0.010):
			wind_spd = 0
		else:
			wind_spd = float('nan')
			
		#Resetting variables used in wind calculations
		windspd_count = 0 #Revolutions of anemometer
		
		#Calculating wind direction
		wind_dir = dir_time #Need the real function
			
	
		#Time of sensor read start
		year1 = time.strftime("%Y")
		day1 = time.strftime("%j")
		h1 = time.strftime("%H")
		m1 = time.strftime("%M")
		s1 = time.strftime("%S")
	
		#Reading from the BMP sensor
		bmp = BMP085.BMP085()
		bmp_temp = bmp.read_temperature()+273.15
		bmp_pres = float(bmp.read_pressure())/100.0
	
		#print "bmp temp is: ", bmp_temp
		#print "bmp pres is: ", bmp_pres
		
		#Reading from the SHT1x
		sht1x_temp = sht1x.read_temperature_C()+273.15
		sht1x_rh = sht1x.read_humidity()
		
		#print "sht1x temp is: ", sht1x_temp
		#print "sht1x rh is: ", sht1x_rh
		
		#Determining rain rate
		rain_rate = (rain_count*0.2/dt)*3600 #rain rate in mm/hr
		
		#print "rain count is: ", rain_count
		#print "rain rate is: ", rain_rate
		rain_count = 0 #Reseting rain count for next measurement period
		
		
		#Time of sensor read end
		year2 = time.strftime("%Y")
		day2 = time.strftime("%j")
		h2 = time.strftime("%H")
		m2 = time.strftime("%M")
		s2 = time.strftime("%S")
		
		#Write to the data file
		lun = open(savefile, 'a')
		lun.write("%r \t %r \t %r \t %r \t %r \t %6.2f \t %6.2f \t %6.2f \t %6.2f \t %6.2f \t %6.2f \t %6.2f \t %r \t %r \t %r \t %r \t %r" % 
			(year1, day1, h1, m1, s1, sht1x_temp, bmp_temp, bmp_pres, sht1x_rh, wind_dir, wind_spd, rain_rate, year2, day2, h2, m2, s2))
		lun.write("\n")
		lun.close()
		
		time.sleep(dt)
		

#----------------------END MAIN LOOP------------------------

except KeyboardInterrupt:
	print "Keyboard Interrupt, cleaning pins..."


#except:
#	print "Unexpected Error"


finally: GPIO.cleanup() #Exiting code cleanly
