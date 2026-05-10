# Treasure Hunt — Multi-Target Pathfinding (Python)

A visual pathfinding game that uses Dijkstra's algorithm to collect multiple treasures on a grid in the shortest possible order.

## What it does
- Generates a random maze grid with walls and treasure locations
- Uses Dijkstra's algorithm to find the shortest path from the player to each treasure
- Applies a greedy nearest-neighbor strategy to decide which treasure to collect next
- Animates the exploration and path in real time using Python Turtle graphics
- Tracks and displays total steps taken

## Controls
| Key | Action |
|-----|--------|
| SPACE | Find and collect all treasures |
| R | Generate a new random maze |

## Algorithms Used
- **Dijkstra's Shortest Path** — finds optimal path between two points on a weighted grid
- **Greedy Nearest Neighbor** — at each step, picks the closest reachable treasure
- **Priority Queue (heapq)** — efficiently selects the next node with minimum distance

## Technologies Used
- Python 3
- `heapq` — min-heap priority queue
- `turtle` — real-time grid visualization

## How to Run

```bash
python treasurehunt.py
```

> Requires Python with Turtle graphics (included in standard Python installation)

## Project Structure
```
treasure_hunt/
├── treasurehunt.py    # full source code
└── README.md
```
# treasure-hunt-dijkstra
