# ShogiNnetAI

The goal of this project is to develop an AI that can play shogi, also called Japanese chess, modeled after DeepMind's [AlphaZero](https://en.wikipedia.org/wiki/AlphaZero). AlphaZero is a superhuman AI that can play Go, chess and shogi. It predicts the next move by performing Monte Carlo Tree Search (MCTS) guided by a neural network. The neural network is trained through self-play, relying only on the game's rules, without any human data.

I developed the shogi engine, the MCTS algorithm guided by a neural network, and the neural network training script.

## Models

The Shogi folder contains two AI versions: A0Jr and SNN.

### AlphaZero Junior (A0Jr)

A0Jr is the AI modeled after AlphaZero. The goal was to create an AI capable of making coherent shogi moves. However, due to the limited computational resources I had at that time (Google Colab), I was unable to train the model to achieve this goal.

### Simple Neural Network (SNN)

After my first attempt, I tried a much simpler model that relies only on the neural network without MCTS to predict the next move. The training process became much faster, but at some point during training, the model was stuck making repetitive moves. Despite many attempts, I was unable to resolve this issue. To diagnose the problem, I tested the model on a toy game, tic-tac-toe. While the model did converge, it was not perfect, raising concerns about the model's potential given tic-tac-toe's simplicity. I concluded that the SNN model is just too inefficient for complex games like shogi. Despite being costly, search seems to be an essential component in this setting.