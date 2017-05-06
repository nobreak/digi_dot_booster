# rainbow.py
import spidev
import time
 
DELAY = 0.04
LED_COUNT = 60
 


def Color(red, green, blue, white = 0):
        """Convert the provided red, green, blue color to a 24-bit color value.
        Each color component should be a value 0-255 where 0 is the lowest intensity
        and 255 is the highest intensity.
        """
        return (white << 24) | (green << 16)| (red << 8) | blue



class DigiDotBooster_LED(object):
        def __init__(self, num, brightness=255 ):    
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
 


 
try:
    strip = DigiDotBooster_LED(60)
    strip.clear()
    strip.setPixelColor(0,Color(0,0,255))
    strip.show()
    time.sleep(2)
    strip.setPixelColorAll(Color(192,64,1))
    strip.show()
        
except KeyboardInterrupt:
    strip.clear()
    strip.spi.close()
