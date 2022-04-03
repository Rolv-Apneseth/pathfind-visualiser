# pathfind-visualiser

![pathfind-visualiser](https://user-images.githubusercontent.com/69486699/161395210-d3d26e3b-7921-4e86-9b2d-54b6478688bd.png)

## Description

Pathfinding algorigthms written in Python and visualised with the [Pygame](https://pypi.org/project/pygame/) library. Also has a couple built-in maze generation algorithms, and gives the user the ability to create their own mazes by hand, so that algorithms can be observed under a variety of different circumstances.

## Installation

1. Requires python 3.6+ to run. Python can be installed from [here](https://www.python.org/downloads/)
2. To download, click on 'Code' to the top right, then download as a zip file. You can unzip using your preferred program.
   - You can also clone the repository using: `git clone https://github.com/Rolv-Apneseth/pathfind-visualiser.git`
3. Install the requirements for the program.
   - In your terminal, navigate to the cloned directory and run: `python3 -m pip install -r requirements.txt`
4. To run the actual program, navigate further into the pathfind-visualiser folder and run: `python3 main.py`

## Usage

1. From the main menu, read the instructions and keys sections to familiarise yourself with how to use the interface
2. In the options section select the number of rows/columns you want and select a maze type (or leave it on none)
   - Note: Random is it's own maze generating algorithm (defined below)
3. Click on the algorithm you wish to visualise and the maze should appear
4. If you wish to view another algorithm (or take another look at the instructions), press the `Esc` key to return to the main menu

## The Algorithms:

#### 1. [A\* Search Algorithm](https://en.wikipedia.org/wiki/A*_search_algorithm)

- Uses a heuristic function (manhattan distance) to guide the pathfinding algorithm via the use of a priority queue
- This makes it one of the faster algorithm, but note that this is because you need to know the position of the end point for the heuristic function
- Nodes are expanded in the direction of the end node
- The shortest path is always guaranteed

#### 2. [Breadth-First Search](https://en.wikipedia.org/wiki/Breadth-first_search)

- Uses a simple FIFO queue so nodes are expanded in every direction equally (searches in a circle outwards from the starting node if maze is empty)
- The shortest path is always guaranteed

#### 3. [Depth-First Search](https://en.wikipedia.org/wiki/Depth-first_search)

- Uses a LIFO queue, where nodes are added in order of direction (top, right, bottom then left) from expanded nodes
- This means that nodes will always be expanded leftwards until there is a barrier, then down, etc.
- Therefore, this is a very inefficient algorithm but it is used because it is the way a human might navigate a maze (left-hand rule)
- Does not guarantee the shortest path. In fact, in an open maze this could take very long to finish even if the end node is directly beside the start

#### 4. [Dijkstra's Shortest Path First](https://en.wikipedia.org/wiki/Dijkstra%27s_algorithm)

- Nodes will be expanded very similarly to breadth-first search, but it is designed to be able to handle paths of different weights
- The main difference is the use of a priority queue
- Unfortunately this visualiser only uses weights of 1 between each adjacent node so the changes are not visualisable, but feel free to check out the code in algorithms.py (they're different, I promise!)
- This always guarantees the shortest possible path

#### 5. [Greedy Best-First Search](http://web.pdx.edu/~arhodes/ai6.pdf)

- Uses the manhattan distance heuristic function like the a\* algorithm
- However, it does not take into account the distance already travelled and just expands the node with the shortest estimated distance next (hence greedy)
- Does not guarantee the shortest path but it often does find the shortest path

## The Maze Types:

- **Random** - All nodes have a 25% chance of becoming a barrier node
- **Swirl** - Basic swirl pattern which takes up the entire grid
- **Imperfect** - My first attempt at a proper maze generating algorithm. Called imperfect because very small sections of the maze may be sectioned off from the rest of the maze
- **Simple** - Based off of recursive division but slightly different
