import time, cv2, logging, datetime, pathlib
import mediapipe as mp

task_file_path = f'{pathlib.Path(__file__).parent}/hand_landmarker.task'
model_file = open(task_file_path, "rb")
model_data = model_file.read()
model_file.close()


class Recorder:
    def __init__(self):
        current_time = datetime.datetime.now()
        formatted_date = f'{current_time.strftime("%Y-%m-%d")}'
        logging.basicConfig(filename=f'{formatted_date}.log', encoding='utf-8', level=logging.INFO)
        self.logger = logging.getLogger(f'{formatted_date}.log')

    def info(self, message):
        self.logger.info(message)
    
    def warn(self, message):
        self.logger.warn(message)
recorder = Recorder()


class landmarker_and_result():
    def __init__(self):
        self.result = mp.tasks.vision.HandLandmarkerResult
        self.hand = mp.tasks.vision.HandLandmarker
        self.createLandmarker()
        recorder.info('initiallized')

    def createLandmarker(self):
        recorder.info('creating...')
        # callback function
        def update_result(result: mp.tasks.vision.HandLandmarkerResult, output_image: mp.Image, timestamp_ms: int):
            self.result = result

        options = mp.tasks.vision.HandLandmarkerOptions(
            base_options=mp.tasks.BaseOptions(
                model_asset_buffer=model_data
                ),  # path to model
            running_mode=mp.tasks.vision.RunningMode.LIVE_STREAM,  # running on a live stream
            num_hands=2,  # 要讀取的手的數量
            # lower than value to get predictions more often
            min_hand_detection_confidence=0.3,
            # lower than value to get predictions more often
            min_hand_presence_confidence=0.3,
            min_tracking_confidence=0.3,  # lower than value to get predictions more often
            result_callback=update_result)

        # initialize landmarker
        self.hand = self.hand.create_from_options(options)
        recorder.info('created!')

    def detect_async(self, frame):
        # convert np frame to mp image
        mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=frame)
        # detect landmarks
        self.hand.detect_async(
            image=mp_image, timestamp_ms=int(time.time() * 1000))

    def close(self):
        # close landmarker
        self.hand.close()
        recorder.info('closing...')

def set_cam():
    # 設定相機來源
    cap = cv2.VideoCapture(1)

    # 調整視訊流的解析度
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 960)

    # 調整視訊流的幀率
    cap.set(cv2.CAP_PROP_FPS, 30)
    return cap

def main():
    mp_drawing = mp.solutions.drawing_utils
    mp_hands = mp.solutions.hands
    hands = mp_hands.Hands(static_image_mode=False )

    # access webcam
    cap = set_cam()
    recorder.info('webcam opened!')
    hand_landmarker = landmarker_and_result()

    while True:
        # pull frame
        ret, frame = cap.read()
        results = hands.process(frame)

        # update landmarker results
        hand_landmarker.detect_async(frame)
        # 繪製手部關節點
        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                mp_drawing.draw_landmarks(
                    frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)
            recorder.info('captured frame processed')
        cv2.imshow('frame', frame)

        recorder.info(hand_landmarker.result)
        print(hand_landmarker.result)
        if cv2.waitKey(1) == ord('q'):
            break


    # release everything
    recorder.info("stopping...")
    cap.release()
    cv2.destroyAllWindows()
    hand_landmarker.close()


if __name__ == "__main__":
    print(mp.__version__)   # version = 0.10.7
    print(cv2.__version__)  # version = 4.8.1

    # create landmarker
    main()
    
    # end of process
    recorder.info('closed')
    