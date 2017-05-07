import spidev
import time

def Color(red, green, blue, white = 0):
        """Convert the provided red, green, blue color to a 24-bit color value.
        Each color component should be a value 0-255 where 0 is the lowest intensity
        and 255 is the highest intensity.
        """
        return (white << 24) | (green << 16)| (red << 8) | blue



class DigiDotBooster_LED(object):
        def __init__(self, num):    
            self.countPixels = num
            self.delay = 0.00003 * float(num)
            # open /dev/spidev0.1 (CS1 Pin wird verwendet)
            self.spi = spidev.SpiDev()
            self.spi.open(0, 1)
            self.spi.mode = 0b00
            # BOOSTER_INIT mit der Anzahl der LEDs und 24 bits pro LED (WS2812)
            self.spi.writebytes([0xB1, num, 24])
            #time.sleep(0.00003 * num)
            time.sleep(0.018)

        def show(self):
            self.spi.writebytes([0xB2])
            time.sleep(0.4)

        def numPixels(self):
            return self.countPixels

        def setPixelColor(self, n, color):
            blue =  color & 255
            green = (color >> 16) & 255
            red =   (color >> 8) & 255
            self.spi.writebytes([0xA1, red, green, blue, 0xA4, n])
            time.sleep(self.delay)

        def setPixelColorAll(self, color):
            blue =  color & 255
            green = (color >> 16) & 255
            red =   (color >> 8) & 255
            self.spi.writebytes([0xA1, red, green, blue, 0xA5])
            time.sleep(self.delay)

        def setPixelColorRange(self, color, start, end):
            blue =  color & 255
            green = (color >> 16) & 255
            red =   (color >> 8) & 255
            self.spi.writebytes([0xA1, red, green, blue, 0xA6, start, end])
            time.sleep(self.delay)    

        def shiftUpRange(self, count, start, end):    
            self.spi.writebytes([0xB3, start, end, count])
            time.sleep(self.delay)

        def shiftDownRange(self, count, start, end):    
            self.spi.writebytes([0xB4, start, end, count])
            time.sleep(self.delay)    

 
        def clear(self):
            # BOOSTER_SETRGB 0x000000, BOOSTER_SETALL, BOOSTER_SHOW
            self.spi.writebytes([0xA1, 0, 0, 0, 0xA5, 0xB2])
            time.sleep(self.delay)
            return

