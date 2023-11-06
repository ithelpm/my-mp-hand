import cv2, logging, datetime, socket, asyncio
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

async def send_img(img):
    while True:
        byte_arr = convert_image_to_byte_array(img)
        send_byte_array(byte_arr, 'localhost', 8080)
        await asyncio.sleep(0.1)

async def get_img(ret, img):
    while True:
        if ret:
                return img
        else:
            await asyncio.sleep(0.1)

async def set_cam():
    cap = cv2.VideoCapture(0)
    # 調整視訊流的解析度
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 960)

    # 調整視訊流的幀率
    cap.set(cv2.CAP_PROP_FPS, 30)
    return cap


async def main_loop():
    mp_drawing = mp.solutions.drawing_utils
    mp_hands = mp.solutions.hands

    hands = mp_hands.Hands(static_image_mode=False )
    cap = await set_cam()

    recorder.info('webcam opened!')

    while True:
        ret, frame = cap.read()
        results = hands.process(frame)
        # 繪製手部關節點
        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                mp_drawing.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)
            recorder.info('captured frame processed')
        send_img(await get_img(ret, frame))
        cv2.imshow('frame', frame)
        byte_arr = convert_image_to_byte_array(frame)
        send_byte_array(byte_arr, 'localhost', 8080)
        if cv2.waitKey(1) == ord("q"):
            break
    cap.release()
    recorder.info("stopping...")

def convert_image_to_byte_array(image):
    """Converts an image to a byte array.

    Args:
        image: A OpenCV image.

    Returns:
        A byte array containing the image data.
    """

    retval, image_byte_array = cv2.imencode(".jpg", image)
    return image_byte_array

def send_byte_array(byte_array, host, port):
    """Sends a byte array to a Java application using UDP.

    The TCP/IP should be socket.SOCK_STREAM.

    Args:
        byte_array: A byte array to send.
        host: The host IP address of the Java application.
        port: The port number of the Java application.
    """

    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_RCVBUF, 1024*1024)
    sock.connect((host, port))
    sock.sendall(byte_array)
    sock.close()

if __name__ == "__main__":
    asyncio.run(main_loop())
    recorder.info('stopped!')