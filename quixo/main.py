import random
import numpy as np
from game import Game, Move, Player, colors
from copy import deepcopy
from tqdm.auto import tqdm

class RandomPlayer(Player):
    def __init__(self) -> None:
        super().__init__()

    def make_move(self, game: 'Game') -> tuple[tuple[int, int], Move]:
        from_pos = (random.randint(0, 4), random.randint(0, 4))
        move = random.choice([Move.TOP, Move.BOTTOM, Move.LEFT, Move.RIGHT])
        return from_pos, move

def is_losing(player_id, game: 'Game') -> bool:
        len = 2
        # if the adversary has a line of len+1 pieces, I am losing
        for i in range(game._board.shape[0]):
            if sum(game._board[i, :] == (player_id+1)%2) > len:
                return True
            if sum(game._board[:, i] == (player_id+1)%2) > len:
                return True
        if sum(game._board.diagonal() == (player_id+1)%2) > len:
            return True
        if sum(game._board[::-1].diagonal() == (player_id+1)%2) > len:
            return True

def is_terminal(node) -> bool:
        if len(node) == 0:
            return True
        return False

class MyPlayer(Player):
    def __init__(self) -> None:
        super().__init__()

    def make_move(self, game: 'Game') -> tuple[tuple[int, int], Move]:
        from_pos = (random.randint(0, 4), random.randint(0, 4))
        move = random.choice([Move.TOP, Move.BOTTOM, Move.LEFT, Move.RIGHT])
        return from_pos, move

class MinMaxPlayer(Player):
    def __init__(self, player_id) -> None:
        super().__init__()
        self.player_id = player_id
        self.counter = 0
        self.total = 0

    # evaluate the board
    def evaluate(self, game: 'Game') -> float:
        if game.check_winner() == self.player_id:
            return 1
        elif game.check_winner() == (self.player_id+1)%2:
            return float('-inf')
        else:
            return 0
        
    def get_possible_moves(self, game: 'Game', maximizing_player) -> list[tuple[tuple[int, int], Move]]:
        possible_moves = []
        # three possible moves for the cornice without the corners
        for i in range(1, 4, 1):
            # if I select a piece from the top row, I can slide it in any other direction, but not in the same
            if game._board[0][i] == -1 or game._board[0][i] == maximizing_player:
                possible_moves.append(((i, 0), Move.BOTTOM))
                possible_moves.append(((i, 0), Move.LEFT))
                possible_moves.append(((i, 0), Move.RIGHT))
            if game._board[4][i] == -1 or game._board[4][i] == maximizing_player:
                possible_moves.append(((i, 4), Move.TOP))
                possible_moves.append(((i, 4), Move.LEFT))
                possible_moves.append(((i, 4), Move.RIGHT))
            if game._board[i][0] == -1 or game._board[i][0] == maximizing_player:
                possible_moves.append(((0, i), Move.TOP))
                possible_moves.append(((0, i), Move.BOTTOM))
                possible_moves.append(((0, i), Move.RIGHT))
            if game._board[i][4] == -1 or game._board[i][4] == maximizing_player:
                possible_moves.append(((4, i), Move.TOP))
                possible_moves.append(((4, i), Move.BOTTOM))
                possible_moves.append(((4, i), Move.LEFT))
        # two possible moves for the corners
        if game._board[0][0] == -1 or game._board[0][0] == maximizing_player:
            possible_moves.append(((0, 0), Move.RIGHT))
            possible_moves.append(((0, 0), Move.BOTTOM))
        if game._board[0][4] == -1 or game._board[0][4] == maximizing_player:
            possible_moves.append(((4, 0), Move.BOTTOM))
            possible_moves.append(((4, 0), Move.LEFT)) 
        if game._board[4][0] == -1 or game._board[4][0] == maximizing_player:
            possible_moves.append(((0, 4), Move.RIGHT))
            possible_moves.append(((0, 4), Move.TOP))
        if game._board[4][4] == -1 or game._board[4][4] == maximizing_player:
            possible_moves.append(((4, 4), Move.LEFT))
            possible_moves.append(((4, 4), Move.TOP))       
        
        return possible_moves

    def minmax(self, node, depth, game: 'Game', alpha, beta, maximizing_player = 0):
        # a node is terminal if there are no more moves to make
        if depth == 0 or is_terminal(node):
            if is_terminal(node):
                print(f"{colors['yellow']} last moves {colors['reset']}")
            value = self.evaluate(game)
            '''if value!=0:
                print(f"{colors['yellow']} Found! {value} {colors['reset']}")
                game.print()'''
            return value, node
        if maximizing_player == 0:   # True, player 1 (0) to maximize
            ch = random.choice(node)
            self.total+=1
            for child in node:
                next_game = deepcopy(game)
                next_game._Game__move(child[0], child[1], self.player_id%2)
                #next_game.print()
                p_moves = self.get_possible_moves(next_game, (maximizing_player+1)%2)
                val, n = self.minmax(p_moves, depth - 1, next_game, alpha, beta, (maximizing_player+1)%2)
                if alpha < val:
                    self.counter+=1
                    alpha = val
                    if val != 0:
                        ch = child
                if beta <= alpha:
                    break
            return alpha, ch
        else:
            ch = random.choice(node)
            self.total+=1
            for child in node:
                next_game = deepcopy(game)
                next_game._Game__move(child[0], child[1], (self.player_id+1)%2)
                #next_game.print()
                p_moves = self.get_possible_moves(next_game, (maximizing_player+1)%2)
                val, n = self.minmax(p_moves, depth - 1, next_game, alpha, beta, (maximizing_player+1)%2)
                if beta > val:
                    self.counter+=1
                    beta = val
                    if val != 0:
                        ch = child
                if beta <= alpha:
                    break
            return beta, ch
    # choose the best position from the possible ones and the best move
    def make_move(self, game: 'Game') -> tuple[tuple[int, int], Move]:
        possible_moves = self.get_possible_moves(game, self.player_id%2)
        
        # if I am losing, I will search deeper
        if is_losing(self.player_id, game):
            depth = 6
        # if I am winning, I will search less
        elif is_losing((self.player_id+1)%2, game):
            depth = 3
        else:
            depth = 2
        
        '''if len(possible_moves) > 20:
            depth = 3
        else:
            depth = 8'''
        
        alpha = float('-inf')
        beta = float('inf')
        from_pos, move = self.minmax(possible_moves, depth, game, alpha, beta, self.player_id%2)[1]
        return from_pos, move


def test(test_episodes):
    win = 0
    rand = 0
    for _ in tqdm(range(test_episodes)):
        g = Game(verbose=True)
        #player1 = MyPlayer()
        player1 = MinMaxPlayer(0)
        player2 = RandomPlayer()
        winner = g.play(player1, player2)
        print()
        g.print()
        print(f"Winner: Player {winner+1}")
        rand += (1- player1.counter/player1.total)
        if winner==0:
            win+=1
    print(f"Win percentage: {win/test_episodes}")
    print(f"Rand percentage: {rand/test_episodes}")

if __name__ == '__main__':
    '''g = Game()
    g.print()
    #player1 = MyPlayer()
    player1 = MinMaxPlayer(0)
    player2 = RandomPlayer()
    winner = g.play(player1, player2)
    print()
    g.print()
    print(f"Winner: Player {winner+1}")'''
    print(f"Player 1: {colors['green']} 0 {colors['reset']}")
    print(f"Player 2: {colors['red']} 1 {colors['reset']}")
    test(1)
