import cv2

from hand import Hand
from config import WIDTH, HEIGHT, FPS

cap = cv2.VideoCapture(0)
# TODO get and assert
cap.set(cv2.CAP_PROP_FRAME_WIDTH, WIDTH)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, HEIGHT)
cap.set(cv2.CAP_PROP_FPS, FPS)

hand = Hand()

while cap.isOpened():
    success, image = cap.read()
    if not success:
        print("Ignoring empty camera frame.")
        continue
    image = cv2.cvtColor(cv2.flip(image, 1), cv2.COLOR_BGR2RGB)
    hand_points = hand.fetch_pose(image)
    image = cv2.cvtColor(image, cv2.COLOR_RGB2BGRA)
    hand_image = hand.overlay()

    cv2.imshow("Jing", cv2.addWeighted(image, 0.5, hand_image, 0.5, 0.0))

    if cv2.waitKey(5) & 0xFF == 27: # escape
        break

cap.release()
