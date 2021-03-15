import cProfile
import re
import time

import cv2
import numpy as np
from audio import Audio
from hand import Hand
from config import INSTRUMENT, CAM_URL, HEIGHT, WIDTH
from instruments.drums import Drums
from instruments.piano import Piano
from instruments.recorder import Recorder
from pyinstrument import Profiler
from utils import Feedback

hand = Hand()
if INSTRUMENT.upper() == "PIANO":
    instrument = Piano()
elif INSTRUMENT.upper() == "DRUMS":
    instrument = Drums()
else:
    instrument = Recorder()

audio = Audio()
fcount = 0
t0 = time.time()
profiler = Profiler()
profiler.start()

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

    instrument_image = instrument.overlay(image)
    hand_image = hand.overlay(instrument_image)
    cv2.imshow("Jing", hand_image)

    fcount = (fcount + 1)
    if fcount == 100:
        print(f"fps: {fcount / (time.time() - t0)}")
        fcount = 0
        t0 = time.time()

    if cv2.waitKey(1) & 0xFF == 27:  # escape
        break

audio.end()
cap.release()
profiler.stop()
print(profiler.output_text(unicode=True, color=True))

