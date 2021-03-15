import numpy as np
import cv2

from instrument import Instrument
from config import HEIGHT, WIDTH


class Recorder(Instrument):
    def __init__(self):
        self.param = []

    def overlay(self):
        pass

    def handle_gesture(self, pose):
        if pose:
            self.param.append((pose[0].landmark[0].x, pose[0].landmark[0].y))

