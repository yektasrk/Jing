import cv2
import numpy as np

from hand import Hand
from config import WIDTH, HEIGHT, FPS
from instruments.piano import Piano
from utils import put_over
from audio import Audio

cap = cv2.VideoCapture(0)
# TODO get and assert
cap.set(cv2.CAP_PROP_FRAME_WIDTH, WIDTH)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, HEIGHT)
cap.set(cv2.CAP_PROP_FPS, FPS)

hand = Hand()
instrument = Piano()
audio = Audio()

while cap.isOpened():
    success, image = cap.read()
    if not success:
        print("Ignoring empty camera frame.")
        continue
    image = cv2.cvtColor(cv2.flip(image, 1), cv2.COLOR_BGR2RGB)
    hand_points = hand.fetch_pose(image)
    midi = instrument.handle_gesture(hand_points)
    if midi:
        audio.start_note(midi)
    image = cv2.cvtColor(image, cv2.COLOR_RGB2BGRA)
    hand_image = hand.overlay()
    instrument_image = instrument.overlay()

    final_image = image
    final_image = put_over(final_image, instrument_image)
    final_image = put_over(final_image, hand_image)

    cv2.imshow("Jing", final_image)

    if cv2.waitKey(5) & 0xFF == 27:  # escape
        break

audio.end()
cap.release()
