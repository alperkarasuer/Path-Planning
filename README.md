# Path-Planning
Simple program to find the shortest path between two points. Currently it uses A* Algorithm to search and find the shortest path (might add others later).
After running "main.py" script press "S" to specify the cell which the cursor is located as start cell,
similarly press "E" in the same manner to determine end cell.
If start or end cells are not specified, they are set to be the upper left and lower right corners respectively.

Clicking on the cells alternates them between "Wall" and "Free". When pressed "R" the script randomly generates wall and free cells.
However, randomizing the walls doesn't guarantee the existence of a path between start and end cells.

Press "Enter" to run the visualisation after generating the maze of walls.
