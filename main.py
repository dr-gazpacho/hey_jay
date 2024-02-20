import time
from machine import Pin, PWM
import machine
import ustruct
import pimoroni_i2c
import breakout_bh1745
import utime
import sys
import math
import gc

buzzer=PWM(Pin(15))
counter=0

try:
    LIGHTSENSOR = {"sda": 0, "scl": 1}
    I2C = pimoroni_i2c.PimoroniI2C(**LIGHTSENSOR)
    bh1745 = breakout_bh1745.BreakoutBH1745(I2C)
    bh1745.leds(False)
except:
    print("Check the sensor. An exception occurred") # A visual cue that therehas been an issue with the sensor setup
    print("Sensor data:", sensor_data)
    
    # read the value from the light sensor
def sensorread():
    rgbc_raw = bh1745.rgbc_raw()
    rgb_clamped = bh1745.rgbc_clamped()
    brightness=rgbc_raw[3]
    buzzer.freq(brightness)
    print("Clamped: {}, {}, {}, {}".format(*rgb_clamped))
    print("Bright="+str(brightness))
    print(counter)
    try:
        EV = math.log2(brightness/calibrationconst)+evcorrection
        print(EV)
    except:
        EV = -10
    return rgb_clamped[0],rgb_clamped[1],rgb_clamped[2],EV

buzzer.freq(500)
buzzer.duty_u16(1000)

while(1):
    red, green, blue, lastmeasure=sensorread()
    print(red,green,blue,lastmeasure)
    time.sleep_ms(1000)
    counter+=1