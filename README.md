# A* Pathfinding
A* pathfinding algorithm implemented and visualized with python

Node: anything in a graph that is visitable

Edge: lines that connect nodes

Weighted Edge: certain length, lowest is shortest/least cost

Informed Search Algorithm: only paths that are optimal are explored, based on a heuristic, as opposed to exporing all paths

## Pseudocode:

Given a graph:
(A) <-> (C) <-> (D) <-> (B)

     1   |   2       1

         | 3

        (B)

Open = {(0, A)} begins with starting node (F(n), node_id)

F(n) = G(n) + H(n)

H(n) gives the estimated distance to the node end from n

G(n) gives the current shortest distance to the start node from n

F(n) is the sum

| Node | F | G | H | Last |
|------|---|---|---|------|
| A    | 0  | 0  | 0  |      |
| B    |  inf | inf  | inf  |      |
| C    | inf  | inf  | inf  |      |
| D    |  inf |  inf | inf  |      |

Pull current node from Open set and examine edges from that node

Open = {}

A<->C
  1

For each path, compare that edge's weight to the current weight (in this case, infinity to begin)

For path with weight of 1, we update G to 1, and take a guess for H (in this case, guess of 1)

F is now updated to G + H = 2

Last is updated to tell us previous location

| Node | F | G | H | Last |
|------|---|---|---|------|
| A    | 0  | 0  | 0  |      |
| B    |  inf | inf  | inf  |      |
| C    | 2  | 1  | 1  |   A   |
| D    |  inf |  inf | inf  |      |

New explored node pushed into Open set

Open = {(2, C)}

Repeat for next item in Open set

Open = {}

C<->B
  3

Add paths from A to B, G = 1 + 3 = 4

Compare to current G (infinity to begin), and guess for H (in this case, guess of 2)

F = H + G = 6

| Node | F | G | H | Last |
|------|---|---|---|------|
| A    | 0  | 0  | 0  |      |
| B    |  6 | 4  | 2  |      |
| C    | 2  | 1  | 1  |   A   |
| D    |  inf |  inf | inf  |      |

Open = {(6, B)}

C node still has a path to explore, so repeat for second path before exploring next node in Open set

C<->D
  2

Add paths from A to D, G = 1 + 2 = 3

Compare to current G (infinity to begin), and guess for H (in this case, guess of 0, due to D being the end node)

F = H + G = 3

| Node | F | G | H | Last |
|------|---|---|---|------|
| A    | 0  | 0  | 0  |   -   |
| B    | 6 | 4  | 2  |   C   |
| C    | 2  | 1  | 1  |   A   |
| D    | 3 |  3 | 0  |   C   |

Open = {(6, B), (3, D)}

Find the lowest F score in the Open set, remove and examine

Open = {(6, B)}

End node is removed from the set, path is now known, ending algorithm

To find the path, backtrack knowing D came from C, C came from A