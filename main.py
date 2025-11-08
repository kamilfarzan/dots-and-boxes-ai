from utils import print_2d, toggle_turn

DOTS = 4
horizontal_edges = [[0] * (DOTS - 1) for _ in range(DOTS)]
vertical_edges = [[0] * (DOTS) for _ in range(DOTS - 1)]
boxes = [[0] * (DOTS - 1) for _ in range(DOTS - 1)]
turn = 1

# FUNCTIONS

def set_move(move, turn):
    if move[0] == "H":
        horizontal_edges[move[1]][move[2]] = turn
    else:
        vertical_edges[move[1]][move[2]] = turn

# a move    = ("H", r, c)           # or "V"
move = ("H", 0, 1)
set_move(move, turn)

print_2d(horizontal_edges)
print_2d(vertical_edges)