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
    

    def __init__(self, row, col, spriteKolonne, spriteRad, board):
        frame_width = 16

        self.frames_idle = self.getImageSpriteList(spriteKolonne * frame_width, spriteRad * frame_width, 4)
        # Bildet vi skal vise til å starte med er idle:
        self.frames = self.frames_idle
        # Om vi vil ha animasjon som går gjennom frames:
        self.current_frame = 0

        # Om vi vil speile bildet:
        self.venstre = False

        # self.row = row
        # self.col = col
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

    '''def update(self, board):
        self.x += self.dx
        self.y += self.dy

        col = int(self.x // TILE_SIZE)
        row = int(self.y // TILE_SIZE)

        if not board.is_road(row, col):
            retninger = [(-1, 0), (1, 0), (0, -1), (0, 1)]
            retning = r.choice(retninger)
            self.dx *= retning[0]
            self.dy *= retning[1]

        # midt_x = col * TILE_SIZE + TILE_SIZE // 2
        # midt_y = row * TILE_SIZE + TILE_SIZE // 2


        
        if abs(self.x - midt_x) < self.speed and abs(self.y - midt_y) < self.speed:
            self.x = midt_x # Ghost x koord er i midten av rute
            self.y = midt_y # Ghost y koord er i midten av rute

            retninger = [(-1, 0), (1, 0), (0, -1), (0, 1)]
            r.shuffle(retninger) # mikser random opp listen

            for rd, kl in retninger:
                ny_rad = self.row + rd
                ny_kol = self.col + kl
                if board.is_road(ny_rad, ny_kol):
                    self.row = ny_rad
                    self.col = ny_kol

                    # retningsfart
                    self.dx = kl * self.speed
                    self.dy = rd * self.speed
                    break
        '''

    def draw(self, surface):
        # Få bildet fra en liste av bilder (om du vil bruke animasjon/sprites):
        current_frame_image = self.frames[self.current_frame]
        
        # Speiler bildet hvis det trengs:
        if self.venstre:
            current_frame_image = pg.transform.flip(current_frame_image, True, False)

        # Sørg for at vi tegner midt i "Tile":
        rect = current_frame_image.get_rect()
        rect.center = (self.x, self.y)

        # Blit images på skjermen (der self.rect befinner seg):
        surface.blit(current_frame_image, rect)