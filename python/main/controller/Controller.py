import math
import cv2
import mediapipe as mp
from mediapipe.tasks.python import vision
from mediapipe.framework.formats import landmark_pb2
import numpy as np
from model.Model import Var

class GestureAndResult:
    GestureRecognizer = vision.GestureRecognizer
    GestureRecognizerOptions = vision.GestureRecognizerOptions
    GestureRecognizerResult = vision.GestureRecognizerResult
    VisionRunningMode = vision.RunningMode

    def print_result(self, result: GestureRecognizerResult, output_image: mp.Image, timestamp_ms: int):
        self.GestureRecognizerResult = result
        print('gesture recognition result: {}'.format(result))

    options = GestureRecognizerOptions(
        base_options=Var.baseOptions,
        running_mode=VisionRunningMode.LIVE_STREAM,
        result_callback=print_result)

    def draw_landmarks_on_image(self, images, results):
        images = [image.numpy_view() for image in images]
        gestures = [top_gesture for (top_gesture, _) in results]
        multi_hand_landmarks_list = [multi_hand_landmarks for (_, multi_hand_landmarks) in results]

        # Auto-squaring: this will drop data that does not fit into square or square-ish rectangle.
        rows = int(math.sqrt(len(images)))
        cols = len(images) // rows

        hand_landmarks_list = results.hand_landmarks
        annotated_image = np.copy(image)

        # Loop through the detected poses to visualize.
        # Display gestures and hand landmarks.
        for i, (image, gestures) in enumerate(zip(images[:rows*cols], gestures[:rows*cols])):
            annotated_image = image.copy()

            for hand_landmarks in multi_hand_landmarks_list[i]:
                hand_landmarks_proto = landmark_pb2.NormalizedLandmarkList()
                hand_landmarks_proto.landmark.extend([
                    landmark_pb2.NormalizedLandmark(x=landmark.x, y=landmark.y, z=landmark.z) for landmark in hand_landmarks
                ])

                Var.mp_drawing.draw_landmarks(
                    annotated_image,
                    hand_landmarks_proto,
                    Var.mp_hands.HAND_CONNECTIONS,
                    Var.mp_drawing_styles.get_default_hand_landmarks_style(),
                    Var.mp_drawing_styles.get_default_hand_connections_style())
            return annotated_image  

def set_cam():
    # 設定相機來源
    cap = cv2.VideoCapture(0)

    # 調整視訊流的解析度
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 960)

    # 調整視訊流的幀率
    cap.set(cv2.CAP_PROP_FPS, 30)
    return cap
