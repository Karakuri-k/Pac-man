import pygame as pg
from constants import *
from board import Board
from pacman import PacMan

pg.init()
board = Board()
vindu = pg.display.set_mode(board.window_size())
clock = pg.time.Clock()


pacman = PacMan(3, 4)

running = True
frames = 0
while running:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False
        elif event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE:
            running = False
        elif event.type == pg.KEYDOWN and event.key == pg.K_w:
            pacman.nextDirection = UP
        elif event.type == pg.KEYDOWN and event.key == pg.K_a:
            pacman.nextDirection = LEFT
        elif event.type == pg.KEYDOWN and event.key == pg.K_s:
            pacman.nextDirection = DOWN
        elif event.type == pg.KEYDOWN and event.key == pg.K_d:
            pacman.nextDirection = RIGHT
        
        

    # Tegn bakgrunn: (En slags "reset" av hele vinduet vårt)
    vindu.fill(BLACK)

    # Tegn brettet først, og pacman og andre ting "oppå":
    board.draw(vindu)

    # TODO: Oppdater objektene våre:
    if frames % 10 == 0:
        pacman.move(board)

    # Tegn objektene våre:
    pacman.draw(vindu)


    # Har alltid disse med til slutt:
    pg.display.flip()
    clock.tick(FPS)
    frames += 1

# While running er slutt: Avslutt pygame på en "ryddig måte":
pg.quit()
