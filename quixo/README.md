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

Other ideas: DEEP PRUNING (order moves based on how likely they are going to be good, it's better to explore it at the beginning (sorting of possible moves)). The sort is poerformed directly in the `get_possible_moves()` method where the moves are sorted according to the number of player's symbols aligned.

Another possible solution can be the use of a different depth value, thanks to the `is_losing` function. If the MinMaxPlayer is losing, it is necessary to explore more moves, so the depth can be increased. In the other case, if the MinMaxPlayer is winning, it is not necessary to predict so many steps, so the depth can be decreased. At the beginning it's not necessary to go more in the deep because the board is empty and each move can give the same results. This approach can be implemented by using a variable depth, that changes according to the situation of the game.

Another possible solution can be the use of a different `evaluation` function, in order to evaluate the board in a different way, so that the algorithm can find the best move in a different way.
* Protect your winning moves
* Block the opponent's winning moves
* Choose the moves that can give you more possibilities to win
* Border moves can be used to block adversary's moves or to protect your winning moves


Note: At the beginning it's better to fill change the neutral cells with the player's symbol, because it's better to have more possible moves to perform. More choices means more possibilities to win.

### Problem encountered
If MinMaxPlayer plays againist itself, with this first implementation can loop forever or lose. Tjis problem is due to the fact that when the board is in a symmetric state, when the `get_possible_moves()` method is called, it returns the same moves sorted in the same way and the alpha beta minmax implemented selected the first optimal move, which is the same for both players.

### Possible solution
A possible solution can be the introduction of some randomness in the sorted list shuffling in the `get_possible_moves()` method the elements with the same piece symbol (neutral and not neutral) and same number of elements in line, in order to avoid the selection of the same moves first in the alpha beta pruning minmax. 

### Other improvements
The depth can changed in different ways. At the beginning the choice is irrelevant, a trick can be begin from angles or borders, because they can be used to block adversary's moves or to protect your winning moves so the minmax can be avoided for the first move and the depth is put to 1 for the next moves. Many attempts have been done in order to provide the best solution in the next turns, trying to increase the depth to 3 if the player is winning or losing (if it's winning it can win in 3 turns or avoid to lose in 3 turns). But the fixed choice of depth=3 is not sufficient. The optimal variation of the depth, but also the slowest one (reaching a maximum depth of 4, more takes too time) is to choose the depth to be proportional to the `max_inline_pieces()` method when one of the two players is winning or losing. When the agent is winning or losing (evaluayed using the `is_losing()` method) the depth can be increased or decreased for the following reasons:
* if the opponent is tricking the MinMaxPlayer making it gain more scores (so faking to lose), it will be able to find recognize the trick finding the moves that can make the opponent to win
* if the opponent is winning, more depth is needed to find the best move to defeat and than to win
Than, if there is a move which makes the player win, it can be performed without goigh through the decision tree.

<!-- 
Potrei anche provare a salvare da qualche parte dei pezzi di albero se possono essere riciclati => Non utile perche se vado piu in profondita non posso riutilizzare i pezzi di albero gia esplorati.
 -->

## Results

The last version of the algorithm takes about 25 minutes to perform 100 games with a random player (about 15 seconds per game) and it takes much more time to play againist himself. This time is variabe according to the depth of the tree, that the minmax algorithm has to explore.

The implemented player is capable to win always againist a random player, but is not able to always win againist itself. This is due to the fact that the algorithm is not able to find the best move in a reasonable time if the depth is increased so much and if the depth is decreased, the algorithm is not always able to find the best move to defeat the opponent.