import numpy as np
import cv2

from instrument import Instrument
from config import HEIGHT, WIDTH

RANGE = 400

class Recorder(Instrument):
    def __init__(self):
        self.param = [(0,0,0)] * RANGE

    def overlay(self, image):
        print(len(self.get_signal()))
        sig = np.array([[x / RANGE * WIDTH, (y * 100) + HEIGHT / 2] for x, y in enumerate(self.get_signal())], np.int32)
        sig = sig.reshape((-1, 1, 2))
        image = cv2.polylines(image, [sig], False, (255, 255, 255), 2)
        return image

    def handle_gesture(self, pose):
        if pose:
            self.param.append((pose[0].landmark[0].x, pose[0].landmark[0].y))

    def get_signal(self):
        return [x[0] for x in self.param[-RANGE:]]
