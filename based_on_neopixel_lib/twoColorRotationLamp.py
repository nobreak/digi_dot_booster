# rainbow.py
import spidev
import time
from thread import start_new_thread
from threading import Thread
 
def Color(red, green, blue, white = 0):
        """Convert the provided red, green, blue color to a 24-bit color value.
        Each color component should be a value 0-255 where 0 is the lowest intensity
        and 255 is the highest intensity.
        """
        return (white << 24) | (green << 16)| (red << 8) | blue



LED_COUNT = 60
DELAY = 0.04 
#0.00003 * float(LED_COUNT)
LED_TIME       = 0.035   # animation time (time from one pixel to the next
LED_START_PIXEL = 0     # where we want to start the animation on stripe
LED_END_PIXEL = 12      # where we want to end the animation on strip
LED_COLOR1         = Color(255,0,0)
LED_COLOR2         = Color(0,0,255)
COUNT_PIXEL_FIRST_COLOR = 6 # count how much pixels the fist color is long, second color count is $
LED_ROWS       = 5
 



class DigiDotBooster_LED(object):
        def __init__(self, num, brightness=255 ):    
            self.countPixels = num
            # open /dev/spidev0.1 (CS1 Pin wird verwendet)
            self.spi = spidev.SpiDev()
            self.spi.open(0, 1)
            self.spi.mode = 0b00
            # BOOSTER_INIT mit der Anzahl der LEDs und 24 bits pro LED (WS2812)
            self.spi.writebytes([0xB1, LED_COUNT, 24])
            time.sleep(DELAY)



        def show(self):
            self.spi.writebytes([0xB2])
            time.sleep(DELAY)

        def numPixels(self):
            return self.countPixels

        def setPixelColor(self, n, color):
            blue =  color & 255
            green = (color >> 16) & 255
            red =   (color >> 8) & 255
            self.spi.writebytes([0xA1, red, green, blue, 0xA4, n])
            time.sleep(DELAY)

        def setPixelColorAll(self, color):
            blue =  color & 255
            green = (color >> 16) & 255
            red =   (color >> 8) & 255
            self.spi.writebytes([0xA1, red, green, blue, 0xA5])
            time.sleep(DELAY)

 
        def clear(self):
            # BOOSTER_SETRGB 0x000000, BOOSTER_SETALL, BOOSTER_SHOW
            self.spi.writebytes([0xA1, 0, 0, 0, 0xA5, 0xB2])
            time.sleep(DELAY)
            return
 

# starts from the left and fills the pixels with the given color starting at startPosition up to c$
#
# strip - the connected stripe
# color - the color which is to use
# startPixel - the pixel on the stripe where we want to start
# countPixels - the count of pixel wich we want to fill with the color after the start pixel
# animationTime - the time we wait to set the next pixel with the color
def fillInAnimation(strip, color, startPixel, countPixels, animationTime):
  #print("fillInAnimation")
  for pixel in range(startPixel, startPixel+countPixels, +1):
          strip.setPixelColor(pixel,color)
          strip.show()
          time.sleep(animationTime)


# move a collection of pixel to the right, all nomore used pixels on the left will be filled with $
#
# strip - the connected stripe
# color1 - the color1 which is to use
# color2 - the color2 which is to use
# startPixelAnimation - the pixel on the stripe where we want to start
# startPixel - the start pixel on the strip where the animation could be - beginning at 0
# endPixel - the end pixel on the strip where the animation could be - beginning at 0
# animationTime - the time we wait to set the next pixel with the color
def moveAnimation(strip, color1, color2, startPixelAnimation, startPixel, endPixel, animationTime):
  #print("moveAnimation")
  for pixel in range(startPixelAnimation,endPixel, +1):
        strip.setPixelColor(pixel, color1)
        #print("Pixel: " + str(pixel) + " StartPixelAnimation:" + str(startPixelAnimation) + " Sta$
        strip.setPixelColor(pixel-startPixelAnimation + startPixel ,color2)
        strip.show()
        time.sleep(animationTime)


# when the pixel collection of color1 reaches the end, we animate pixel by pixel again from the st$
#
# strip - the connected stripe
# color1 - the color1 which is to use
# color2 - the color2 which is to use
# startPixel - the start pixel on the strip where the animation could be - beginning at 0
# endPixel - the end pixel on the strip where the animation could be - beginning at 0
# animationTime - the time we wait to set the next pixel with the color
def lineBreakAnimation(strip, color1, color2, countPixel, startPixel, endPixel, animationTime):
  #print("lineBreakAnimation")
  for pixel in range(endPixel-countPixel, endPixel):
        strip.setPixelColor(pixel, color2)
        #print("Pixel:" + str(pixel) + " EndPixel: " + str(endPixel) + " CountPixel: " + str(count$
        strip.setPixelColor((endPixel-pixel-countPixel)*-1+startPixel, color1)
        strip.show()
        time.sleep(animationTime)


# strip - the strip object a connected strip
# color1 - first color
# color2 - second color
# countPixelColor1 - count of pixels for color1, the count of pixels for color 2 will be calculate$
# timeValue - time to switch to the next pixel
# startPixel - the start pixel on the strip where the animation could be - beginning at 0
# endPixel - the end pixel on the strip where the animation could be - beginning at 0
def twoColorRotationLampMatrix(strip, color1, color2, countPixelColor1, timeValue, startPixel, endPixel, rows):
   f = 1
   # loop for all needed pixels
   while 1: # endless loop      
      # fill the first pixels up to countPixelColor1
      # but only one time (f)
     fillInAnimationThreads = []
     while f == 1:
        for row in range(0,rows,+1):
           t = Thread(target=fillInAnimation, args=(strip, color1, startPixel+(endPixel*row), countPixelColor1, timeValue, ))
           fillInAnimationThreads.append(t)
        for t in fillInAnimationThreads:
           t.start()
        f = f+1

     for t in fillInAnimationThreads:
       t.join()

     # now move the first color to the right and add the second color on the left
     #endPixel = strip.numPixels()
     #endPixel = startPixel+6 #countLedPerRow
     moveAnimationThreads = []
     for row in range(0,rows, +1):
        t = Thread(target=moveAnimation, args=(strip, color1, color2, startPixel+countPixelColor1+(endPixel*row), startPixel+(endPixel*row), endPixel+(endPixel*row), timeValue, ))
        moveAnimationThreads.append(t)
     for t in moveAnimationThreads:
        t.start()

     for t in moveAnimationThreads:
        t.join()


     # the following loop realized the animation of a coolection of pixels
     # with the same color over the end of the strip and starting again
     # at the beginning on the strip
     lineBreakAnimationThreads = []
     for row in range(0,rows, +1):
        t = Thread(target=lineBreakAnimation, args=(strip, color1, color2, countPixelColor1, startPixel+(endPixel*row), endPixel+(endPixel*row), timeValue, ))
        lineBreakAnimationThreads.append(t)
     for t in lineBreakAnimationThreads:
        t.start()
     for t in lineBreakAnimationThreads:
        t.join()


 
try:
    
    strip = DigiDotBooster_LED(60)
    strip.clear()
    while True:
              # Color wipe animations.
              twoColorRotationLampMatrix(strip, LED_COLOR1, LED_COLOR2, COUNT_PIXEL_FIRST_COLOR, LED_TIME, LED_START_PIXEL, LED_END_PIXEL, LED_ROWS)

        
except KeyboardInterrupt:
    strip.clear()
    strip.spi.close()
