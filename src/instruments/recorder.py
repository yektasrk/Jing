from time import time

import numpy as np
import cv2

from utils import Feedback, SAMPLE_RATE
from instrument import Instrument
from config import HEIGHT, WIDTH


DURATION = 10

class Recorder(Instrument):
    def __init__(self):
        self.feedback = Feedback(DURATION) # in seconds
        self.feedback.start()
        self.param = []

    def overlay(self, image):
        hand_sig = self.get_signal()
        hand_plot = np.array([[t / DURATION * WIDTH, (x * 200) + HEIGHT / 4] for x, t in hand_sig], np.int32)
        hand_plot = hand_plot.reshape((-1, 1, 2))
        image = cv2.polylines(image, [hand_plot], False, (0, 255, 255), 2)

        aud_sig = self.feedback.get_signal()
        aud_plot = np.array([[i / DURATION / SAMPLE_RATE * WIDTH, (x * 200) + 3 * HEIGHT / 4] for i, x in enumerate(aud_sig)], np.int32)
        aud_plot = aud_plot.reshape((-1, 1, 2))
        image = cv2.polylines(image, [aud_plot], False, (255, 255, 0), 2)

        z_pos = np.array([x for x,t in hand_sig if aud_sig[int(t * SAMPLE_RATE)] == 1])
        z_neg = np.array([x for x,t in hand_sig if aud_sig[int(t * SAMPLE_RATE)] == 0])
        print(z_pos.mean(), z_pos.std())
        print(z_neg.mean(), z_neg.std())
        return image

    def handle_gesture(self, pose):
        if pose:
            self.param.append((pose[0].landmark[8].z - pose[0].landmark[6].z, time()))
        else:
            self.param.append((-100, time()))
        while self.param and self.param[0][1] < time() - DURATION:
            self.param.pop(0)

    def get_signal(self):
        return [(x,DURATION + t - time()) for x,t in self.param]
