# -*- coding: utf-8 -*-
"""
Created on Thu Jul 25 13:43:25 2019

@author: Sniper 101
"""

import numpy as np
import scipy.io.wavfile as wav
from sklearn import mixture
import matplotlib.pyplot as plt
from ExtractionTheFeatures import extract_features
import pickle
from silence_removal import remove_silent
import os


folder_data = "DataToTrain/karammahfood/"
GMMs_location = "GMM_models/"
training_files = "Data_names_word.txt"


files = os.listdir(folder_data)
        

file_counter = 1
features = np.asarray(())

for file in files:
    file = file.strip()

    # read audio signal
    L=folder_data+file
    print(L)
    sr,audio = wav.read(L)
    audio = remove_silent(audio,sr)
    # extract the feature matrix for each udio file 40 features each row
    vector = extract_features(audio,sr)
    
    if features.size == 0:
        features = vector
    else:
        features = np.vstack((features, vector))
    
    if file_counter == 6:
        gmm = mixture.GaussianMixture(n_components = 16 ,max_iter = 400 ,tol = 0.0001,covariance_type = 'diag',n_init = 9)
        gmm.fit(features)
        
        nameOfgaussian = file.split("_")[0]+".gmm"
        filename = GMMs_location + nameOfgaussian
        with open(filename, 'wb') as handle:
            pickle.dump(gmm, handle, protocol=pickle.HIGHEST_PROTOCOL)
        print ('modeling completed for speaker:',file.split("_")[0]," with data point = ",features.shape)    
        features = np.asarray(())
        file_counter = 0
    file_counter = file_counter + 1 


    
