import numpy as np
import tkinter as tk
from board import Board
import tkinter.messagebox as messagebox

class Game:
    def __init__(self, master, player1, player2, Q_learn=None, Q={}, alpha=0.3, gamma=0.9):

        #styling the tkinter board
        frame = tk.Frame(bg="#B4BDFF", bd=10)  
        frame.grid(padx=10, pady=10) 

        self.master = master
        master.title("Tic Tac Toe")
        master.iconbitmap('favicon.ico')

        self.player1 = player1
        self.player2 = player2
        self.current_player = player1
        self.other_player = player2
        self.empty_text = ""        #text to be displayed on the unfilled grids
        self.board = Board()

        self.buttons = [[None for _ in range(3)] for _ in range(3)] #all the grids on the boards willact as buttons

        for i in range(3):
            for j in range(3):

                #styling the grids on rhe board
                self.buttons[i][j] = tk.Button(
                    frame,
                    text=self.empty_text,
                    width=4,
                    height=2,
                    font=("Helvetica", 30, "bold"),
                    command=lambda i=i, j=j: self.callback(self.buttons[i][j]),
                    bg="#83A2FF",  # Button color
                    fg="#676767"     # Text color
                )
                self.buttons[i][j].grid(row=i, column=j, padx=5, pady=5)  # Add some padding


        self.reset_button = tk.Button(text="Play Again??", command=self.reset, bg="#2E97A7", fg="white", font=("Helvetica", 12, "bold"), relief=tk.GROOVE)
        self.reset_button.grid(row=6, pady=(0, 10))


        self.Q_learn = Q_learn
        self.Q_learn_or_not()
        if self.Q_learn:
            self.Q = Q
            self.alpha = alpha          # Learning rate
            self.gamma = gamma          # Discount rate
            self.share_Q_with_players()

    # checking if either of the 2 players is a QPlayer ie. capable of Q-learning, start Q-learning
    def Q_learn_or_not(self):       
        if self.Q_learn is None:
            if isinstance(self.player1, QPlayer) or isinstance(self.player2, QPlayer):
                self.Q_learn = True

    # The action value table Q is shared with the QPlayers to help them make their move decisions
    def share_Q_with_players(self):            
        if isinstance(self.player1, QPlayer):
            self.player1.Q = self.Q
        if isinstance(self.player2, QPlayer):
            self.player2.Q = self.Q

    #This method is called when a button ie. a grid on the board is clicked.
    #It manages player moves based on the button clicked and the type of players playing the game.
    def callback(self, button):
        if self.board.over():
            pass                # Do nothing if the game is already over
        else:
            if isinstance(self.current_player, HumanPlayer) and isinstance(self.other_player, HumanPlayer):
                if self.empty(button):  #check if the grid is empty ie. it is a valid move
                    move = self.get_move(button)    #get the coordinates of the grid
                    self.handle_move(move)

            elif isinstance(self.current_player, HumanPlayer) and isinstance(self.other_player, ComputerPlayer):
                computer_player = self.other_player
                if self.empty(button):
                    human_move = self.get_move(button)
                    self.handle_move(human_move)

                    #if the game is not over yet, make the computer play the next move
                    if not self.board.over():             
                        computer_move = computer_player.get_move(self.board)
                        self.handle_move(computer_move)

    #check if the current button ie. grid is empty ie. a valid move or not
    def empty(self, button):
        return button["text"] == self.empty_text

    # Get move coordinates of the current button grid
    def get_move(self, button):
        info = button.grid_info()
        move = (int(info["row"]), int(info["column"]))               
        return move

    def handle_move(self, move):
        if self.Q_learn:
            self.learn_Q(move)

        # To get row and column number of the corresponding button
        i, j = move         
        self.buttons[i][j].configure(text=self.current_player.mark)     # Change the label on the button to the current player's mark
        self.board.place_mark(move, self.current_player.mark)           # Update the board
        
        #if game is over then declare outcome as amesasge box else switch both players for the next turn 
        if self.board.over():
            self.declare_outcome()
        else:
            self.switch_players()


    def declare_outcome(self):
        if self.board.winner() is None:
            print ("Draw match")
        else:
            print("The game is over. The player with mark %s won!" % self.current_player.mark)

    def declare_outcome_test(self):
        if self.board.winner() is None:
            print ("Draw match")
            messagebox.showinfo("Game Over", "Draw match")
            
        else:
            print("The game is over. The player with mark %s won!" % self.current_player.mark)
            winner_mark = self.current_player.mark
            messagebox.showinfo("Game Over", f"The game is over. The player with mark {winner_mark} won!")
            

    def reset(self):
        print("Resetting...")
        for i in range(3):
            for j in range(3):
                self.buttons[i][j].configure(text=self.empty_text)  #resetting all the buttons as unfilled
        self.board = Board(grid=np.ones((3,3))*np.nan)
        self.current_player = self.player1
        self.other_player = self.player2
        self.play()

    #after each turrn, the players will be switched
    def switch_players(self):
        if self.current_player == self.player1:
            self.current_player = self.player2
            self.other_player = self.player1
        else:
            self.current_player = self.player1
            self.other_player = self.player2

    def play(self):

        # For human vs. human, play relies on the buttons pressed by the humans, so no more code required
        if isinstance(self.player1, HumanPlayer) and isinstance(self.player2, HumanPlayer):
            pass        

        #if the current player is human, then current move will depend on the human itself
        elif isinstance(self.player1, HumanPlayer) and isinstance(self.player2, ComputerPlayer):
            pass

        elif isinstance(self.player1, ComputerPlayer) and isinstance(self.player2, HumanPlayer):
            first_computer_move = self.player1.get_move(self.board)      # If player 1 is a computer, it needs to be triggered to make the first move.
            self.handle_move(first_computer_move)
        
        #if both are computers ie, while training, best moves will be taken and game will go on
        elif isinstance(self.player1, ComputerPlayer) and isinstance(self.player2, ComputerPlayer):
            while not self.board.over():        # Make the two computer players play against each other without button presses
                self.play_turn()
            

    def play_turn(self):
        move = self.current_player.get_move(self.board)
        self.handle_move(move)

    # If Q-learning is toggled on, "learn_Q" should be called after receiving a move from an instance of Player and before implementing the move (using Board's "place_mark" method)
    def learn_Q(self, move):                       
        state_key = QPlayer.make_and_maybe_add_key(self.board, self.current_player.mark, self.Q)
        next_board = self.board.get_next_board(move, self.current_player.mark)  #mark the current move on the board and continune the game
        reward = next_board.give_reward()   #checking if any player wins to give reward
        
        next_state_key = QPlayer.make_and_maybe_add_key(next_board, self.other_player.mark, self.Q)
        if next_board.over():
            expected = reward
        else:
            next_Qs = self.Q[next_state_key]             # The Q values represent the expected future reward for player X for each available move in the next state (after the move has been made)
            if self.current_player.mark == "X":
                expected = reward + (self.gamma * min(next_Qs.values()))        # If the current player is X, the next player is O, and the move with the minimum Q value should be chosen according to our "sign convention"
            elif self.current_player.mark == "O":
                expected = reward + (self.gamma * max(next_Qs.values()))        # If the current player is O, the next player is X, and the move with the maximum Q vlue should be chosen
        change = self.alpha * (expected - self.Q[state_key][move])
        self.Q[state_key][move] += change

