import cv2, logging, datetime
import mediapipe as mp


class Recorder:
    def __init__(self):
        current_time = datetime.datetime.now()
        formatted_date = f'{current_time.strftime("%Y-%m-%d.%H-%M-%S")}'
        logging.basicConfig(filename=f'{formatted_date}.log', encoding='utf-8', level=logging.INFO)
        self.logger = logging.getLogger(f'{formatted_date}.log')

    def info(self, message):
        self.logger.info(message)
    
    def warn(self, message):
        self.logger.warn(message)
recorder = Recorder()

def main():
    mp_drawing = mp.solutions.drawing_utils
    mp_hands = mp.solutions.hands

    hands = mp_hands.Hands(static_image_mode=False )
    cap = cv2.VideoCapture(0)
    # 調整視訊流的解析度
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 960)

    # 調整視訊流的幀率
    cap.set(cv2.CAP_PROP_FPS, 30)

    recorder.info('webcam opened!')
    while True:
        ret, frame = cap.read()
        results = hands.process(frame)
        recorder.info('captured frame processed')
        # 繪製手部關節點
        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                mp_drawing.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

        cv2.imshow("Image", frame)
        if cv2.waitKey(1) == ord("q"):
            break
    cap.release()
    recorder.info("stopping...")

if __name__ == "__main__":
    main()
    recorder.info('stopped!')