import datetime
import sys
import chess
import chess.svg
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QLineEdit, QLabel
from PyQt5.QtSvg import QSvgWidget
from PyQt5.QtCore import QByteArray, Qt
from mcts import Node, mcts_pred  # Import from your MCTS module
from minimax import Minimax
from iterative_deepening import IterativeDeepening


class ChessGame:
    def __init__(self):
        self.board = chess.Board()

    def minimax_move(self):

        if not self.is_game_over()[0]:
            print("Computer is thinking...")
            time_before = datetime.datetime.now()
            move = Minimax.minimaxRoot(self.board, 3, True, time_before,
                                       5)  # Depth set at 3 and time limit at 5 seconds
            time_after = datetime.datetime.now()
            if move is not None:
                move = chess.Move.from_uci(str(move))
                self.board.push(move)
            else:
                print("No valid moves found by Minimax or time exceeded.")
            print("Time taken per move: ", (time_after - time_before), "seconds")

    def iterative_deepening_move(self):
        if not self.is_game_over()[0]:
            print("Computer is thinking using iterative deepening...")
            time_before = datetime.datetime.now()
            # move = self.iterative_deepening.iterative_deepening(self.board, True, 3, 5)
            move = IterativeDeepening.iterative_deepening(self.board, 3, True, 5)
            time_after = datetime.datetime.now()
            if move is not None:
                self.board.push(move)
            else:
                print("No valid moves found or time exceeded.")
            print("Time taken for move: ", (time_after - time_before), "seconds")

    def mcts_computer_move(self):
        print("Computer is thinking...")
        time_before = datetime.datetime.now()
        root = Node(self.board.copy())
        best_move = mcts_pred(root, self.board.is_game_over(), self.board.turn)
        time_after = datetime.datetime.now()
        if best_move:
            self.board.push_san(best_move)
        print("Time taken per move: ", (time_after - time_before), "seconds")

    def is_game_over(self):
        # return self.board.is_game_over()
        outcome = self.board.outcome()
        if outcome is not None:
            if outcome.winner is None:
                return (True, "Draw!")
            elif outcome.winner:
                return (True, "White wins!")
            else:
                return (True, "Black wins!")
        return (False, "")


class InteractiveChessBoard(QSvgWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFixedSize(600, 600)  # This matches the 8x8 board at 75 pixels each square

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            x = event.x()
            y = event.y()
            row = 7 - (y // 75)  # Make sure the origin (0, 0) corresponds to the bottom-left
            col = x // 75
            if 0 <= row < 8 and 0 <= col < 8:  # Ensure the click is within the board bounds
                square = chess.square(col, row)
                self.parent().square_clicked(chess.SQUARE_NAMES[square])
            else:
                print("Clicked outside the board boundaries.")


class ChessGUI(QWidget, ChessGame):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Chess')
        self.setGeometry(100, 100, 600, 600)
        self.layout = QVBoxLayout()

        # Chess board display
        self.svgWidget = InteractiveChessBoard(self)  # Use the interactive board
        self.layout.addWidget(self.svgWidget)

        # NOT REQUIRED JAY_1
        # self.moveInput = QLineEdit(self)
        # self.moveInput.setPlaceholderText('Your move (e.g., e2e4)')
        # self.layout.addWidget(self.moveInput)

        # NOT REQUIRED JAY_1
        # self.userMoveButton = QPushButton('User Move', self)
        # self.userMoveButton.clicked.connect(self.make_user_move)
        # self.layout.addWidget(self.userMoveButton)

        # Button for the computer to make a MCTS move
        self.computerMoveButton = QPushButton('MCTS Move', self)
        self.computerMoveButton.clicked.connect(self.make_computer_move)
        self.layout.addWidget(self.computerMoveButton)

        # Button for the computer to make a move using Minimax
        self.minimaxMoveButton = QPushButton('Minimax Move', self)
        self.minimaxMoveButton.clicked.connect(self.make_minimax_move)
        self.layout.addWidget(self.minimaxMoveButton)

        self.iterDeepeningMoveButton = QPushButton('Iterative Deepening Move', self)
        self.iterDeepeningMoveButton.clicked.connect(self.make_iterative_deepening_move)
        self.layout.addWidget(self.iterDeepeningMoveButton)

        self.statusLabel = QLabel("Game in progress...")
        self.layout.addWidget(self.statusLabel)

        self.setLayout(self.layout)
        self.update_board()

    def square_clicked(self, square):
        print(f"Square clicked: {square}")
        if hasattr(self, 'source_square'):
            move_uci = f"{self.source_square}{square}"
            try:
                move = chess.Move.from_uci(move_uci)
                if move in self.board.legal_moves:
                    self.board.push(move)
                    self.update_board()
                    delattr(self, 'source_square')  # Clear the source square after making a move
                else:
                    print("Illegal move attempted.")
                    # Optionally reset the source square if the move was illegal
                    delattr(self, 'source_square')
            except:
                print("Illegal move attempted.")
                # Optionally reset the source square if the move was illegal
                delattr(self, 'source_square')
        else:
            self.source_square = square

    def update_board(self):
        last_move = self.board.peek() if self.board.move_stack else None
        svg_bytes = chess.svg.board(self.board, lastmove=last_move).encode('utf-8')
        self.svgWidget.load(QByteArray(svg_bytes))
        game_over, result = self.is_game_over()
        if game_over:
            self.statusLabel.setText(result)
            # self.userMoveButton.setDisabled(True)
            self.computerMoveButton.setDisabled(True)
            self.minimaxMoveButton.setDisabled(True)
            self.iterDeepeningMoveButton.setDisabled(True)
            print(result)

    # NOT REQUIRED JAY_1
    # def make_user_move(self):
    #     if not self.is_game_over()[0]:
    #         player_move = self.moveInput.text()
    #         if player_move:
    #             try:
    #                 move = chess.Move.from_uci(player_move)
    #                 if move in self.board.legal_moves:
    #                     self.board.push(move)
    #                     self.update_board()
    #                     self.moveInput.clear()
    #                 else:
    #                     print("Illegal move. Try again.")
    #             except ValueError:
    #                 print("Invalid move format. Please use UCI format (e.g., e2e4).")
    #         # if self.is_game_over():
    #         #     self.userMoveButton.setDisabled(True)
    #         #     self.computerMoveButton.setDisabled(True)
    #         #     print("Game Over")
    #     self.update_board()

    def make_computer_move(self):
        if not self.is_game_over()[0]:
            self.mcts_computer_move()
            self.update_board()
            # if self.is_game_over()[0]:
            #     self.userMoveButton.setDisabled(True)
            #     self.computerMoveButton.setDisabled(True)
            #     print("Game Over")

    def make_minimax_move(self):
        if not self.is_game_over()[0]:
            self.minimax_move()
            self.update_board()
            # if self.is_game_over()[0]:
            #     self.userMoveButton.setDisabled(True)
            #     self.minimaxMoveButton.setDisabled(True)
            #     print("Game Over")

    def make_iterative_deepening_move(self):
        if not self.is_game_over()[0]:
            self.iterative_deepening_move()
            self.update_board()


def main():
    app = QApplication(sys.argv)
    ex = ChessGUI()
    ex.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
