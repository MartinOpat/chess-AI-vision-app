import chess
import chess.engine
import chess.svg
import chess.pgn

from abc import ABC, abstractmethod




class ChessBotClass(ABC):
    @abstractmethod
    def __call__(self, board_fen: str) -> chess.Move:
        pass


class PychessBot(ChessBotClass):
    def __init__(self, engine_path: str):
        self.engine = chess.engine.SimpleEngine.popen_uci(engine_path)
        self.board = chess.Board()

    def __call__(self, board_fen: str) -> chess.Move:
        self.board = chess.Board(board_fen)
        result = self.engine.play(self.board, chess.engine.Limit(time=3))
        return result.move

