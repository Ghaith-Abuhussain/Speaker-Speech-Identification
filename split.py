# -*- coding: utf-8 -*-
"""
Created on Sat Sep  7 20:52:49 2019

@author: Sniper 101
"""

# -*- coding: utf-8 -*-
"""
Created on Sat Sep  7 20:47:51 2019

@author: Sniper 101
"""

from pydub import AudioSegment
from pydub.silence import split_on_silence
from math import log, ceil
#from utils import ratio_to_db
#from utils import db_to_float
import pyaudio
from record import Recorder
import struct
import math
import scipy.io.wavfile as wav
import wave

def db_to_float(db, using_amplitude=True):
    """
    Converts the input db to a float, which represents the equivalent
    ratio in power.
    """
    db = float(db)
    if using_amplitude:
        return 10 ** (db / 20)
    else:  # using power
        return 10 ** (db / 10)


def ratio_to_db(ratio, val2=None, using_amplitude=True):
    """
    Converts the input float to db, which represents the equivalent
    to the ratio in power represented by the multiplier passed in.
    """
    ratio = float(ratio)

    # accept 2 values and use the ratio of val1 to val2
    if val2 is not None:
        ratio = ratio / val2

    # special case for multiply-by-zero (convert to silence)
    if ratio == 0:
        return -float('inf')

    if using_amplitude:
        return 20 * log(ratio, 10)
    else:  # using power
        return 10 * log(ratio, 10)



def segments_split(test):
    """
    CHUNK = 64
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
    """



    #R = Recorder()
    #R.listen()
    

    
    filename = test
    
    sound = AudioSegment.from_wav(filename)
    sound_noise = sound[len(sound)-442:len(sound)-1]
    a2 = sound_noise.rms
    d = ratio_to_db(a2/sound_noise.max_possible_amplitude)+5
    chunks = split_on_silence(sound, 
                              # must be silent for at least half a second
                              min_silence_len=300,

                            # consider it silent if quieter than -16 dBFS
                            silence_thresh=d

     )

    for i, chunk in enumerate(chunks):
        chunk.export("DataToTest1/chunk_{0}.wav".format(i), format="wav")
    return d
#d = segments_split("single_speaker/out.wav")
        
