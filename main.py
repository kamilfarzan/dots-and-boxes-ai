from utils import print_2d, toggle_turn
from terminal import draw_board

DOTS = 4
horizontal_edges = [[0] * (DOTS - 1) for _ in range(DOTS)]
vertical_edges = [[0] * (DOTS) for _ in range(DOTS - 1)]
boxes = [[0] * (DOTS - 1) for _ in range(DOTS - 1)]

# FUNCTIONS
def check_move_legality(move):
    if (move[0] == "H"):
        if not(0 <= move[1] < DOTS and 0 <= move[2] < DOTS - 1):
            return 0
        if (horizontal_edges[move[1]][move[2]] != 0):
            return 0
        return 1
    elif (move[0] == "V"):
        if not(0 <= move[1] < DOTS - 1 and 0 <= move[2] < DOTS):
            return 0
        if (vertical_edges[move[1]][move[2]] != 0):
            return 0
        return 1
    else:
        return 0

def set_move(move, turn):
    if move[0] == "H":
        horizontal_edges[move[1]][move[2]] = turn
    else:
        vertical_edges[move[1]][move[2]] = turn

def list_all_legal_moves():
    horiz_legal_moves, verti_legal_moves = [], []

    for r1 in range(DOTS):
        for e1 in range(DOTS - 1):
            if horizontal_edges[r1][e1] != 0:
                horiz_legal_moves.append(("H", r1, e1))
    
    for r2 in range(DOTS - 1):
        for e2 in range(DOTS):
            if vertical_edges[r2][e2] != 0:
                verti_legal_moves.append(("V", r2, e2))

    return horiz_legal_moves + verti_legal_moves

def get_boxes_for_edge(orientation, row, col):
    if orientation == "H":
        # if 0, 0 -> box=0,0
        # if 1, 0 -> box=0,0 or 1,0
        # if 2, 0 -> box=1,0 or 2,0
        # if 3, 0 -> box=2,0

        # if 0, 1 -> box=0,1
        # if 1, 1 -> box=0,1 or 1,1
        # if 2, 1 -> box=1,1 or 2,1
        # if 3, 1 -> box=2,1

        # if 0, 2 -> box=0,2
        # if 1, 2 -> box=0,2 or 1,2
        # if 2, 2 -> box=1,2 or 2,2
        # if 3, 2 -> box=2,2
        
        if row == 0:
            return ((0, col),)
        elif row == 3:
            return ((2, col),)
        else:
            # return (1) -> ((row, 0), (row-1, 1)) and (2) -> ((row, 1), (row-1, 2))
            return ((row, col), (row - 1, col))
    else:
        # if 0, 0 -> box=0,0
        # if 0, 1 -> box=0,0 or 0,1
        # if 0, 2 -> box=0,1 or 0,2
        # if 0, 3 -> box=0,2

        # if 1, 0 -> box=1,0
        # if 1, 1 -> box=1,0 or 1,1
        # if 1, 2 -> box=1,1 or 1,2
        # if 1, 3 -> box=1,2

        # if 2, 0 -> box=2,0
        # if 2, 1 -> box=2,0 or 2,1
        # if 2, 2 -> box=2,1 or 2,2
        # if 2, 3 -> box=2,2

        if col == 0:
            return ((row, 0),)
        elif col == 3:
            return ((row, 2),)
        else:
            # return (1) -> ((row, 0), (row, 1)) and (2) -> ((row, 1), (row, 2))
            return ((row, col - 1), (row, col))

