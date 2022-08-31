# -*- coding: utf-8 -*-
"""
Created on Wed Jul 24 11:58:45 2019

@author: Sniper 101
"""

from sklearn import preprocessing
import numpy as np
from sklearn import mixture
import scipy.io.wavfile as wav
import python_speech_features as mfcc
import matplotlib.pyplot as plt
from scipy.signal import butter, lfilter
import librosa


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
def cut_silent(audio,sr):
    frame_size = np.int(0.01 * sr)
    num_frames = np.int(np.floor(len(audio)/frame_size) + 1)
    i = np.int(1)
    s = np.int(0)
    Sum = np.float64(0)
    B=[]
    E = np.zeros((num_frames,1))
    while i <= num_frames:
        R=[]
        if (i*frame_size-1 <= len(audio)):
            y = np.float64(audio[(i-1)*frame_size : i*frame_size-1])
            R = y*y
        else:
            y = np.float64(audio[(i-1)*frame_size:len(audio)])
            R = y*y
        B.append(R);
        E[s] = sum(R) / frame_size
        s+=1
        i+=1
    M = np.mean(E)
    V = np.sqrt(np.var(E))
    mi = np.min(E)
    T = np.float64(mi + 0.01*(M-mi))
    sig2=np.zeros((len(audio),1))
    sig=[]
    n=1
    while n <= len(E):
        if(E[n-1] > T):
            if(n*frame_size-1 <= len(audio)):
                sig2 =audio[(n-1)*frame_size : n*frame_size-1]
            else:
                sig2 =audio[(n-1)*frame_size : len(audio)]
            sig = np.hstack((sig,sig2))
        n+=1
    return sig

def remove_silent(audio,sr):    
    fs = sr
    lowcut = 300
    highcut = 4000
    a = np.array(audio, dtype=float)
    #y_term = librosa.effects.trim(a,top_db=20,frame_length=512,hop_length=128)
    y = butter_bandpass_filter(a, lowcut, highcut, fs, order=6)
    signal=cut_silent(y,sr)
    return signal

"""
sr,audio = wav.read("ghaith_1.wav")
#plt.plot(audio)
audio = remove_silent(audio,sr)
plt.plot(audio)
"""

        
    




"""
frame_size = np.int(0.01 * sr)
    num_frames = np.int(np.floor(len(audio)/frame_size) + 1)
    i = np.int(1)
    s = np.int(0)
    Sum = np.float64(0)
    B=[]
    E = np.zeros((num_frames,1))
    while i <= num_frames:
        R=[]
        if (i*frame_size-1 <= len(audio)):
            y = np.float64(audio[(i-1)*frame_size : i*frame_size-1])
            R = y*y
        else:
            y = np.float64(audio[(i-1)*frame_size:len(audio)])
            R = y*y
        B.append(R);
        E[s] = sum(R) / frame_size
        s+=1
        i+=1
    M = np.mean(E)
    V = np.sqrt(np.var(E))
    mi = np.min(E)
    T = np.float64(mi + 0.01*(M-mi))
    sig2=np.zeros((len(audio),1))
    sig=[]
    n=1
    while n <= len(E):
        if(E[n-1] > T):
            if(n*frame_size-1 <= len(audio)):
                sig2 =audio[(n-1)*frame_size : n*frame_size-1]
            else:
                sig2 =audio[(n-1)*frame_size : len(audio)]
            sig = np.hstack((sig,sig2))
        n+=1
"""