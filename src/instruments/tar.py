import numpy as np
import cv2

from instrument import Instrument
from config import HEIGHT, WIDTH


FORGET_RATE = 0.3
COLOR = (0, 204, 204, 255)
THICKNESS = 10
SPEED_THRESHOLD = 0.06
START_POINT = (650, 450)
END_POINT = (50, 200)
BAR_PORTION = 0.75

notes = [(0, 49, 64, 25), (0, 51, 64, 25), (0, 53, 64, 25), (0, 54, 64, 25), (0, 56(0, 54, 64, 25), 64, 25)]



class TAR(Instrument):
    def __init__(self):
        self.a = (END_POINT[1] - START_POINT[1]) / (START_POINT[0] - END_POINT[0])
        self.b = 1
        self.c = (START_POINT[1] * END_POINT[0] - END_POINT[1] * START_POINT[0]) / (START_POINT[0] - END_POINT[0])
        self.x_speed = 0
        self.y_speed = 0
        self.z_speed = 0
        self.last_pose = None

    def overlay(self, back_image):
        self.image = cv2.line(back_image, START_POINT, END_POINT, COLOR, THICKNESS)
        return self.image

    def _line_intersection(self, line1, line2):
        xdiff = (line1[0][0] - line1[1][0], line2[0][0] - line2[1][0])
        ydiff = (line1[0][1] - line1[1][1], line2[0][1] - line2[1][1])

        def det(a, b):
            return a[0] * b[1] - a[1] * b[0]

        div = det(xdiff, ydiff)
        if div == 0:
            return None, None
        first_point_diff = self.a * line2[0][0] + self.b * line2[0][1] + self.c
        second_point_diff = self.a * line2[1][0] + self.b * line2[1][1] + self.c
        if second_point_diff * first_point_diff > 0:
            return None, None

        d = (det(*line1), det(*line2))
        x = det(d, xdiff) / div
        y = det(d, ydiff) / div
        return x, y
    
    def _find_note(self, point):
        if not point[0] or not point[1]:
            return 0
        if point[0] < END_POINT[0]:
            return 0
        note_index = int((len(notes) - 1) * ((point[0] - END_POINT[0]) / (START_POINT[0] * BAR_PORTION - END_POINT[0]))) + 1
        if note_index >= len(notes):
            return 0
        return note_index
    
    def right_hand(self, pose, note):
        if pose and self.last_pose:
            for hand_index in range(len(pose)):
                if hand_index < len(self.last_pose):
                    before_point = pose[hand_index].landmark[8].x * WIDTH, pose[hand_index].landmark[8].y * HEIGHT
                    now_point = self.last_pose[hand_index].landmark[8].x * WIDTH, self.last_pose[hand_index].landmark[8].y * HEIGHT
                    before_point_diff = self.a * before_point[0] + self.b * before_point[1] + self.c
                    now_point_diff = self.a * now_point[0] + self.b * now_point[1] + self.c
                    if now_point_diff * before_point_diff < 0:
                        if now_point[0] > BAR_PORTION * (START_POINT[0] - END_POINT[0]) + END_POINT[0] and now_point[0] < START_POINT[0]:
                            return note
        self.last_pose = pose
        
        
    def left_hand(self, pose):
        note_index = 0
        for hand_index in range(len(pose)):
            finger_start = pose[hand_index].landmark[5].x * WIDTH, pose[hand_index].landmark[5].y * HEIGHT
            finger_end = pose[hand_index].landmark[8].x * WIDTH, pose[hand_index].landmark[8].y * HEIGHT
            intersection_point = self._line_intersection((START_POINT, END_POINT), (finger_start, finger_end))
            note_index = max(note_index, self._find_note(intersection_point))
        print(note_index)
        return notes[note_index]
    
        

    def handle_gesture(self, pose):
        if pose and self.last_pose:
            note = self.left_hand(pose)
            return self.right_hand(pose, note)                   
        self.last_pose = pose
