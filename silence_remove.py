# -*- coding: utf-8 -*-
"""
Created on Sun Aug 25 12:00:26 2019

@author: Sniper 101
"""

import pyaudio
import wave
import scipy.io.wavfile as wav
import math
import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import butter, lfilter


def butter_bandpass(lowcut, highcut, fs, order=5):
    nyq = 0.5 * fs
    low = lowcut / nyq
    high = highcut / nyq
    b, a = butter(order, [low, high], btype='band')
    return b, a


def butter_bandpass_filter(data, lowcut, highcut, fs, order=5):
    b, a = butter_bandpass(lowcut, highcut, fs, order=order)
    y = lfilter(b, a, data)
    return y




def cut_silence():
    sr,audio = wav.read("single_speaker/out.wav")

    CHUNK = 1024
    FORMAT = pyaudio.paInt16
    CHANNELS = 1
    RATE = 44100
    RECORD_SECONDS = 0.5
    WAVE_OUTPUT_FILENAME = "voice.wav"
    
    p = pyaudio.PyAudio()
    
    stream = p.open(format=FORMAT,
                    channels=CHANNELS,
                    rate=RATE,
                    input=True,
                    frames_per_buffer=CHUNK)
    
    print("* recording")
    
    frames = []
    
    for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
        data = stream.read(CHUNK,exception_on_overflow=False)
        frames.append(data)

    print("* done recording")

    stream.stop_stream()
    stream.close()
    p.terminate()
        
    wf = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
    wf.setnchannels(CHANNELS)
    wf.setsampwidth(p.get_sample_size(FORMAT))
    wf.setframerate(RATE)
    wf.writeframes(b''.join(frames))
    wf.close()

    sr,Noise = wav.read("voice.wav")


    mu = Noise.mean()
    sd = math.sqrt(Noise.var())
    

    sig = np.zeros(len(audio))
    one_or_zero = np.zeros(len(audio))
    for i in range(0,len(audio)):
        if ((np.abs(audio[i]-mu)/sd) > 3):
            sig[i] = audio[i]
            one_or_zero[i]=1

    segment_length = int(sr*0.01)
    num_segments = int(len(audio)/segment_length)
    frames1= []
    j=1
    print("hello world")
    chunks = np.zeros(num_segments*segment_length)
    sig2 = np.zeros(num_segments*segment_length)
    while j<=num_segments:
        x1 = one_or_zero[(j-1)*segment_length:j*segment_length-1]
        ones = np.sum(x1)
        if (ones >= len(x1)/2):
            frames1 = np.hstack((frames1,sig[(j-1)*segment_length:j*segment_length]))
            chunks[(j-1)*segment_length:j*segment_length-1] = np.ones(segment_length-1)
        j+=1

    plt.plot(audio)
    plt.plot(max(audio)*chunks)
    fs = sr
    lowcut = 300
    highcut = 4000
    y = butter_bandpass_filter(frames1, lowcut, highcut, fs, order=6)
    #wav.write("ghaith.wav",sr,y)
    return y
    
#cut_silence()
