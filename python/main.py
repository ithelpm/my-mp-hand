import math
import time
import cv2
import mediapipe as mp
from mediapipe.tasks.python import vision
from mediapipe.tasks import python
from mediapipe import solutions
from mediapipe.tasks.python.vision.gesture_recognizer import GestureRecognizerResult
from mediapipe.framework.formats import landmark_pb2
import numpy as np
import unittest

mp_hands = solutions.hands
mp_drawing = solutions.drawing_utils
mp_drawing_styles = solutions.drawing_styles

model_file = open('gesture_recognizer.task', "rb")
model_data = model_file.read()
model_file.close()
baseOptions = python.BaseOptions(model_asset_buffer=model_data)


class Var:
    GestureRecognizer = vision.GestureRecognizer
    GestureRecognizerOptions = vision.GestureRecognizerOptions
    RecognizerResult = GestureRecognizerResult
    VisionRunningMode = vision.RunningMode
    HandLandMark = None
    Gestures = None
    Handedness = None
    Hand_world_landmarks = None
    myResult = HandLandMark, Gestures, Handedness, Hand_world_landmarks


def print_result(result: GestureRecognizerResult, output_image: mp.Image, timestamp_ms: int):
    Var.myResult = (
        result.hand_landmarks, result.gestures, result.handedness, result.hand_world_landmarks
    )
    print(f'gesture recognition result: {result}')


options = Var.GestureRecognizerOptions(
    base_options=baseOptions,
    running_mode=Var.VisionRunningMode.LIVE_STREAM,
    num_hands=1,
    min_hand_presence_confidence=0.3,
    min_hand_detection_confidence=0.3,
    min_tracking_confidence=0.3,
    result_callback=print_result)


def draw_landmarks_on_image(image, results):
    images = image
    gestures = results[1]
    multi_hand_landmarks_list = results[0]

    # Auto-squaring: this will drop data that does not fit into square or square-ish rectangle.
    rows = int(math.sqrt(len(images)))
    cols = len(images) // rows

    # hand_landmarks_list = results.hand_landmarks
    annotated_image = image.copy()

    # Loop through the detected poses to visualize.
    # Display gestures and hand landmarks.
    for i, (image, gestures) in enumerate(zip(images[:rows * cols], gestures[:rows * cols])):
        annotated_image = image.copy()

        for hand_landmarks in multi_hand_landmarks_list[i]:
            hand_landmarks_proto = landmark_pb2.NormalizedLandmarkList()
            hand_landmarks_proto.landmark.extend([
                landmark_pb2.NormalizedLandmark(x=landmark.x, y=landmark.y, z=landmark.z) for landmark in hand_landmarks
            ])

            mp_drawing.draw_landmarks(
                annotated_image,
                hand_landmarks_proto,
                mp_hands.HAND_CONNECTIONS,
                mp_drawing_styles.get_default_hand_landmarks_style(),
                mp_drawing_styles.get_default_hand_connections_style())
    return annotated_image


def set_cam():
    # 設定相機來源
    cam = cv2.VideoCapture(0)

    # 調整視訊流的解析度
    cam.set(cv2.CAP_PROP_FRAME_WIDTH, 128)
    cam.set(cv2.CAP_PROP_FRAME_HEIGHT, 96)

    # 調整視訊流的幀率
    cam.set(cv2.CAP_PROP_FPS, 30)
    return cam


if __name__ == "__main__":
    print(mp.__version__)  # version = 0.10.8
    print(cv2.__version__)  # version = 4.8.1

    # process image with recognizer
    with Var.GestureRecognizer.create_from_options(options) as recognizer:
        cap = set_cam()
        flag = False
        while cv2.waitKey(1) & 0XFF != ord('q'):
            ret, frame = cap.read()
            mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=frame)
            recognizer.recognize_async(
                image=mp_image, timestamp_ms=int(time.time() * 1000))
            # unittest.TestCase.assertIsInstance(obj=Var.RecognizerResult, cls=GestureRecognizerResult)
            if flag:
                draw_landmarks_on_image(frame, Var.myResult)
            flag = True
            cv2.imshow('frame', frame)
        cap.release()
        cv2.destroyAllWindows()
