# emesh_driver
This code drives the raspberry pi emesh weather stations
It is still INCOMPLETE

The code currently works with:
BMP 180 pressure sensor
SHT15 temperature sensor
Model 380/382 12" tipping rain gauge

Future implementations:
Particulate sensor
Davis anemometer
File writing

Sensor libraries used:
BMP sensor -- https://github.com/adafruit/Adafruit_Python_BMP
SHT15 -- https://pypi.python.org/pypi/rpiSht1x/1.2

To use the rpi sht1x library, the library code must have the gpio cleanups removed before it can be used.
