# digi_dot_booster

This is a python library which allows you to control LED stripes on Raspberry Pi with a [Digi Dot Booster](http://www.led-genial.de/DIGI-DOT-Booster-WS2812-und-SK6812-ueber-SPI-Schnittstelle-ansteuern) micro controller. 

Digi Dot Booster supports WS2812, SK6812 (and compatible) LED's.

For me the reason to use Digi Dot Booster was the requirement to use WS2812b stripes and audio on a Raspberry PI (the use of a WS2812B strip and audio on Raspberry Pi at the same time is not possible, because of the use of the PCM channel by the WS2812b).

Digi Dot Booster uses controlled by the SPI bus on Raspberry Pi. An example and tutorial how to connect and make runable you could found here: [http://www.ledswork.de/wp/2016/02/09/led-booster-am-raspberry-pi-mit-python-ansteuern/](http://www.ledswork.de/wp/2016/02/09/led-booster-am-raspberry-pi-mit-python-ansteuern/)

Before I used the Digi Dot Booster, I developed a python script which controlls the WS2812b directly connected on Raspberry Pi (without audio). For that I used the library from [jgarff](https://github.com/jgarff/rpi_ws281x) which is the most recommended library for WS2812 on Raspberry Pi.

After the desicion to use the Digi Dot Booster, I don't wanted to rewrite my python code. So I developed this python class which wrappes the functions from [jgarff](https://github.com/jgarff/rpi_ws281x) but controlls the Digi Dot Booster. I also added the Digi Dot Booster features like "BOOSTER_REPLACE" or "BOOSTER_RAINBOW".

## Usage

### init

To use you only need to import the DigiDotBooster file. Initalise than the DigiDotBooster_LED class with the count of used LED's on you strip.

````
# YourScript.py
from digiDotBooster import *

LED_COUNT = 60

try:
  strip = DigiDotBooster_LED(LED_COUNT)
  # set color red on first pixel on your strip 
  strip.setPixelColor(1, Color(255,0,0))
  strip.show()
except KeyboardInterrupt:
  strip.clear()
  strip.spi.close()  
````

To set a color on a LED or a range of LED's you should start with index 1 not 0. That means you first LED is number 1 and so on.


### set brightness of LED's

I've added some helper functions to convert RGB color's to HSV colors and back. With them you are able to controll the brighness of a LED.

Helper function to convert RGB to HSV or to change the brightness:

````
def ConvertRGB2HSV(red, green, blue):
def ConvertHSV2RGB(hue, sat, vol):
def ChangeBrightnessOfColor(color, brightness):
````


Here is an example how to change the brightness of on LED:

````
  red = Color(255,0,0)
  brightness = 20 # should be 0..255
  redLight = ChangeBrightnessOfColor(red, brightness)
  
  strip.setPixelColor(1, redlight)
  strip.show()
````


## Scripts

### example.py
This script shows some examples and cases how to use the DigiDotBooster class.

###rainbow.py
This script is stolen from the [DigiDotBooster/RaspberryPi tutorial](http://www.ledswork.de/wp/2016/02/09/led-booster-am-raspberry-pi-mit-python-ansteuern/) and shows the direct use of the Digi Dot Booster commands

### strandtest_neopixellib.py
This script is based on the example script from [jgarff](https://github.com/jgarff/rpi_ws281x/blob/master/python/examples/strandtest.py) and shows how easy it us to use jgarff library with Digi Dot Booster.



## Limitations
 Digi Dot Booster has some limitations:
 
  * the maximum number of LED's that could be controlled by Digi Dot Booster could is 256 - you need to ive an even number
  * after every write the booster commands on the SPI bus, Digi Dot Booster needs some time to proces the commands. It depends by the count of LED you want to use. For every LED we need 0.0003 seconds. This library is calculating and handling the time for you, every time when you call `show()` on your DigiDotBooster instance.
  * the maximum count of commands that could be writen on the SPI bus is 256 - currently this is not checked by the class
  
## Road Map

* check for maximum numbers of commands that could be written on the SPI bus
* implement the last missing Digi Dot feature: BOOSTER_COPYLED, BOOSTER_RGBBORDER, BOOSTER_SETRGBW









 