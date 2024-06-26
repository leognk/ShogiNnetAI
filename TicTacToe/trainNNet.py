import torch
import torch.optim as optim

import runManager
from gameGenerator import *
import nnet
import jsonManager
import snnAI
import evaluateAI


torch.set_printoptions(profile="full")


class NNetTrainer:
# Train a neural net by generating games.

    def __init__(self, c):

        self.c = c
        self.evaluator = evaluateAI.Evaluator('random', c.num_eval_games)
        self.nnet = nnet.NNet(c.num_kernels, c.num_res_blocks)
        self.nnet.cuda()
        
        if c.load:
            self.rm = jsonManager.load(c.run_manager_file_name)
            self.rm.c = c
            nnet_file_name = self.rm.number_file_name(c.nnet_file_name)
            # We load a nnet only if there exists one (ie. with a non zero number).
            if self.rm.get_number_file_name(nnet_file_name) > 0:
                self.nnet.load_state_dict(torch.load(nnet_file_name))
            self.buffer = jsonManager.load(c.buffer_file_name)
            self.buffer.c = c
        
        else:
            self.rm = runManager.RunManager(c)
            self.buffer = Buffer(c)
        
        # Evaluation of the initial AI.
        if self.rm.iter_count == 0:
            self.evaluation()

    # Train the neural network using the given buffer with 'epochs_per_iter' training steps.
    def mini_train(self):

        optimizer = optim.Adam(
            self.nnet.parameters(),
            lr=self.c.lr,
            weight_decay=self.c.weight_decay
        )
        
        while self.rm.epoch_count < self.c.epochs_per_iter:

            self.rm.begin_epoch()

            batch = self.buffer.sample_batch(self.nnet)
            batch = torch.utils.data.DataLoader(batch, batch_size=len(batch))
            batch = next(iter(batch))

            s, ids, z_1d = batch
            s, ids, z_1d = s.cuda(), ids.cuda(), z_1d.cuda()
            
            v = self.nnet(s)
            z = self.get_z(v, ids, z_1d)

            loss = ((v - z) ** 2).sum() / self.c.batch_size
            
            optimizer.zero_grad()
            loss.backward()
            optimizer.step()

            self.rm.end_epoch(self.nnet, loss.item())
    
    # def correct_labels(self, z, v):
    #     ids = (z == 10)
    #     z[ids] = v[ids]

    def get_z(self, v, ids, z_1d):
        # z = v.clone().detach().flatten(start_dim=1)
        z = torch.zeros(v.shape).cuda().flatten(start_dim=1)
        rge = torch.arange(len(z))
        z[rge, ids.long()] = z_1d.float()
        z = z.reshape(v.shape).requires_grad_(True)
        return z

    # Main function for the training phase of the AI.
    def train_nnet(self):

        while self.rm.iter_count < self.c.num_iter:
            
            self.generate_games()
            self.mini_train()
            self.evaluation()

            self.rm.end_iter(self.nnet)
    
    # The self-play phase.
    def generate_games(self):
        gen = GameGenerator(self.c, self.rm, self.nnet)
        gen.generate_games(self.buffer)
        self.rm.end_games(self.buffer)
    
    # Evaluate the AI.
    def evaluation(self):
        ai = snnAI.SnnAI(self.c, self.nnet)
        self.evaluator.evaluate_ai(ai)
        self.rm.eval_ai(self.evaluator)