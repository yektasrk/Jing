from variables import MAX_Y, MAX_X
import cv2


graph = [
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
            int(hand_landmark.landmark[first_index].x * MAX_X),
            int(hand_landmark.landmark[first_index].y * MAX_Y),
        ),
        (
            int(hand_landmark.landmark[second_index].x * MAX_X),
            int(hand_landmark.landmark[second_index].y * MAX_Y),
        ),
        (0, 255, 0),
        2,
    )
    return image


def draw_point(hand_landmark, image, index):
    x = int(hand_landmark.landmark[index].x * MAX_X)
    y = int(hand_landmark.landmark[index].y * MAX_Y)
    z = -min(hand_landmark.landmark[index].z, 0)
    image = cv2.circle(
        image, (x, y,), int(z * 10), color=(0, 0, 255), thickness=int(z * 10),
    )
    return image


def draw_hand(image, hand_points):
    if hand_points.multi_hand_landmarks:
        for hand_landmark in hand_points.multi_hand_landmarks:
            for point in graph:
                image = draw_line(hand_landmark, image, point[0], point[1])
            for i in range(21):
                image = draw_point(hand_landmark, image, i)

    return image
