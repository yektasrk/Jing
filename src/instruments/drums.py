import numpy as np
import cv2

from instrument import Instrument
from config import HEIGHT, WIDTH


FORGET_RATE = 0.3
COLOR = (0, 204, 204, 255)
SPEED_THRESHOLD = 0.04

centers = [(WIDTH // 4, HEIGHT // 4), (WIDTH * 3 // 4, HEIGHT // 4), (WIDTH // 4, HEIGHT * 3 /4), (WIDTH * 3 // 4, HEIGHT * 3 //4)]
radiuses = [WIDTH // 10, WIDTH // 10, WIDTH // 10, WIDTH //10]
bidis = [(9, 35, 64, 1), (9, 40, 64, 1), (9, 49, 64, 1), (9, 49, 64, 1)]



class Drums(Instrument):
    def __init__(self):
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
        # self.image = dst
        # for i in range(len(centers)):
        #     self.image = cv2.circle(self.image, (int(centers[i][0]), int(centers[i][1])), int(radiuses[i]), COLOR, -1)
        return dst

    def _find_hand_center(self, pose, hand_index):
        points_list = [0, 5, 9, 13, 17]
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

                    if self.z_speed < -SPEED_THRESHOLD:
                        for i in range(len(centers)):
                            if self._check_circle_collision((x * WIDTH, y * HEIGHT), centers[i], radiuses[i]):
                                print("played")
                                return bidis[i]
                        
        self.last_pose = pose
