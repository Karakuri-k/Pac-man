import pygame as pg
from constants import *

class Board:
    def __init__(self):
        grid_strings = [
            "#################",
            "#...##.....##...#",
            "#.#.###.###.#.#.#",
            "#.#...........#.#",
            "#.#.###.#.###.#.#",
            "#.....#...#.....#",
            "###.#.#####.#.###",
            "#...............#",
            "###.#.#####.#.###",
            "#.....#...#.....#",
            "#.#.###.#.###.#.#",
            "#.#...........#.#",
            "#.#.###.###.#.#.#",
            "#...##.....##...#",
            "#################",
        ]
        self.grid = [list(row) for row in grid_strings]
        self.rows = len(self.grid)
        self.cols = len(self.grid[0])

    def window_size(self):
        return self.cols*TILE_SIZE, self.rows*TILE_SIZE

    def draw(self, surface):
        """Tegn brettet på den gitte pygame-flaten."""
        for y, row in enumerate(self.grid):
            for x, tile in enumerate(row):
                rect = pg.Rect(x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE, TILE_SIZE)
                if tile == '#':
                    pg.draw.rect(surface, DARK_BLUE, rect, border_radius=5)
                if tile == '.':
                    center = (x * TILE_SIZE + TILE_SIZE // 2, y * TILE_SIZE + TILE_SIZE // 2)
                    radius = TILE_SIZE // 6.5
                    pg.draw.circle(surface, YELLOW, center, radius)


    def is_road(self, row: int, col: int) -> bool:
        """Returnerer True hvis posisjonen er fri for vegg."""
        if row < 0 or row >= self.rows or col < 0 or col >= self.cols:
            return False
        return self.grid[row][col] != '#'
    
    def visit(self, col, row):
        if self.grid[row][col] == ".":
            self.grid[row][col] = " "