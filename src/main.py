from engine import PychessBot
from image_to_board import ImageToBoard




STOCKFISH_PATH = '../stockfish/stockfish-ubuntu-x86-64-avx2'
IMAGE_PATH = 'test/pretty-board.png'

itb = ImageToBoard(IMAGE_PATH)
fen = itb()
print(fen)

bot = PychessBot(STOCKFISH_PATH)