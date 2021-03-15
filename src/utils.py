import numpy as np
import pyaudio


CHUNK = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 2
RATE = 44100

p = pyaudio.PyAudio()

class Feedback():
    def __init__(self):
        pass

    def start(self):
        stream = p.open(format=FORMAT,
            channels=CHANNELS,
            rate=RATE,
            input=True,
            frames_per_buffer=CHUNK)

    def get_result(self):
        yield stream.read(CHUNK)

