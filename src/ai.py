from copy import deepcopy
from math import inf
from typing import List, Tuple, Dict
# from utils import toggle_turn

DOTS = 5

Move = Tuple[str, int, int]

# FUNCTIONS
def clone_board_state(horizontal_edges: List[List[int]],
                      vertical_edges: List[List[int]],
                      boxes: List[List[int]],
                      turn: int) -> Dict:
    
    return {
        "horizontal_edges": deepcopy(horizontal_edges),
        "vertical_edges": deepcopy(vertical_edges),
        "boxes": deepcopy(boxes),
        "turn": turn
    }

def get_hashable_state(state: Dict, depth: int) -> Tuple:
    # for caching
    # flatten the arrays, include turn and depth
    flat_horiz_edges = tuple(edge for row in state["horizontal_edges"] for edge in row)
    flat_verti_edges = tuple(edge for row in state["vertical_edges"] for edge in row)
    flat_boxes = tuple(edge for row in state["boxes"] for edge in row)
    return (flat_horiz_edges, flat_verti_edges, flat_boxes, state["turn"], depth)

def list_all_legal_moves(state: Dict) -> List[Move]:
    legal_moves = []
    
    for r1 in range(DOTS):
        for e1 in range(DOTS - 1):
            if state["horizontal_edges"][r1][e1] == 0:
                legal_moves.append(("H", r1, e1))
    
    for r2 in range(DOTS - 1):
        for e2 in range(DOTS):
            if state["vertical_edges"][r2][e2] == 0:
                legal_moves.append(("V", r2, e2))
    
    return legal_moves

def get_boxes_for_edge(orientation: str, row: int, col: int) -> Tuple[Tuple[int, int], ...]:
    box_rows, box_cols = DOTS - 1, DOTS - 1
    boxes = []

    if (orientation == "H"):
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

        if (0 <= col < box_cols):
            if (0 <= row - 1 < box_rows):
                boxes.append((row - 1, col))
            if (0 <= row < box_rows):
                boxes.append((row, col))
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

        if (0 <= row < box_rows):
            if (0 <= col - 1 < box_cols):
                boxes.append((row, col - 1))
            if (0 <= col < box_cols):
                boxes.append((row, col))
    
    return tuple(boxes)

def check_box_complete(state: Dict, box: Tuple[int, int]) -> bool:
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

    top_edge = state["horizontal_edges"][box_row][box_col]
    bottom_edge = state["horizontal_edges"][box_row + 1][box_col]
    left_edge = state["vertical_edges"][box_row][box_col]
    right_edge = state["vertical_edges"][box_row][box_col + 1]

    if top_edge and bottom_edge:
        if left_edge and right_edge:
            return 1

    return 0

def count_scores(state: Dict) -> Tuple[int, int]:
    p1_score, p2_score = 0, 0

    for row in state["boxes"]:
        p1_score += row.count(1)
        p2_score += row.count(2)
    
    return (p1_score, p2_score)


def check_if_game_end(state: Dict) -> bool:
    for r1 in state["horizontal_edges"]:
        for e1 in r1:
            if e1 == 0:
                return False
    
    for r2 in state["vertical_edges"]:
        for e2 in r2:
            if e2 == 0:
                return False
    
    return True

# SIMULATE MOVE

def simulate_move(state: Dict, move: Move, player: int):
    new_state = deepcopy(state)
    orientation, row, col = move

    if orientation == "H":
        new_state["horizontal_edges"][row][col] = player
    else:
        new_state["vertical_edges"][row][col] = player
    
    box_filled = False
    box_touching = get_boxes_for_edge(orientation, row, col)
    
    for box in box_touching:
        if check_box_complete(new_state, box):
            box_row, box_col = box
            if new_state["boxes"][box_row][box_col] == 0:
                new_state["boxes"][box_row][box_col] = player
                box_filled = True
    
    if not box_filled:
        # new_state["turn"] = toggle_turn(new_state["turn"])
        new_state["turn"] = player % 2 + 1
    
    return new_state, box_filled

# EVALUATION OF HEURISTIC

