from board_to_fen.board_to_fen.predict import get_fen_from_image
from PIL import Image

W = 1
B = 0

class ImageToBoard:
    def __init__(self, path_to_image: str):
        self.path_to_image = path_to_image

    def __call__(self, us=W):
        img = Image.open(self.path_to_image)
        return get_fen_from_image(img, black_view=us==B)
    

# # IMAGE_PATH = 'src/test/pretty-board.png'
# # IMAGE_PATH = 'src/board_to_fen/test_images/test_image2.jpeg'
# IMAGE_PATH = 'src/board_to_fen/test_images/no_edges.png'

# # print(get_fen_from_image(IMAGE_PATH))


# img = Image.open(IMAGE_PATH)
# print("HERE", img)

# print(get_fen_from_image(img))