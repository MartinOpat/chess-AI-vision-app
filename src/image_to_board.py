from board_to_fen.board_to_fen.predict import get_fen_from_image
from PIL import Image

import tensorflow as tf
import os

# Configure TensorFlow logging
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'  # Suppress TensorFlow logging
tf.get_logger().setLevel('ERROR')

W = 1
B = 0

class ImageToBoard:
    def __init__(self, path_to_image: str):
        self.path_to_image = path_to_image

    def __call__(self, us=W):
        try:
            img = Image.open(self.path_to_image)
        except:
            print("Error opening image")
            return None
        return get_fen_from_image(img, black_view=us==B)
    

# # # IMAGE_PATH = 'src/test/pretty-board.png'
# # # IMAGE_PATH = 'src/board_to_fen/test_images/test_image2.jpeg'
IMAGE_PATH = 'src/board_to_fen/test_images/no_edges.png'

# # # print(get_fen_from_image(IMAGE_PATH))


img = Image.open(IMAGE_PATH)
# # print("HERE", img)

# print(get_fen_from_image(img, black_view=True))
# itb = ImageToBoard(IMAGE_PATH)()
# print(itb)
# # print(itb())