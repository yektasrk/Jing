import numpy as np
import cv2

from instrument import Instrument
from config import HEIGHT, WIDTH

N_KEYS = 12
KEY_HEIGHT = HEIGHT // 2
KEY_WIDTH = WIDTH // N_KEYS
PADDING = 4

FORGET_RATE = 0.3
class Piano(Instrument):
    def __init__(self):
        self.image = np.zeros((HEIGHT, WIDTH, 4), np.uint8)
        for i in range(N_KEYS):
            self.image[HEIGHT - KEY_HEIGHT:, PADDING + i * KEY_WIDTH:i * KEY_WIDTH + KEY_WIDTH, :] = 255
        for i in range(N_KEYS):
            if not i % 7 in [2, 6]: 
                self.image[HEIGHT - KEY_HEIGHT // 2:, PADDING + i * KEY_WIDTH + KEY_WIDTH // 2:i * KEY_WIDTH + KEY_WIDTH + KEY_WIDTH // 2, 3] = 255
                self.image[HEIGHT - KEY_HEIGHT // 2:, PADDING + i * KEY_WIDTH + KEY_WIDTH // 2:i * KEY_WIDTH + KEY_WIDTH + KEY_WIDTH // 2, :3] = 0
        
        self.z_speed = 0
        self.last_pose = None

    def overlay(self):
        return self.image

    def handle_gesture(self, pose):
        fingers = [(1, 4), (5, 8), (9, 12), (13, 16), (17, 20)]
        if pose and self.last_pose:
            for hand_index in range(len(pose)):
                for finger in fingers:
                        if hand_index < len(self.last_pose):
                            relative_z = pose[hand_index].landmark[finger[1]].z - pose[hand_index].landmark[finger[0]].z
                            last_relative_z = self.last_pose[hand_index].landmark[finger[1]].z - self.last_pose[hand_index].landmark[finger[0]].z

                            self.z_speed = (relative_z - last_relative_z) * (1 - FORGET_RATE) + \
                                self.z_speed * FORGET_RATE

                            # print('asghar bebin %f, %f' % (relative_z, self.z_speed))
                            if relative_z > 0.0 and self.z_speed > 0.01:
                                return 0, 25, 64
                                print('asghar bia')
        self.last_pose = pose
