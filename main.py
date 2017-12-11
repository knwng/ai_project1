import pygame
import sys
from pygame.locals import *
import pygame.mixer
import time
from ui_component import *
from search import *
from color_map import *


pygame.init()

FPS = 30  # frames per second setting
fpsClock = pygame.time.Clock()

STATE_WELCOME = 0
STATE_START = 1
STATE_GENERATED = 2
STATE_SOLVE = 3
STATE_WIN = 4
STATE = ('WELCOME', 'START', 'GENERATED', 'SOLVE', 'WIN')

state = STATE_WELCOME

pygame.display.set_caption('Tom and Jerry')
startPage = pygame.image.load(startpage_fn)
winpage = pygame.image.load(catchpage_fn)
shape = [startPage.get_width(), startPage.get_height()]
DISPLAYSURF = pygame.display.set_mode((shape[0], shape[1]), SRCALPHA, 32)

start_button_1 = pygame.image.load(start_button_fn[0])
start_button_height = start_button_1.get_height()
del start_button_1
start_button = DynamicButton(start_button_fn[0], start_button_fn[1],
                             (50, shape[1]-start_button_height-50))

play_button_1 = pygame.image.load(play_button_fn[0])
play_button_width = play_button_1.get_width()
del play_button_1
play_button = DynamicButton(play_button_fn[0], play_button_fn[1], (shape[0]-play_button_width-50, 50))

restart_button_1 = pygame.image.load(restart_button_fn[0])
restart_button_width = restart_button_1.get_width()
restart_button_height = restart_button_1.get_height()
del restart_button_1
# restart_button = DynamicButton(restart_button_fn[0], restart_button_fn[1], (shape[0]-restart_button_width-50,
#                                                                             shape[1]-restart_button_height-50))
restart_button = DynamicButton(restart_button_fn[0], restart_button_fn[1], (50, 50))


m = 30
n = 30

DISPLAYSURF.blit(startPage, (0, 0))
# run the game loop
while True:
    if state == STATE_WELCOME:
        DISPLAYSURF.blit(startPage, (0, 0))
        start_button.display(DISPLAYSURF)
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.mixer.music.stop()
                pygame.quit()
                sys.exit()
            elif event.type == MOUSEBUTTONDOWN:
                if start_button.mouse_on_button():
                    DISPLAYSURF.fill(WHITE)
                    pygame.display.flip()
                    puzzle_map = PuzzleMap(m, n, 'square', 4)
                    puzzle_map.map_generator()
                    state = STATE_START
    elif state == STATE_START:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.mixer.music.stop()
                pygame.quit()
                sys.exit()
            elif event.type == MOUSEBUTTONDOWN:
                if play_button.mouse_on_button():
                    DISPLAYSURF.fill(WHITE)
                    pygame.display.flip()
                    agent = Agent(puzzle_map)
                    state = STATE_SOLVE
                    break
        puzzle_map.display(DISPLAYSURF)
        play_button.display(DISPLAYSURF)
    elif state == STATE_GENERATED:
        pass
    elif state == STATE_SOLVE:
        agent.solver(DISPLAYSURF, puzzle_map.block_lt_pos, puzzle_map.block_shape)
        state = STATE_WIN
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.mixer.music.stop()
                pygame.quit()
                sys.exit()

    elif state == STATE_WIN:
        DISPLAYSURF.fill(WHITE)
        DISPLAYSURF.blit(winpage, (50, 50))
        restart_button.display(DISPLAYSURF)
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.mixer.music.stop()
                pygame.quit()
                sys.exit()
            elif event.type == MOUSEBUTTONDOWN:
                if restart_button.mouse_on_button():
                    DISPLAYSURF.fill(WHITE)
                    pygame.display.flip()
                    puzzle_map.map_generator()
                    state = STATE_START
                    break
    else:
        pass
    pygame.display.update()
    fpsClock.tick(FPS)
