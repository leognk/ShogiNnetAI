import random


class RandomAI:
    
    # Generate a random move from the state s.
    def best_move(self, s):
        if s.finished:
            return "resign"
        best_move = random.choice(s.legal_moves)
        return best_move
    
    def best_moves(self, states):
        return [self.best_move(s) for s in states]