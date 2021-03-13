import cv2
import mediapipe as mp
from pygame import mixer
mp_drawing = mp.solutions.drawing_utils
mp_hands = mp.solutions.hands
mixer.init()
MAX_X = 1280
MAX_Y = 720
FPS = 30
cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, MAX_X)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, MAX_Y)
cap.set(cv2.CAP_PROP_FPS, FPS)

with mp_hands.Hands(
    min_detection_confidence=0.5,
    min_tracking_confidence=0.5) as hands:
  while cap.isOpened():
    success, image = cap.read()
    if not success:
      print("Ignoring empty camera frame.")
      continue

    image = cv2.cvtColor(cv2.flip(image, 1), cv2.COLOR_BGR2RGB)
    image.flags.writeable = False
    results = hands.process(image)

    image.flags.writeable = True
    image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
    image = cv2.circle(image, (1120, 200), 100, (0, 255, 0), 9)
    image = cv2.circle(image, (1120, 200), 2, (0, 255, 0), 9)
    if results.multi_hand_landmarks:
      drum_snare = mixer.Sound('./sounds_snare_1.wav')
      point_x = results.multi_hand_landmarks[0].landmark[6].x * 1280
      point_y = results.multi_hand_landmarks[0].landmark[6].y * 720
      image = cv2.circle(image, (int(point_x), int(point_y)), 2, (0, 255, 0), 9)
      distance = (((point_y - 200)**2 + (point_x - 1120)**2 )**(1/2))
      if distance < 100:
        drum_snare.play()
    cv2.imshow('MediaPipe Hands', image)
    if cv2.waitKey(5) & 0xFF == 27:
      break
cap.release()