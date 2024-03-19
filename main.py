import time
import board
import synthio
import audiopwmio
import audiomixer
from digitalio import DigitalInOut, Direction, Pull
from adafruit_apds9960.apds9960 import APDS9960
from adafruit_apds9960 import colorutility
import ulab.numpy as np
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

SAMPLE_SIZE = 1024
SAMPLE_VOLUME = 32000  # 0-32767
half_period = SAMPLE_SIZE // 2

wave_sine = np.array(np.sin(np.linspace(0, 2*np.pi, SAMPLE_SIZE, endpoint=False)) * SAMPLE_VOLUME,dtype=np.int16)
wave_saw = np.linspace(SAMPLE_VOLUME, -SAMPLE_VOLUME, num=SAMPLE_SIZE, dtype=np.int16)
wave_tri = np.concatenate((np.linspace(-SAMPLE_VOLUME, SAMPLE_VOLUME, num=half_period, dtype=np.int16), np.linspace(SAMPLE_VOLUME, -SAMPLE_VOLUME, num=half_period, dtype=np.int16)))
wave_square = np.concatenate((np.full(half_period, SAMPLE_VOLUME, dtype=np.int16), np.full(half_period, -SAMPLE_VOLUME, dtype=np.int16)))

lfo_tremolo_one = synthio.LFO(rate=2 / 20, scale=.5, offset=0)
lfo_tremolo_two = synthio.LFO(rate=.5 / 20, scale=.5, offset=0)
lfo_tremolo_three = synthio.LFO(rate=4 / 20, scale=.5, offset=0)

c_one=(synthio.Note(frequency=260, waveform=wave_tri), synthio.Note(frequency=220, waveform=wave_tri))
c_two=(synthio.Note(frequency=195, waveform=wave_tri), synthio.Note(frequency=247, waveform=wave_tri))
c_three=(synthio.Note(frequency=130, waveform=wave_tri), synthio.Note(frequency=165, waveform=wave_tri))
c_four=(synthio.Note(frequency=110, waveform=wave_tri), synthio.Note(frequency=195, waveform=wave_tri))

t_one=(
        synthio.Note(frequency=586, waveform=wave_tri, amplitude=lfo_tremolo_one),
        synthio.Note(frequency=784, waveform=wave_tri, amplitude=lfo_tremolo_two),
        synthio.Note(frequency=880, waveform=wave_tri, amplitude=lfo_tremolo_three),
    )
t_two=(
        synthio.Note(frequency=784, waveform=wave_tri, amplitude=lfo_tremolo_one),
        synthio.Note(frequency=880, waveform=wave_tri, amplitude=lfo_tremolo_two),
        synthio.Note(frequency=988, waveform=wave_tri, amplitude=lfo_tremolo_three),
    )
t_three=(
        synthio.Note(frequency=784, waveform=wave_tri, amplitude=lfo_tremolo_one),
        synthio.Note(frequency=988, waveform=wave_tri, amplitude=lfo_tremolo_two),
        synthio.Note(frequency=1319, waveform=wave_tri, amplitude=lfo_tremolo_three),
    )
t_four=(
        synthio.Note(frequency=880, waveform=wave_tri, amplitude=lfo_tremolo_one),
        synthio.Note(frequency=1047, waveform=wave_tri, amplitude=lfo_tremolo_two),
        synthio.Note(frequency=1319, waveform=wave_tri, amplitude=lfo_tremolo_three),
    )

b_one=synthio.Note(frequency=260, waveform=wave_tri)
b_two=synthio.Note(frequency=195, waveform=wave_tri)
b_three=synthio.Note(frequency=130, waveform=wave_tri)
b_four=synthio.Note(frequency=110, waveform=wave_tri)


chords=(c_one, c_two, c_three, c_four)
twinkles=(t_one, t_two, t_three, t_four)
bassi=(b_one, b_two, b_three, b_four)
freaks=[0, 1000, 20000, 30000, 40000, 50000]
waves=[wave_sine, wave_saw, wave_tri, wave_square]

mixer_level=.8

audio=audiopwmio.PWMAudioOut(board.GP2)
mixer=audiomixer.Mixer(channel_count=1, sample_rate=88200, buffer_size=4092)
synth=synthio.Synthesizer(sample_rate=88200)
audio.play(mixer)
mixer.voice[0].play(synth)
mixer.voice[0].level=mixer_level
amp_env = synthio.Envelope(attack_time=3, attack_level=mixer_level, release_time=3)
synth.envelope = amp_env

def get_color_data():
    while not apds.color_data_ready:
        time.sleep(0.005)
    r, g, b, c = apds.color_data 
    return r, g, b, c

def get_chord(color_data):
    lowest_light_present=min(color_data)
    return chords[color_data.index(lowest_light_present)]

def get_twinkle(color_data):
    largest_light_present=max(color_data)
    return twinkles[largest_light_present%4]

def get_bass(color_data):
    lowest_light_present=min(color_data)
    return bassi[color_data.index(lowest_light_present)]

def get_bend_and_pass_filter(color_data):
    r, g, b, c=color_data
    lux=colorutility.calculate_lux(r, g, b)
    length=len(str(c))
    return synthio.LFO(rate=lux, scale=.5, offset=0), synth.low_pass_filter(freaks[length])

def get_the_temp_and_twist_it(color_data):
    r, g, b, c=color_data
    temp=colorutility.calculate_color_temperature(r, g, b)
    the_last_leg=0
    if(temp > 5000):
        the_last_leg=3
    elif(temp > 3500):
        the_last_leg=2
    elif(temp > 2000):
        the_last_leg=1
    return synthio.Note(frequency=24, waveform=waves[the_last_leg], amplitude=lfo_tremolo_two)

state=0
previous_chord=0
current_chord=0
previous_twinkle=0
current_twinkle=0
current_bass=0
previous_bass=0
bend=0
pass_filter=0
temp=0
previous_temp=0

while True:
#   I might use gesture - wait to see if this button feels good
#   gesture = apds.gesture()
    button_value=btn.value
    
    if state is 0:
        if button_value is False: # gesture > 0:
            state=1
    if state is 1:
        if button_value is True: # gesture == 0:
            state=2
    if state is 2:
        color_data=get_color_data()
        bend, pass_filter=get_bend_and_pass_filter(color_data);
        current_chord=get_chord(color_data)
        current_twinkle=get_twinkle(color_data)
        current_bass=get_bass(color_data)
        current_temp=get_the_temp_and_twist_it(color_data)
        if current_chord!=previous_chord:
            synth.release(previous_chord)
            current_chord[1].filter=pass_filter
            previous_chord=current_chord
            synth.press(current_chord)
        if current_twinkle!=previous_twinkle:
            synth.release(previous_twinkle)
            previous_twinkle=current_twinkle
            synth.press(current_twinkle)
        if temp!=previous_temp:
            synth.release(previous_temp)
            previous_temp=current_temp
            synth.press(current_temp)

        synth.release(previous_bass)
        current_bass.bend=bend
        previous_bass=current_bass
        synth.press(current_bass)
        
        state=0
    time.sleep(.05)
    
# TODO
# do something with color temp
