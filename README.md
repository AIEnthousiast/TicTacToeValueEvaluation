# TicTacToeValueEvaluation

Inspired by the study case of chapter 01 of "Reinforcement Learning: An introduction" by Sutton and Barto.

Let's say we want to train an agent to play Tic-Tac-Toe. This agent should be able to learn about the mistakes of an imperfect player to improve. Using the classical MiniMax algorithm is not suitable for this task, as this algorithm assume that the oppponent is perfect , i.e always selected the best possible move for his current position. 

In this project, we will use the concept of value functions to help us training such an agent. Each state will therefore be valued by a probability of winning which will be updated after each step. Self-play will be used in order to let the agent familiarize himself with playing on both sides. 
