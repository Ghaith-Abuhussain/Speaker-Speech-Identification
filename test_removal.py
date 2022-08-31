
# -*- coding: utf-8 -*-
"""
Created on Fri Aug  9 18:23:19 2019

@author: Sniper 101
"""

import numpy as np
import scipy.io.wavfile as wav
from sklearn import mixture
import matplotlib.pyplot as plt
from ExtractionTheFeatures import extract_features
from ExtractionTheFeaturesforword import extract_featuresforword
import pickle
import os
from silence_removal import remove_silent
import pyaudio
import wave
import math
import struct
import time
from splitTowords import segments
from playsound import play
from silence_remove import cut_silence

Threshold = 150

SHORT_NORMALIZE = (1.0/32768.0)
chunk = 64
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100
swidth = 2

TIMEOUT_LENGTH = 2

f_name_directory = r'/home/pi/final/single_speaker'
def rms(frame):
    count = len(frame) / swidth
    format = "%dh" % (count)
    shorts = struct.unpack(format, frame)

    sum_squares = 0.0
    for sample in shorts:
        n = sample * SHORT_NORMALIZE
        sum_squares += n * n
    rms = math.pow(sum_squares / count, 0.5)
    return rms * 1000

def record():
    print('Noise detected, recording beginning')
    
    current = time.time()
    end = time.time() + TIMEOUT_LENGTH

    while current <= end:

        data = stream.read(chunk,exception_on_overflow=False)
        if rms(data) >= Threshold: end = time.time() + TIMEOUT_LENGTH

        current = time.time()
        rec.append(data)
        #write(b''.join(rec))
        
def write(recording):
    n_files = len(os.listdir(f_name_directory))

    filename = os.path.join(f_name_directory, 'out.wav'.format(n_files))

    wf = wave.open(filename, 'wb')
    wf.setnchannels(CHANNELS)
    wf.setsampwidth(p.get_sample_size(FORMAT))
    wf.setframerate(RATE)
    wf.writeframes(recording)
    wf.close()
    print('Written to file: {}'.format(filename))
    print('Returning to listening')

def listen():
    print('Listening beginning')
    i = 1
    while i<2:
        input = stream.read(chunk,exception_on_overflow=False)
        rms_val = rms(input)
        if rms_val > Threshold:
            record()
            i+=1

def microphone():
    listen()
    recording=b''.join(rec)
    write(recording)

p = pyaudio.PyAudio()
rec = []
stream = p.open(format=FORMAT,
                channels=CHANNELS,
                rate=RATE,
                input=True,
                frames_per_buffer=chunk)
microphone()
stream.stop_stream()
stream.close()
p.terminate()

sr,audio = wav.read("single_speaker/out.wav")
#audio = remove_silent(audio,sr)
audio = remove_silent(audio,sr)
cut_silence()
wav.write("ghaith1.wav",sr,audio)
