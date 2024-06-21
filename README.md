# Hey Jay

## Intro
You will make the light sing. You’re going to assemble a Hey Jay, a little device that I like to think of as a reverse light organ. Once it’s assembled and powered up, you can wave your hand close to the device and trigger the motion sensor. Then, the microcontroller takes a sample of the ambient light from the sensor, maps the measurements onto a digital synthesizer, and finally it outputs the music to an ⅛” headphone jack. Think of it like a sort of digital wind chime that plays when you strum the light.

## What This Kit Includes
- 1x Raspberry Pi Pico H
- 1x Breadboard
- 2x 1k resistors (one for the build, one spare)
- 2x 0.1 100nF ceramic capacitors (one for the build, one spare)
- 1x APDS-9960 Light and Motion Sensor
- 1x TRRS Jack
- 1x Micro USB/USB C Cable
- 1x Pair of Earbuds
- Jumper wire

## More on the Individual Components
### Raspberry Pi Pico pre-mounted on a breadboard

Raspberry Pi makes wonderful little computers for hobbyists. [The Pico is their microcontroller](https://www.raspberrypi.com/documentation/microcontrollers/raspberry-pi-pico.html), a small but powerful integrated circuit that has tons of open source support, projects, and help. It is the brains of our project, and where the software runs. It communicates with the two attached devices, the APDS-9960 and the TRRS Jack.

![pico pinout](./images/Pico-R3-A4-Pinout.pdf "Raspberri Pi Pico Pinout Diagram")

All the actual programming and software is done, so you’ll only need to worry about the assembly. But, knowing how the guts work is half the fun. The software only uses a few of the pins on the Pico for this project: the 3V3 power output and ground pins to pull electricity through the circuit, the SDA and SCL pins to communicate with the APDS-9960, and a general purpose pin to output the audio.

[The Pico is already embedded in a breadboard](https://learn.sparkfun.com/tutorials/how-to-use-a-breadboard/all?gad_source=1&gclid=CjwKCAjwg8qzBhAoEiwAWagLrCOuPgeaCGzUKGcsefkz8sO2QxBlmTG8HAUSbq4eaGX5hsJnfJ0WjBoCZXoQAvD_BwE), a small development board that lets you easily assemble electronics without solder. The breadboard I’ve included is printed specially for the Pico, you’ll note that each row on the board is numbered/lettered to correspond to the pinout diagram. 



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
