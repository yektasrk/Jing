import cv2
import numpy as np
import mediapipe as mp

from config import FPS, WIDTH, HEIGHT


hand_graph = [
    (0, 1),
    (1, 2),
    (2, 3),
    (3, 4),
    (0, 5),
    (5, 6),
    (6, 7),
    (7, 8),
    (5, 9),
    (9, 10),
    (10, 11),
    (11, 12),
    (9, 13),
    (13, 14),
    (14, 15),
    (15, 16),
    (13, 17),
    (17, 18),
    (18, 19),
    (19, 20),
    (0, 17),
]


def draw_line(hand_landmark, image, first_index, second_index):
    image = cv2.line(
        image,
        (
            int(hand_landmark.landmark[first_index].x * WIDTH),
            int(hand_landmark.landmark[first_index].y * HEIGHT),
        ),
        (
            int(hand_landmark.landmark[second_index].x * WIDTH),
            int(hand_landmark.landmark[second_index].y * HEIGHT),
        ),
        (0, 255, 0, 255),
        2,
    )
    return image


def draw_point(hand_landmark, image, index):
    x = int(hand_landmark.landmark[index].x * WIDTH)
    y = int(hand_landmark.landmark[index].y * HEIGHT)
    z = -min(hand_landmark.landmark[index].z, 0)
    image = cv2.circle(
        image, (x, y,), int(z * 10), color=(0, 0, 255, 255), thickness=int(z * 10),
    )
    return image


class Hand():
    def __init__(self):
        self.mp_hand = mp.solutions.hands.Hands(min_detection_confidence=0.5, min_tracking_confidence=0.3)

    def start(self):
        pass

    def overlay(self):
        image = np.zeros((HEIGHT,WIDTH,4), np.uint8)
        if self.last_hands_points:
            for hand in self.last_hands_points:
                for point in hand_graph:
                    image = draw_line(hand, image, point[0], point[1])
                for i in range(21):
                    image = draw_point(hand, image, i)
        return image

    def fetch_pose(self, image):
        self.last_hands_points = self.mp_hand.process(image).multi_hand_landmarks
        return self.last_hands_points


    def shutdown(self):
        pass
