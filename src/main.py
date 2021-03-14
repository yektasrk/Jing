import cv2
import numpy as np

from hand import Hand
from config import CAM_URL
from instruments.drums import Drums
from instruments.piano import Piano
from utils import put_over
from audio import Audio
import time


hand = Hand()
instrument = Drums()
audio = Audio()
fcount = 0
t0 = time.time()

cap = cv2.VideoCapture(CAM_URL)
cap.set(cv2.CAP_PROP_BUFFERSIZE, 1)
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

    fcount = (fcount + 1)
    if fcount == 100:
        print(f"fps: {fcount / (time.time() - t0)}")
        fcount = 0
        t0 = time.time()

    if cv2.waitKey(1) & 0xFF == 27:  # escape
        break

audio.end()
cap.release()
