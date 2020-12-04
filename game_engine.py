import numpy as np

import randomAI
import snnAI



class GameState:

    def __init__(self):
        self.board = np.zeros((2, 3, 3), dtype=np.int8)
        self.side = 0
        self.legal_moves = []
        self.update_legal_moves()
        self.num_moves = 0
        self.finished = False
        # The winner is 0 or 1 or 2 if it's a draw.
        self.winner = -1
        self.history = []

    # Update the state after the move by the current side.
    # A move is a pair of integers representing a square.
    def update(self, move):
        x, y = move
        self.board[self.side, x, y] = 1
        self.side = 1 - self.side
        self.update_legal_moves()
        self.num_moves += 1
        if self.num_moves >= 5:
            self.update_finished()
        self.history.append(move)
    
    # Return the list of the legal moves.
    def update_legal_moves(self):
        self.legal_moves = []
        for x in range(3):
            for y in range(3):
                if not self.board[0,x,y] and not self.board[1,x,y]:
                    self.legal_moves.append((x,y))
    
    # Return True if the side of the plane (self.board[side]) wins.
    def win(self, plane):
        for i in range(3):
            if plane[i,:].all() or plane[:,i].all():
                return True
        ids = np.arange(3)
        if plane[ids,ids].all() or plane[::-1,:][ids,ids].all():
            return True
        return False
    
    # Update the 'finished' and the 'winner' atributes.
    def update_finished(self):
        win0 = self.win(self.board[0])
        win1 = self.win(self.board[1])
        draw = (self.num_moves == 3*3) and not (win0 or win1)
        if win0: self.winner = 0
        elif win1: self.winner = 1
        elif draw: self.winner = 2
        self.finished = (self.winner != -1)
    
    def string_board(self):
        res = ''
        blank = ' ' * 3
        for x in range(3):
            for y in range(3):
                if self.board[0,x,y]:
                    res += 'X' + blank
                elif self.board[1,x,y]:
                    res += 'O' + blank
                else:
                    res += '.' + blank
            if x != 2: res += '\n\n'
        return res



if __name__ == '__main__':

    from encoding import *
    from configuration import Configuration

    c = Configuration()

    randAI = randomAI.RandomAI()
    nnAI = snnAI.SnnAI(c)

    nnAI_plays = True
    human_plays = True

    s = GameState()
    while not s.finished:

        if human_plays and not nnAI_plays:
            move_str = input("\nChoose your move: ")
            move = tuple(int(x) for x in move_str.split(','))
        
        elif nnAI_plays:
            v = nnAI.nnet(encode_game_state(s).unsqueeze(0).cuda()) # pylint: disable=E
            v = v.squeeze(0).detach().cpu().numpy()
            print(
                f"\n{v}"
            )
            move = nnAI.best_move(s)
        
        else:
            move = randAI.best_move(s)

        s.update(move)

        print(
            f"\n{s.string_board()}"
            + "\n" + "_" * 10
        )

        nnAI_plays = not nnAI_plays
    
    if s.winner != 2:
        print(f"\n\nWinner: {'X' if s.winner == 0 else 'O'}")
    else:
        print("\n\nDraw")