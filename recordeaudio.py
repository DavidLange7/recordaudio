#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Apr  2 13:14:09 2022

@author: david
"""

import pyaudio
import numpy as np
import matplotlib.pyplot as plt
from scipy.fft import rfft, rfftfreq

#this is for printing all the available input microphones (a bunch of errors are printed, but it doesnt matter ..)
p = pyaudio.PyAudio()
info = p.get_host_api_info_by_index(0)
numdevices = info.get('deviceCount')
for i in range(0, numdevices):
        if (p.get_device_info_by_host_api_device_index(0, i).get('maxInputChannels')) > 0:
            print ("Input Device id ", i, " - ", p.get_device_info_by_host_api_device_index(0, i).get('name'))
            
#%%
CHUNK = 8192 # number of data points to read at a time
RATE = 44100 # time resolution of the recording device (Hz)

p=pyaudio.PyAudio()
stream=p.open(format=pyaudio.paInt16,channels=1,rate=RATE,input=True,
              frames_per_buffer=CHUNK,input_device_index=6)

data = np.fromstring(stream.read(CHUNK,exception_on_overflow = False),dtype=np.int16)

fig, (ax3, ax4) = plt.subplots(2)

line3, = ax3.plot(data,'r-')
psi = rfft(data)
freq_sp = np.linspace(0, RATE/2.0, len(psi))
line4, = ax4.plot(np.linspace(0, RATE/2.0, len(psi)),(psi/max(psi)))

#maybe try plt.magnitude_spectrum(psi,Fs = 4097,sides='twosided')[1], to get the frequeny range

for i in range(100):
    data = np.fromstring(stream.read(CHUNK,exception_on_overflow = False),dtype=np.int16)
    line3.set_ydata(data)
    psi = rfft(data)
    line4.set_ydata(psi/max(psi))
    #line4.set_xdata(freq_sp)
    ax3.set_ylim([-3000, 3000])
    ax4.set_ylim([0, 1.1])
    ax4.set_xlim([0,1000])
    fig.canvas.draw()
    fig.canvas.flush_events()
    plt.pause(0.01)
    
stream.stop_stream()
stream.close()
p.terminate()