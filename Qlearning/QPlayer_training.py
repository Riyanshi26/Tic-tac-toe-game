import tkinter as tk    # Importing the Tkinter library for GUI
import pickle    
from ttt_game import Game, QPlayer

tk.wantobjects = False
root = tk.Tk()
epsilon = 0.9

# making the 2 players play against each other and the result will be stored in the Qtable for training
player1 = QPlayer(mark="X",epsilon = epsilon)
player2 = QPlayer(mark="O",epsilon = epsilon)
game = Game(root, player1, player2)

N_episodes = 20000
for episodes in range(N_episodes):
    game.play()
    game.reset()

Q = game.Q

filename = "Q_table_dictionary.p" 
pickle.dump(Q, open(filename, "wb"))
