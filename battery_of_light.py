import board
import digitalio
import time

led = digitalio.DigitalInOut(board.LED)
led.direction = digitalio.Direction.OUTPUT

white = digitalio.DigitalInOut(board.GP2)
white.direction = digitalio.Direction.OUTPUT

blue = digitalio.DigitalInOut(board.GP3)
blue.direction = digitalio.Direction.OUTPUT

green = digitalio.DigitalInOut(board.GP4)
green.direction = digitalio.Direction.OUTPUT

red = digitalio.DigitalInOut(board.GP5)
red.direction = digitalio.Direction.OUTPUT

while True:
    white.value = True
    blue.value = True
    green.value = True
    red.value = True
    time.sleep(10)
    white.value = False
    blue.value = False
    green.value = False
    red.value = False
    white.value = True
    time.sleep(10)
    white.value = False
    blue.value = True
    time.sleep(10)
    blue.value = False
    green.value = True
    time.sleep(10)
    green.value = False
    red.value = True
    time.sleep(10)
    red.value = False

