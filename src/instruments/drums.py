import numpy as np
import cv2

from instrument import Instrument
from config import HEIGHT, WIDTH


FORGET_RATE = 0.3
COLOR = (0, 204, 204, 255)
SPEED_THRESHOLD = 0.06

#TODO change points with width and height
centers = [(0.132, 0.677), (0.167, 0.490), (0.208, 0.312), (0.368, 0.219), (0.576, 0.208), (0.764, 0.271), 
(0.833, 0.646), (0.333, 0.438), (0.472, 0.344), (0.618, 0.427), (0.472, 0.552), (0.347, 0.740), (0.604, 0.740), ]

bidis = [(9, 57, 64, 1), (9, 49, 64, 1), (9, 55, 64, 1), (9, 51, 64, 1), (9, 53, 64, 1), (9, 46, 64, 1), (9, 43, 64, 1), 
(9, 45, 64, 1), (9, 50, 64, 1), (9, 41, 64, 1), (9, 36, 64, 1), (9, 40, 64, 1), (9, 38, 64, 1), (9, 27, 64, 1)]

radiuses = [0.083, 0.090, 0.104, 0.083, 0.090, 0.125, 0.111, 0.069, 0.069, 0.083, 0.097, 0.125, 0.125, ] 

class Drums(Instrument):
    def __init__(self):
        for i in range(len(centers)):
            centers[i] = (centers[i][0] * WIDTH, centers[i][1] * HEIGHT)
            radiuses[i] = radiuses[i] * WIDTH
        self.x_speed = 0
        self.y_speed = 0
        self.z_speed = 0
        self.last_pose = None

    def overlay(self, back_image):
        rgb_drums = cv2.imread('./src/instruments/drums.png')
        drums = cv2.cvtColor(rgb_drums, cv2.COLOR_RGB2RGBA)
        dim = (WIDTH, HEIGHT)
        resized = cv2.resize(drums, dim)
        dst = cv2.addWeighted(back_image,0.2,resized,1,0)
        self.image = dst
        # for i in range(len(centers)):
        #     self.image = cv2.circle(self.image, (int(centers[i][0]), int(centers[i][1])), int(radiuses[i]), COLOR, -1)
        return dst

    def _find_hand_center(self, pose, hand_index):
        points_list = range(5, 17)
        x = 0
        y = 0
        z = 0
        for i in points_list:
            x += pose[hand_index].landmark[i].x
            y += pose[hand_index].landmark[i].y
            z += pose[hand_index].landmark[i].z
        return (x / len(points_list), y / len(points_list), z / len(points_list))

    def _check_circle_collision(self, point, center, radius):
        distance = ((point[0] - center[0]) ** 2 + (point[1] - center[1]) ** 2) ** (1/2)
        if distance < radius:
            return True
        return False

    def handle_gesture(self, pose):
        if pose and self.last_pose:
            for hand_index in range(len(pose)):
                if hand_index < len(self.last_pose):
                    x, y, z = self._find_hand_center(pose, hand_index)
                    last_x, last_y, last_z = self._find_hand_center(self.last_pose, hand_index) 

                    self.x_speed = (x - last_x) * (1 - FORGET_RATE) + self.x_speed * FORGET_RATE
                    self.y_speed = (y - last_y) * (1 - FORGET_RATE) + self.y_speed * FORGET_RATE
                    self.z_speed = (z - last_z) * (1 - FORGET_RATE) + self.z_speed * FORGET_RATE
                    speed = (self.x_speed ** 2 + self.y_speed ** 2 + self.z_speed ** 2)**(1/2)

                    if self.z_speed > SPEED_THRESHOLD:
                        for i in range(len(centers)):
                            if self._check_circle_collision((x * WIDTH, y * HEIGHT), centers[i], radiuses[i]):
                                print("played")
                                return bidis[i]
                        
        self.last_pose = pose
