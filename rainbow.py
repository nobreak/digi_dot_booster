# rainbow.py
import spidev
import time
 
DELAY = 0.04
LED_COUNT = 60
 
spi = spidev.SpiDev()
 
def initSPI():
    # open /dev/spidev0.1 (CS1 Pin wird verwendet)
    spi.open(0, 1)  
    spi.mode = 0b00
    return
 
def initLEDs():
    # BOOSTER_INIT mit der Anzahl der LEDs und 24 bits pro LED (WS2812)
    spi.writebytes([0xB1, LED_COUNT, 24])
    time.sleep(DELAY)
    return
 
 
def clear():
    # BOOSTER_SETRGB 0x000000, BOOSTER_SETALL, BOOSTER_SHOW
    spi.writebytes([0xA1, 0, 0, 0, 0xA5, 0xB2])
    time.sleep(DELAY)
    return
 
i = 0
initSPI()
initLEDs()
 
try:
    while True:
        i += 5
        i = i % 360
        # BOOSTER_SETRAINBOW HUE (2 Bytes), SATURATION, VALUE, von der ersten (0) bis
        # zur letzten LED in 10-er Schritten, BOOSTER_SHOW
        spi.writebytes([0xA7, i & 0xFF, i >> 8, 255, 100, 0, LED_COUNT - 1, 10, 0xB2])  
        time.sleep(DELAY)
except KeyboardInterrupt:
    clear()
    spi.close()
