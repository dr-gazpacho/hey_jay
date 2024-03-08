import time
import board
import synthio
import audiopwmio
import audiomixer
from digitalio import DigitalInOut, Direction, Pull
from adafruit_apds9960.apds9960 import APDS9960
from adafruit_apds9960 import colorutility
#get the first initialization out of the way
i2c = board.STEMMA_I2C()
apds = APDS9960(i2c)
# apds.enable_proximity = True
# apds.enable_gesture = True
apds.enable_color = True
# set up the button
btn = DigitalInOut(board.GP14)
btn.direction = Direction.INPUT
btn.pull = Pull.UP

Dm7=(60, 57)
G7=(55, 59)
Cmaj7=(48, 52)
Am7=(45, 55)

chords=(Dm7, G7, Cmaj7, Am7)
mixer_level=.5

audio = audiopwmio.PWMAudioOut(board.GP2)
mixer = audiomixer.Mixer(channel_count=1, sample_rate=44100, buffer_size=2048)
synth = synthio.Synthesizer(sample_rate=44100)
audio.play(mixer)
mixer.voice[0].play(synth)
mixer.voice[0].level=mixer_level
amp_env = synthio.Envelope(attack_time=3, attack_level=mixer_level, release_time=1)
synth.envelope = amp_env
frequency = 2000
resonance = 1.5
lpf = synth.low_pass_filter(frequency, resonance)


def get_color_data():
    while not apds.color_data_ready:
        time.sleep(0.005)
    r, g, b, c = apds.color_data 
    return r, g, b, c

def get_chord():
    color_data=get_color_data()
    lowest_light_present=min(color_data)
    return chords[color_data.index(lowest_light_present)]
    

#instead of moving tone to tone, maybe just fade one thing in and out over the other
#chuck on an envelope?


lfo = synthio.LFO(rate=0.6, scale=0.05)  # 1 Hz lfo at 0.25%

synth.press(Dm7)
time.sleep(1)
synth.release(Dm7)
synth.press(G7)
time.sleep(1)
synth.release(G7)
synth.press(Cmaj7)
time.sleep(1)
synth.release(Cmaj7)
synth.press(Am7)
time.sleep(1)
synth.release(Am7)

state=0
previous_chord=0
current_chord=0

frequency = 2000
resonance = 1.5
lpf = synth.low_pass_filter(frequency, resonance)

while True:
#   I might use gesture - wait to see if this button feels good
#   gesture = apds.gesture()
    button_value=btn.value
    
    if state is 0:
        if button_value is False:
            state=1
    if state is 1:
        if button_value is True:
            state=2
    if state is 2:
        current_chord=get_chord()
        if current_chord!=previous_chord:
            synth.release(previous_chord)
            synth.press(current_chord)
            previous_chord=current_chord
#         print("color temp {}".format(colorutility.calculate_color_temperature(r, g, b)))
#         print("light lux {}".format(colorutility.calculate_lux(r, g, b)))
#         print("r: {}, g: {}, b: {}, c: {}".format(r, g, b, c))
        state=0
    time.sleep(.05)
    
# TODO
# We know colors are 16 bit values (between 0 and 65k) so map those onto the synth params
# Learn the synth params, so map the values into something sensible
# Write the functions to slowly increase or decrease - or make the one WAY better
