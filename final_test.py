# -*- coding: utf-8 -*-
"""
Created on Mon Aug  5 23:40:18 2019

@author: Sniper 101
"""

from pydub import AudioSegment
from pydub.silence import split_on_silence
import numpy as np
import scipy.io.wavfile as wav
from sklearn import mixture
import matplotlib.pyplot as plt
from ExtractionTheFeatures import extract_features
import pickle
import os
import pyaudio
import wave
# recording for 5 seconds
chunk = 64  # Record in chunks of 1024 samples
sample_format = pyaudio.paInt16  # 16 bits per sample
channels = 1
fs = 44100  # Record at 44100 samples per second
seconds = 5
filename = "output1.wav"
p = pyaudio.PyAudio()  # Create an interface to PortAudio

print('Recording')

stream = p.open(format=sample_format,
                channels=channels,
                rate=fs,
                frames_per_buffer=chunk,
                input=True)

frames = []  # Initialize array to store frames

# Store data in chunks for 3 seconds
for i in range(0, int(fs / chunk * seconds)):
    data = stream.read(chunk)
    frames.append(data)

# Stop and close the stream 
stream.stop_stream()
stream.close()
# Terminate the PortAudio interface
p.terminate()

print('Finished recording')

# Save the recorded data as a WAV file
wf = wave.open(filename, 'wb')
wf.setnchannels(channels)
wf.setsampwidth(p.get_sample_size(sample_format))
wf.setframerate(fs)
wf.writeframes(b''.join(frames))
wf.close()

# test the record

fileOftests = os.listdir('DataToTest1')
GMMs_location = "GMMHMM_models/"
Test_Date_location = "DataToTest1/"

for file in fileOftests:
    path = os.path.join(Test_Date_location, file)
    os.remove(path)
    
sound = AudioSegment.from_wav(filename)
chunks = split_on_silence(sound, 
    # must be silent for at least half a second
    min_silence_len=500,

    # consider it silent if quieter than -16 dBFS
    silence_thresh=-35

 )

for i, chunk in enumerate(chunks):
    chunk.export("DataToTest1/chunk_{0}.wav".format(i), format="wav")

fileOftests = os.listdir('DataToTest1')

gmm_files = [os.path.join(GMMs_location,fname) for fname in 
              os.listdir(GMMs_location) if fname.endswith('.gmmhmm')]

speakers   = [fname.split("/")[-1].split(".gmmhmm")[0] for fname 
              in gmm_files]
models=[]
for fname in gmm_files:
    with open(fname, 'rb') as handle:
        models.append(pickle.load(handle))

#tests = "DataToTest1.txt"


 
num_samples = 0.0
error = 0
false=[]
winner = []
for test in fileOftests:
    num_samples += 1.0
    test = test.strip()
    print ("Testing Audio : ", test)
    sr,audio = wav.read(Test_Date_location + test)
    vector   = extract_features(audio,sr)
    log_likelihood = np.zeros(len(models)) 
    for i in range(len(models)):
        gmm    = models[i]  #checking with each model one by one
        scores = np.array(gmm.score(vector))
        log_likelihood[i] = scores.sum()   
    
    winner.append(np.argmax(log_likelihood))
    error += 1

print ("\tdetected as - ")

for k in range(error):
    print (speakers[winner[k]],  end=' ')
    