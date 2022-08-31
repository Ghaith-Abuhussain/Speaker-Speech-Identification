from pydub import AudioSegment
from pydub.silence import split_on_silence




def segments(test):
    filename = test
    
    sound = AudioSegment.from_wav(filename)
    chunks = split_on_silence(sound, 
                              # must be silent for at least half a second
                              min_silence_len=500,

                            # consider it silent if quieter than -16 dBFS
                            silence_thresh=-30

     )

    for i, chunk in enumerate(chunks):
        chunk.export("DataToTest1/chunk_{0}.wav".format(i), format="wav")
