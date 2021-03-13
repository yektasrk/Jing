import cv2
import mediapipe as mp
from pygame import mixer
mp_drawing = mp.solutions.drawing_utils
mp_hands = mp.solutions.hands
mixer.init()
drum_snare = mixer.Sound('./sounds_snare_1.wav')


# For webcam input:
cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1080)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 1920)
cap.set(cv2.CAP_PROP_FPS, 30)
with mp_hands.Hands(
    min_detection_confidence=0.5,
    min_tracking_confidence=0.5) as hands:
  while cap.isOpened():
    success, image = cap.read()
    if not success:
      print("Ignoring empty camera frame.")
      # If loading a video, use 'break' instead of 'continue'.
      continue

    # Flip the image horizontally for a later selfie-view display, and convert
    # the BGR image to RGB.
    image = cv2.cvtColor(cv2.flip(image, 1), cv2.COLOR_BGR2RGB)
    # To improve performance, optionally mark the image as not writeable to
    # pass by reference.
    image.flags.writeable = False
    results = hands.process(image)

    # Draw the hand annotations on the image.
    image.flags.writeable = True
    image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
    image = cv2.circle(image, (1120, 200), 100, (0, 255, 0), 9)
    image = cv2.circle(image, (1120, 200), 2, (0, 255, 0), 9)
    if results.multi_hand_landmarks:
      point_x = results.multi_hand_landmarks[0].landmark[6].x * 1280
      point_y = results.multi_hand_landmarks[0].landmark[6].y * 720
      image = cv2.circle(image, (int(point_x), int(point_y)), 2, (0, 255, 0), 9)
      distance = (((point_y - 200)**2 + (point_x - 1120)**2 )**(1/2))
      # print(distance)
      if distance < 100:
        drum_snare.play()
      # for hand_landmarks in results.multi_hand_landmarks:
      #   mp_drawing.draw_landmarks(
      #       image, hand_landmarks, mp_hands.HAND_CONNECTIONS)
    cv2.imshow('MediaPipe Hands', image)
    if cv2.waitKey(5) & 0xFF == 27:
      break
cap.release()