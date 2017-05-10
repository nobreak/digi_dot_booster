# example.py
import spidev
import time
from digiDotBooster import *


def clear():
    strip = DigiDotBooster_LED(60)
    strip.clear()


def rotation(led_count, led_rows, delay, colors, brightness=255):
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
#   rainbow() 
#   testHSV()
#   convertTest()
    rotation(60, 5 , 0.075, [Color(255,0,0), Color(0,255,0), Color(0,0,255)], 180) 
#   clear()
except KeyboardInterrupt:
    print "you should clean up"
