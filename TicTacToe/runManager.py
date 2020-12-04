import time
import datetime
import torch
import os

import jsonManager


class RunManager:
# Print informations on the progress of the training and manage
# the savings of the variables.

    def __init__(self, c):

        self.c = c

        self.iter_count = 0
        self.total_duration = 0

        self.eval_win_perc = -1
        self.eval_win_no_draws_perc = -1
        self.eval_draw_perc = -1
        self.eval_avg_game_length = -1
        self.eval_duration = 0

        self.game_total_count = 0
        self.game_count = 0
        self.game_tick_start_time = 0
        self.game_tick_duration = 0
        self.games_duration = 0

        self.total_proba_max = 0
        self.total_noise_max = 0
        self.total_proba_dictate = 0
        self.move_count = 0

        self.epoch_total_count = 0
        self.epoch_count = 0
        self.epoch_start_time = 0
        self.epoch_duration = 0
        self.epochs_duration = 0

        self.first_loss = 0


    def end_iter(self, nnet):
        
        # Reset
        self.game_count = 0
        self.games_duration = 0
        self.total_proba_max = 0
        self.total_noise_max = 0
        self.total_proba_dictate = 0
        self.move_count = 0
        self.epoch_count = 0
        self.epochs_duration = 0

        self.iter_count += 1

        # Save of the run_manager and the nnet.
        jsonManager.save(self, self.c.run_manager_file_name)
        torch.save(nnet.state_dict(), self.number_file_name(self.c.nnet_file_name))

        print(
            "_" * 100 + "\n\n" +
            self.str_general_progression()
        )
    

    def eval_ai(self, evaluator):
        self.eval_win_perc = evaluator.win_perc
        self.eval_win_no_draws_perc = evaluator.win_no_draws_perc
        self.eval_draw_perc = evaluator.draw_perc
        self.eval_avg_game_length = evaluator.avg_game_length
        self.eval_duration = evaluator.duration
    

    def begin_game_tick(self):
        self.game_tick_start_time = time.time()
    

    def proba(self, proba_max, noise_max, proba_dictate):
        self.total_proba_max += proba_max
        self.total_noise_max += noise_max
        self.total_proba_dictate += proba_dictate
        self.move_count += 1


    def end_game(self, buffer, num_moves):
        self.game_tick_duration = time.time() - self.game_tick_start_time
        self.game_total_count += 1
        self.game_count += 1

        self.games_duration += self.game_tick_duration
        self.total_duration += self.game_tick_duration

        # Save of the run_manager and the buffer.
        if self.game_count % self.c.games_save_interval == 0 and self.game_count > 0:
            jsonManager.save(self, self.c.run_manager_file_name)
            jsonManager.save(buffer, self.c.buffer_file_name)

        str_games_duration = str(datetime.timedelta(seconds=round(self.games_duration)))
        str_tick_duration = str(datetime.timedelta(seconds=round(self.game_tick_duration)))

        proba_max_mean = round(self.total_proba_max / self.move_count, 2)
        noise_max_mean = round(self.total_noise_max / self.move_count, 2)
        P_max_mean2 = round(
            (self.total_proba_max - self.total_noise_max) / self.move_count, 2
        )

        proba_dictate_perc = round(100 * self.total_proba_dictate / self.move_count)

        if self.game_count % self.c.games_per_iter == 0:
            print(
                "_" * 100 + "\n\n" +
                self.str_general_progression() +

                f"\n\ngame: {self.game_count} / {self.c.games_per_iter} | "
                f"moves: {num_moves} | "
                f"duration: {str_games_duration} | "
                f"tick duration: {str_tick_duration}"

                f"\n\nproba dictates: {proba_dictate_perc} % | "
                f"proba max mean: {proba_max_mean} = {P_max_mean2} + {noise_max_mean}"
            )

    
    # Called at the end of the generation of all the games in one iteration.
    def end_games(self, buffer):
        # Save of the run_manager and the buffer.
        jsonManager.save(self, self.c.run_manager_file_name)
        jsonManager.save(buffer, self.c.buffer_file_name)
    

    def begin_epoch(self):
        self.epoch_start_time = time.time()
    

    def end_epoch(self, nnet, loss):

        self.epoch_duration = time.time() - self.epoch_start_time
        self.epoch_total_count += 1
        self.epoch_count += 1

        self.epochs_duration += self.epoch_duration
        self.total_duration += self.epoch_duration

        if self.epoch_count == 1:
            self.first_loss = loss

        # Save of the run_manager and the nnet.
        if self.epoch_count % self.c.epochs_save_interval == 0 and self.epoch_count > 0:
            jsonManager.save(self, self.c.run_manager_file_name)
            torch.save(nnet.state_dict(), self.number_file_name(self.c.nnet_file_name))

        str_epochs_duration = str(datetime.timedelta(seconds=round(self.epochs_duration)))
        str_epoch_duration = str(datetime.timedelta(seconds=round(self.epoch_duration)))
        
        if self.epoch_count % self.c.epochs_per_iter == 0:
            print(
                "_" * 100 + "\n\n" +
                self.str_general_progression() +

                f"\n\nepoch: {self.epoch_count} / {self.c.epochs_per_iter} | "
                f"duration: {str_epochs_duration} | "
                f"last epoch duration: {str_epoch_duration}"

                f"\n\nfirst loss: {round(self.first_loss, 3)} | "
                f"loss: {round(loss, 3)}"
            )
    

    def str_general_progression(self):

        str_total_duration = str(datetime.timedelta(seconds=round(self.total_duration)))
        str_eval_duration = str(datetime.timedelta(seconds=round(self.eval_duration)))

        return (
            f"iter: {self.iter_count} / {self.c.num_iter} | "
            f"total games: {self.game_total_count} | "
            f"total epochs: {self.epoch_total_count} | "
            f"total duration: {str_total_duration}"

            f"\n\nwins: {round(self.eval_win_perc)} % | "
            f"draws: {round(self.eval_draw_perc)} % | "
            f"wins no draws: {round(self.eval_win_no_draws_perc)} % | "
            f"average length: {round(self.eval_avg_game_length)} | "
            f"eval duration: {str_eval_duration}"
        )
    

    # Add a number to the file name of the nnet according to the number of training steps done.
    def number_file_name(self, file_name):
        name, extension = file_name.split('.')
        return name + str(self.epoch_total_count) + '.' + extension
    

    # Extract the number from a file name.
    def get_number_file_name(self, file_name):
        names = file_name.split('/')
        name = names[-1].split('.')[0]
        i= 0
        while not ord('0') <= ord(name[i]) <= ord('9'):
            i += 1
        return int(name[i:])




# Return the file name with the highest number.
def get_last_file_name(c, file_name):
    name, extension = file_name.split('.')
    max_num = -1
    max_file_name = ''
    for f_name in os.listdir(os.getcwd() + '/' + c.folder):
        f_name = c.folder + f_name
        if name in f_name:
            part1, part2 = f_name.split('.')[:2]
            num = int(part1[-1])
            if part2 == '5': num += 0.5
            if num > max_num:
                max_num = num
                max_file_name = f_name
    return max_file_name