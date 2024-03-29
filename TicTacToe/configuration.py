class Configuration:
# Contains all the values of the parameters of the program.
# The values indicated in commentary are those used in Alpha(Go) Zero.
    
    def __init__(self):

        self.load = False

        # Files
        self.folder = "checkpoints/session1/"
        self.run_manager_file_name = self.folder + "runManager.json"
        self.nnet_file_name = self.folder + "nnet.pt"
        self.buffer_file_name = self.folder + "buffer.json"

        # Hyperparameters
        self.num_kernels = 64 # 64 # 256
        self.num_res_blocks = 14 # 14 # 19
        self.lr = 0.001 # 0.01 # 0.2 -> 0.02 -> 0.002 -> 0.0002
        self.weight_decay = 1e-4 # 1e-4
        self.alpha_dir = 1.3 # 0.15
        self.eps_dir = 0.75 # 0.25
        self.eval_move = 100

        # Number iterations
        self.num_iter = 1000 # 700 (= 700,000 / 1,000 ; 700,000 training steps / gradient descent steps)
        self.games_per_iter = 1000 # 25,000
        self.epochs_per_iter = 100 # 1e3
        self.games_save_interval = 10**6
        self.epochs_save_interval = 10**6
        self.num_eval_games = 1000

        # Data sizes
        self.window_size = int(1e4) # 1e6
        self.batch_size = 64 # 64 # 700 # 4096
        self.parallel_games = 10**6



if __name__ == "__main__":

    import trainNNet

    c = Configuration()
    nnet_trainer = trainNNet.NNetTrainer(c)
    nnet_trainer.train_nnet()
