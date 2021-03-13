import cv2
from instruments.button import Button
from variables import MAX_X, MAX_Y


class Drums:
    circles_thickness = 9
    points_thickness = 2

    def __init__(self):
        self.buttons = []
        self.buttons.append(
            Button("Snare", 0.875, 0.278, 100, (0, 255, 0), "sounds_snare_1.wav")
        )

    def draw(self, image):
        for button in self.buttons:
            image = cv2.circle(
                image,
                (int(button.x * MAX_X), int(button.y * MAX_Y)),
                int(button.radius),
                button.color,
                self.circles_thickness,
            )
            image = cv2.circle(
                image,
                (int(button.x * MAX_X), int(button.y * MAX_Y)),
                int(self.points_thickness),
                button.color,
                self.circles_thickness,
            )

        return image
