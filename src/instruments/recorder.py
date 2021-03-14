import numpy as np
import cv2

from instrument import Instrument
from config import HEIGHT, WIDTH


class Recorder(Instrument):
    def __init__(self):
        self.param = []

    def overlay(self):
        return self.image

    def handle_gesture(self, pose):
        if pose:
            self.param.append((pose[0].landmark[0].x, pose[0].landmark[0].y))
        fingers = [(1, 4), (5, 8), (9, 12), (13, 16), (17, 20)]
        if pose and self.last_pose:
            for hand_index in range(len(pose)):
                for finger in fingers:
                    if hand_index < len(self.last_pose):
                        relative_z = pose[hand_index].landmark[finger[1]
                                                               ].z - pose[hand_index].landmark[finger[0]].z
                        y = pose[hand_index].landmark[finger[1]].y * HEIGHT
                        x = pose[hand_index].landmark[finger[1]].x
                        last_relative_z = self.last_pose[hand_index].landmark[finger[1]
                                                                              ].z - self.last_pose[hand_index].landmark[finger[0]].z

                        self.z_speed = (relative_z - last_relative_z) * (1 - FORGET_RATE) + \
                            self.z_speed * FORGET_RATE

                        # print('asghar bebin %f, %f' % (relative_z, self.z_speed))
                        if relative_z > 0.0 and self.z_speed > 0.01:
                            print("y", y)
                            if y > HEIGHT - KEY_HEIGHT // 2:
                                note_index = int(
                                    (x - 0.5 / N_KEYS) * N_KEYS)
                                if not note_index % 7 in [2, 6]:
                                    print('asghar bia',
                                          BLACK_NOTES[note_index])
                                    return 0, BLACK_NOTES[note_index] + 24, 64
                            elif y > HEIGHT - KEY_HEIGHT:
                                note_index = int(x * N_KEYS)
                                print('asghar bia', WHITE_NOTES[note_index])
                                return 0, WHITE_NOTES[note_index] + 24, 64
        self.last_pose = pose
