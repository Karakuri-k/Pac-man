from pathlib import Path
import pygame as pg
from constants import *
from board import Board

class PacMan:
    IMAGE_FILE = Path(__file__).parent / "sprites" / "pacman2.png"

    def getImageSpriteList(self, x_start, y_start, num_frames) -> list[pg.Surface]:
        full_image = pg.image.load(self.IMAGE_FILE)
        frame_width = 16
        
        # Dele opp bildet i frames, som lagres i en liste:
        frames = []
        for i in range(num_frames):
            # Bildene er kvadratiske - bruker frame widht både som høye og bredde:
            frame = full_image.subsurface(pg.Rect(x_start + i * frame_width, y_start, frame_width, frame_width))
            frames.append(frame)
        return frames
    

    def __init__(self, col, row):
        self.pos = [col * TILE_SIZE, row * TILE_SIZE]

        self.frames_idle = self.getImageSpriteList(0, 0, 4)
        # Bildet vi skal vise til å starte med er idle:
        self.frames = self.frames_idle
        # Om vi vil ha animasjon som går gjennom frames:
        self.current_frame = 0

        # Om vi vil speile bildet:
        self.venstre = False
        self.currentDirection : None|tuple = None
        self.nextDirection : None|tuple = None
        self.speed = 2


    def is_at_tile_center(self):
        return (self.pos[0] % TILE_SIZE == 0 and 
                self.pos[1] % TILE_SIZE == 0)

    def get_tile_pos(self):
        return (self.pos[1] // TILE_SIZE, self.pos[0] // TILE_SIZE)

    def checkDirection(self, board):
        if not self.nextDirection:
            return

        if self.currentDirection is None or self.is_at_tile_center():
            row, col = self.get_tile_pos()
            next_row = row + self.nextDirection[0]
            next_col = col + self.nextDirection[1]
            if board.is_road(next_row, next_col):
                self.currentDirection = self.nextDirection
                self.nextDirection = None

    def move(self, board: Board):
        if self.currentDirection:
            next_x = self.pos[0] + self.currentDirection[1] * self.speed
            next_y = self.pos[1] + self.currentDirection[0] * self.speed

            left = next_x
            right = next_x + TILE_SIZE - 1
            top = next_y
            bottom = next_y + TILE_SIZE - 1
            
            left_tile = left // TILE_SIZE
            right_tile = right // TILE_SIZE
            top_tile = top // TILE_SIZE
            bottom_tile = bottom // TILE_SIZE
            
            can_move = True
            for row in range(top_tile, bottom_tile + 1):
                for col in range(left_tile, right_tile + 1):
                    if not board.is_road(row, col):
                        can_move = False
                        break
                if not can_move:
                    break
            
            if can_move:
                self.pos[0] = next_x
                self.pos[1] = next_y

    def draw(self, surface):

        # Få bildet fra en liste av bilder (om du vil bruke animasjon/sprites):
        current_frame_image = self.frames[self.current_frame]
        
        # Speiler bildet hvis det trengs:
        if self.venstre:
            current_frame_image = pg.transform.flip(current_frame_image, True, False)

        rect = current_frame_image.get_rect()
        rect.center = (self.pos[0] + TILE_SIZE // 2, self.pos[1] + TILE_SIZE // 2)

        # Blit images på skjermen (der self.rect befinner seg):
        surface.blit(current_frame_image, rect)

