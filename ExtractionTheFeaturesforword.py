# -*- coding: utf-8 -*-
"""
Created on Sun Aug 18 21:51:12 2019

@author: Sniper 101
"""

# -*- coding: utf-8 -*-
"""
Created on Mon Jul 22 23:11:22 2019

@author: Sniper 101
"""
from sklearn import preprocessing
import numpy as np
from sklearn import mixture
import scipy.io.wavfile as wav
import python_speech_features as features
import matplotlib.pyplot as plt

""" This function is To extract the mfcc and the delta_mfcc features and combine them with each others"""
def delta_MFCC(feat):
    rows,clomns = feat.shape
    D_mfcc = np.zeros((rows,13))
    N=2
    g = [1 , 4]
    s = 2*sum(g)

    for t in range(rows):
        n = 1
        while n <= N:
            first_vector_index = max(t-n , 0)
            second_vector_index = min(t+n , rows-1)
            D_mfcc[t] +=  (n*(feat[second_vector_index]-feat[first_vector_index]))/s
            n+=1
    return D_mfcc
    
    
    
def extract_featuresforword(audio,rate):    
    
    mfcc_feature = preprocessing.scale( features.mfcc(audio,rate, winlen = 0.015,winstep = 0.0075,numcep = 13,nfilt =46,nfft = 1200, appendEnergy = True,winfunc=np.hamming))  
    rows,clomns = mfcc_feature.shape
    D_mfcc = delta_MFCC(mfcc_feature)
    
    combined = np.hstack((mfcc_feature,D_mfcc))
    
    return combined

    


        
        
        
        