import game_engine as egn
import randomAI
import snnAI
from configuration import Configuration
import time



class Evaluator:


    def __init__(self, evaluator_ai, num_games):

        if evaluator_ai == 'random':
            self.evaluator_ai = randomAI.RandomAI()
        else:
            self.evaluator_ai = evaluator_ai
        self.num_games = num_games

        self.num_wins = 0
        self.num_draws = 0
        self.num_moves = 0
        self.duration = 0

        self.win_perc = -1
        self.draw_perc = -1
        self.win_no_draws_perc = -1
        self.avg_game_length = -1
        self.duration = -1


    def reset(self):
        self.num_wins = 0
        self.num_draws = 0
        self.num_moves = 0
        self.duration = 0


    # Evaluate the given AI with another AI by playing num_games games.
    def evaluate_ai(self, evaluated_ai):

        start_time = time.time()

        self.reset()

        # The games are separated in half.
        # The first part is the games for which the evaluated AI is black
        # and the second one is those for which the evaluator is black.
        states1 = [egn.GameState() for _ in range(self.num_games // 2)]
        states2 = [egn.GameState() for _ in range(self.num_games - len(states1))]
        
        # Whether it's the evaluator's turn in states1.
        evaluator_plays1 = False

        while states1 or states2:

            if evaluator_plays1:
                player1, player2 = self.evaluator_ai, evaluated_ai
            else:
                player1, player2 = evaluated_ai, self.evaluator_ai
            
            # if evaluator_plays1:
            #     player1, player2 = self.evaluator_ai, self.evaluator_ai
            # else:
            #     player1, player2 = evaluated_ai, evaluated_ai

            moves1 = player1.best_moves(states1)
            moves2 = player2.best_moves(states2)

            self.update_states(states1, moves1, evaluator_plays1)
            self.update_states(states2, moves2, not evaluator_plays1)
            # self.update_states(states2, moves2, evaluator_plays1)

            evaluator_plays1 = not evaluator_plays1
        
        # Compute results
        self.compute_results()
        self.duration = time.time() - start_time
    

    # Update states list according to the moves and return the results
    # of the updates.
    # evaluator_plays indicates whether the player playing the moves
    # is the evaluator AI.
    def update_states(self, states, moves, evaluator_plays):

        i = len(states) - 1
        while i >= 0:

            s = states[i]
            s.update(moves[i])

            if s.finished:
                states.pop(i)
                if s.winner != 2:
                    self.num_moves += s.num_moves
                if s.winner == 2:
                    self.num_draws += 1
                elif not evaluator_plays:
                    self.num_wins += 1

            i -= 1
    

    def compute_results(self):
        self.win_perc = 100 * self.num_wins / self.num_games
        self.draw_perc = 100 * self.num_draws / self.num_games
        self.win_no_draws_perc = -1
        self.avg_game_length = -1
        if self.num_games != self.num_draws:
            self.win_no_draws_perc = 100 * self.num_wins / (self.num_games - self.num_draws)
            self.avg_game_length = self.num_moves / (self.num_games - self.num_draws)



if __name__ == '__main__':

    c = Configuration()
    ###
    # import nnet
    # nnet = nnet.NNet(32, 2).cuda()
    # evaluated_ai = snnAI.SnnAI(c, nnet, add_noise=False)
    ###
    evaluated_ai = snnAI.SnnAI(c, add_noise=False)
    # evaluated_ai = randomAI.RandomAI()

    num_games = 100000
    
    ev = Evaluator('random', num_games)
    ev.evaluate_ai(evaluated_ai)

    # print(
    #     f"\n\nwins: {round(ev.win_perc)} % | "
    #     f"draws: {round(ev.draw_perc)} % | "
    #     f"wins no draws: {round(ev.win_no_draws_perc)} %"

    #     f"\naverage length: {round(ev.avg_game_length)} | "
    #     f"duration: {round(ev.duration, 2)}"
    # )

    print(
        f"\n\nwins: {ev.win_perc} % | "
        f"draws: {ev.draw_perc} % | "
        f"wins no draws: {ev.win_no_draws_perc} %"

        f"\naverage length: {round(ev.avg_game_length)} | "
        f"duration: {round(ev.duration, 2)}"
    )