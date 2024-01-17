import random
import numpy as np
from game import Game, Move, Player
from copy import deepcopy
from tqdm.auto import tqdm

colors = {
    'reset': "\033[0m",
    'red': "\033[91m",
    'green': "\033[92m",
    'yellow': "\033[93m",
    'blue': "\033[94m"
}

class RandomPlayer(Player):
    def __init__(self) -> None:
        super().__init__()

    def make_move(self, game: 'Game') -> tuple[tuple[int, int], Move]:
        from_pos = (random.randint(0, 4), random.randint(0, 4))
        move = random.choice([Move.TOP, Move.BOTTOM, Move.LEFT, Move.RIGHT])
        return from_pos, move
    
class MyPlayer(Player):
    def __init__(self) -> None:
        super().__init__()

    def make_move(self, game: 'Game') -> tuple[tuple[int, int], Move]:
        from_pos = (random.randint(0, 4), random.randint(0, 4))
        move = random.choice([Move.TOP, Move.BOTTOM, Move.LEFT, Move.RIGHT])
        return from_pos, move

class HumanPlayer(Player):
    def make_move(self, game: 'Game') -> tuple[tuple[int, int], Move]:
        print("Enter your move:")
        while True:
            try:
                # Get user input for row and column
                row = int(input("Enter row (0-4): "))
                col = int(input("Enter column (0-4): "))

                # Get user input for move direction
                move_input = input("Enter move direction (TOP, BOTTOM, LEFT, RIGHT): ").upper()
                move = Move[move_input]

                # Check if the move is valid
                if 0 <= row <= 4 and 0 <= col <= 4 and move in Move:
                    return (col, row), move
                else:
                    print("Invalid move. Please try again.")
            except (ValueError, KeyError):
                print("Invalid input. Please enter integers for row and column, and a valid move direction.")


class MyGame(Game):
    def __init__(self, verbose=False) -> None:
        self._board = np.ones((5, 5), dtype=np.uint8) * -1
        self.current_player_idx = 1
        self.verbose = verbose

    def print(self):
        '''Prints the board. -1 are neutral pieces, 0 are pieces of player 0, 1 pieces of player 1'''
        # print(self._board)
        # cnt_0 = 0
        # cnt_1 = 0
        for row in self._board:
            for col in row:
                if col == -1:
                    print(f"{colors['blue']} {col} {colors['reset']}", end="")
                elif col == 1:
                    # cnt_1 += 1
                    print(f"{colors['red']}  {col} {colors['reset']}", end="")
                else:
                    # cnt_0 += 1
                    print(f"{colors['green']}  {col} {colors['reset']}", end="")
            print()
        # It's ok to have a difference of symbols > 1, because, in some turns a player
        # can decide to use cube with his symbol, so it doesn't change the number of symbol used
        '''if abs(cnt_0-cnt_1) > 1:
            print(f"{colors['yellow']} Player 1: {cnt_0} symbols\tPlayer 2: {cnt_1} symbols {colors['reset']}")
        else :
            print(f"Player 1: {cnt_0} symbols\tPlayer 2: {cnt_1} symbols")'''

    def play(self, player1: Player, player2: Player) -> int:
        '''Play the game. Returns the winning player'''
        players = [player1, player2]
        winner = -1
        while winner < 0:
            self.current_player_idx += 1
            self.current_player_idx %= len(players)
            ok = False
            while not ok:
                from_pos, slide = players[self.current_player_idx].make_move(
                    self)
                ok = self.__move(from_pos, slide, self.current_player_idx)
                if not ok and self.verbose:
                    if self.current_player_idx == 0:
                        print(f"{colors['red']} Player {self.current_player_idx+1} moves {from_pos} {slide} {colors['reset']}")
                    else:
                        print(f"Player {self.current_player_idx+1} moves {from_pos} {slide}")
            if self.verbose:
                if self.current_player_idx == 0:
                    print(f"{colors['green']} Player {self.current_player_idx+1} moves {from_pos} {slide} {colors['reset']}")
                else:
                    print(f"Player {self.current_player_idx+1} moves {from_pos} {slide}")
                self.print()
            winner = self.check_winner()
        return winner
    
    def __move(self, from_pos: tuple[int, int], slide: Move, player_idx: int) -> bool:
        return super()._Game__move(from_pos, slide, player_idx)


