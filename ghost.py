from pathlib import Path
import pygame as pg
from constants import *
import random as r

class Ghost:
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
    

    def __init__(self, row, col, spriteRad, board):
        frame_width = 16

        self.frames_right = self.getImageSpriteList(0 * frame_width, spriteRad * frame_width, 2) # Høyre
        self.frames_left = self.getImageSpriteList(2 * frame_width, spriteRad * frame_width, 2) # Venstre

        self.frames_up = self.getImageSpriteList(4 * frame_width, spriteRad * frame_width, 2) # Opp
        self.frames_down = self.getImageSpriteList(6 * frame_width, spriteRad * frame_width, 2) # Ned

        self.frames = self.frames_right
        self.current_frame = 0
        self.animation_timer = 0

        self.x = col * TILE_SIZE + TILE_SIZE // 2
        self.y = row * TILE_SIZE + TILE_SIZE // 2
        self.speed = 1.5

        retninger = [(-1, 0), (1, 0), (0, -1), (0, 1)]
        r.shuffle(retninger)
        for rd, kl in retninger:
            if board.is_road(row + rd, col + kl):
                self.dx = kl * self.speed
                self.dy = rd * self.speed
                break


    def update(self, board):
        self.x += self.dx
        self.y += self.dy

        # Endrer retning på spøkelse (animasjon)
        if self.dx > 0:
            self.frames = self.frames_right
        elif self.dx < 0:
            self.frames = self.frames_left
        elif self.dy > 0:
            self.frames = self.frames_down
        elif self.dy < 0:
            self.frames = self.frames_up

        # Endrer spøkelse detalj (animasjon)
        self.animation_timer += 1
        if self.animation_timer >= 10: # per 10ende frame
            self.animation_timer = 0
            self.current_frame = (self.current_frame + 1) % len(self.frames)

        col = int(self.x // TILE_SIZE)
        row = int(self.y // TILE_SIZE)

        midt_x = col * TILE_SIZE + TILE_SIZE // 2
        midt_y = row * TILE_SIZE + TILE_SIZE // 2
        
        if abs(self.x - midt_x) < self.speed and abs(self.y - midt_y) < self.speed:
            self.x = midt_x
            self.y = midt_y

            # sjekker neste pos
            neste_rad = row + int(self.dy / self.speed)
            neste_kol = col + int(self.dx / self.speed)

            if board.is_road(neste_rad, neste_kol):
                pass 
            else:
                # vegg, skift retning
                retninger = [(-1, 0), (1, 0), (0, -1), (0, 1)]
                r.shuffle(retninger)
                for rd, kl in retninger:
                    if board.is_road(row + rd, col + kl):
                        self.dx = kl * self.speed
                        self.dy = rd * self.speed
                        break
                    

    def draw(self, surface):
        # Få bildet fra en liste av bilder (om du vil bruke animasjon/sprites):
        current_frame_image = self.frames[self.current_frame]

        # Sørg for at vi tegner midt i "Tile":
        rect = current_frame_image.get_rect()
        rect.center = (self.x, self.y)

        # Blit images på skjermen (der self.rect befinner seg):
        surface.blit(current_frame_image, rect)