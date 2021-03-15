import numpy as np
import pyaudio


CHUNK = 200
FORMAT = pyaudio.paInt16
CHANNELS = 1
SAMPLE_RATE = 8000

p = pyaudio.PyAudio()

class Feedback():
    def __init__(self, seconds):
        self.buffer_size = SAMPLE_RATE * seconds
        self.sig = np.array([0] * self.buffer_size)

    def start(self):
        stream = p.open(format=FORMAT,
            channels=CHANNELS,
            rate=SAMPLE_RATE,
            input=True,
            frames_per_buffer=CHUNK,
            stream_callback=lambda indata, framecount, timeinfo, status: self.callback(indata))
        stream.start_stream()

    def callback(self, data):
        new_data = np.frombuffer(data, np.int16)
        self.sig = np.append(self.sig[new_data.size - self.buffer_size:], new_data)
        return (data, pyaudio.paContinue)

    def get_signal(self):
        return self.sig / 65535

    
