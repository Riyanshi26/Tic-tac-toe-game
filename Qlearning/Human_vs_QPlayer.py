import tkinter as tk    # Importing the Tkinter library for GUI
import pickle  
from ttt_game import Game, HumanPlayer, QPlayer
tk.wantobjects = False

#this will load the Qtable that was generated during training
Q = pickle.load(open("Q_table_dictionary.p", "rb"))

root = tk.Tk()

#The human player is 'X' playing against coputer player 'O'
player1 = HumanPlayer(mark="X")     
player2 = QPlayer(mark="O", epsilon=0)

game = Game(root, player1, player2, Q=Q)

game.play()
root.mainloop()
