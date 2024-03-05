import time
import board
import digitalio
import synthio
import audiopwmio
import audiomixer
import busio
from adafruit_register import i2c_bit
from adafruit_bus_device import i2c_device
from adafruit_apds9960.apds9960 import APDS9960

audio = audiopwmio.PWMAudioOut(board.GP2)
mixer = audiomixer.Mixer(channel_count=1, sample_rate=22050, buffer_size=2048)
synth = synthio.Synthesizer(sample_rate=22050)
audio.play(mixer)
mixer.voice[0].play(synth)
mixer.voice[0].level = 0.1
amp_env = synthio.Envelope(attack_time=0.05, sustain_level=0.2, release_time=0.5)
# 
# while True:
#     synth.envelope = amp_env
#     synth.press(46)
#     time.sleep(1.25)                
#     synth.release(46)
#     time.sleep(1.25)

i2c = board.STEMMA_I2C()
apds = APDS9960(i2c)

apds.enable_color = True
synth.envelope = amp_env
synth.press(42)  

while True:
    while not apds.color_data_ready:
        time.sleep(0.005)

    r, g, b, c = apds.color_data
    print("r: {}, g: {}, b: {}, c: {}".format(r, g, b, c))
  