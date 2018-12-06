import time
from itertools import product, combinations, repeat, permutations, chain
#import numpy as np
from copy import deepcopy
import string

class ChessBoard():

    field_symbol = "."
    covered_field_symbol = "x"
    ok_fields = [field_symbol, covered_field_symbol]

    def __init__(self, ):
        self.board = [[self.field_symbol] * n for i in xrange(n)]
        self.free_positions = list(product(range(n),range(n)))

    def update_free_positions(self, ):
        self.free_positions = filter(lambda pos: self.board[pos[0]][pos[1]] == self.field_symbol, self.free_positions)


class Figure():
    
    def __init__(self, figure):
        self.name = figure
        self.s = figure[:1]
        self.range = n
        if self.name in ["King", "Rider"]: 
            self.range = 2
        self.position = None
        self.potential = list(permutations(range(n),2))

    def put_on_board(self, position, chessBoard):
        w, h = self.position = position
        if chessBoard.board[w][h] == chessBoard.field_symbol:
            if self.fire(chessBoard):
                chessBoard.board[w][h] = self.s
                return chessBoard

    def fire(self, chessBoard):
        self.get_moves()
        clear_targets = [(w, h) for (w, h) in self.potential if chessBoard.board[w][h] in chessBoard.ok_fields]
        if self.potential == clear_targets:
            for w, h in self.potential:
                chessBoard.board[w][h] = chessBoard.covered_field_symbol
            return chessBoard

    def get_moves(self):
        w, h = self.position
        figure_targets = []
        for i in range(1, self.range):
            target =   [
                        (w,   h-i),
                        (w,   h+i),
                        (w+i, h  ),
                        (w-i, h  ),

                        (w+i, h+i),
                        (w+i, h-i),
                        (w-i, h+i),
                        (w-i, h-i)
                                  ]
            if self.name == "Laufer":
                target = target[4:]
            elif self.name == "Tower":
                target = target[:4]
            elif self.name == "Rider":
                target =   [
                        (w+2, h+1),
                        (w-2, h+1),
                        (w+2, h-1),
                        (w-2, h-1),

                        (w+1, h+2),
                        (w+1, h-2),
                        (w-1, h+2),
                        (w-1, h-2)
                                  ]
            figure_targets.extend(target)
        if (w, h) in figure_targets: 
            figure_targets.remove((w, h))
        self.potential = self.targets_purge(figure_targets)

    def targets_purge(self, figure_targets):
        return filter(self.board_limit, figure_targets)

    def board_limit(self, target):
        w, h = target
        if w >= 0 and h >= 0:
            if w < n and h < n:
                return (w, h)

def new_game(figures, n):
    
    def turn(prev_turn_boards, figure):

        def boards_to_play(board, figure):
            for board_temp in positions_to_take(board, figure):
                board_temp.update_free_positions()
                yield board_temp
        
        def positions_to_take(board, figure):
            for position in board.free_positions:
                positions = figure.put_on_board(position, deepcopy(board))
                if positions:
                    yield positions

        def decider(board_temp):
            if board_temp.free_positions and figs > 0:
                next_turn_boards.append(board_temp)
            elif figs == 0:
                if board_temp.board not in result:
                    result.append(board_temp.board)

        def run(board, figure):
            [decider(board_temp) for board_temp in boards_to_play(board, figure)]

        next_turn_boards = []
        [run(board, figure) for board in prev_turn_boards]
        
        return next_turn_boards

    figures = [Figure(f) for f in figures_order_optimalisation(figures)]
    boards = [ChessBoard()]

    figs = len(figures)
    result = []
    for figure in figures:
        figs -= 1
        start_time = time.time()
        boards = turn(boards, figure)
        print figs, "\t\t", len(boards), "\t\t{:.5f}".format(time.time() - start_time)
    return result

def figures_order_optimalisation(figures):
    a,b,c,d,e = [], [], [], [], []
    for fig in figures:
        if fig == "Hetman": a.append(fig)
        elif fig == "Tower": b.append(fig)
        elif fig == "Laufer": c.append(fig)
        elif fig == "Rider": d.append(fig)
        else: e.append(fig)
    return chain(a,b,c,d,e)

def timing():
    start_time = time.time()
    return lambda x: "{} {:.5f}s".format(x, time.time() - start_time)



# define Chessboard size and Figures by input (optional):
def start_by_input():
    n = default_n = 5
    initial_chessboard_creation_msg = "Define size of a chessboard by passing n * m size:"
    print initial_chessboard_creation_msg
    n = int(raw_input("Define n: "))
    #m = int(raw_input("Define m: "))

    initial_figures_creation_msg = "Define number figures:"
    print initial_figures_creation_msg
    figure_names = ["King", "Hetman", "Tower", "Laufer", "Rider"]
    number_of_figures = []
    for figure in figure_names:
        msg = "{} figures ({}): ".format(figure, figure[:1])
        nr = repeat(figure, int(raw_input(msg))) 
        number_of_figures.append(nr)
    list_of_figures = list(chain.from_iterable(number_of_figures))
    
    return n, list_of_figures

def start_by_demo():
    # Demo figure sets
    a = ["Rider", "Laufer", "Laufer", "King", "King" "Hetman", "Hetman"]
    b = ["Hetman", "Hetman", "Hetman", "Hetman"] 
    b2 = ["Hetman", "Hetman", "Hetman", "Rider"] 
    c = ["Hetman", "Rider","Hetman", "King", "Rider"]
    d = ["Hetman", "Hetman", "Rider","Hetman", "King", "Rider"]
    e = ["Rider", "Rider", "King", "King", "Laufer", "Tower"]
    d3 = ["Hetman", "Hetman"]
    # Suspicous sets:
    f = ["Tower", "Tower", "Tower"] # ok
    g = ["King"] # ok
    # Task set:
    task_set = ["King","King","Hetman","Hetman", "Laufer", "Laufer",  "Rider"]
    # Default demo set:
    figures = c # task_set
    # Demo board size
    n = 5
    return n, figures

def start_by_demo_or_input():
    demo_or_input_decision_msg = "Pass none for demo, pass any letter for declaring"
    demo_or_input_decision = raw_input(demo_or_input_decision_msg)
    if demo_or_input_decision == "": # DEMO
        return start_by_demo()
    else:
        return start_by_input()


if __name__ == '__main__':
    n, figures = start_by_demo_or_input()
    t = timing()
    result = new_game(figures, n)

    print "\nFigures: {}".format(" ".join([f[:1] for f in figures]))
    print "Unique combinations: {}".format(len(result))
    print t("Computation time:")

# To do:
# N x M
# SPRZATANIE: 
    # naming (result lol, order lol, w/h, fin2, boards etc)
    # pep
    # struktura programu
# Ucz sie generatorow i partiali - moze cos z tego jeszcze wejdzie