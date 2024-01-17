from game import Game, Player, Move
import numpy as np

colors = {
    'reset': "\033[0m",
    'red': "\033[91m",
    'green': "\033[92m",
    'yellow': "\033[93m",
    'blue': "\033[94m"
}

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
