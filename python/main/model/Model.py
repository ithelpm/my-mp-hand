from mediapipe.tasks import python
from mediapipe import solutions

    
class Var:
    mp_hands = solutions.hands
    mp_drawing = solutions.drawing_utils
    mp_drawing_styles = solutions.drawing_styles

    __task_file_path = 'gesture_recognizer.task'
    __model_file = open(f'{__task_file_path}', "rb")
    __model_data = __model_file.read()
    __model_file.close()
    baseOptions = python.BaseOptions(model_asset_buffer=__model_data)