def get_heuristic_evaluation(state: Dict, ai_player: int) -> float:
    p1_score, p2_score = count_scores(state)
    score_difference = (p2_score - p1_score) if ai_player == 2 else (p1_score - p2_score)

    # count boxes with 3 sides filled
    three_side_boxes_ai = 0
    three_side_boxes_opponent = 0
    free_boxes_for_ai = 0
    safe_moves = 0
    remaining_boxes = 0

    opponent_player = ai_player % 2 + 1

    # helper function for count sides filled of a given box
    def sides_filled_of_box(state, box_row, box_col):
        sides_filled = 0
        
        if (state["horizontal_edges"][box_row][box_col] != 0):
            sides_filled += 1
        if (state["horizontal_edges"][box_row + 1][box_col] != 0):
            sides_filled += 1
        if (state["vertical_edges"][box_row][box_col] != 0):
            sides_filled += 1
        if (state["vertical_edges"][box_row][box_col + 1] != 0):
            sides_filled += 1
        
        return sides_filled

    # actual evaluation from here
    box_rows, box_cols = DOTS - 1, DOTS - 1

    for box_row in range(box_rows):
        for box_col in range(box_cols):
            owner = state["boxes"][box_row][box_col]
            if (owner == 0):
                remaining_boxes += 1
            
            sides = sides_filled_of_box(state, box_row, box_col)

            if (sides == 3):
                # check which edge is missing
                top_edge = state["horizontal_edges"][box_row][box_col]
                bottom_edge = state["horizontal_edges"][box_row+1][box_col]
                left_edge = state["vertical_edges"][box_row][box_col]

                if (top_edge == 0):
                    missing_move = ("H", box_row, box_col)
                elif (bottom_edge == 0):
                    missing_move = ("H", box_row + 1, box_col)
                elif (left_edge == 0):
                    missing_move = ("V", box_row, box_col)
                else:
                    missing_move = ("V", box_row, box_col + 1)
                
                # check for legality
                legal = False
                if (missing_move[0] == "H"):
                    r, c = missing_move[1], missing_move[2]
                    if (0 <= r < DOTS and 0 <= c < DOTS - 1) and (state["horizontal_edges"][r][c] == 0):
                        legal = True
                else:
                    r, c = missing_move[1], missing_move[2]
                    if (0 <= r < DOTS - 1 and 0 <= c < DOTS) and (state["vertical_edges"][r][c] == 0):
                        legal = True
                
                if (legal):
                    free_boxes_for_ai += 1 if ai_player == state["turn"] else 0
                
                # classify if opponent can take or ai can take
                if state["turn"] == opponent_player:
                    three_side_boxes_opponent += 1
                else:
                    three_side_boxes_ai += 1
    
    # safe moves: when played, dont create a 3 sided box
    legal_moves = list_all_legal_moves(state)
    for move in legal_moves:
        # simulate creating the edge and see if it creates a 3 sided box
        orientation, row, col = move
        creates_three = False
        box_touching = get_boxes_for_edge(orientation, row, col)
        
        for box in box_touching:
            box_r, box_c = box
            sides = 0

            if state["horizontal_edges"][box_r][box_c] or (orientation == "H" and row == box_r and col == box_c):
                sides += 1
            if state["horizontal_edges"][box_r + 1][box_c] or (orientation == "H" and row == box_r + 1 and col == box_c):
                sides += 1
            if state["vertical_edges"][box_r][box_c] or (orientation == "V" and row == box_r and col == box_c):
                sides += 1
            if state["vertical_edges"][box_r][box_c + 1] or (orientation == "V" and row == box_r and col == box_c + 1):
                sides += 1
            
            if sides == 3:
                creates_three = True
                break
        
        if not(creates_three):
            safe_moves += 1
    
    # evaluate heuristic with weights (adjustable)
    heuristic_val = 0
    heuristic_val += (10.0 * score_difference)
    heuristic_val -= (4.0 * three_side_boxes_opponent)
    heuristic_val += (1.5 * free_boxes_for_ai)
    heuristic_val += (0.25 * safe_moves)
    heuristic_val += (0.1 * remaining_boxes)

    # prefer being current player
    if (state["turn"] == ai_player):
        heuristic_val += 0.05
    
    return heuristic_val

