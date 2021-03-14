import numpy as np
import sounddevice as sd

class Feedback():
    def __init__():
        sd.default.samplerate = 9600
        sd.default.channels = 1
        pass

    def start():
        self.recording = sd.rec(int(10 * 9600))

    def get_result():
        self.recording.wait()

def put_over(image, overlay):
    alpha = overlay[:, :, 3:] / 255.0
    image[:, :, :3] = image[:, :, :3] * (1 - alpha) + overlay[:, :, :3] * alpha
    return image.astype(np.uint8)
