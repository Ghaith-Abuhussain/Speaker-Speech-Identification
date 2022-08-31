
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
    
  
    

t = 0
while (t != 1):
    print("please define your identity")
    # whait the permession
    play("/home/pi/final/confirms/confirm_identity.wav")
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
    # test the record
    
    GMMs_location = "GMM_models/"
    #Test_Date_location = "DataToTest/"
    
    gmm_files = [os.path.join(GMMs_location,fname) for fname in 
                 os.listdir(GMMs_location) if fname.endswith('.gmm')]
    
    speakers   = [fname.split("/")[-1].split(".gmm")[0] for fname 
                  in gmm_files]
    models=[]
    for fname in gmm_files:
        with open(fname, 'rb') as handle:
            models.append(pickle.load(handle))


    #fileOftests = open(tests,'r')
    num_samples = 0.0
    error = 0
    false=[]
    num_samples += 1.0
    test = "single_speaker/out.wav"
    print ("Testing Audio : ", test)
    sr,audio = wav.read(test)
    #audio = remove_silent(audio,sr)
    audio = remove_silent(audio,sr)
    #audio = cut_silence()
    vector   = extract_features(audio,sr)
    log_likelihood = np.zeros(len(models)) 
    for i in range(len(models)):
        gmm    = models[i]  #checking with each model one by one
        scores = np.array(gmm.score(vector))
        log_likelihood[i] = scores.sum()   
    winner = np.argmax(log_likelihood)
    cheker_name = "ghaith"
    if (speakers[winner] == cheker_name ):
        play("/home/pi/final/confirms/true_confirm.wav")
        print ("The Detection is Right")
        #t = 1
    else:
        print ("False Detection")
        play("/home/pi/final/confirms/false_confirm.wav")









#voicecommand ={"browseropen","computerclose","savefilepathtwo","openprogramone" }
voicecommand = open("orders.txt","r")
voicecommand = voicecommand.read().splitlines()
check=0
while(check!=1):
    voicecommand = open("orders.txt","r")
    voicecommand = voicecommand.read().splitlines()
    print("please enter your command")
    play("/home/pi/final/confirms/confirm_command.wav")
    # recording for 5 seconds
    file9 = os.listdir("DataToTest1")
    for fil in file9:
        os.remove("DataToTest1/"+fil)
    
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
    
    # test the record
    

    fileOftests = os.listdir('DataToTest1')
    GMMHMMs_location = "GMMHMM_models/"
    Test_Date_location = "DataToTest1/"

    for file in fileOftests:
        path = os.path.join(Test_Date_location, file)
        os.remove(path)
    segments("single_speaker/out.wav")
    f = os.listdir('DataToTest1')
    if(len(f)!=0):
        os.remove("DataToTest1/chunk_0.wav")
    fileOftests = os.listdir('DataToTest1')
    fileOftests.sort()

    gmmhmm_files = [os.path.join(GMMHMMs_location,fname) for fname in 
                 os.listdir(GMMHMMs_location) if fname.endswith('.gmmhmm')]

    words   = [fname.split("/")[-1].split(".gmmhmm")[0] for fname 
                  in gmmhmm_files]
    models=[]
    for fname in gmmhmm_files:
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
        vector   = extract_featuresforword(audio,sr)
        log_likelihood = np.zeros(len(models)) 
        for i in range(len(models)):
            gmmhmm    = models[i]  #checking with each model one by one
            scores = np.array(gmmhmm.score(vector))
            log_likelihood[i] = scores.sum()   
    
        winner.append(np.argmax(log_likelihood))
        error += 1

    print ("\tdetected as - ")
    order =""
    ord_index=-1
    truecommand=0
    for k in range(error):
        order +=words[winner[k]]
        print (words[winner[k]],  end=' ')
    print("\n")

    for command in voicecommand:
        print(command)
        ord_index +=1
        if(command==order):
            truecommand=1
            break
    print(ord_index)

    terminalcommand = open("terminal_orders.txt","r")
    terminalcommand = terminalcommand.read().splitlines()
    length = -1
    for termcom in terminalcommand:
        length+=1
    print(length)
    if(truecommand==0):
        print("the command is not defined select another command \n")
        play("/home/pi/final/confirms/command_false.wav")
    else:
        print("the order has been executed")
        play("/home/pi/final/confirms/command_true.wav")
        print(ord_index)
        if(ord_index > 0 & ord_index <= length):
            os.system(terminalcommand[ord_index])
        if(ord_index == 0):
            check=1

