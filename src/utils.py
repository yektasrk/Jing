import numpy as np
import pyaudio


CHUNK = 2000
FORMAT = pyaudio.paInt16
CHANNELS = 1
SAMPLE_RATE = 8000

p = pyaudio.PyAudio()

class Feedback():
    def __init__(self, seconds):
        self.buffer_size = SAMPLE_RATE * seconds
        self.silence_sig = np.array([0] * self.buffer_size)
        self.sig = np.array([0] * self.buffer_size)
        self.state = 'silence'
        self.silence_var = 0
        self.silence_samples = 0

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
        new_data = new_data.astype(np.float64)
        if self.state == 'silence':
            self.silence_var = (self.silence_var * self.silence_samples + \
                ((new_data) ** 2).sum()) / (self.silence_samples + new_data.size)
            self.silence_samples += new_data.size
            if self.silence_samples > 5 * SAMPLE_RATE:
                self.state = 'go'
        else:
            window_size = 120
            outliers = np.abs(new_data) > 3 * np.sqrt(self.silence_var)
            self.silence_sig = np.append(self.silence_sig[new_data.size - self.buffer_size:], outliers)
        self.sig = np.append(self.sig[new_data.size - self.buffer_size:], new_data)
        return (data, pyaudio.paContinue)

    def get_signal(self):
        return np.array([self.silence_sig[max(i - 60, 0):min(i + 60, self.silence_sig.size)].max() for i in range(self.silence_sig.size)], np.uint8)

    
