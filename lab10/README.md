## Algorithm Implementation README

# LAB10

Use reinforcement learning to devise a tic-tac-toe player.

## Overview

In this laboratory there is the implementation of a tic-tac-toe player using reinforcement learning. In particular the player is trained using the Q-Learning algorithm. But let's start from the beginning.

## Implementation

### Structure
For the implementation of a reinforcement learning algorithm, it is necessary to define the following elements:
* **Environment**: the environment in this case is the tic-tac-toe game, represented by a board, filled with Xs and Os. The board can be easily printed with the provided method `print_board()`, which takes as input the actual state of the board and prints it putting dots for white spaces.
* **States**: the states are the possible configurations of the environment. In this case the states are the possible configurations of the tic-tac-toe game, represented by the provided code `State = namedtuple('State', ['x', 'o'])` where x and o are lists of the actions chosen by the two players.
* **Actions**: the possible actions that a player can perform on the environment are represented by `MAGIC = [2, 7, 6, 9, 5, 1, 4, 3, 8]`. Each number corresponds to a position on the board. This list is used to evaluate the winner of the game by using the sum method. The player that has a sum of 3 elements equal to 15 wins.
  
  | 2 | 7 | 6 |
  |---|---|---|
  | 9 | 5 | 1 |
  | 4 | 3 | 8 |


* **Reward**: the reward is the value that the agent receives for each action. The reward is implemented in the `get_reward()` method. Different versions of this method have been implemented, in order to evaluate the performances of the agent learning.
  - The first version was the simplest one, in which the agent receives a reward of 1 if it wins, -1 if it loses and 0 if it draws.
  - The second version was adding +1 to the reward for each action blocking the opponent from winning.
  - The third version was adding a penalty of -3 for each action taken from x that did not block the opponent from winning, because the opponent won in the next move.
  . . .
  - !!!if no action is blocking the winning of o => reward = -10 NOT IMPLEMENTED YET

### Deadlines:

* Submission: [Dies Natalis Solis Invicti](https://en.wikipedia.org/wiki/Sol_Invictus)
* Reviews: [Befana](https://en.wikipedia.org/wiki/Befana)

Notes:

* Reviews will be assigned  on Monday, December 4
* You need to commit in order to be selected as a reviewer (ie. better to commit an empty work than not to commit)