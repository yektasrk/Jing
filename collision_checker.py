from variables import MAX_X, MAX_Y
import cv2


class CollisionChecker:
    def __init__(self, player):
        self.player = player

    def check_collision(self, image, instruments, hand_points):
        if hand_points.multi_hand_landmarks:
            finger_x = hand_points.multi_hand_landmarks[0].landmark[6].x * MAX_X
            finger_y = hand_points.multi_hand_landmarks[0].landmark[6].y * MAX_Y
            image = cv2.circle(image, (int(finger_x), int(finger_y)), 2, (0, 255, 0), 9)
            for button in instruments.buttons:
                distance = (((finger_x - button.x * MAX_X)**2 + (finger_y - button.y * MAX_Y)**2 )**(1/2))
                if distance < 100:
                    self.player.play(button.soundfile)

        return image