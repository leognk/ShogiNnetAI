# ShogiNnetAI

The report of the project is available in the PDF file (written in French). In this project, I developed the shogi engine and the neural network training script. The neural network is trained through self-play using Monte Carlo Tree Search (MCTS).

This project aimed to design an AI capable of playing shogi, modeled after DeepMind's AlphaZero. AlphaZero is an AI that can play Go, chess and shogi, achieving superhuman performance. It combines Monte Carlo Tree Search with neural networks and is trained through unsupervised self-play, only relying on the game's rules. The AI independently learns strategies solely through self-play.

The Shogi folder contains two AI versions: A0Jr and SNN.

A0Jr is the AI modeled on AlphaZero. The goal was to create an AI capable of making coherent shogi moves. However, due to limited computational resources, even with the use of Google Colab's GPU, I was unable to train the model to achieve even this modest goal.

Consequently, I explored a simpler model that relies solely on neural networks, omitting Monte Carlo Tree Search. This model, located in the SNN (Simple Neural Network) folder, incorporates several techniques to maximize computational efficiency. The training process became significantly faster. However, at some point during training, the model was stuck into making repetitive moves. Despite numerous attempts, I was unable to resolve this issue. In an effort to diagnose the problem, I tested the model with tic-tac-toe, a much simpler game than shogi. While the model did converge, it was not flawless, which is concerning given tic-tac-toe's simplicity and low combinatorial complexity. Furthermore, this test did not clarify the original issue. Therefore, I concluded that the SNN model, as it stands, is too inefficient for complex games like shogi. Search is very costly, but seems to be essential.