class Player(object):
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

class ComputerPlayer(Player):
    pass

#returns a random move from the available moves
class RandomPlayer(ComputerPlayer):
    @staticmethod
    def get_move(board):
        moves = board.available_moves()
        if moves:   # If "moves" is not an empty list (as it would be if the game is tie)
            return moves[np.random.choice(len(moves))]    # Apply random selection to the index, as otherwise it will be seen as a 2D array

#identifies and tries to make the best possible move to win or blocking the opponent from winning
class THandPlayer(ComputerPlayer):
    def __init__(self, mark):
        super(THandPlayer, self).__init__(mark=mark)

    def get_move(self, board):
        moves = board.available_moves()
        if moves:
            for move in moves:
                if THandPlayer.next_move_winner(board, move, self.mark):    #if the move results in win, then it return that move
                    return move
                elif THandPlayer.next_move_winner(board, move, self.opponent_mark): #If no immediate winning move is found, it checks for moves that prevent the opponent from winning in the next move. If found, it returns that move.
                    return move
            else:
                return RandomPlayer.get_move(board)     # if none of the obove moves are there, it returns a random move

    @staticmethod
    def next_move_winner(board, move, mark):
        return board.get_next_board(move, mark).winner() == mark

#will incorporate Qleaning to get the best possible move
class QPlayer(ComputerPlayer):
    def __init__(self, mark, Q={}, epsilon=0.2):
        super(QPlayer, self).__init__(mark=mark)
        self.Q = Q
        self.epsilon = epsilon      #probability of exploration for epsilon-greedy strategy

    def get_move(self, board):
        if np.random.uniform() < self.epsilon:              # With probability epsilon, choose a move at random ("epsilon-greedy" exploration)
            return RandomPlayer.get_move(board)
        else:                                               #if not random, then choose a move based on Q values
            state_key = QPlayer.make_and_maybe_add_key(board, self.mark, self.Q)
            print(state_key)
            Qs = self.Q[state_key]
            print(Qs)

            #For "X" players, it looks for the move with the maximum Q-value and for "Y" players, it looks for the move with the manimum Q-value among the available moves
            if self.mark == "X":
                print(QPlayer.stochastic_argminmax(Qs, max))
                return QPlayer.stochastic_argminmax(Qs, max)
            elif self.mark == "O":
                print(QPlayer.stochastic_argminmax(Qs, min))
                return QPlayer.stochastic_argminmax(Qs, min)

    @staticmethod
    # Make a dictionary key for the current state (board + player turn) and if Q does not yet have it, add it to Q
    def make_and_maybe_add_key(board, mark, Q):     
        default_Qvalue = 1.0       # Encourages exploration
        state_key = board.make_key(mark)
        if Q.get(state_key) is None:
            moves = board.available_moves()
            Q[state_key] = {move: default_Qvalue for move in moves}    # The available moves in each state are initially given a default value of zero
        return state_key

    @staticmethod
    def stochastic_argminmax(Qs, min_or_max):       # Determines either the argmin or argmax of the array Qs such that if there are 'ties', one is chosen at random
        min_or_maxQ = min_or_max(Qs.values())
        count_of_min_or_max = list(Qs.values()).count(min_or_maxQ)
        if (count_of_min_or_max) > 1:      # If there is more than one move corresponding to the maximum Q-value, choose one at random
            best_options = [move for move in Qs.keys() if Qs[move] == min_or_maxQ]
            move = best_options[np.random.choice(len(best_options))]
        else:
            move = min_or_max(Qs, key=Qs.get)
        return move

