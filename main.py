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
startPage = pygame.image.load('./img/startpage.jpg')
start_button_1 = pygame.image.load('./img/start_button_1.gif')
start_button_height = start_button_1.get_height()
del start_button_1
shape = [startPage.get_width(), startPage.get_height()]
DISPLAYSURF = pygame.display.set_mode((shape[0], shape[1]))
play_button_1 = pygame.image.load('./img/button_green.jpg')
play_button_width = play_button_1.get_width()
del play_button_1
start_button = DynamicButton('./img/start_button_1.gif', './img/start_button_2.gif',
                             (50, shape[1]-start_button_height-50))
play_button = DynamicButton('./img/button_green.jpg', './img/button_yellow.jpg', (shape[0]-play_button_width-50, 50))

'''
cat_head = pygame.image.load('./img/tom_head.gif').convert_alpha()
mouse_head = pygame.image.load('./img/jerry_head.gif').convert_alpha()
grass_block = pygame.image.load('./img/map_block_grass.gif').convert_alpha()
stone_block = pygame.image.load('./img/map_block_stone.gif').convert_alpha()
grass_block = pygame.transform.scale(grass_block, (cat_head.get_width(), cat_head.get_height()))
stone_block = pygame.transform.scale(stone_block, (cat_head.get_width(), cat_head.get_height()))

block_lt_pos = [50, 50]
block_shape = [grass_block.get_width(), grass_block.get_height()]
'''

m = 9
n = 8
cat_init = [1, 3]
mouse_init = [5, 2]
puzzle_map = PuzzleMap(m, n, cat_init, mouse_init)

agent = Agent(puzzle_map)


DISPLAYSURF.blit(startPage, (0, 0))
# run the game loop
while True:
    print('state: ', STATE[state])
    # event = pygame.event.poll()
    if state == STATE_WELCOME:
        DISPLAYSURF.blit(startPage, (0, 0))
        # mouse_pos = pygame.mouse.get_pos()
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
                    state = STATE_START
    elif state == STATE_START:
        puzzle_map.display('./img/tom_head.gif', './img/jerry_head.gif', './img/map_block_grass.gif',
                           './img/map_block_stone.gif', DISPLAYSURF)
        # mouse_pos = pygame.mouse.get_pos()
        play_button.display(DISPLAYSURF)

        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.mixer.music.stop()
                pygame.quit()
                sys.exit()
            elif event.type == MOUSEBUTTONDOWN:
                if play_button.mouse_on_button():
                    # DISPLAYSURF.fill(WHITE)
                    # pygame.display.flip()
                    state = STATE_SOLVE
                    break
    elif state == STATE_GENERATED:
        pass
    elif state == STATE_SOLVE:
        agent.solver(DISPLAYSURF, puzzle_map.block_lt_pos, puzzle_map.block_shape)
        pass
    elif state == STATE_WIN:
        pass
    else:
        pass
    # only draw display surface(which is declared by pygame.display.set_mode()) onto screen
    # if you want to draw another surface onto screen, use blit
    pygame.display.update()
    fpsClock.tick(FPS)
