4x4 DOTS == 3x3 BOXES

```
o   o   o   o

o   o   o   o

o   o   o   o

o   o   o   o
```


Horizontal edges    = 3*4 = 12
Vertical edges      = 4*3 = 12

Boxes = 3*3 = 9


Game State must keep track of:
-   Which edges have been drawn (& by whom)
-   Whose turn it is
-   Which boxes have formed


For box completion detection, for each move:
-   find which boxes the move touches
-   check if the four sides of the boxes are filled
-   if yes, mark that box by the turn

For box completion, if move is horizontal:
    ```
    # if 0, 0 -> box=0,0
    # if 0, 1 -> box=0,1
    # if 0, 2 -> box=0,2

    # if 1, 0 -> box=0,0 or 1,0
    # if 1, 1 -> box=0,1 or 1,1
    # if 1, 2 -> box=0,2 or 1,2

    # if 2, 0 -> box=1,0 or 2,0
    # if 2, 1 -> box=1,1 or 2,1
    # if 2, 2 -> box=1,2 or 2,2

    # if 3, 0 -> box=2,0
    # if 3, 1 -> box=2,1
    # if 3, 2 -> box=2,2
    ```

    If move is vertical:

    ```
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
    ```


to check if a box is complete, check for these coordinates:
```
# if box = 0, 0 --> ("H" -> (0, 0), (1, 0)), ("V" -> (0, 0), (0, 1))
# if box = 0, 1 --> ("H" -> (0, 1), (1, 1)), ("V" -> (0, 1), (0, 2))
# if box = 0, 2 --> ("H" -> (0, 2), (1, 2)), ("V" -> (0, 2), (0, 3))

# if box = 1, 0 --> ("H" -> (1, 0), (2, 0)), ("V" -> (1, 0), (1, 1))
# if box = 1, 1 --> ("H" -> (1, 1), (2, 1)), ("V" -> (1, 1), (1, 2))
# if box = 1, 2 --> ("H" -> (1, 2), (2, 2)), ("V" -> (1, 2), (1, 3))

# if box = 2, 0 --> ("H" -> (2, 0), (3, 0)), ("V" -> (2, 0), (2, 1))
# if box = 2, 1 --> ("H" -> (2, 1), (3, 1)), ("V" -> (2, 1), (2, 2))
# if box = 2, 2 --> ("H" -> (2, 2), (3, 2)), ("V" -> (2, 2), (2, 3))
```
