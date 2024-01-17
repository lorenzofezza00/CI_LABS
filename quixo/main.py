import numpy as np
from game import Game, Move, Player
from tqdm.auto import tqdm
import random
from mygame import MyGame, colors
from minmax import MinMaxPlayer
from mcts import MctsPlayer

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
    
def test_0_begin_first(test_episodes):
    win = 0
    i = 0
    for _ in tqdm(range(test_episodes)):
        #g = MyGame(verbose=True)
        g = Game()
        #player1 = MyPlayer()
        player1 = MinMaxPlayer()
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

def test_0(test_episodes, mode='Game'):
    win = 0
    i = 0
    for _ in tqdm(range(test_episodes)):
        if mode=='Game':
            g = Game()
        else:
            g = MyGame(verbose=True)
        
        #player1 = MyPlayer()
        player1 = RandomPlayer()
        player2 = MinMaxPlayer()
        winner = g.play(player1, player2)
        print()
        g.print()
        print(f"Winner: Player {winner+1}")
        if winner==1:
            win+=1    
        print(f"Actual percentage: {win/(i+1)}")
        i+=1
    print(f"Win percentage: {win/test_episodes}")

def test_1(test_episodes, mode='Game'):
    win = 0
    i = 0
    for _ in tqdm(range(test_episodes)):
        if mode=='Game':
            g = Game()
        else:
            g = MyGame(verbose=True)
        #player1 = MyPlayer()
        player1 = MinMaxPlayer()
        player2 = MinMaxPlayer()
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
    player1 = MinMaxPlayer()
    player2 = HumanPlayer()

    game = MyGame(verbose=True)

    while True:
        winner = game.play(player1, player2)
        if winner != -1:
            print(f"Player {winner + 1} wins!")
            break

def test_fra(test_episodes, mode='Game'):
    win = 0
    i = 0
    for _ in tqdm(range(test_episodes)):
        if mode=='Game':
            g = Game()
        else:
            g = MyGame(verbose=True)
        #player1 = MyPlayer()
        player1 = MinMaxPlayer()
        player2 = MctsPlayer()
        winner = g.play(player1, player2)
        print()
        g.print()
        print(f"Winner: Player {winner+1}")
        if winner==0:
            win+=1
        print(f"Actual percentage: {win/(i+1)}")
        i+=1
    print(f"Win percentage: {win/test_episodes}")

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
    
    print(f"Player 1: {colors['green']} 0 {colors['reset']}")
    print(f"Player 2: {colors['red']} 1 {colors['reset']}")
    
    # Test with random player
    # test_0(100, mode='MyGame')
    
    # Test with minmax player
    # test_1(100)

    # human_test()
    test_fra(20, mode='MyGame')