# MINIMAX ALGO (WITH ALPHA BETA PRUNING AND CACHING)

def minimax(state: Dict, depth: int, alpha: float, beta: float, ai_player: int, maximizing_player: bool, cache: Dict) -> float:
    # depth limited minimax with alpha-beta pruning
    # returns numeric score

    if check_if_game_end(state):
        p1_score, p2_score = count_scores(state)
        final_score = (p2_score - p1_score) if ai_player == 2 else (p1_score - p2_score)
        return float(100.0 * final_score) # big weightage for final results
    
    if (depth <= 0):
        return get_heuristic_evaluation(state, ai_player)
    
    hash_key = get_hashable_state(state, depth)
    if hash_key in cache:
        return cache[hash_key]
    
    legal_moves = list_all_legal_moves(state)

    # move priority ordering: try those moves first which instantly complete a box
    def move_priority(move):
        new_state, box_filled = simulate_move(state, move, state["turn"])
        return 1 if box_filled else 0
    legal_moves.sort(key=move_priority, reverse=True)

    if (maximizing_player):
        value = -inf
        for move in legal_moves:
            new_state, box_filled = simulate_move(state, move, state["turn"])

            if box_filled: # if filled, same player continues (don't decrease depth)
                score = minimax(new_state, depth, alpha, beta, ai_player, True, cache)
            else:
                # next player's turn, depth decreases
                score = minimax(new_state, depth - 1, alpha, beta, ai_player, False, cache)
            
            value = max(value, score)
            alpha = max(alpha, value)

            if (alpha >= beta):
                break # beta cutoff
        
        cache[hash_key] = value
        return value
    else:
        value = inf
        for move in legal_moves:
            new_state, box_filled = simulate_move(state, move, state["turn"])
            
            if box_filled:
                score = minimax(new_state, depth, alpha, beta, ai_player, False, cache)
            else:
                score = minimax(new_state, depth - 1, alpha, beta, ai_player, True, cache)
            
            value = min(value, score)
            beta = min(beta, value)

            if (alpha >= beta):
                break # alpha cutoff
        
        cache[hash_key] = value
        return value

# Actual Returning Function
# best_ai_move

def best_ai_move(horizontal_edges: List[List[int]],
                 vertical_edges: List[List[int]],
                 boxes: List[List[int]],
                 turn: int,
                 depth: int = 4) -> Move:
    
    # returns best move for ai
    # returns move tuple eg. ("H", r, c)
    # depth: 4 - 6 recommended for 3x3 boxes

    assert turn in (1, 2)
    ai_player = turn
    root_state = clone_board_state(horizontal_edges, vertical_edges, boxes, turn)
    legal_moves = list_all_legal_moves(root_state)

    # print(len(legal_moves))

    if not(legal_moves):
        raise ValueError("No legal moves available.")

    total_possible_initial_moves = 2*((DOTS - 1)**2 + (DOTS - 1)) # formula for square grids: 2*(n^2 + n) where n is the number of boxes
    
    if (DOTS > 4):
        if (len(legal_moves) >= (total_possible_initial_moves * 0.75)): # decrease depth when number of legal moves left are more than 75% of initial possible moves
            depth -= 1 # decrease depth for the first few moves, because search for unnecessary improvements

    best_move = None
    best_score = -inf
    cache = {}

    def move_priority(move):
        new_state, box_filled = simulate_move(root_state, move, ai_player)
        return 1 if box_filled else 0
    
    # give priority to moves that complete a box
    legal_moves.sort(key=move_priority, reverse=True) 

    maximizing = True   # currently AI's move, so root is maximizing
    alpha = -inf
    beta = inf

    for move in legal_moves:
        new_state, box_filled = simulate_move(root_state, move, ai_player)
        if (box_filled):
            score = minimax(new_state, depth, alpha, beta, ai_player, True, cache)
        else:
            score = minimax(new_state, depth - 1, alpha, beta, ai_player, False, cache)
        
        # prefer moves with higher score
        if (score > best_score) or (best_move is None):
            best_score = score
            best_move = move
    
    return best_move
