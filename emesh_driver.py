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
#Winds are a 15s average, so temporal resolution is dt+15s
dt = 15 #seconds

#Declaring counter variables to be global
#These are used for wind and rain
global rain_count
global windspd_count
global wind_dir

#Variable initialization
rain_count = 0
windspd_count = 0

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
GPIO.setup(rain_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.add_event_detect(rain_pin, GPIO.FALLING, callback=rain_detect, bouncetime=500)

GPIO.setup(windspd_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(winddir_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)


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
		
		#Wind loop
		#This loop should take 15s of the 30s total delay between obs
		#Resetting variables used in wind loop
		windspd_count = 0 #Revolutions of anemometer
		dir_time = 0 #Relative timing for wind direction
		i = 0 #loop counter
		
		timeout = 5 #Time out in seconds, reccomend timeout = 15/3
		wtime = 15 #time to average wind measurements over in seconds
		wt1 = time.clock()
		while ((wt2-wt1)<wtime):
			wt2 = time.clock()
			GPIO.wait_for_edge(windspd_pin, GPIO.FALLING, timeout)
			wts1 = time.clock()
			GPIO.wait_for_edge(winddir_pin, GPIO.RISING, timeout)
			wtd = time.clock()
			err = GPIO.wait_for_edge(windspd_pin, GPIO.FALLING, timeout)
			wts2 = time.clock
			if err == 0:
				windspd_count = windspd_count+1
			else:
				windspd_count = -999
			dir_time = (wtd-wts1)/(wts2-wts1)+dir_time
			i += 1
			
			
		wind_dir = (dir_time/i) #Needs completion
		wrps = windspd_count/wtime
		if (wrps >= 0.010) and (wrps < 3.229 ):
			wind_spd = (-0.1095*wrps**2 +2.9318*wrps-0.1412)*0.48037
		elif (wrps >= 3.230) and (wrps < 54.362):
			wind_spd = (0.0052*wrps**2+2.1980*wrps+1.1091)*0.48037
		elif (wrps >= 54.362) and (wrps < 66.332):
			wind_spd = (0.1104*wrps**2-9.5685*wrps+329.87)*0.48037
		elif (wrps >= 66.332):
			wind_spd = 999
		elif (windspd_count == -999):
			wind_spd = 0
		else:
			wind_spd = float('nan')
			
	
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
		
		#Determining Wind Speed and Wind Direction
		wind_dir = float('NaN')
		wind_spd = float('NaN')
		
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
		lun.write("%r \t %r \t %r \t %r \t %r \t %r \t %r \t %r \t %r \t %r \t %r \t %r \t %r \t %r \t %r \t %r \t %r" % 
			(year1, day1, h1, m1, s1, sht1x_temp, bmp_temp, bmp_pres, sht1x_rh, wind_dir, wind_spd, rain_rate, year2, day2, h2, m2, s2))
		lun.write("\n")
		lun.close()
		
		time.sleep(dt)
		

#----------------------END MAIN LOOP------------------------

except KeyboardInterrupt:
	print "Keyboard Interrupt, cleaning pins..."


except:
	print "Unexpected Error"


finally: GPIO.cleanup() #Exiting code cleanly
