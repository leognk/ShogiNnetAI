import numpy as np
import torch

import game_engine as egn
import encoding
import snnAI
import jsonManager


class Game:
# A shogi game data structure.
# Has the history of the game and can give a position of the game
# and its label. Used for the training of the neural net.

    def __init__(self, history, winner):
        self.history = history
        self.winner = winner
    
    # # Return the encoded game state of the position reached before
    # # the move with the index 'move_idx' (in the game history) was played
    # # and its label.
    # def get_labelled_pos(self, c, move_idx):
    #     s = self.get_s(move_idx)
    #     return (
    #         encoding.encode_game_state(s),
    #         self.label_pos(s, move_idx)
    #     )

    def get_labelled_pos(self, c, move_idx):
        s = self.get_s(move_idx)
        a_id = np.ravel_multi_index(
            self.history[move_idx], (3, 3)
        )
        z_move = self.label_pos(s)
        return (
            encoding.encode_game_state(s),
            a_id, z_move
        )
    
    # Return the state corresponding to the light state before
    # the move of index 'move_idx' is played.
    def get_s(self, move_idx):
        s = egn.GameState()
        for i in range(move_idx):
            s.update(self.history[i])
        return s
    
    # # Label the move 'move_idx' from the position before 'move_idx'.
    # def label_pos(self, s, move_idx):

    #     z = torch.zeros(3, 3) + 10

    #     if self.winner == 2:
    #         move_label = 0
    #     elif (s.side == self.winner):
    #         move_label = 1
    #     else:
    #         move_label = -1
    #     z[tuple(self.history[move_idx])] = move_label

    #     return z

    # Label the move 'move_idx' from the position before 'move_idx'.
    def label_pos(self, s):

        if self.winner == 2:
            move_label = 0
        elif (s.side == self.winner):
            move_label = 1
        else:
            move_label = -1

        return move_label
    
    # # Label the move 'move_idx' from the position before 'move_idx'.
    # def label_pos(self, s, move_idx):

    #     z = torch.zeros(3, 3) - 1
    #     for a in s.legal_moves:
    #         z[a] = 10

    #     if self.winner == 2:
    #         move_label = 0
    #     elif (s.side == self.winner):
    #         move_label = 1
    #     else:
    #         move_label = -1
    #     z[tuple(self.history[move_idx])] = move_label

    #     return z


class Buffer:
# A buffer containing games and their labels.
# It can sample batches.

    def __init__(self, c):
        self.c = c
        self.buffer = []
    
    # Save the game in the buffer without exceeding the window size.
    def save_game(self, game):
        self.buffer.append(game)
        if len(self.buffer) > self.c.window_size:
            self.buffer.pop(0)
    
    # Sample a mini-batch of positions from the games of the buffer.
    def sample_batch(self, P):
        total_nb_pos = sum(len(g.history) for g in self.buffer)

        games_sample = np.random.choice(
            self.buffer,
            size=self.c.batch_size,
            p=[len(g.history) / total_nb_pos for g in self.buffer]
        )

        pos_sample = [(g, np.random.randint(len(g.history))) for g in games_sample]
        
        return [
            g.get_labelled_pos(self.c, move_idx) \
            for (g, move_idx) in pos_sample
        ]


class GameGenerator:
# A generator of games. The generated games are saved in a buffer.
    

    def __init__(self, c, rm, nnet):
        self.c = c
        self.rm = rm
        self.ai = snnAI.SnnAI(c, nnet, add_noise=True)
        # The list of the GenGameState objets representing the games
        # played in parallel.
        self.states = []
    

    def generate_games(self, buffer):
        
        num_s = min(self.c.parallel_games, self.c.games_per_iter - self.rm.game_count)
        self.states = [egn.GameState() for _ in range(num_s)]

        self.rm.begin_game_tick()

        while self.rm.game_count < self.c.games_per_iter:
            moves = self.ai.best_moves(self.states, self.rm)
            # We iterate in reverse because of the pop on the states.
            i = len(self.states) - 1
            while i >= 0:
                self.make_one_move(buffer, moves, i)
                i -= 1
    

    # Make all the updates for one state after one move.
    def make_one_move(self, buffer, moves, i):

        s = self.states[i]
        s.update(moves[i])

        if s.finished:

            # Save the finished game.
            game = Game(s.history, s.winner)
            buffer.save_game(game)

            # Update runManager.
            self.rm.end_game(buffer, s.num_moves)
            self.rm.begin_game_tick()
            
            # Update states.
            if self.c.games_per_iter - self.rm.game_count < self.c.parallel_games:
                self.states.pop(i)
            else:
                self.states[i] = egn.GameState()