def check_box_complete(box):
    # if box = 0, 0 --> ("H" -> (0, 0), (1, 0)), ("V" -> (0, 0), (0, 1))
    # if box = 0, 1 --> ("H" -> (0, 1), (1, 1)), ("V" -> (0, 1), (0, 2))
    # if box = 0, 2 --> ("H" -> (0, 2), (1, 2)), ("V" -> (0, 2), (0, 3))

    # if box = 1, 0 --> ("H" -> (1, 0), (2, 0)), ("V" -> (1, 0), (1, 1))
    # if box = 1, 1 --> ("H" -> (1, 1), (2, 1)), ("V" -> (1, 1), (1, 2))
    # if box = 1, 2 --> ("H" -> (1, 2), (2, 2)), ("V" -> (1, 2), (1, 3))

    # if box = 2, 0 --> ("H" -> (2, 0), (3, 0)), ("V" -> (2, 0), (2, 1))
    # if box = 2, 1 --> ("H" -> (2, 1), (3, 1)), ("V" -> (2, 1), (2, 2))
    # if box = 2, 2 --> ("H" -> (2, 2), (3, 2)), ("V" -> (2, 2), (2, 3))

    box_row, box_col = box[0], box[1]
    # horiz_edges_of_box = ((box_row, box_col), (box_row + 1, box_col))
    # verti_edges_of_box = ((box_row, box_col), (box_row, box_col + 1))

    top_edge = horizontal_edges[box_row][box_col]
    bottom_edge = horizontal_edges[box_row + 1][box_col]
    left_edge = vertical_edges[box_row][box_col]
    right_edge = vertical_edges[box_row][box_col + 1]

    if top_edge and bottom_edge:
        if left_edge and right_edge:
            return 1

    return 0

def detect_box_completion(move, turn):
    # not changing horizontal_edges and vertical_edges here
    # already changed before
    
    box_filled = False
    orientation, row, col = move[0], move[1], move[2]
    boxes_touching = get_boxes_for_edge(orientation, row, col)

    for box in boxes_touching:
        if check_box_complete(box):
            boxes[box[0]][box[1]] = turn
            box_filled = True
    
    return box_filled

def game_end_detection():
    # horizontal_edges, vertical_edges
    for r1 in horizontal_edges:
        for e1 in r1:
            if e1 == 0:
                return 0
    
    for r2 in vertical_edges:
        for e2 in r2:
            if e2 == 0:
                return 0

    return 1

def count_boxes():
    p1_score, p2_score = 0, 0

    for row in boxes:
        for box in row:
            if box == 1:
                p1_score += 1
            else:
                p2_score += 1

    return (p1_score, p2_score)
# a move    = ("H", r, c)           # or "V"
# moves = (("H", 0, 1), ("V", 0, 2), ("H", 1, 1), ("V", 0, 1), ("V", 0, 1))

# for move in moves:
#     if not(check_move_legality(move)):
#         print("ILLEGAL: ", move)
#         continue
#     set_move(move, turn)
#     box_complete = detect_box_completion(move, turn)
#     if not(box_complete):
#         turn = toggle_turn(turn)

# print("Current list of moves:", moves)
# draw_board(horizontal_edges, vertical_edges, boxes)
# print('Turn is:', turn)



### GAME LOOP BETWEEN HUMAN PLAYERS
turn = 1
draw_board(horizontal_edges, vertical_edges, boxes)
while not(game_end_detection()):
    # INPUT
    print(f"For inputting move (current turn is Player {turn}): ")
    orientation = input("Enter horizontal or vertical, either 'H' or 'V': ")
    # row, col = map(int, tuple(input("Enter row and col: (r, c)")))
    row = int(input("Enter row: "))
    col = int(input("Enter col: "))
    move = (orientation, row, col)

    if not(check_move_legality(move)):
        print("ILLEGAL MOVE. TRY AGAIN.")
        continue

    set_move(move, turn)

    box_complete = detect_box_completion(move, turn)

    ### PRINT GRID
    draw_board(horizontal_edges, vertical_edges, boxes)

    if not(box_complete):
        turn = toggle_turn(turn)
else:
    p1_score, p2_score = count_boxes()
    if p1_score > p2_score:
        print("P1 WINS")
    elif p2_score > p1_score:
        print("P2 WINS")
    else:
        print("DRAW")