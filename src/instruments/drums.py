import numpy as np
import cv2

from instrument import Instrument
from config import HEIGHT, WIDTH


FORGET_RATE = 0.3
X_PADDING = WIDTH // 6
Y_PADDING = HEIGHT // 6
RADIUS = WIDTH // 10
SPEED_THRESHOLD = 0.05
colors = [(0, 204, 204, 255), (0, 204, 204, 255), (0, 204, 204, 255), (0, 204, 204, 255)]
bidis = [(0, 25, 64, 117), (0, 64, 64, 116), (0, 49, 64, 115), (0, 49, 64, 114)]



class Drums(Instrument):
    def __init__(self):
        self.x_speed = 0
        self.y_speed = 0
        self.last_pose = None

    def overlay(self, back_image):
        self.image = back_image
        self.image = cv2.circle(self.image, (X_PADDING, Y_PADDING), RADIUS, colors[0], -1)
        self.image = cv2.circle(self.image, (WIDTH - X_PADDING, Y_PADDING), RADIUS, colors[1], -1)
        self.image = cv2.circle(self.image, (X_PADDING, HEIGHT - Y_PADDING), RADIUS, colors[2], -1)
        self.image = cv2.circle(self.image, (WIDTH - X_PADDING, HEIGHT - Y_PADDING), RADIUS, colors[3], -1)
        return self.image

    def _find_hand_center(self, pose, hand_index):
        points_list = [0, 5, 9, 13, 17]
        x = 0
        y = 0
        for i in points_list:
            x += pose[hand_index].landmark[i].x
            y += pose[hand_index].landmark[i].y
        return (x / len(points_list), y / len(points_list))

    def handle_gesture(self, pose):
        if pose and self.last_pose:
            for hand_index in range(len(pose)):
                if hand_index < len(self.last_pose):
                    x, y = self._find_hand_center(pose, hand_index)
                    last_x, last_y = self._find_hand_center(self.last_pose, hand_index) 

                    self.x_speed = (x - last_x) * (1 - FORGET_RATE) + self.x_speed * FORGET_RATE
                    self.y_speed = (y - last_y) * (1 - FORGET_RATE) + self.y_speed * FORGET_RATE
                    speed = (self.x_speed ** 2 + self.y_speed ** 2)**(1/2)

                    if self.x_speed < 0 and self.y_speed < 0:
                        distance = ((x * WIDTH - (X_PADDING))**2 + (y * HEIGHT - (Y_PADDING))**2)**(1/2)
                        if distance < RADIUS:
                            return bidis[0]
                    if self.x_speed > 0 and self.y_speed < 0:
                        distance = ((x * WIDTH - (WIDTH - X_PADDING))**2 + (y * HEIGHT - (Y_PADDING))**2)**(1/2)
                        if distance < RADIUS:
                            return bidis[1]
                    if self.x_speed < 0 and self.y_speed > 0:
                        distance = ((x * WIDTH - (X_PADDING))**2 + (y * HEIGHT - (HEIGHT - Y_PADDING))**2)**(1/2)
                        if distance < RADIUS:
                            return bidis[2]
                    if self.x_speed > 0 and self.y_speed > 0:
                        distance = ((x * WIDTH - (WIDTH - X_PADDING))**2 + (y * HEIGHT - (HEIGHT - Y_PADDING))**2)**(1/2)
                        if distance < RADIUS:
                            return bidis[3]
        self.last_pose = pose
