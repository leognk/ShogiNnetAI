# ShogiNnetAI

The report of the project is in the pdf file but unfortunately, it's written in French. I wrote the shogi engine part and the MCTS and neural networks part.

The project aimed at designing an AI playing shogi on the same model as AlphaZero by DeepMind. AlphaZero is an AI able to play go, chess and shogi and it reached superhuman performance. It uses Monte Carlo Tree Search combined with neural networks and it is trained in an unsupervised manner by playing with itself. It only knows the game's rules without any other prior knowledge. The AI learns the strategies by itself only through self-play.

The Shogi folder contains two AIs: A0Jr and SNN.

A0Jr is the AI on the model of AlphaZero. The objective was just to have an AI able to make coherent moves. But the computational power I had was too low to train the model so that it reaches even this modest objective (even with Google Colab's GPU).

This is why I then tried to design a simpler model using only neural networks without using Monte Carlo Tree Search. The model is in the folder SNN (Simple Neural Network). I used several tricks to accelerate the computation as much as possible and at the end, the training was indeed very fast. However, in any game, at some point the AI only makes repetitive moves. Despite many attempts, this bug was too hard to fix. To understand the issue, I tried to run the model on TicTacToe, which is a much simpler game than shogi. The model did converge but not perfectly, which is bad because TicTacToe is very simple and has a very low combinatorial complexity. Moreover, it did not explain the initial bug. So I concluded that the SNN model is just too inefficient.
