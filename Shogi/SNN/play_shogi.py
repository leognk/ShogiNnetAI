import re

import shogi_engine as egn
import snnAI
import randomAI
from configuration import Configuration


class GameOrganizer:
# Organize shogi games with a given AI (a class).
# The AI must have a "best_move" method.
# The best_move method must take a game state as the input and
# return one of the moves of this state's legal moves list.
    
    def __init__(self, AI):
        self.AI = AI

    def usi_engine(self, usi_engine_name):

        s = egn.GameState()

        while True:
            # Catch the command sent by the GUI.
            usi_command = input()
            
            # The engine is being registered.
            if usi_command == "usi":
                print("id name", usi_engine_name)
                print("usiok")
            
            elif usi_command == "isready":
                print("readyok")
            
            # Save the opponent's last move and update the current game state.
            elif re.search("position startpos moves", usi_command):
                last_move = usi_command.split()[-1]
                s.update(last_move)
            
            # Make a move.
            elif re.search("go", usi_command):
                best_move = self.AI.best_move()
                s.update(best_move)
                print("bestmove", best_move)
            
            elif usi_command == "quit":
                break
    
    def ai_vs_ai(self, max_moves, print_moves=False, print_outcome=False):

        s = egn.GameState()
        
        if print_moves:
            print()
            print(s.string_board())
            print('\n')

        for i in range(1, max_moves + 1):
            best_move = self.AI.best_move(s)
            if best_move == "resign":
                if print_outcome: self.print_outcome(s, i)
                break
            
            s.update(best_move)

            if print_moves: self.print_move(s, best_move, i)
    
    # The AI plays itself step by step. You can cancel a move by pressing 'c'.
    # Stop the game by pressing 's'.
    def ai_vs_ai_step(self, nb_moves, print_moves=False, print_outcome=False):

        s = egn.GameState()

        if print_moves:
            print()
            print(s.string_board())
            print('\n')

        for i in range(1, nb_moves+1):
            instruction = input('')

            if instruction == 's':
                break

            if instruction == 'c':
                s.undo()
                if print_moves: self.print_move(s, "cancel", i)
                continue
            
            best_move = self.AI.best_move()

            if best_move == "resign":
                if print_outcome: self.print_outcome(s, i)
                break

            s.update(best_move)

            if print_moves: self.print_move(s, best_move, i)
    
    def print_move(self, s, move, i):
        print(f"Move number {i}")
        print(f"{s.playing_side} : {move}")
        print("Board after move :")
        print(s.string_board())
        print('\n')
    
    def print_outcome(self, s, i):
        print()
        print(s.string_board())
        print()
        print("Total moves :", i-1)
        print()
        print(f"{s.playing_side} resigns")
    
    def player_vs_player(self):
        s = egn.GameState()
        print()
        print(s.string_board())
        print('\n')
        i = 1
        while True:
            move = input(f"Move number {i} by {s.playing_side} : ")

            if move == "resign":
                print(f"{s.playing_side} resigns")
                break

            elif move == 'c':
                s.undo()
            
            else:
                s.update(move)
            
            print("Board after move :")
            print(s.string_board())
            print()

            i += 1
    
    def ai_vs_player(self):
        s = egn.GameState()
        print()
        player_side = input("Select your side (b or w) : ")
        print()
        print("Initial board position :")
        print(s.string_board())
        print('\n')
        i = 1
        while True:
            if s.playing_side == player_side:
                move = input(f"Move number {i} by {s.playing_side} : ")
                s.update(move)
            else:
                move = self.AI.best_move()
                s.update(move)
                print(f"Move number {i} by {s.playing_side} : {move}")
            if move == "quit":
                break
            elif move == "resign":
                print(f"{s.playing_side} resigns")
                break
            print("Board after move :")
            print(s.string_board())
            print()
            i += 1


if __name__ == "__main__":

    ai = randomAI.RandomAI()
    c = Configuration()
    ai = snnAI.SnnAI(c)

    org = GameOrganizer(ai)
    
    # org.usi_engine("SNN AI")
    org.ai_vs_ai(512, print_moves=True, print_outcome=True)
    # org.ai_vs_player()
    # org.player_vs_player()