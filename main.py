import pygame
import sys
from pygame.locals import *
import pygame.mixer
from ui_component import *
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
start_button = DynamicButton('./img/start_button_1.gif', './img/start_button_2.gif', (50, height-start_button_height-50))

DISPLAYSURF.blit(startPage, (0, 0))
# run the game loop
while True:
    print('state: ', STATE[state])
    # event = pygame.event.poll()
    if state == STATE_WELCOME:
        DISPLAYSURF.blit(startPage, (0, 0))
        mouse_pos = pygame.mouse.get_pos()
        lt_pos, bt_shape = start_button.display(mouse_pos, DISPLAYSURF)
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.mixer.music.stop()
                pygame.quit()
                sys.exit()
            elif event.type == MOUSEMOTION:
                mouse_pos = pygame.mouse.get_pos()
                print('mouse position: ', mouse_pos)
                # pygame.draw.rect(DISPLAYSURF, RED, (*lt_pos, *bt_shape))
            elif event.type == MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                if start_button.mouse_on_button(mouse_pos):
                    state = STATE_START
                    continue
    elif state == STATE_START:
        pass
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
