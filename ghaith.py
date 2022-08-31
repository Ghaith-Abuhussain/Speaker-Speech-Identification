# -*- coding: utf-8 -*-
"""
Created on Sun Aug 25 12:00:26 2019

@author: Sniper 101
"""

import record as r
import pyaudio
import wave
import scipy.io.wavfile as wav
import math
import numpy as np
import matplotlib.pyplot as plt

def segments(test):

    sr,audio = wav.read(test)
    Noise = audio[len(audio)-5000:len(audio)-1]
    #plt.plot(Noise)
    mu = Noise.mean()
    sd = math.sqrt(Noise.var())
    
    sig = np.zeros(len(audio))
    one_or_zero = np.zeros(len(audio))
    for i in range(0,len(audio)):
        if ((np.abs(audio[i]-mu)/sd) > 3):
            sig[i] = audio[i]
            one_or_zero[i]=1
            #plt.plot(sig)
            #plt.plot(max(sig)*one_or_zero)
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
            sig2[(j-1)*segment_length:j*segment_length-1] = sig[(j-1)*segment_length:j*segment_length-1]
        j+=1

    #plt.plot(sig2)
#audio1 = b''.join(frames1)
#plt.plot(audio)
#plt.plot(chunks*max(audio))

    i=1
    ind1=0
    word=1
    zerocnt=0
    thresh=20000
    words=[]
    while i < len(chunks):
        if(chunks[i-1]==1 and chunks[i]==0):
            ind2 = i-1
        if(chunks[i]==0 and word==1): zerocnt+=1
        if(zerocnt>=thresh and word==1):
            zerocnt=0
            word=0
            words.append(audio[ind1:ind2])
        if(chunks[i]==1 and word==1):
            zerocnt=0
        if(chunks[i-1]==0 and chunks[i]==1):
            if(word==1):
                if(zerocnt > 0):
                    zerocnt=0
            else:
                word = 1
                ind1 = i
        i+=1

    rms=[]
    l=0
    for w in words:
        rms=len(w)
        if(rms >= 3000):
            wav.write("DataToTest1/chunk_"+str(l)+".wav",sr,w)
            l+=1
    #return chunks,sig2,words
#segments("single_speaker/out.wav")