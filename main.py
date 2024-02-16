import time
from rotary_irq_rp2 import RotaryIRQ
from machine import Pin, SoftI2C
import machine
import ustruct
import pimoroni_i2c
import breakout_bh1745
import utime
import sys
import math
import gc

led = Pin("LED", Pin.OUT)
r = RotaryIRQ(pin_num_clk=12, 
              pin_num_dt=13, 
              min_val=0, 
              max_val=5, 
              reverse=False, 
              range_mode=RotaryIRQ.RANGE_WRAP)
              
val_old = r.value()



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
    print("Clamped: {}, {}, {}, {}".format(*rgb_clamped))
    print("Bright="+str(brightness))
    try:
        EV = math.log2(brightness/calibrationconst)+evcorrection
        print(EV)
    except:
        EV = -10
    return rgb_clamped[0],rgb_clamped[1],rgb_clamped[2],EV

while(1):
    red, green, blue, lastmeasure=sensorread()
    print(red,green,blue,lastmeasure)
    led.value(0)
    val_new = r.value()
    
    if val_old != val_new:
        val_old = val_new
        print('result =', val_new)
    time.sleep_ms(50)