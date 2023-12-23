import tkinter as tk
from functools import partial
from copy import deepcopy
from tkinter import messagebox
from MCTS import MCTS

class TicTacToeGUI:
    def __init__(self, root, player1, player2):
        frame = tk.Frame(bg="#B4BDFF", bd=10)  # Light gray background color, border width=10, ridge relief
        frame.grid(padx=10, pady=10)
        self.root = root
        self.root.title("Tic Tac Toe")
        self.root.iconbitmap('favicon.ico')
        self.board = Board()
        self.current_player = player1
        self.player1 = player1
        self.player2 = player2
        self.empty_text = ""
        self.buttons = [[None, None, None] for _ in range(3)]
        for i in range(3):
            for j in range(3):
                self.buttons[i][j] = tk.Button(
                    frame,
                    text=self.empty_text,
                    width=4,
                    height=2,
                    font=("Helvetica", 30, "bold"),
                    # command=lambda i=i, j=j: self.callback(self.buttons[i][j]),
                    command=partial(self.make_move, i, j),
                    bg="#83A2FF",  # Button color
                    fg="#FFE3BB"     # Text color
                )
                self.buttons[i][j].grid(row=i, column=j, padx=5, pady=5)  # Add some padding

        self.reset_button = tk.Button(text="Play Again??", command=self.reset_game, bg="#2E97A7", fg="white", font=("Helvetica", 12, "bold"), relief=tk.GROOVE)
        self.reset_button.grid(row=6, pady=(0, 10))
        # self.reset_button = tk.Button(text="Play Again??", command=self.reset, bg="#2E97A7", fg="white", font=("Helvetica", 12, "bold"), relief=tk.GROOVE)
        # self.reset_button.grid(row=6, pady=(0, 10))
        # for i in range(3):
        #     for j in range(3):
        #         self.buttons[i][j] = tk.Button(root, text="", font=('normal', 20), width=5, height=2,
        #                                        command=partial(self.make_move, i, j))
        #         self.buttons[i][j].grid(row=i, column=j)

    def make_move(self, row, col):
        if self.board.position[row, col] == self.board.empty_square:
            self.board = self.board.make_move(row, col)
            self.update_board()

            if self.board.is_win():
                messagebox.showinfo("Game Over", f"Player {self.current_player.mark} wins!")
          
            elif self.board.is_draw():
                messagebox.showinfo("Game Over", "It's a draw!")
               
            else:
                self.switch_players()

            if self.current_player == self.player2:
                self.ai_move()

    def switch_players(self):
        self.current_player = self.player2 if self.current_player == self.player1 else self.player1

    def ai_move(self):
        best_move = self.player2.get_move(self.board)
        self.board = best_move
        self.update_board()

        if self.board.is_win():
            messagebox.showinfo("Game Over", f"Player {self.current_player.mark} wins!")
          
        elif self.board.is_draw():
            messagebox.showinfo("Game Over", "It's a draw!")
           
        else:
            self.switch_players()

    def update_board(self):
        for i in range(3):
            for j in range(3):
                self.buttons[i][j]['text'] = self.board.position[i, j]
                self.buttons[i][j]['state'] = 'disabled' if self.board.position[i, j] != self.board.empty_square else 'normal'

    def reset_game(self):
        self.board = Board()
        self.current_player = self.player1

        for i in range(3):
            for j in range(3):
                self.buttons[i][j]['text'] = ""
                self.buttons[i][j]['state'] = 'normal'


class Player:
    def __init__(self, mark):
        self.mark = mark
        self.get_opponent_mark()

    def get_opponent_mark(self):
        if self.mark == 'X':
            self.opponent_mark = 'O'
        elif self.mark == 'O':
            self.opponent_mark = 'X'
        else:
            print("The player's mark must be either 'X' or 'O'.")


class HumanPlayer(Player):
    pass


class AIPlayer(Player):
    def __init__(self, mark):
        super(AIPlayer, self).__init__(mark=mark)
        self.mcts = MCTS()

    def get_move(self, board):
        return self.mcts.search(board).board


class Board:
    def __init__(self, board=None):
        self.player_1 = 'X'
        self.player_2 = 'O'
        self.empty_square = ' '
        self.position = {}
        self.init_board()
        if board is not None:
            self.__dict__ = deepcopy(board.__dict__)

    def init_board(self):
        for row in range(3):
            for col in range(3):
                self.position[row, col] = self.empty_square

    def make_move(self, row, col):
        board = Board(self)
        board.position[row, col] = self.player_1
        (board.player_1, board.player_2) = (board.player_2, board.player_1)
        return board

    def is_draw(self):
        for row, col in self.position:
            if self.position[row, col] == self.empty_square:
                return False
        return True

    def is_win(self):
        for col in range(3):
            winning_sequence = []
            for row in range(3):
                if self.position[row, col] == self.player_2:
                    winning_sequence.append((row, col))
                if len(winning_sequence) == 3:
                    return True

        for row in range(3):
            winning_sequence = []
            for col in range(3):
                if self.position[row, col] == self.player_2:
                    winning_sequence.append((row, col))
                if len(winning_sequence) == 3:
                    return True

        winning_sequence = []
        for row in range(3):
            col = row
            if self.position[row, col] == self.player_2:
                winning_sequence.append((row, col))
            if len(winning_sequence) == 3:
                return True

        winning_sequence = []
        for row in range(3):
            col = 3 - row - 1
            if self.position[row, col] == self.player_2:
                winning_sequence.append((row, col))
            if len(winning_sequence) == 3:
                return True

        return False

    def generate_states(self):
        actions = []
        for row in range(3):
            for col in range(3):
                if self.position[row, col] == self.empty_square:
                    actions.append(self.make_move(row, col))
        return actions


if __name__ == '__main__':
    player1 = HumanPlayer('X')
    player2 = AIPlayer('O')
    root = tk.Tk()
    game = TicTacToeGUI(root, player1, player2)
    root.mainloop()
