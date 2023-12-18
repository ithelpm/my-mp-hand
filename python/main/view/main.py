import time, cv2
import mediapipe as mp
from controller.Controller import GestureAndResult, set_cam


GnR = GestureAndResult()

with GnR.GestureRecognizer.create_from_options(GnR.options) as recognizer:
    cap = set_cam()
    while True:
        ret, frame = cap.read()
        mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=frame)
        recognizer.recognize_async(image=mp_image, timestamp_ms=int(time.time() * 1000))
        # GnR.draw_landmarks_on_image(frame, (GnR.GestureRecognizerResult.gestures[0][0], GnR.GestureRecognizerResult.hand_landmarks))
        cv2.imshow('frame', frame)
        if cv2.waitKey(1) & 0XFF == ord('q'):
            break
    cap.release()
    cv2.destroyAllWindows

