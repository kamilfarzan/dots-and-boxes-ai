from rich.console import Console

console = Console()

def draw_board(horizontal_edges, vertical_edges, boxes):
    DOTS = len(horizontal_edges)
    box_size = len(boxes)

    for r in range(DOTS):
        # First: print dot + horizontal edges row 
        dot_row = ""
        for c in range(len(horizontal_edges[0])):
            dot_row += "•"
            val = horizontal_edges[r][c]
            if val == 0:
                dot_row += "   "
            elif val == 1:
                dot_row += "[bold blue]───[/]"
            elif val == 2:
                dot_row += "[bold red]───[/]"
        dot_row += "•"  # last dot
        console.print(dot_row)

        # Then: print vertical edges + boxes row (except after last dots row)
        if r < box_size:
            box_row = ""
            for c in range(len(vertical_edges[0])):
                val = vertical_edges[r][c]
                if val == 0:
                    box_row += " "
                elif val == 1:
                    box_row += "[bold blue]│[/]"
                elif val == 2:
                    box_row += "[bold red]│[/]"

                # print box content if within box area
                if c < box_size:
                    b = boxes[r][c]
                    if b == 0:
                        box_row += "   "
                    elif b == 1:
                        box_row += "[on blue] 1 [/]"
                    elif b == 2:
                        box_row += "[on red] 2 [/]"
            # last vertical bar on right side
            box_row += " " if vertical_edges[r][-1] == 0 else (
                "[bold blue]│[/]" if vertical_edges[r][-1] == 1 else "[bold red]│[/]"
            )
            console.print(box_row)
