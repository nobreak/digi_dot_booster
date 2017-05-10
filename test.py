# test.py
import spidev
import time
from digiDotBooster import DigiDotBooster_LED
from digiDotBooster import Color
from digiDotBooster import ConvertRGB2HSV
from digiDotBooster import ConvertHSV2RGB
from digiDotBooster import ChangeBrightnessOfColor
 
DELAY = 0.125
LED_COUNT = 60
LED_ROWS = 5
 

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

def clear():
    strip = DigiDotBooster_LED(60)
    strip.clear()

def newRotation3Color(led_count, led_rows, delay, colors, brightness=255):
   if (brightness != 255):
     for idx, color in enumerate(colors):
       colors[idx] = ChangeBrightnessOfColor(color, brightness)

   num_colors = len(colors)
   led_count_row = led_count/led_rows
   color_width = led_count_row/num_colors

   strip = DigiDotBooster_LED(led_count)

   while (1):
     for color in colors:
       for pixel in range(1,color_width):
         strip.shiftUpRange(pixel, led_count_row, 1)
         strip.setPixelColor(pixel, color)
         strip.repeatPixelRange(1,led_count_row,led_rows-1)
         strip.show()
         time.sleep(delay)



def newRoation():
   delay = 0.025   
   strip = DigiDotBooster_LED(60)
   for p in range(0,6):
     strip.setPixelColor(p, Color(0,0,255))
     strip.repeatPixelRange(0,11,4)
     strip.show()
     time.sleep(delay)
   while (1):
     for x in range(0, 6):
        strip.shiftUpRange( x, x+6, 1)
        strip.setPixelColor(x, Color(255,0,0))
        strip.repeatPixelRange(0,11,4)
        strip.show()
        time.sleep(delay)
     for x in range(0, 6):
        strip.shiftUpRange( x, x+6, 1)
        strip.setPixelColor(x, Color(0,0,255))
        strip.repeatPixelRange(0,11,4)
        strip.show()
        time.sleep(delay)


def newRotationByte():
   delay = 0.025
   spi = spidev.SpiDev()
   spi.open(0, 1)
   spi.mode = 0b00
   # init
   spi.writebytes([0xB1, LED_COUNT, 24])
   time.sleep(0.018)
   for p in range(0,6):
     spi.writebytes([0xA1, 0, 0, 255, 0xA4, p, 0xB6, 0, 11, 4, 0xB2])    
     time.sleep(0.018)
     time.sleep(delay)
   while (1):
     for x in range(0,6):
       spi.writebytes([0xB3, x, x+6, 1, 0xA1, 255,0,0, 0xA4,x, 0xB6, 0, 11, 4, 0xB2])
       time.sleep(0.018)
       time.sleep(delay)
     for x in range(0,6):
       spi.writebytes([0xB3, x, x+6, 1, 0xA1, 0,0,255, 0xA4,x, 0xB6, 0, 11, 4, 0xB2])
       time.sleep(0.018)
       time.sleep(delay)


def rainbow():
   delay = 1.025   
   strip = DigiDotBooster_LED(60)
   strip.setRainbow(0,5, 180, 255, 30, 100)
   strip.repeatPixelRange(0,11,4)
   strip.show()
   time.sleep(delay)

def testHSV():
   strip = DigiDotBooster_LED(60)
   strip.setPixelColorHSVAll(0,200,100)
   strip.setPixelColorHSV(0,180, 200, 255)
   strip.repeatPixelRange(0,11,4)
   strip.setPixelColorHSVRange(15, 20, 60, 255, 80)
   strip.show()

def convertTest():
   strip = DigiDotBooster_LED(60)
   red = 126
   green = 0
   blue = 174

   print "RGB:" + str(red) + " " + str(green) + " " + str(blue)
   
   strip.setPixelColorRange(0, 5, Color(red, green, blue))

   hue, sat, vol = ConvertRGB2HSV(red, green, blue)
   print "HSV:" + str(hue) + " " + str(sat) + " " + str(vol)
 
   strip.setPixelColorHSVRange(12, 17, hue, sat, vol)

   r,g,b, = ConvertHSV2RGB(hue, sat, vol)
   print "RGB2:" + str(r) + " " + str(g) + " " + str(b)
  
   strip.setPixelColorRange(24, 29, Color(r,g,b))

   strip.show()



try:
#   spi = spidev.SpiDev()
#   spi.open(0, 1)
#   spi.mode = 0b00
#   # init
#   spi.writebytes([0xB1, LED_COUNT, 24])
#   time.sleep(DELAY)
#   i = 0
#   while True:
#        i += 5
#        i = i % 360
#        print i
        # BOOSTER_SETRAINBOW HUE (2 Bytes), SATURATION, VALUE, von der ersten (0) bis
        # zur letzten LED in 10-er Schritten, BOOSTER_SHOW
#        spi.writebytes([0xA7, i & 0xFF, i >> 8, 255, 100, 0, LED_COUNT - 1, 10, 0xB2])  
#        time.sleep(DELAY)

#   demo3(spi)

#   demo3self()
#   rainbow() 
#   testHSV()
#   convertTest()
#   newRoation()
#   newRotation3Color(LED_COUNT, LED_ROWS,0.075, [Color(255,0,0), Color(0,255,0), Color(0,0,255)], 25) 
   #newRotationByte() 
   clear()

    
except KeyboardInterrupt:
    strip.clear()
    strip.spi.close()
