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

# Dm7
c_four=60
a_three=57
f_three=53
d_three=50
Dm7=(c_four, a_three, f_three, d_three)

# G7
g_three=55
b_three=59
d_four=62
f_four=65
G7=(g_three, b_three, d_four, f_four)

#Cmaj7
b_three=59
g_three=55
e_three=52
c_three=48
Cmaj7=(b_three, g_three, e_three, c_three)

#Am7
a_two=45
c_three=48
e_three=52
g_three=55
Am7=(45, 48, 52, 55)

chords=(Dm7, G7, Cmaj7, Am7)

audio = audiopwmio.PWMAudioOut(board.GP2)
mixer = audiomixer.Mixer(channel_count=1, sample_rate=44100, buffer_size=2048)
synth = synthio.Synthesizer(sample_rate=44100)
audio.play(mixer)
mixer.voice[0].play(synth)
mixer.voice[0].level = 0.5
amp_env = synthio.Envelope(attack_time=0.05, sustain_level=0.2, release_time=0.5)
synth.envelope = amp_env

def getColorData():
    while not apds.color_data_ready:
        time.sleep(0.005)
    r, g, b, c = apds.color_data 
    return r, g, b, c

#when I change chords, which direction do we move the synth?
def getChordChangeDirection(cur, dest):
    one_up=cur[0]<dest[0]
    two_up=cur[1]<dest[1]
    three_up=cur[2]<dest[2]
    four_up=cur[3]<dest[3]
    return one_up, two_up, three_up, four_up

# where current is index of current chord and destination is well.. the destination
def changeChords(current, destination, chords):
    if current==destination:
        return
    current_chord=list(chords[current])
    destination_chord=list(chords[destination])
    one_up, two_up, three_up, four_up=getChordChangeDirection(current_chord, destination_chord)
    chord_two=chords[current]
    while tuple(current_chord)!=tuple(destination_chord):
        synth.release(current_chord)
        if current_chord[0]!=destination_chord[0]:
            if one_up:
                current_chord[0]=int(((current_chord[0] * 10) + 10) / 10)
            else: current_chord[0]=int(((current_chord[0] * 10) - 10) / 10)
        if current_chord[1]!=destination_chord[1]:
            if two_up:
                current_chord[1]=int(((current_chord[1] * 10) + 10) / 10)
            else: current_chord[1]=int(((current_chord[1] * 10) - 10) / 10)
        if current_chord[2]!=destination_chord[2]:
            if two_up:
                current_chord[2]=int(((current_chord[2] * 10) + 10) / 10)
            else: current_chord[2]=int(((current_chord[2] * 10) - 10) / 10)
        if current_chord[3]!=destination_chord[3]:
            if two_up:
                current_chord[3]=int(((current_chord[3] * 10) + 10) / 10)
            else: current_chord[3]=int(((current_chord[3] * 10) - 10) / 10)
        synth.press(current_chord)
        time.sleep(.005)
    print("done")
        
changeChords(1, 2, chords)
time.sleep(1)
changeChords(2, 3, chords)
time.sleep(1)
changeChords(3, 0, chords)
time.sleep(1)

lfo = synthio.LFO(rate=0.6, scale=0.05)  # 1 Hz lfo at 0.25%

# synth.press(Dm7)
# time.sleep(1)
# synth.release(Dm7)
# synth.press(G7)
# time.sleep(1)
# synth.release(G7)
# synth.press(Cmaj7)
# time.sleep(1)
# synth.release(Cmaj7)
# synth.press(Am7)
# time.sleep(1)
# synth.release(Am7)

state=0

while True:
#     I might use gesture - wait to see if this button feels good
#     gesture = apds.gesture()
    button_value=btn.value
    if state is 0:
        if button_value is False:
            state=1
    if state is 1:
        if button_value is True:
            state=2
    if state is 2:
        r, g, b, c = getColorData()
        print("color temp {}".format(colorutility.calculate_color_temperature(r, g, b)))
        print("light lux {}".format(colorutility.calculate_lux(r, g, b)))
        print("r: {}, g: {}, b: {}, c: {}".format(r, g, b, c))
        state=0
    time.sleep(.05)
    
# TODO
# We know colors are 16 bit values (between 0 and 65k) so map those onto the synth params
# Learn the synth params, so map the values into something sensible
# Write the functions to slowly increase or decrease - or make the one WAY better
