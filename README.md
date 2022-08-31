# Speaker-Speech-Identification
The aim of this project is speaker recognition (depending on GMM "Gaussian Mixture Model") and speech recognition "isolated words" depending on HMM-GMM model
This Project consists of two parts: speaker recognition and speech recognition (isolated words).
The speaker recognition part is done using the GMM model depending on the MFCC features. First, the model was trained using the VoxFroge dataset. The training process was on 654 speaker (500 male and 154 female). The system acheived accuercy reached to 96.65%. In average 36s for training sample and 6s for testing sample for each user and the sampling frequency was 16KHz. Then, we built a local dataset from 32 users with 44.1KHz sampling frequency and we acheived 98.96% accuercy.
the speech recognition part is done using the GMM-HMM model depending on the DTW "Dynamic Time Wrapping" Algotithm. The Trainging and testing stages are done depending on local dataset of 32 words, each word was repeated from 21 different speakers. The sampling frequency was 41.1KHz and we acheived accuercy reached to 97.82%.
The system was applyed on raspberry pi 3 model B using python 3.6.