def is_losing(player_id, len, game: 'Game') -> bool:
        # if the adversary has a line of len+1 pieces, I am losing
        for i in range(game._board.shape[0]):
            if sum(game._board[i, :] == (player_id+1)%2) >= len:
                return True
            if sum(game._board[:, i] == (player_id+1)%2) >= len:
                return True
        if sum(game._board.diagonal() == (player_id+1)%2) >= len:
            return True
        if sum(game._board[::-1].diagonal() == (player_id+1)%2) >= len:
            return True
        
def max_inline_pieces(maximizing_player, game: 'Game') -> int:
    cnt = 0
    for i in range(game._board.shape[0]):
        cnt = max(cnt, sum(game._board[i, :] == maximizing_player))
        cnt = max(cnt, sum(game._board[:, i] == maximizing_player))
    cnt = max(cnt, sum(game._board.diagonal() == maximizing_player))
    cnt = max(cnt, sum(game._board[::-1].diagonal() == maximizing_player))
    return cnt

def is_terminal(node) -> bool:
        if len(node) == 0:
            return True
        return False

'''class TreeNode:
    def __init__(self, state, move):
        self.state = state
        self.move = move
        self.children = []

    def add_child(self, child):
        self.children.append(child)

    def search(self, state):
        if self.state == state:
            return deepcopy(self)
        else:
            for child in self.children:
                return child.search(state)'''

class MinMaxPlayer(Player):
    def __init__(self, player_id) -> None:
        super().__init__()
        self.player_id = player_id
        # self.tree = None
    # evaluate the board
    '''def evaluate(self, game: 'Game') -> float:
        if game.check_winner() == self.player_id:
            return 1
        elif game.check_winner() == (self.player_id+1)%2:
            return float('-inf')
        else:
            return 0'''
    def evaluate(self, winner, game : 'Game') -> float:
        if winner == self.player_id%2:
            return float('inf')
        elif winner == (self.player_id+1)%2:
            return float('-inf')
        else:
            max_p1 = max_inline_pieces(self.player_id, game)
            max_p2 = max_inline_pieces((self.player_id+1)%2, game)
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
            if new_game.check_winner() == maximizing_player:
                return [(pm, 5, game._board[pm[0][1]][pm[0][0]])]
            # count the number of pieces in line the move creates and indicate if the piece is neutral or not in the original board
            sorted_pm.append((pm, max_inline_pieces(maximizing_player, new_game), game._board[pm[0][1]][pm[0][0]]))
        # sort the possible moves in descending order based on the number of pieces in line
        # putting firstly the moves with neutral pieces
        sorted_pm = sorted(sorted_pm, key=lambda x: (x[1], -x[2]), reverse=True)
        grouped_pm = {}
        for pm in sorted_pm:
            if (pm[1], pm[2]) not in grouped_pm:
                grouped_pm[(pm[1], pm[2])] = []
            grouped_pm[(pm[1], pm[2])].append(pm)
        
        for group in grouped_pm:
            random.shuffle(grouped_pm[group])
        shuffled_sorted_pm = [item for group in grouped_pm.values() for item in group]
        return shuffled_sorted_pm

    def minmax(self, node, depth, game: 'Game', alpha, beta, maximizing_player = 0):
        # a node is terminal if there are no more moves to make
        # NON VA BENE PERCHE SE MI PAREGGIA POTREBBE DIRMI CHE HA PERSO SOLO PERCHE LO VALUTA PRIMA
        winner = game.check_winner()
        if depth == 0 or winner != -1 or is_terminal(node):
            value = self.evaluate(winner, game)
            '''if value!=0:
                print(f"{colors['yellow']} Found! {value} {colors['reset']}")
                game.print()'''
            return value
        if maximizing_player == self.player_id:
            b_val = float('-inf')
            for child in node:
                next_game = deepcopy(game)
                next_game._Game__move(child[0][0], child[0][1], self.player_id%2)
                # self.tree.add_child(TreeNode(next_game._board, (child[0][0], child[0][1])))
                # next_game.print()
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
                # self.tree.add_child(TreeNode(next_game._board, (child[0][0], child[0][1])))
                # next_game.print()
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
        
        '''# if I am losing because the opponent has len symbols in line, I will search deeper to find the best move to avoid losing
        depth = 1
        if is_losing(self.player_id, 3, game):
            depth = 4
        # if I am winning because I have len symbols in line, I will search less to find the best move to win
        elif is_losing((self.player_id+1)%2, 3, game):
            depth = 3'''
        
        '''if is_losing(self.player_id, game) or is_losing((self.player_id+1)%2, game):
            depth = 3
        # if I am far from winning or losing, I don't need to search
        else:
            depth = 1'''

        alpha = float('-inf')
        beta = float('inf')
        b_val = float('-inf')
        # A trick can be to begin from one corner so this if should work only for the first move
        if possible_moves[0][1] <= 1:
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
        '''if depth != 1:
            if self.tree is None:
                self.tree = TreeNode(game._board, None)
            else:
                self.tree = self.tree.search(game._board)'''
        
        # if someone is losign depth variation
        '''if is_losing(self.player_id, 3, game) or is_losing((self.player_id+1)%2, 3, game):
            max_p1 = max_inline_pieces(self.player_id, game)
            max_p2 = max_inline_pieces((self.player_id+1)%2, game)
            # depth = min(abs(max_p1 - max_p2) + 3, 4)
            depth = abs(max_p1 - max_p2) + 1
            print(f"depth: {depth}")
        else:
            depth = 1'''
        
        # advantage depth variation
        # if the opponent is playing bad, I don't need to anticipate so many moves
        # if the opponent is playing good, max_p2 will be more than or equal to
        # the (advantage + 1) = [abs(max_p1 - max_p2) + 1]
        # so I will go deep of (advantage + 1)
        max_p1 = max_inline_pieces(self.player_id, game)
        max_p2 = max_inline_pieces((self.player_id+1)%2, game)
        depth = min(abs(max_p1 - max_p2) + 1, max_p2)
        print(f"depth: {depth}")
        
        for child in possible_moves:
            next_game = deepcopy(game)
            next_game._Game__move(child[0][0], child[0][1], self.player_id%2)
            # self.tree.add_child(TreeNode(next_game._board, (child[0][0], child[0][1])))
            p_moves = self.get_possible_moves(next_game, (self.player_id+1)%2)
            val = self.minmax(p_moves, depth - 1, next_game, alpha, beta, (self.player_id+1)%2)
            if val > b_val: # and val > 0:
                b_val = val
                from_pos = child[0][0]
                move = child[0][1]
        return from_pos, move
    
