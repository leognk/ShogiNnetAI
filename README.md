# ShogiNnetAI

The project aimed at designing an AI playing shogi on the same model as AlphaZero by DeepMind. AlphaZero is an AI able to play go, chess and shogi and it reached superhuman performance. It uses Monte Carlo Tree Search combined with neural networks and it is trained in an unsupervised manner by playing with itself. It only knows the game's rules without any other prior knowledge. The AI learns the strategies by itself only through self-play.

The Shogi folder contains two AI: A0Jr and SNN.
A0Jr is the AI on the model of AlphaZero. The objective was only to have an AI able to make coherent moves. But the low computational power I had made the training too slow to reach even this modest objective (even with Google Colab's GPU). This is why I tried to design a simpler model using only neural networks without using Monte Carlo Tree Search. The model is in the folder SNN (Simple Neural Network). However, at some point in any game, the AI only makes repetitive moves. Despite many attempts, this bug was too hard to fix. To understand the issue, I tried to run the model on TicTacToe, a much simpler game than shogi. The model did converge but not perfectly even though TicTacToe is very simple with a very low combinatorial complexity, and it did not explain the initial bug.
