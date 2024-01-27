from game import Game, Move, Player
from copy import deepcopy
import random
import matplotlib.pyplot as plt
import networkx as nx
from networkx.drawing.nx_pydot import graphviz_layout

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

class TreeNode:
    node_count = 0

    def __init__(self, val,  player_id=None):
        self.val = val
        self.player_id = player_id
        self.index = TreeNode.node_count
        TreeNode.node_count += 1
        self.child = []

    def add_to_graph(self, graph, parent_name=None, parent_node=None):
        node_name = str(self.index)
        node_color = 'lightgreen' if self.player_id == 0 else 'lightcoral'
        graph.add_node(node_name, color=node_color, value=str(self.val))

        if parent_name:
            graph.add_edge(parent_name, node_name)

        for child in self.child:
            child.add_to_graph(graph, node_name, self)

    def add_child(self, child):
        self.child.append(child)

class MinMaxPlayer(Player):
    def __init__(self, plot_trees=False) -> None:
        super().__init__()
        self.plot_trees = plot_trees
    
    # evaluate the board
    
    '''def evaluate(self, game: 'Game') -> float:
        if game.check_winner() == self.player_id:
            return 1
        elif game.check_winner() == (self.player_id+1)%2:
            return float('-inf')
        else:
            return 0'''
    
    '''if is_losing(self.player_id%2, game):
            return -1
        if is_losing((self.player_id+1)%2, game):
            return 1
        return 0'''
    
    def evaluate(self, winner, pid, game : 'Game') -> float:
        if winner == pid%2:
            return float('inf')
        elif winner == (pid+1)%2:
            return float('-inf')
        else:
            max_p1 = max_inline_pieces(pid, game)
            max_p2 = max_inline_pieces((pid+1)%2, game)
            return max_p1 - max_p2
        
        
    def get_possible_moves(self, game: 'Game', player) -> list[tuple[tuple[int, int], Move]]:
        possible_moves = []
        # three possible moves for the cornice without the corners
        for i in range(1, 4, 1):
            # if I select a piece from the top row, I can slide it in any other direction, but not in the same
            if game._board[0][i] == -1 or game._board[0][i] == player:
                possible_moves.append(((i, 0), Move.BOTTOM))
                possible_moves.append(((i, 0), Move.LEFT))
                possible_moves.append(((i, 0), Move.RIGHT))
            if game._board[4][i] == -1 or game._board[4][i] == player:
                possible_moves.append(((i, 4), Move.TOP))
                possible_moves.append(((i, 4), Move.LEFT))
                possible_moves.append(((i, 4), Move.RIGHT))
            if game._board[i][0] == -1 or game._board[i][0] == player:
                possible_moves.append(((0, i), Move.TOP))
                possible_moves.append(((0, i), Move.BOTTOM))
                possible_moves.append(((0, i), Move.RIGHT))
            if game._board[i][4] == -1 or game._board[i][4] == player:
                possible_moves.append(((4, i), Move.TOP))
                possible_moves.append(((4, i), Move.BOTTOM))
                possible_moves.append(((4, i), Move.LEFT))
        # two possible moves for the corners
        if game._board[0][0] == -1 or game._board[0][0] == player:
            possible_moves.append(((0, 0), Move.RIGHT))
            possible_moves.append(((0, 0), Move.BOTTOM))
        if game._board[0][4] == -1 or game._board[0][4] == player:
            possible_moves.append(((4, 0), Move.BOTTOM))
            possible_moves.append(((4, 0), Move.LEFT)) 
        if game._board[4][0] == -1 or game._board[4][0] == player:
            possible_moves.append(((0, 4), Move.RIGHT))
            possible_moves.append(((0, 4), Move.TOP))
        if game._board[4][4] == -1 or game._board[4][4] == player:
            possible_moves.append(((4, 4), Move.LEFT))
            possible_moves.append(((4, 4), Move.TOP))

        sorted_pm = []
        for pm in possible_moves:
            new_game = deepcopy(game)
            new_game._Game__move(pm[0], pm[1], player)
            if new_game.check_winner() == player:
                return [(pm, 5, game._board[pm[0][1]][pm[0][0]])]
            # count the number of pieces in line the move creates and indicate if the piece is neutral or not in the original board
            sorted_pm.append((pm, max_inline_pieces(player, new_game), game._board[pm[0][1]][pm[0][0]]))
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

    def minmax(self, node, depth, game: 'Game', alpha, beta, maximizing_player, pid, tree):
        # a node is terminal if there are no more moves to make
        winner = game.check_winner()
        if depth == 0 or winner != -1 or is_terminal(node):
            value = self.evaluate(winner, pid, game)
            tree.val = value
            return value
        if maximizing_player == pid:
            b_val = float('-inf')
            for child in node:
                next_game = deepcopy(game)
                next_game._Game__move(child[0][0], child[0][1], pid%2)
                # next_game.print()
                p_moves = self.get_possible_moves(next_game, (maximizing_player+1)%2)
                treechild = TreeNode('child', (maximizing_player+1)%2)
                val = self.minmax(p_moves, depth - 1, next_game, alpha, beta, (maximizing_player+1)%2, treechild)
                treechild.val = val
                tree.add_child(treechild)
                b_val = max(b_val, val)
                alpha = max(alpha, b_val)
                if beta <= alpha:
                    break
            return alpha
        else:
            b_val = float('inf')
            for child in node:
                next_game = deepcopy(game)
                next_game._Game__move(child[0][0], child[0][1], (pid+1)%2)
                # next_game.print()
                p_moves = self.get_possible_moves(next_game, (maximizing_player+1)%2)
                treechild = TreeNode('child', (maximizing_player+1)%2)
                val = self.minmax(p_moves, depth - 1, next_game, alpha, beta, (maximizing_player+1)%2, pid, treechild)
                treechild.val = val
                tree.add_child(treechild)
                b_val = min(b_val, val)
                beta = min(beta, b_val)
                if beta <= alpha:
                    break
            return beta
    
    # choose the best position from the possible ones and the best move
    def make_move(self, game: 'Game') -> tuple[tuple[int, int], Move]:
        pid = game.get_current_player()
        possible_moves = self.get_possible_moves(game, pid%2)
        # initial
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
        
        #actual

        # advantage depth variation
        # if the opponent is playing bad, I don't need to anticipate so many moves
        # if the opponent is playing good, max_p2 will be more than or equal to
        # the (advantage + 1) = [abs(max_p1 - max_p2) + 1]
        # so I will go deep of (advantage + 1)
        max_p1 = max_inline_pieces(pid, game)
        max_p2 = max_inline_pieces((pid+1)%2, game)
        depth = min(abs(max_p1 - max_p2) + 1, max_p2)
        TreeNode.node_count = 0
        tree = TreeNode('root', pid%2)

        for child in possible_moves:
            next_game = deepcopy(game)
            next_game._Game__move(child[0][0], child[0][1], pid%2)
            p_moves = self.get_possible_moves(next_game, (pid+1)%2)
            treechild = TreeNode('child', (pid+1)%2)
            val = self.minmax(p_moves, depth - 1, next_game, alpha, beta, (pid+1)%2, pid, treechild)
            treechild.val = val
            tree.add_child(treechild)
            if val > b_val:
                tree.val = val
                b_val = val
                from_pos = child[0][0]
                move = child[0][1]

        if self.plot_trees:
            print(f"depth: {depth}")
            graph = nx.Graph()
            tree.add_to_graph(graph)
            # colors is a sequence
            colors = [graph.nodes[n]['color'] for n in graph.nodes]
            # labels is a dictionary
            labels = nx.get_node_attributes(graph, 'value')

            pos = graphviz_layout(graph, prog="dot")
            # pos = graphviz_layout(graph, prog="twopi")
            plt.figure(figsize=(12, 8))
            nx.draw_networkx_labels(graph, pos, labels=labels, font_size=10, font_color="black")
            nx.draw(graph, pos, node_color=colors)
            plt.show()
            print("best value : ", b_val)
        return from_pos, move