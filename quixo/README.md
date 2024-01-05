## Algorithm Implementation README

# Quixo Project

## Overview

In this project there is the implementation of the Quixo game and possible player algorithms used to achieve the best performances during the game. The game is played on a 5x5 board, where the two players fight for the victory. The game is played by two players, one with Xs and the other with Os, respectively represented on the board as 0s and 1s and neutral cells are represented with -1s. The players take turns to move, and the winner is the first player that has 5 elements in a row, either horizontally, vertically or diagonally. The game ends when one of the players wins or when the board is full and there is no winner.

## Implementation
For the implementation of the optimal player, the method used is the Adversarial Search, where the player focuses on finding the optimal moves, so that the current player can minimize the opponent's score. In particular, the algorithm used is the MinMax algorithm, where the player tries to maximize its score and minimize the opponent's score. The algorithm is implemented in the `MinMaxPlayer` class, which makes a move using the `make_move()` method, which uses the `minimax()` method to find the best move. The `minimax()` method is a recursive method that evaluates the best move for the current player, by evaluating the best move for the opponent. This evaluation is performed using the `evaluate()` method that simply attributes 1 in case of `MinMaxPlayer` victory, -inf in case of lost, and 0 in all the other cases.

### Problems
At the beginning a basic minmax version was implemented, in order to try the algorithm and to evaluate the performances. Unfortunately, the basic version was not able to find the best move in a reasonable time, due to several reasons:

* The decisional tree to explore is too big, considering that each move takes the board in a different configuration with a variable (often large) number of different possible moves to perform, so the tree grows almost exponentially in terms of depth and breadth.

* The algorithm is not able to prune the tree, so it explores all the possible moves, even if they are not useful to find the best move.

* At the beginning of the game, the choice of a big fixed depth can be costly, because the action space is still very big to be explored. It is not necessary to explore all the possible moves when the board is almost empty. In the other case, instead, when the player is losing, it is necessary to explore more possible moves in order to find the best move to defeat from the opponent and than to win.

So, the problems are found in the following points:

* Depth of the tree too large
* Breadth of the tree too large


### Possible solutions
Some possible approaches to mitigate this problems can be adopted.

The first one is to use the so called `alpha beta pruning`, a method to discard some paths of the tree that are not useful to find the best move, in order to decrease the number of nodes to evaluate. It works as follows: two values, `alpha` and `beta` respectively represents the minimum score that the maximizing player is assured of and the maximum score that the minimizing player is assured of. Whenever the maximum score that the minimizing player (beta) is assured of becomes less than the minimum score that the maximizing player (alpha) is assured of, the maximizing player need not consider further descendants of this node, as they will never be reached in the actual play.

Other ideas: DEEP PRUNING (order moves based on how likely they are going to be good, it's better to explore it at the beginning)