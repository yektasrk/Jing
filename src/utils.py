import numpy as np
import sounddevice as sd


class Feedback():
    def __init__(self):
        sd.default.samplerate = 9600
        sd.default.channels = 1
        pass

    def start(self):
        self.recording = sd.rec(int(10 * 9600))

    def get_result(self):
        self.recording.wait()
