import numpy as np
from game import Game, Move, Player
from tqdm.auto import tqdm
import random
from mygame import MyGame, colors
from minmax import MinMaxPlayer
import argparse

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

def test(test_episodes, p1, p2, my_player, mode='Game'):
    win = 0
    i = 0
    for _ in tqdm(range(test_episodes)):
        if mode=='Game':
            g = Game()
        else:
            g = MyGame(verbose=True)
        
        #player1 = MyPlayer()
        player1 = p1()
        player2 = p2()
        winner = g.play(player1, player2)
        print()
        g.print()
        print(f"Winner: Player {winner+1}")
        if winner==my_player%2:
            win+=1    
        print(f"Actual percentage: {win/(i+1)}")
        i+=1
    print(f"Win percentage: {win/test_episodes}")

def human_test(p1, p2, mode='Game'):
    player1 = p1()
    player2 = p2()

    if mode=='Game':
        g = Game()
    else:
        g = MyGame(verbose=True)

    while True:
        winner = g.play(player1, player2)
        if winner != -1:
            print(f"Player {winner + 1} wins!")
            break

def parse_args():
    parse = argparse.ArgumentParser()

    parse.add_argument('--mode',
                       dest='mode',
                       type=str,
                       default='MyGame',
    )
    parse.add_argument('--p1',
                       dest='p1',
                       type=str,
                       default='RandomPlayer',
    )
    parse.add_argument('--p2',
                       dest='p2',
                       type=str,
                       default='MinMaxPlayer',
    )
    parse.add_argument('--n_tests',
                       dest='n_tests',
                       type=int,
                       default=100,
    )
    parse.add_argument('--my_player',
                       dest='my_player',
                       type=int,
                       default=1,
    )
    parse.add_argument('--human',
                       dest='human',
                       type=bool,
                       default=False,
    )
    return parse.parse_args()

if __name__ == '__main__':
    # Prof test
    '''g = Game()
    g.print()
    #player1 = MyPlayer()
    player1 = MinMaxPlayer()
    player2 = RandomPlayer()
    winner = g.play(player1, player2)
    print()
    g.print()
    print(f"Winner: Player {winner+1}")'''
    
    args = parse_args()

    print(f"Player 1: {colors['green']} 0 {colors['reset']}")
    print(f"Player 2: {colors['red']} 1 {colors['reset']}")
    # test(100, MinMaxPlayer, RandomPlayer, mode='MyGame')
    if args.human:
        human_test(HumanPlayer, MinMaxPlayer, mode=args.mode)
    else:
        p1 = globals()[args.p1]
        p2 = globals()[args.p2]
        test(args.n_tests, p1, p2, args.my_player, mode=args.mode)
        
