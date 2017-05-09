import spidev
import time
import colorsys

def Color(red, green, blue, white = 0):
        """Convert the provided red, green, blue color to a 24-bit color value.
        Each color component should be a value 0-255 where 0 is the lowest intensity
        and 255 is the highest intensity.
        """
        return (white << 24) | (green << 16)| (red << 8) | blue

def ConvertRGB2HSV(red, green, blue):
   r, g, b = [x/255.0 for x in red, green, blue]
   h, s, v = colorsys.rgb_to_hsv(r, g, b)
   hue = h*360.0
   sat, vol = [x*255.0 for x in s,v]
   return int(hue), int(sat), int(vol)

def ConvertHSV2RGB(hue, sat, vol):
   h = hue/360.0
   s, v = [x/255.0 for x in sat, vol]
   r, g, b = colorsys.hsv_to_rgb(h,s,v)
   red, green, blue = [x*255.0 for x in r, g, b]
   return int(red), int(green), int(blue)

def ChangeBrightnessOfColor(color, brightness):
   red = (color >> 8) & 255
   blue =  color & 255
   green =   (color >> 16) & 255

   h,s,v = ConvertRGB2HSV(red, blue, green)
   v = brightness
   r,g,b = ConvertHSV2RGB(h,s,v)
   return Color(r,g,b)

class DigiDotBooster_LED(object):
        def __init__(self, num):    
            self.countPixels = num
            self.delay = 0.00003 * float(num)
            self.byteData = []
            # open /dev/spidev0.1 (CS1 Pin wird verwendet)
            self.spi = spidev.SpiDev()
            self.spi.open(0, 1)
            self.spi.mode = 0b00
            # BOOSTER_INIT mit der Anzahl der LEDs und 24 bits pro LED (WS2812)
            self.spi.writebytes([0xB1, num, 24])
            #time.sleep(0.00003 * num)
            time.sleep(0.018)

        def show(self):
            self.byteData.append(0xB2)
            self.spi.writebytes(self.byteData)
            self.byteData[:] = []
            time.sleep(self.delay)

        def numPixels(self):
            return self.countPixels

        def setPixelColor(self, n, color, shouldShow=False):
            n = n-1
            blue =  color & 255
            green = (color >> 16) & 255
            red =   (color >> 8) & 255
	    self.byteData.extend([0xA1, red, green, blue, 0xA4, n])
            if (shouldShow):
              self.show()

        def setPixelColorHSV(self, n, hue, sat, vol, shouldShow=False):
            n = n-1
            self.byteData.extend([0xA3, hue & 0xFF, hue >> 8, sat, vol, 0xA4, n])
            if (shouldShow):
              self.show()

        def setPixelColorAll(self, color, shouldShow=False):
            blue =  color & 255
            green = (color >> 16) & 255
            red =   (color >> 8) & 255
            self.byteData.extend([0xA1, red, green, blue, 0xA5])
            if (shouldShow):
               self.show()

        def setPixelColorHSVAll(self, hue, sat, vol, shouldShow=False):
            self.byteData.extend([0xA3, hue & 0xFF, hue >> 8, sat, vol, 0xA5])
            if (shouldShow):
              self.show()

        def setPixelColorRange(self, start, end, color, shouldShow=False):
            start = start -1
            end = end -1
            blue =  color & 255
            green = (color >> 16) & 255
            red =   (color >> 8) & 255
            self.byteData.extend([0xA1, red, green, blue, 0xA6, start, end])
            if (shouldShow):
               self.show()

        def setPixelColorHSVRange(self, start, end, hue, sat, vol, shouldShow=False):
            start = start -1
            end = end -1
            self.byteData.extend([0xA3, hue & 0xFF, hue >> 8, sat, vol, 0xA6, start, end])
            if (shouldShow):
              self.show()

        def shiftUpRange(self, start, end, count, shouldShow=False):
            start = start -1
            end = end -1 
            self.byteData.extend([0xB3, start, end, count])
            if (shouldShow):
               self.show()

        def shiftDownRange(self, start, end, count, shouldShow=False):
            start = start -1
            end = end -1
            self.byteData.extend([0xB4, start, end, count])
            if (shouldShow):
               self.show()               

        def repeatPixelRange(self, start, end, count, shouldShow=False):
            start = start -1
            end = end -1
            self.byteData.extend([0xB6, start, end, count])
            if (shouldShow):
               self.show() 

        def setRainbow(self, start, end, hue, sat, vol, inc, shouldShow=False):
            start = start -1
            end = end -1
            self.byteData.extend([0xA7, hue & 0xFF, hue >> 8, sat, vol, start, end, inc])
            if (shouldShow):
               self.show()


        def clear(self):
            # BOOSTER_SETRGB 0x000000, BOOSTER_SETALL, BOOSTER_SHOW
            self.spi.writebytes([0xA1, 0, 0, 0, 0xA5, 0xB2])
            time.sleep(self.delay)
            return

