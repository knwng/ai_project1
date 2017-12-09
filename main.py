import pygame
import sys
from pygame.locals import *
import pygame.mixer
from ui_component import *
from search import *
import time

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)

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
width = startPage.get_width()
height = startPage.get_height()
DISPLAYSURF = pygame.display.set_mode((width, height))
play_button_1 = pygame.image.load('./img/button_green.jpg')
play_button_width = play_button_1.get_width()
del play_button_1
start_button = DynamicButton('./img/start_button_1.gif', './img/start_button_2.gif', (50, height-start_button_height-50))
play_botton = DynamicButton('./img/button_green.jpg', './img/button_yellow.jpg', (width-play_button_width-50, 50))

cat_head = pygame.image.load('./img/tom_head.gif').convert_alpha()
mouse_head = pygame.image.load('./img/jerry_head.gif').convert_alpha()
grass_block = pygame.image.load('./img/map_block_grass.gif').convert_alpha()
stone_block = pygame.image.load('./img/map_block_stone.gif').convert_alpha()
grass_block = pygame.transform.scale(grass_block, (cat_head.get_width(), cat_head.get_height()))
stone_block = pygame.transform.scale(stone_block, (cat_head.get_width(), cat_head.get_height()))

block_lt_pos = [50, 50]
block_width = grass_block.get_width()
block_height = grass_block.get_height()

m = 9
n = 8
cat_init = [1, 3]
mouse_init = [5, 2]
puzzle_map = PuzzleMap(m, n, cat_init, mouse_init)


DISPLAYSURF.blit(startPage, (0, 0))
# run the game loop
while True:
    print('state: ', STATE[state])
    # event = pygame.event.poll()
    if state == STATE_WELCOME:
        DISPLAYSURF.blit(startPage, (0, 0))
        mouse_pos = pygame.mouse.get_pos()
        start_button.display(mouse_pos, DISPLAYSURF)
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.mixer.music.stop()
                pygame.quit()
                sys.exit()
            elif event.type == MOUSEBUTTONDOWN:
                if start_button.mouse_on_button(mouse_pos):
                    DISPLAYSURF.fill(WHITE)
                    pygame.display.flip()
                    state = STATE_START
    elif state == STATE_START:
        mouse_pos = pygame.mouse.get_pos()
        for i in range(m):
            for j in range(n):
                DISPLAYSURF.blit(grass_block, (block_lt_pos[0]+i*block_width, block_lt_pos[1]+j*block_height))
        for i in puzzle_map.obstacle:
            lt_x = block_lt_pos[0]+i[0]*block_width
            lt_y = block_lt_pos[1]+i[1]*block_height
            DISPLAYSURF.blit(stone_block, (lt_x, lt_y))
        DISPLAYSURF.blit(cat_head, (block_lt_pos[0]+block_width*cat_init[0], block_lt_pos[1]+block_height*cat_init[1]))
        DISPLAYSURF.blit(mouse_head, (block_lt_pos[0]+block_width*mouse_init[0], block_lt_pos[1]+block_height*mouse_init[1]))
        play_botton.display(mouse_pos, DISPLAYSURF)


        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.mixer.music.stop()
                pygame.quit()
                sys.exit()
            elif event.type == MOUSEBUTTONDOWN:
                if play_botton.display(mouse_pos, DISPLAYSURF):
                    # DISPLAYSURF.fill(WHITE)
                    # pygame.display.flip()
                    state = STATE_SOLVE
    elif state == STATE_GENERATED:
        pass
    elif state == STATE_SOLVE:

        pass
    elif state == STATE_WIN:
        pass
    else:
        pass
    # only draw display surface(which is declared by pygame.display.set_mode()) onto screen
    # if you want to draw another surface onto screen, use blit
    pygame.display.update()
    fpsClock.tick(FPS)
