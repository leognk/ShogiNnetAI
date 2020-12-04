import torch
from torch.distributions.dirichlet import Dirichlet
import torch.nn.functional as F
import numpy as np

import encoding
import nnet


class SnnAI:
# Simple Neural Net AI.
# Track a game state and generate a move based on the game state
# and the evaluation of its neural net.

    def __init__(self, c, nnet=None, add_noise=False):
        self.c = c
        # The neural network used to evaluate positions.
        self.nnet = nnet
        if not nnet: self.load_nnet()
        # Whether some noise must be added to the evaluations.
        self.add_noise = add_noise
    

    # Load a nnet from a file.
    def load_nnet(self):
        self.nnet = nnet.NNet(self.c.num_kernels, self.c.num_res_blocks)
        self.nnet.cuda()
        self.nnet.load_state_dict(torch.load(self.c.nnet_file_name))
    

    # Return the best move from the state s.
    def best_move(self, s):
        if s.finished: return "resign"
        return self.best_moves([s])[0]
    

    # Return the list of the best moves from each of the given states.
    def best_moves(self, states, rm=None):

        v = self.get_v(states)

        best_moves = []
        for i, s in enumerate(states):
            best_move = self.get_best_move(s, v[i], rm)
            best_moves.append(best_move)
        
        return best_moves
    

    # Return the tensor P (with a batch axis) computed from the ouput of the nnet
    # with a batch of all of the states as the input.
    def get_v(self, states):
        with torch.no_grad():
            batch = torch.stack([encoding.encode_game_state(s) for s in states])
            v = self.nnet(batch.cuda())
        return v.cpu().numpy()
    

    # Return the best move according to the proba list of the p values of
    # each legal moves of the state s according to the tensor P (no batch axis)
    # returned by the nnet.
    def get_best_move(self, s, v, rm=None):

        proba = torch.tensor([v[a] for a in s.legal_moves]) # pylint: disable=E
        proba = F.softmax(self.c.eval_move * proba, dim=0).numpy()
        i_max_no_noise = proba.argmax()

        if self.add_noise:
            dir_dist = Dirichlet(torch.zeros(len(s.legal_moves)) + self.c.alpha_dir)
            noise = dir_dist.sample().numpy()
            proba = (1 - self.c.eps_dir) * proba + self.c.eps_dir * noise
        
        # Best move
        i_max = proba.argmax()
        best_move = s.legal_moves[i_max]
        
        # For RunManager
        if rm:
            proba_dictate = int(i_max_no_noise == i_max)
            rm.proba(
                proba[i_max],
                self.c.eps_dir * noise[i_max],
                proba_dictate
            )
        
        return best_move