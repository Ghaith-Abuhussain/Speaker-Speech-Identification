# -*- coding: utf-8 -*-
"""
Created on Thu Jul 25 21:57:01 2019

@author: Sniper 101
"""

import numpy as np
import scipy.io.wavfile as wav
from sklearn import mixture
import matplotlib.pyplot as plt
from ExtractionTheFeatures import extract_features
import pickle
import os
from silent import remove_all_silent
from silence_removal import remove_silent


GMMs_location = "GMM_models/"
Test_Date_location = "DataToTest/"

gmm_files = [os.path.join(GMMs_location,fname) for fname in 
              os.listdir(GMMs_location) if fname.endswith('.gmm')]

speakers   = [fname.split("/")[-1].split(".gmm")[0] for fname 
              in gmm_files]
models=[]
for fname in gmm_files:
    with open(fname, 'rb') as handle:
        models.append(pickle.load(handle))

tests = os.listdir('DataToTest')

#fileOftests = open(tests,'r')
num_samples = 0.0
error = 0
false=[]
for test in tests:
    num_samples += 1.0
    test = test.strip()
    print ("Testing Audio : ", test)
    sr,audio = wav.read(Test_Date_location + test)
    #audio = remove_silent(audio,sr)
    audio = remove_silent(audio,sr)
    vector   = extract_features(audio,sr)
    log_likelihood = np.zeros(len(models)) 
    for i in range(len(models)):
        gmm    = models[i]  #checking with each model one by one
        scores = np.array(gmm.score(vector))
        log_likelihood[i] = scores.sum()   
    winner = np.argmax(log_likelihood)
    print ("\tdetected as - ", speakers[winner])
    checker_name = test.split("_")[0]
    if speakers[winner] != checker_name:
        error += 1
        false.append((speakers[winner],checker_name))
print (error, num_samples)
accuracy = ((num_samples - error) / num_samples) * 100
print("The Accuracy Percentage for the current testing Performance with MFCC + delta MFCC + GMM is : ", accuracy, "%")
