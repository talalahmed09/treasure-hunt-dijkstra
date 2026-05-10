import turtle
import random
import time
import heapq

# Grid settings
ROWS = 15
COLS = 25
CELL_SIZE = 25
NUM_TREASURES = 6

# Colors
COLOR_EMPTY = "white"
COLOR_WALL = "black"
COLOR_PLAYER = "blue"
COLOR_TREASURE = "gold"
COLOR_CONNECTION = "lime"
COLOR_EXPLORING = "orange"

class TreasureHuntDijkstra:
    def __init__(self):
        # Setup screen
        self.screen = turtle.Screen()
        self.screen.title("Treasure Hunt - Dijkstra Shortest Path")
        self.screen.setup(width=COLS * CELL_SIZE + 100, height=ROWS * CELL_SIZE + 250)
        self.screen.bgcolor("lightgray")
        self.screen.tracer(0)
        
        # Game data
        self.grid = [[0 for _ in range(COLS)] for _ in range(ROWS)]
        self.player = (1, 1)
        self.treasures = []
        self.is_solving = False
        self.paths = []        # store edges
        self.total_cost = 0
        
        # Turtles
        self.drawer = turtle.Turtle()
        self.drawer.hideturtle()
        self.drawer.speed(0)
        
        self.text_turtle = turtle.Turtle()
        self.text_turtle.hideturtle()
        self.text_turtle.speed(0)
        
        # Generate environment
        self.generate_maze()
        self.grid[self.player[0]][self.player[1]] = 2
        self.place_treasures()
        
        self.draw_grid()
        self.draw_instructions()
        
        # Keyboard
        self.screen.onkey(self.solve_dijkstra, "space")
        self.screen.onkey(self.reset, "r")
        self.screen.listen()
        
        self.screen.mainloop()
    
    # -------------------- MAZE + TREASURES --------------------

    def generate_maze(self):
        """Generate random maze walls"""
        for _ in range(60):
            r = random.randint(0, ROWS - 1)
            c = random.randint(0, COLS - 1)
            if (r, c) != self.player:
                self.grid[r][c] = 1

    def place_treasures(self):
        """Place random treasures"""
        self.treasures = []
        while len(self.treasures) < NUM_TREASURES:
            r = random.randint(2, ROWS - 3)
            c = random.randint(2, COLS - 3)
            if self.grid[r][c] == 0 and (r, c) != self.player:
                self.treasures.append((r, c))
                self.grid[r][c] = 3

    # -------------------- DRAWING --------------------

    def draw_cell(self, row, col, color):
        x = col * CELL_SIZE - (COLS * CELL_SIZE) // 2
        y = (ROWS * CELL_SIZE) // 2 - row * CELL_SIZE
        
        self.drawer.penup()
        self.drawer.goto(x, y)
        self.drawer.pendown()
        self.drawer.fillcolor(color)
        self.drawer.begin_fill()
        for _ in range(4):
            self.drawer.forward(CELL_SIZE)
            self.drawer.right(90)
        self.drawer.end_fill()

        # Border
        self.drawer.pencolor("gray")
        self.drawer.penup()
        self.drawer.goto(x, y)
        self.drawer.pendown()
        for _ in range(4):
            self.drawer.forward(CELL_SIZE)
            self.drawer.right(90)

    def draw_connection(self, pos1, pos2, color="lime", width=3):
        r1, c1 = pos1
        r2, c2 = pos2
        
        # convert to screen coords
        x1 = c1 * CELL_SIZE - (COLS * CELL_SIZE) // 2 + CELL_SIZE // 2
        y1 = (ROWS * CELL_SIZE) // 2 - r1 * CELL_SIZE - CELL_SIZE // 2
        x2 = c2 * CELL_SIZE - (COLS * CELL_SIZE) // 2 + CELL_SIZE // 2
        y2 = (ROWS * CELL_SIZE) // 2 - r2 * CELL_SIZE - CELL_SIZE // 2
        
        self.drawer.penup()
        self.drawer.goto(x1, y1)
        self.drawer.pendown()
        self.drawer.pencolor(color)
        self.drawer.pensize(width)
        self.drawer.goto(x2, y2)
        self.drawer.pensize(1)

    def draw_grid(self):
        self.drawer.clear()
        
        for r in range(ROWS):
            for c in range(COLS):
                v = self.grid[r][c]
                if v == 0:
                    color = COLOR_EMPTY
                elif v == 1:
                    color = COLOR_WALL
                elif v == 2:
                    color = COLOR_PLAYER
                elif v == 3:
                    color = COLOR_TREASURE
                else:
                    color = COLOR_EMPTY
                
                self.draw_cell(r, c, color)

        # Draw paths
        for p1, p2 in self.paths:
            self.draw_connection(p1, p2, COLOR_CONNECTION, 3)

        self.screen.update()

    def draw_instructions(self):
        self.text_turtle.clear()

        self.text_turtle.penup()
        self.text_turtle.goto(0, ROWS * CELL_SIZE // 2 + 40)
        self.text_turtle.pencolor("darkblue")
        self.text_turtle.write(
            "Treasure Hunt - Dijkstra Shortest Path",
            align="center",
            font=("Arial", 12, "bold")
        )

        self.text_turtle.goto(0, -ROWS * CELL_SIZE // 2 - 60)
        self.text_turtle.write(
            "SPACE = Find shortest paths | R = New Maze",
            align="center",
            font=("Arial", 11)
        )

        if self.total_cost > 0:
            self.text_turtle.goto(0, -ROWS * CELL_SIZE // 2 - 85)
            self.text_turtle.pencolor("darkgreen")
            self.text_turtle.write(
                f"Total Steps: {self.total_cost}",
                align="center",
                font=("Arial", 11, "bold")
            )

        self.text_turtle.goto(-COLS * CELL_SIZE // 2, -ROWS * CELL_SIZE // 2 - 35)
        self.text_turtle.pencolor("black")
        self.text_turtle.write(
            "🔵 Player  🟡 Treasure  ⬛ Wall  🟢 Path",
            align="left",
            font=("Arial", 9)
        )

    # -------------------- DIJKSTRA --------------------

    def dijkstra(self, start):
        pq = []
        heapq.heappush(pq, (0, start))

        dist = {start: 0}
        parent = {}

        while pq:
            d, (r, c) = heapq.heappop(pq)

            if d > dist[(r, c)]:
                continue

            for dr, dc in [(-1,0),(1,0),(0,-1),(0,1)]:
                nr, nc = r + dr, c + dc
                if not (0 <= nr < ROWS and 0 <= nc < COLS):
                    continue
                if self.grid[nr][nc] == 1:
                    continue

                nd = d + 1

                if (nr, nc) not in dist or nd < dist[(nr, nc)]:
                    dist[(nr, nc)] = nd
                    parent[(nr, nc)] = (r, c)
                    heapq.heappush(pq, (nd, (nr, nc)))

        return dist, parent

    # -------------------- SOLVING (PERFECT) --------------------

    def solve_dijkstra(self):
        if self.is_solving:
            return
        self.is_solving = True

        self.paths = []
        self.total_cost = 0

        # Start from player
        current_pos = self.player
        remaining_treasures = self.treasures.copy()

        while remaining_treasures:

            # Step 1 – Run Dijkstra from current position
            dist, parent = self.dijkstra(current_pos)

            # Step 2 – Find nearest reachable treasure
            reachable = [(t, dist[t]) for t in remaining_treasures if t in dist]
            if not reachable:
                print("Some treasures unreachable!")
                break

            nearest, _ = min(reachable, key=lambda x: x[1])

            # Step 3 – Reconstruct path current → nearest
            path = []
            cur = nearest
            while cur != current_pos:
                path.append(cur)
                cur = parent[cur]
            path.append(current_pos)
            path.reverse()

            # Step 4 – Animate movement & save edges
            for i in range(len(path) - 1):
                self.paths.append((path[i], path[i+1]))
                self.total_cost += 1

                self.draw_grid()
                self.draw_connection(path[i], path[i+1], COLOR_EXPLORING, 5)
                self.screen.update()
                time.sleep(0.2)

                self.draw_grid()
                time.sleep(0.12)

            # Step 5 – Update player position
            current_pos = nearest
            remaining_treasures.remove(nearest)

        # Update final player position
        self.player = current_pos

        self.is_solving = False
        self.draw_instructions()

    # -------------------- RESET --------------------

    def reset(self):
        if self.is_solving:
            return

        self.grid = [[0 for _ in range(COLS)] for _ in range(ROWS)]
        self.paths = []
        self.total_cost = 0
        self.treasures = []

        self.generate_maze()
        self.grid[self.player[0]][self.player[1]] = 2
        self.place_treasures()

        self.draw_grid()
        self.draw_instructions()


# Run the game
if __name__ == "__main__":
    TreasureHuntDijkstra()
