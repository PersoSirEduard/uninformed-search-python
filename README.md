# Uninformed search using Python
Basic use of uniformed search (depth and breath search first) to solve mazes in python.

## To run the code:
1) Install Python 3
2) Go into the `./src` directory using the command `cd src` on a Windows or Linux terminal.
3) Run `python maze-solver.py <file>` (3 examples are included in the folder)

Note: By default the code uses depth first search, but it can be switched to breath search first by switching the class StackFrontier to QueueFrontier in the solve method part of the Maze class. Furthermore, the solving algorithm can be easily be transformed to an informed search algorithm like the A* search algorithm by including specific heuristic estimations.

Example:
```
> python maze-solver.py maze1.txt
██████████
█     B█ █
█ ██ ███ █
█ ██   █ █
█ ████ █ █
█       A█
██████████

Solved!
██████████
█   **B█ █
█ ██*███ █
█ ██***█ █
█ ████*█ █
█     **A█
██████████
```
