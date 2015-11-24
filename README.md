# emesh_driver
This code drives the raspberry pi emesh weather stations
It requires the emesh_system repo to be installed first, and the user is best off following the directions
  found in the emesh_system README.
  
This code is still unfinished and requires wind measurements to be corrected.

The code currently works with:
BMP 180 pressure sensor
SHT15 temperature sensor
Model 380/382 12" tipping rain gauge

Ongoing work:
Correct code for working with the Ultimeter Anemometer and Wind Vane

Future implementations:
Particulate sensor
Davis anemometer

Sensor libraries used:
BMP sensor -- https://github.com/adafruit/Adafruit_Python_BMP
SHT15 -- https://pypi.python.org/pypi/rpiSht1x/1.2

To use the rpi sht1x library, the library code must have the gpio cleanups removed before it can be used. For this reason, it is best to use the emesh_system repo instead of installing these libraries yourself.
