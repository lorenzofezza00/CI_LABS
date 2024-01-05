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
        
def count_pieces(maximizing_player, new_game: 'Game') -> int:
    cnt = 0
    for i in range(new_game._board.shape[0]):
        cnt = max(cnt, sum(new_game._board[i, :] == maximizing_player))
        cnt = max(cnt, sum(new_game._board[:, i] == maximizing_player))
    cnt = max(cnt, sum(new_game._board.diagonal() == maximizing_player))
    cnt = max(cnt, sum(new_game._board[::-1].diagonal() == maximizing_player))
    return cnt

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
    '''def evaluate(self, game: 'Game') -> float:
        if game.check_winner() == self.player_id:
            return 1
        elif game.check_winner() == (self.player_id+1)%2:
            return float('-inf')
        else:
            return 0'''
    def evaluate(self, game: 'Game') -> float:
        if game.check_winner() == self.player_id:
            return float('inf')
        elif game.check_winner() == (self.player_id+1)%2:
            return float('-inf')
        else:
            max_p1 = count_pieces(self.player_id, game)
            max_p2 = count_pieces((self.player_id+1)%2, game)
            return max_p1 - max_p2
            '''if is_losing(self.player_id%2, game):
                return -1
            if is_losing((self.player_id+1)%2, game):
                return 1
            return 0'''
        
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

        sorted_pm = []
        for pm in possible_moves:
            new_game = deepcopy(game)
            new_game._Game__move(pm[0], pm[1], maximizing_player)
            sorted_pm.append((pm, count_pieces(maximizing_player, new_game)))

        return sorted(sorted_pm, key=lambda x: x[1], reverse=True)

    def minmax(self, node, depth, game: 'Game', alpha, beta, maximizing_player = 0):
        # a node is terminal if there are no more moves to make
        if depth == 0 or is_terminal(node):
            value = self.evaluate(game)
            '''if value!=0:
                print(f"{colors['yellow']} Found! {value} {colors['reset']}")
                game.print()'''
            return value
        if maximizing_player == 0:
            b_val = float('-inf')
            for child in node:
                next_game = deepcopy(game)
                next_game._Game__move(child[0][0], child[0][1], self.player_id%2)
                #next_game.print()
                p_moves = self.get_possible_moves(next_game, (maximizing_player+1)%2)
                # qui posso sortare le p_moves in base a una euristica
                val = self.minmax(p_moves, depth - 1, next_game, alpha, beta, (maximizing_player+1)%2)
                b_val = max(b_val, val)
                alpha = max(alpha, b_val)
                if beta <= alpha:
                    break
            return alpha
        else:
            b_val = float('inf')
            for child in node:
                next_game = deepcopy(game)
                next_game._Game__move(child[0][0], child[0][1], (self.player_id+1)%2)
                #next_game.print()
                p_moves = self.get_possible_moves(next_game, (maximizing_player+1)%2)
                # qui posso sortare le p_moves in base a una euristica
                val = self.minmax(p_moves, depth - 1, next_game, alpha, beta, (maximizing_player+1)%2)
                b_val = min(b_val, val)
                beta = min(beta, b_val)
                if beta <= alpha:
                    break
            return beta
    
    # choose the best position from the possible ones and the best move
    def make_move(self, game: 'Game') -> tuple[tuple[int, int], Move]:
        possible_moves = self.get_possible_moves(game, self.player_id%2)
        '''if len(possible_moves) > 20:
            depth = 3
        else:
            depth = 6'''
        # if I am losing, I will search deeper to find the best move to avoid losing
        '''if is_losing(self.player_id, game):
            depth = 5
        # if I am winning, I will search less to find the best move to win
        elif is_losing((self.player_id+1)%2, game):
            depth = 3'''
        if is_losing(self.player_id, game) or is_losing((self.player_id+1)%2, game):
            depth = 3
        # if I am far from winning or losing, I don't need to search
        else:
            depth = 1

        alpha = float('-inf')
        beta = float('inf')
        b_val = float('-inf')
        if possible_moves[0][1] <= 1:
            # A trick can be to begin from one corner
            from_pos, move = random.choice(list(filter(lambda pm : pm[0][0] == (0, 0) or
                                                                        pm[0][0] == (0, game._board.shape[1]-1) or
                                                                        pm[0][0] == (game._board.shape[0]-1, 0) or
                                                                        pm[0][0] == (game._board.shape[0]-1, game._board.shape[1]-1)
                                                                     , possible_moves)))[0]
            return from_pos, move
        elif possible_moves[0][1] == 5 :
            return possible_moves[0][0]
        else:
            from_pos, move = possible_moves[0][0]

        for child in possible_moves:
            next_game = deepcopy(game)
            next_game._Game__move(child[0][0], child[0][1], self.player_id%2)
            p_moves = self.get_possible_moves(next_game, (self.player_id+1)%2)
            val = self.minmax(p_moves, depth - 1, next_game, alpha, beta, (self.player_id+1)%2)
            if val > b_val and val > 0:
                b_val = val
                from_pos = child[0][0]
                move = child[0][1]
        return from_pos, move


def test_0(test_episodes):
    win = 0
    for _ in tqdm(range(test_episodes)):
        g = Game(verbose=True)
        #player1 = MyPlayer()
        player1 = MinMaxPlayer(0)
        player2 = RandomPlayer()
        winner = g.play(player1, player2)
        print()
        g.print()
        print(f"Winner: Player {winner+1}")
        if winner==0:
            win+=1
    print(f"Win percentage: {win/test_episodes}")

def test_1(test_episodes):
    win = 0
    for _ in tqdm(range(test_episodes)):
        g = Game(verbose=True)
        #player1 = MyPlayer()
        player1 = MinMaxPlayer(0)
        player2 = MinMaxPlayer(1)
        winner = g.play(player1, player2)
        print()
        g.print()
        print(f"Winner: Player {winner+1}")
        if winner==0:
            win+=1
    print(f"Win percentage: {win/test_episodes}")

if __name__ == '__main__':
    # Prof test
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
    
    # Test with random player
    # test_0(100)
    
    # Test with minmax player
    test_1(100)
