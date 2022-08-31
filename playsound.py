from pygame import mixer
from pygame import time
def play(filename,x):
    mixer.pre_init(44100, -16, 1, 2048)
    mixer.init()
    mixer.music.load(filename)
    mixer.music.play()
    time.delay(x)
    mixer.get_busy()
#"/home/pi/final/confirms/confirm_identity.wav"
#play("/home/pi/final/confirms/confirm_identity.wav")
#play("/home/pi/final/confirms/confirm_command.wav")

