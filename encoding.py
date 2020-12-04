import torch
import game_engine as egn


# def encode_game_state(s):
#     t = torch.zeros(4, 3, 3)
#     t[0] = torch.tensor(s.board[s.side]) # pylint: disable=E
#     t[1] = torch.tensor(s.board[1-s.side]) # pylint: disable=E
#     t[2] = s.side
#     t[3] = s.num_moves
#     return t

def encode_game_state(s):
    t = torch.zeros(3, 3, 3)
    t[0] = torch.tensor(s.board[s.side]) # pylint: disable=E
    t[1] = torch.tensor(s.board[1-s.side]) # pylint: disable=E
    t[2] = s.side
    return t

# def encode_game_state(s):
#     t = torch.zeros(6, 3, 3)
#     s0 = egn.GameState()
#     for i in range(len(s.history)-1):
#         s0.update(s.history[i])
#     t[0] = torch.tensor(s0.board[s.side]) # pylint: disable=E
#     t[2] = torch.tensor(s0.board[1-s.side]) # pylint: disable=E
#     t[1] = torch.tensor(s.board[s.side]) # pylint: disable=E
#     t[3] = torch.tensor(s.board[1-s.side]) # pylint: disable=E
#     t[4] = s.side
#     t[5] = s.num_moves
#     return t