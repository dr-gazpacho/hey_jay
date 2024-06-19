# hey_jay
I wanted to make the light sing.

## This is only possible with the great work of literally everyone else
You're gonna need this, I installed mine with Thonny, but one way or another you need to install this library after you installed Circuit Python
- https://github.com/adafruit/Adafruit_CircuitPython_APDS9960
This little program relies on Synthio - it's a super rad part of Circuit Python
- https://learn.adafruit.com/audio-synthesis-with-circuitpython-synthio/overview?gad_source=1&gclid=Cj0KCQjw4MSzBhC8ARIsAPFOuyVt3TkldHVSHByX8WePLlkY1TtWVS5IaBSWcsrIdmO11f7y1o3PGMkaAh2JEALw_wcB

## Starting up from scrach with a brand new Pico?
I'll be real with you, I'm gonna be super vauge here and just give you the broad strokes of what you need to do. How you do it is entirely up to you.
1. Load the circuit python firmware onto your pico (you can get this from Adafruit directly or use the version I have in the repo)
1. Flash code.py onto the pico
1. Install the circuit python apds9960 onto the pico to use the sensor without the hell
1. Discover that the pico doesn't have enough memory to install all the packages. This is probably fine...
1. Run it.
1. Rejoice
1. Battery of light is just a little program i wrote to trigger different color LEDs to test this thing out, it's all whatever man