def test_0_begin_first(test_episodes):
    win = 0
    i = 0
    for _ in tqdm(range(test_episodes)):
        #g = MyGame(verbose=True)
        g = Game()
        #player1 = MyPlayer()
        player1 = MinMaxPlayer(0)
        player2 = RandomPlayer()
        winner = g.play(player1, player2)
        print()
        g.print()
        print(f"Winner: Player {winner+1}")
        if winner==0:
            win+=1    
        print(f"Actual percentage: {win/(i+1)}")
        i+=1
    print(f"Win percentage: {win/test_episodes}")

def test_0(test_episodes):
    win = 0
    i = 0
    for _ in tqdm(range(test_episodes)):
        #g = MyGame(verbose=True)
        g = Game()
        #player1 = MyPlayer()
        player1 = RandomPlayer()
        player2 = MinMaxPlayer(1)
        winner = g.play(player1, player2)
        print()
        g.print()
        print(f"Winner: Player {winner+1}")
        if winner==1:
            win+=1    
        print(f"Actual percentage: {win/(i+1)}")
        i+=1
    print(f"Win percentage: {win/test_episodes}")

def test_1(test_episodes):
    win = 0
    i = 0
    for _ in tqdm(range(test_episodes)):
        g = MyGame(verbose=True)
        #player1 = MyPlayer()
        player1 = MinMaxPlayer(0)
        player2 = MinMaxPlayer(1)
        winner = g.play(player1, player2)
        print()
        g.print()
        print(f"Winner: Player {winner+1}")
        if winner==0:
            win+=1
        print(f"Actual percentage: {win/(i+1)}")
        i+=1
    print(f"Win percentage: {win/test_episodes}")

def human_test():
    player1 = MinMaxPlayer(0)
    player2 = HumanPlayer()

    game = MyGame(verbose=True)

    while True:
        winner = game.play(player1, player2)
        if winner != -1:
            print(f"Player {winner + 1} wins!")
            break

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
    test_0(100)
    
    # Test with minmax player
    # test_1(100)

    # human_test()
