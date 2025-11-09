def print_2d(arr_2d: list[list[int]]):
    for row in arr_2d:
        print(row)

def toggle_turn(turn):
    # returns: (1)->(2) & (2)->(1)
    return turn % 2 + 1 

# def update_boxes(boxes, horizontal_edges, vertical_edges):
