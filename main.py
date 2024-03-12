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

c_one=(synthio.Note(frequency=260, waveform=wave_tri), synthio.Note(frequency=220, waveform=wave_tri))
c_two=(synthio.Note(frequency=195, waveform=wave_tri), synthio.Note(frequency=247, waveform=wave_tri))
c_three=(synthio.Note(frequency=130, waveform=wave_tri), synthio.Note(frequency=165, waveform=wave_tri))
c_four=(synthio.Note(frequency=110, waveform=wave_tri), synthio.Note(frequency=195, waveform=wave_tri))

lfo_tremolo = synthio.LFO(rate=2 /10, scale=1, offset=0)
lfo_tremolo_two = synthio.LFO(rate=.5 /10, scale=1, offset=0)
lfo_tremolo_three = synthio.LFO(rate=4 / 10, scale=1, offset=0)

a_one=(
        synthio.Note(frequency=586, waveform=wave_sine, amplitude=lfo_tremolo),
        synthio.Note(frequency=784, waveform=wave_saw, amplitude=lfo_tremolo_two),
        synthio.Note(frequency=880, waveform=wave_square, amplitude=lfo_tremolo_three),
    )
a_two=(
        synthio.Note(frequency=784, waveform=wave_tri),
        synthio.Note(frequency=880, waveform=wave_tri),
        synthio.Note(frequency=988, waveform=wave_tri),
    )
a_three=(
        synthio.Note(frequency=784, waveform=wave_tri),
        synthio.Note(frequency=988, waveform=wave_tri),
        synthio.Note(frequency=1319, waveform=wave_tri),
    )
a_four=(
        synthio.Note(frequency=880, waveform=wave_tri),
        synthio.Note(frequency=1047, waveform=wave_tri),
        synthio.Note(frequency=1319, waveform=wave_tri),
    )


chords=(c_one, c_two, c_three, c_four)
mixer_level=.8

audio=audiopwmio.PWMAudioOut(board.GP2)
mixer=audiomixer.Mixer(channel_count=1, sample_rate=44100, buffer_size=2048)
synth=synthio.Synthesizer(sample_rate=44100)
audio.play(mixer)
mixer.voice[0].play(synth)
mixer.voice[0].level=mixer_level
amp_env = synthio.Envelope(attack_time=3, attack_level=mixer_level, release_time=3)
synth.envelope = amp_env
frequency=2000
resonance=1.5
lpf = synth.low_pass_filter(frequency, resonance)

synth.press(a_one)

# synth.release_all_then_press(c_one)
# time.sleep(10)
# synth.release_all_then_press(c_two)
# time.sleep(10)
# synth.release_all_then_press(c_three)
# time.sleep(10)
# synth.release_all_then_press(c_four)
# time.sleep(10)


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

state=0
previous_chord=0
current_chord=0

frequency = 2000
resonance = 1.5
lpf = synth.low_pass_filter(frequency, resonance)
# current_chord[1].filter=lpf assign filters to the Note object

while True:
#   I might use gesture - wait to see if this button feels good
#   gesture = apds.gesture()
    button_value=btn.value
#     synth.release_all_then_press(c_one)
#     time.sleep(10)
#     synth.release_all_then_press(c_two)
#     time.sleep(10)
#     synth.release_all_then_press(c_three)
#     time.sleep(10)
#     synth.release_all_then_press(c_four)
#     time.sleep(10)
    
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
            previous_chord=current_chord
            synth.press(current_chord)
            # synth.release_all_then_press(current_chord)
#         print("color temp {}".format(colorutility.calculate_color_temperature(r, g, b)))
#         print("light lux {}".format(colorutility.calculate_lux(r, g, b)))
#         print("r: {}, g: {}, b: {}, c: {}".format(r, g, b, c))
        state=0
    time.sleep(.05)
    
# TODO
# We know colors are 16 bit values (between 0 and 65k) so map those onto the synth params
# Learn the synth params, so map the values into something sensible
# Write the functions to slowly increase or decrease - or make the one WAY better
