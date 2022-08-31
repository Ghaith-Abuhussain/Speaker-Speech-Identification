import sys
from PyQt5.QtWidgets import QMainWindow, QApplication, QWidget, QPushButton, QAction, QLineEdit, QMessageBox,QLabel,QTextBrowser,QDialog,QProgressBar
from PyQt5.QtGui import *
from PyQt5.QtCore import pyqtSlot
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
#from splitTowords import segments
from playsound import play
import threading
from hmmlearn import hmm
from split import segments_split
from ghaith import segments





class App(QWidget):
    
    def __init__(self):
        super().__init__()
        self.title = 'application'
        self.left = 10
        self.top = 10
        self.width = 800
        self.height = 500
        self.initUI()
    
    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)
        #bottons
        self.button1 = QPushButton('START', self)
        self.button1.setToolTip('This is an example button')
        self.button1.move((self.width)/2-60, 50)
        self.button1.clicked.connect(self.START)

        self.button3 = QPushButton('TRAIN', self)
        self.button3.setToolTip('This is an example button')
        self.button3.move(250,250)
        self.button3.clicked.connect(self.ADD_SPEAKER)

        self.button4 = QPushButton('TRAIN', self)
        self.button4.setToolTip('This is an example button')
        self.button4.move(600,250)
        self.button4.clicked.connect(self.ADD_WORD)

        self.button5 = QPushButton('ADD Command', self)
        self.button5.setToolTip('This is an example button')
        self.button5.move((self.width)/2-80, 450)
        self.button5.clicked.connect(self.ADD_COMMAND)

        self.button6 = QPushButton('Record Speaker', self)
        self.button6.setToolTip('This is an example button')
        self.button6.move(100,250)
        self.button6.clicked.connect(self.Record_Speaker)

        self.button6 = QPushButton('Record Word', self)
        self.button6.setToolTip('This is an example button')
        self.button6.move(450,250)
        self.button6.clicked.connect(self.Record_Word)


        #text boxes
        
        self.textbox3 = QLineEdit(self)
        self.textbox3.move(100, 210)
        self.textbox3.resize(250,40)

        self.textbox4 = QLineEdit(self)
        self.textbox4.move(450, 210)
        self.textbox4.resize(250,40)

        self.textbox5 = QLineEdit(self)
        self.textbox5.move(50, 400)
        self.textbox5.resize(250,40)

        self.textbox6 = QLineEdit(self)
        self.textbox6.move(450, 400)
        self.textbox6.resize(250,40)
        
        self.progress = QProgressBar(self)
        self.progress.setGeometry(0, 0, 300, 25)
        self.progress.setMaximum(100)
        self.progress.move(100,280)

        self.progress1 = QProgressBar(self)
        self.progress1.setGeometry(0, 0, 300, 25)
        self.progress1.setMaximum(100)
        self.progress1.move(450,280)
        
        self.textbox9 = QLineEdit(self)
        self.textbox9.move(50,100)
        self.textbox9.resize(250,30)
        """
        self.lbl = QTextBrowser(self)
        self.lbl.resize(250,30) # Typically you create a layout and put the widget in the layout.
        self.lbl.move(90,100)
        """
        self.textbox10 = QLineEdit(self)
        self.textbox10.move(490,100)
        self.textbox10.resize(250,30)
        

        
        #labels
        self.label1 = QLabel(self)
        self.label1.setText('MAIN PROGRAM')
        self.label1.setFont(QFont("Times", 12, QFont.Bold))
        self.label1.move((self.width)/2-80, 20)

        self.label3 = QLabel(self)
        self.label3.setText('Add Single Speaker')
        self.label3.setFont(QFont("Times", 12, QFont.Bold))
        self.label3.move(50, 180)

        self.label4 = QLabel(self)
        self.label4.setText('Location')
        self.label4.setFont(QFont("Times", 12, QFont.Bold))
        self.label4.move(20, 220)

        self.label5 = QLabel(self)
        self.label5.setText('Add Single Word')
        self.label5.setFont(QFont("Times", 12, QFont.Bold))
        self.label5.move(450, 180)

        self.label6 = QLabel(self)
        self.label6.setText('ADD COMMAND')
        self.label6.setFont(QFont("Times", 12, QFont.Bold))
        self.label6.move((self.width)/2-80, 350)

        self.label7 = QLabel(self)
        self.label7.setText('Command in Terminal')
        self.label7.setFont(QFont("Times", 12, QFont.Bold))
        self.label7.move(50, 380)

        self.label8 = QLabel(self)
        self.label8.setText('Command in txt')
        self.label8.setFont(QFont("Times", 12, QFont.Bold))
        self.label8.move(450, 380)
    
        self.label9 = QLabel(self)
        self.label9.setText('Message From The System')
        self.label9.setFont(QFont("Times", 12, QFont.Bold))
        self.label9.move(50,80)

        self.label10 = QLabel(self)
        self.label10.setText('End Train')
        self.label10.setFont(QFont("Times", 12, QFont.Bold))
        self.label10.move(20, 290)

        self.label11 = QLabel(self)
        self.label11.setText('Clim ID')
        self.label11.setFont(QFont("Times", 12, QFont.Bold))
        self.label11.move(500,80)
        
        self.show()

    @pyqtSlot()
    def START(self):
        
        Threshold = 100
        SHORT_NORMALIZE = (1.0/32768.0)
        chunk = 1024
        FORMAT = pyaudio.paInt16
        CHANNELS = 1
        RATE = 44100
        swidth = 2

        TIMEOUT_LENGTH = 2

        f_name_directory = r'F:/final/single_speaker'
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
            self.textbox9.setText("Noise detected, recording beginning")
            self.repaint()
            self.update()
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
            #print('Written to file: {}'.format(filename))
            #print('Returning to listening')

        def listen():
            self.textbox9.setText("Listening beginning")
            self.repaint()
            self.update()
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
            self.textbox9.setText("please define your identity")
            self.repaint()
            self.update()
            # whait the permession
            play("F:/final/confirms/confirm_identity.wav",200)
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
            #print ("Testing Audio : ", test)
            sr,audio = wav.read(test)
            #audio = remove_silent(audio,sr)
            audio = remove_silent(audio,sr)
            vector   = extract_features(audio,sr)
            log_likelihood = np.zeros(len(models)) 
            for i in range(len(models)):
                gmm    = models[i]  #checking with each model one by one
                scores = np.array(gmm.score(vector))
                log_likelihood[i] = scores.sum()   
            winner = np.argmax(log_likelihood)
            cheker_name = self.textbox10.text()
            if (speakers[winner] == cheker_name ):
                self.textbox9.setText("The Detection is Right")
                self.repaint()
                self.update()
                play("F:/final/confirms/true_confirm.wav",3000)
                t = 1
            else:
                print(speakers[winner])
                self.textbox9.setText("False Detection")
                play("F:/final/confirms/false_confirm.wav",3000)
                self.repaint()
                self.update()

        voicecommand = open("orders.txt","r")
        voicecommand = voicecommand.read().splitlines()
        check=0
        while(check!=1):
            voicecommand = open("orders.txt","r")
            voicecommand = voicecommand.read().splitlines()
            self.textbox9.setText("please enter your command")
            self.repaint()
            self.update()
            play("F:/final/confirms/confirm_command.wav",200)
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
            #segments("single_speaker/out.wav")
            segments_split("single_speaker/out.wav")
            #segments("single_speaker/out.wav")
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
                self.textbox9.setText("not defined!! Try again")
                self.repaint()
                self.update()
                play("F:/final/confirms/command_false.wav",3000)
            else:
                self.textbox9.setText("the order has been executed")
                self.repaint()
                self.update()
                play("F:/final/confirms/command_true.wav",3000)
                print(ord_index)
                if(ord_index > 0 &  ord_index <= length):
                    os.system(terminalcommand[ord_index])
                if(ord_index == 0):
                    check=1

    def ADD_SPEAKER(self):
        folder_data = self.textbox3.text()+"/"
        GMMs_location = "GMM_models/"
        GMMs=os.listdir(GMMs_location)
        print(GMMs)
        
        
        file1 = os.listdir(folder_data)
        sr,audio = wav.read(folder_data+file1[0])
        files = []
        frame_size = int(len(audio)/10)
        
        for j in range(10):
            files.append(audio[j*frame_size:(j+1)*frame_size-1])
            
        print(folder_data)
        file_counter = 1
        features = np.asarray(())
        count = int(80/len(files))+1
        self.progress.setValue(count)
        self.repaint()
        self.update()
        for file in files:
            file = remove_silent(file,sr)
            # extract the feature matrix for each udio file 40 features each row
            vector = extract_features(file,sr)
    
            if features.size == 0:
                features = vector
                self.progress.setValue(count)
                self.repaint()
                self.update()
            else:
                features = np.vstack((features, vector))
                self.progress.setValue(count)
                self.repaint()
                self.update()
    
            if file_counter == len(files):
                self.progress.setValue(count)
                self.repaint()
                self.update()
                gmm = mixture.GaussianMixture(n_components = 16 ,max_iter = 200 ,tol = 0.0001,covariance_type = 'diag',n_init = 9)
                gmm.fit(features)
        
                nameOfgaussian = folder_data.split("/")[1]+".gmm"
                filename = GMMs_location + nameOfgaussian
                with open(filename, 'wb') as handle:
                    pickle.dump(gmm, handle, protocol=pickle.HIGHEST_PROTOCOL)
                count=100
                self.progress.setValue(count)
                self.repaint()
                self.update()
                features = np.asarray(())
                file_counter = 0
            count = count + int(80/len(files))+1
            file_counter = file_counter + 1
        count = 0
        self.progress.setValue(count)
        self.textbox3.setText("")
        self.repaint()
        self.update()
        
    def ADD_WORD(self):
        DataToTrain = self.textbox4.text()+"/"
        GMMHMMs_location = "GMMHMM_models/"
        file9 = os.listdir("DataToTest1")
        """
            for fil in file9:
                os.remove("DataToTest1/"+fil)
        """
        file1 = os.listdir(DataToTrain)
        sr,audio = wav.read(DataToTrain+file1[0])
        print("SSS")
        segments(DataToTrain+file1[0])
        
        files = os.listdir("DataToTest1/")
        file_counter = 1
        features = np.asarray(())

        states_num = 6
        GMM_mix_num = 3
        tmp_p = 1.0/(states_num-2)
        transmatPrior = np.array([[tmp_p, tmp_p, tmp_p, 0 ,0], \
                                  [0, tmp_p, tmp_p, tmp_p , 0], \
                                  [0, 0, tmp_p, tmp_p,tmp_p], \
                                  [0, 0, 0, 1, 1], \
                                  [0, 0, 0, 0, 1]],dtype=np.float)
        startprobPrior = np.array([0.5, 0.5, 0, 0, 0],dtype=np.float)
        count = int(80/len(files))+1
        self.progress1.setValue(count)
        self.repaint()
        self.update()
        for file in files:
            sr,audio = wav.read("DataToTest1/"+file)
            vector = extract_featuresforword(audio,sr)
            if features.size == 0:
                features = vector
                self.progress1.setValue(count)
                self.repaint()
                self.update()
            else:
                features = np.vstack((features, vector))
                self.progress1.setValue(count)
                self.repaint()
                self.update()
            if file_counter == len(files):
                self.progress1.setValue(count)
                self.repaint()
                self.update()
        
                param=set(features.ravel())
                model = hmm.GMMHMM(n_components=states_num, n_mix=GMM_mix_num, \
                                   transmat_prior=transmatPrior, startprob_prior=startprobPrior,params=param, \
                                   covariance_type='diag', n_iter=10)
                model.fit(features)
                nameOfmodels = DataToTrain.split("/")[1] + ".gmmhmm"
                filename = GMMHMMs_location + nameOfmodels
                with open(filename, 'wb') as handle:
                    pickle.dump (model , handle ,protocol = pickle.HIGHEST_PROTOCOL)
                
                features = np.asarray(())
                count=100
                self.progress1.setValue(count)
                self.repaint()
                self.update()
            count=count + int(80/len(files))+1
            file_counter += 1
        count = 0
        self.progress1.setValue(count)
        self.textbox4.setText("")
        self.repaint()
        self.update()

        
    def ADD_COMMAND(self):
        txtcom= open("terminal_orders.txt","a+")
        txtcom.write("\n")
        txtcom.write(self.textbox5.text())
        txtcom.close()
        termcom= open("orders.txt","a+")
        termcom.write("\n")
        termcom.write(self.textbox6.text())
        termcom.close()
        self.textbox5.setText("")
        self.textbox6.setText("")

    def Record_Speaker(self):
        save_Location = self.textbox3.text()
        os.system("mkdir F:\\final\\DataToTrain\\"+save_Location.split("/")[1])
        CHUNK = 1024
        FORMAT = pyaudio.paInt16
        CHANNELS = 1
        RATE = 44100
        RECORD_SECONDS = 30
        WAVE_OUTPUT_FILENAME = save_Location

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

        
        wf = wave.open(WAVE_OUTPUT_FILENAME+"/"+save_Location.split("/")[1]+".wav", 'wb')
        wf.setnchannels(CHANNELS)
        wf.setsampwidth(p.get_sample_size(FORMAT))
        wf.setframerate(RATE)
        wf.writeframes(b''.join(frames))
        wf.close()
        

    def Record_Word(self):
        save_Location = self.textbox4.text()
        os.system("mkdir F:\\final\\DataToTrain1\\"+save_Location.split("/")[1])
        
        CHUNK = 1024
        FORMAT = pyaudio.paInt16
        CHANNELS = 1
        RATE = 44100
        RECORD_SECONDS = 15
        WAVE_OUTPUT_FILENAME = save_Location

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

        
        wf = wave.open(WAVE_OUTPUT_FILENAME+"/"+save_Location.split("/")[1]+".wav", 'wb')
        wf.setnchannels(CHANNELS)
        wf.setsampwidth(p.get_sample_size(FORMAT))
        wf.setframerate(RATE)
        wf.writeframes(b''.join(frames))
        wf.close()
        
        
        
        
    
if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())

