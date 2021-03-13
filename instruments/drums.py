import cv2
from instruments.instrument import Instrument
from variables import MAX_X, MAX_Y
class Drums:
    circles_thickness = 9
    points_thickness = 2

    def __init__(self):
        self.instruments = []
        self.instruments.append(Instrument("Snare", 0.875, 0.278, 100, (0, 255, 0), "sounds_snare_1.wav"))

    def draw(self, image):
        for instrument in self.instruments:
            image = cv2.circle(image, (int(instrument.x * MAX_X), int(instrument.y * MAX_Y)), int(instrument.radius), instrument.color, self.circles_thickness)
            image = cv2.circle(image, (int(instrument.x * MAX_X), int(instrument.y * MAX_Y)), int(self.points_thickness), instrument.color, self.circles_thickness)

        return image


