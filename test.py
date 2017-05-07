# test.py
import spidev
import time
from digiDotBooster import DigiDotBooster_LED
from digiDotBooster import Color
 
DELAY = 0.04
LED_COUNT = 60
 

def demo3(spi):
   # hsv to all
   spi.writebytes([0xA3, 255, 70, 255, 128, 0xA5]) 
   time.sleep(DELAY)
   # rgb to pixel - yellow on 0
   spi.writebytes([0xA1, 100, 100, 0, 0xA4, 0])
   time.sleep(DELAY)
   #show
   spi.writebytes([0xB2])
   time.sleep(DELAY)

   for x in range(0, 30):
     # shift up
     spi.writebytes([0xB3, 0, LED_COUNT-1, 1])
     time.sleep(DELAY) 
     # rgb to pixel
     spi.writebytes([0xA1, 0, 0, 128, 0xA4, 0])
     time.sleep(DELAY)
     #show
     spi.writebytes([0xB2])
     time.sleep(DELAY)
     time.sleep(0.125)

def demo3self():
    strip = DigiDotBooster_LED(60)
    strip.setPixelColorAll(Color(255,0,255))
    strip.setPixelColor(0,Color(100,100,0))
    strip.show()
    for x in range(0, 30):
      strip.shiftUpRange(1,0, LED_COUNT-1)
      strip.setPixelColor(0,Color(0,0,128))
      strip.show()
      time.sleep(0.5)

def newRoation():
   strip = DigiDotBooster_LED(60)
   strip.setPixelColorRange(Color(0,0,255), 0, 5)
   strip.show()
   for x in range(0, 6):
     strip.shiftUpRange(1, x, x+6)
     strip.setPixelColor(x, Color(255,0,0))
#     strip.spi.writebytes([0xB6,0,11,4 ])
     strip.show()
     time.sleep(0.5)

try:
#   spi = spidev.SpiDev()
#   spi.open(0, 1)
#   spi.mode = 0b00
   # init
#   spi.writebytes([0xB1, LED_COUNT, 24])
#   time.sleep(DELAY)
#   demo3(spi)

#    demo3self()

   newRoation()

   # time.sleep(2)
#    strip.shiftUpRange(1,0,2)
#    strip.setPixelColorAll(Color(255,0,0))
#    strip.show()
#    time.sleep(2)
#    strip.setPixelColor(13,Color(0,125,255))
#    strip.show()
    
except KeyboardInterrupt:
    strip.clear()
    strip.spi.close()
