# rainbow.py
import spidev
import time
 
LED_COUNT = 60
DELAY = 0.00003 * float(LED_COUNT)
 


def Color(red, green, blue, white = 0):
        """Convert the provided red, green, blue color to a 24-bit color value.
        Each color component should be a value 0-255 where 0 is the lowest intensity
        and 255 is the highest intensity.
        """
        return (white << 24) | (green << 16)| (red << 8) | blue



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
 
def colorWipe(strip, color, wait_ms=50):
        """Wipe color across display a pixel at a time."""
        for i in range(strip.numPixels()):
                strip.setPixelColor(i, color)
                strip.show()
                time.sleep(wait_ms/1000.0)

def theaterChase(strip, color, wait_ms=50, iterations=10):
        """Movie theater light style chaser animation."""
        for j in range(iterations):
                for q in range(3):
                        for i in range(0, strip.numPixels(), 3):
                                strip.setPixelColor(i+q, color)
                        strip.show()
                        time.sleep(wait_ms/1000.0)
                        for i in range(0, strip.numPixels(), 3):
                                strip.setPixelColor(i+q, 0)

def wheel(pos):
        """Generate rainbow colors across 0-255 positions."""
        if pos < 85:
                return Color(pos * 3, 255 - pos * 3, 0)
        elif pos < 170:
                pos -= 85
                return Color(255 - pos * 3, 0, pos * 3)
        else:
                pos -= 170
                return Color(0, pos * 3, 255 - pos * 3)

def rainbow(strip, wait_ms=20, iterations=1):
        """Draw rainbow that fades across all pixels at once."""
        for j in range(256*iterations):
                for i in range(strip.numPixels()):
                        strip.setPixelColor(i, wheel((i+j) & 255))
                strip.show()
                time.sleep(wait_ms/1000.0)

def rainbowCycle(strip, wait_ms=20, iterations=5):
        """Draw rainbow that uniformly distributes itself across all pixels."""
        for j in range(256*iterations):
                for i in range(strip.numPixels()):
                        strip.setPixelColor(i, wheel((int(i * 256 / strip.numPixels()) + j) & 255))
                strip.show()
                time.sleep(wait_ms/1000.0)

def theaterChaseRainbow(strip, wait_ms=50):
        """Rainbow movie theater light style chaser animation."""
        for j in range(256):
                for q in range(3):
                        for i in range(0, strip.numPixels(), 3):
                                strip.setPixelColor(i+q, wheel((i+j) % 255))
                        strip.show()
                        time.sleep(wait_ms/1000.0)
                        for i in range(0, strip.numPixels(), 3):
                                strip.setPixelColor(i+q, 0)

 
try:
    
    strip = DigiDotBooster_LED(60)
    strip.clear()
    while True:
                # Color wipe animations.
                colorWipe(strip, Color(255, 0, 0))  # Red wipe
                colorWipe(strip, Color(0, 255, 0))  # Blue wipe
                colorWipe(strip, Color(0, 0, 255))  # Green wipe
                # Theater chase animations.
                theaterChase(strip, Color(127, 127, 127))  # White theater chase
                theaterChase(strip, Color(127,   0,   0))  # Red theater chase
                theaterChase(strip, Color(  0,   0, 127))  # Blue theater chase
                # Rainbow animations.
                rainbow(strip)
                rainbowCycle(strip)
                theaterChaseRainbow(strip)
    #strip.setPixelColor(0,Color(0,0,255))
    #strip.show()
    #time.sleep(2)
    #strip.setPixelColorAll(Color(192,64,1))
    #strip.show()
        
except KeyboardInterrupt:
    strip.clear()
    strip.spi.close()
