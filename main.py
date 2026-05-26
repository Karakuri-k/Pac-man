import pygame as pg
from constants import *
from board import Board
from pacman import PacMan
from ghost import Ghost

pg.init()
board = Board()
vindu = pg.display.set_mode(board.window_size())
clock = pg.time.Clock()


pacman = PacMan(3, 4)
redGhost = Ghost(5, 4, RED_GHOST_RAD, board)
blueGhost = Ghost(7, 11, BLUE_GHOST_RAD, board)
whiteGhost = Ghost(1, 7, WHITE_GHOST_RAD, board)
greenGhost = Ghost(7, 5, GREEN_GHOST_RAD, board)
ghosts = [redGhost, blueGhost, whiteGhost, greenGhost]

running = True
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
    pacman.checkDirection(board)
    pacman.move(board)
    for ghost in ghosts:
        ghost.update(board)

    # Tegn objektene våre:
    pacman.draw(vindu)
    for ghost in ghosts:
        ghost.draw(vindu)


    # Har alltid disse med til slutt:
    pg.display.flip()
    clock.tick(FPS)

# While running er slutt: Avslutt pygame på en "ryddig måte":
pg.quit()
