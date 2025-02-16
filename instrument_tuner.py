#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Apr  2 13:14:09 2022

@author: david
"""

'''
This code can be used to tune any instrument, as reference I use the middle C (C4 on piano),
but can be changed quite easily. Then I also plot the harmonics, for more reference. 
There is still a mistake with harmonics to frequency, since the fundamental seems not to correspond
correctly, however it should correspond to harmonics, could be fixed later but already works, 
simply use harmonics to tune the instrument..

the important parameter here is "device_index", which should correspond to the mic input you want!
'''

import pyaudio
import numpy as np
import matplotlib.pyplot as plt
from scipy.fft import rfft, rfftfreq 


p = pyaudio.PyAudio()
info = p.get_host_api_info_by_index(0)
numdevices = info.get('deviceCount')
for i in range(0, numdevices):
    device_info = p.get_device_info_by_host_api_device_index(0, i)
    if device_info.get('maxInputChannels') > 0:
        print(f"Input Device id {i} - {device_info.get('name')}, Max Channels: {device_info.get('maxInputChannels')}")

#%%
CHUNK = 8192  # number of data points to read at a time
RATE = 44100  # time resolution of the recording device (Hz)

device_index = 1
channels = 1

p = pyaudio.PyAudio()
stream = p.open(format=pyaudio.paInt16, channels=channels, rate=RATE, input=True,
                frames_per_buffer=CHUNK, input_device_index=device_index)

fig, (ax3, ax4) = plt.subplots(2)
data = np.frombuffer(stream.read(CHUNK, exception_on_overflow=False), dtype=np.int16)

line3, = ax3.plot(data, 'r-')
psi = rfft(data)
freq_sp = rfftfreq(len(data), 1 / RATE)
line4, = ax4.plot(freq_sp, np.abs(psi) / np.max(np.abs(psi)))


# so i use the Middle C frequency (C4 on piano) in Hz and its harmonics as my measure
middle_c_freq = 261.63
harmonics = [middle_c_freq * (i + 1) for i in range(5)]

for harmonic in harmonics:
    ax4.axvline(harmonic, color='g', linestyle='--', label=f'Harmonic {harmonics.index(harmonic) + 1} ({harmonic:.2f} Hz)')

ax3.set_ylim([-30000, 5000])
ax4.set_ylim([0, 1.1])
ax4.set_xlim([0, 2000])

for i in range(1000):
    data = np.frombuffer(stream.read(CHUNK, exception_on_overflow=False), dtype=np.int16)
    line3.set_ydata(data)
    
    psi = rfft(data)
    line4.set_ydata(np.abs(psi) / np.max(np.abs(psi)))
    
    fig.canvas.draw()
    fig.canvas.flush_events()
    plt.pause(0.01)

stream.stop_stream()
stream.close()
p.terminate()