import pygame
import sys
from pygame.locals import *
import pygame.mixer
import time
from ui_component import *
from search import *
from config import *
from pgu import gui

pygame.init()
# app = gui.App()
desktop = gui.Desktop(theme=gui.Theme('default'))

FPS = 30  # frames per second setting
fpsClock = pygame.time.Clock()

state = STATE_WELCOME

pygame.display.set_caption('Tom and Jerry')
startPage = pygame.image.load(startpage_fn)
winpage = pygame.image.load(catchpage_fn)
shape = [startPage.get_width(), startPage.get_height()]
DISPLAYSURF = pygame.display.set_mode((shape[0], shape[1]), SRCALPHA, 32)

start_button_1 = pygame.image.load(start_button_fn[0])
start_button_shape = [start_button_1.get_width(), start_button_1.get_height()]
del start_button_1
start_button = DynamicButton(start_button_fn[0], start_button_fn[1],
                             (50, shape[1]-start_button_shape[0]-50))

generate_button_1 = pygame.image.load(generate_button_fn[0])
generate_button_shape = [generate_button_1.get_width(), generate_button_1.get_height()]
del generate_button_1
generate_button = DynamicButton(generate_button_fn[0], generate_button_fn[1], (shape[0]-generate_button_shape[0]-50, 50))

play_button_1 = pygame.image.load(play_button_fn[0])
play_button_shape = [play_button_1.get_width(), play_button_1.get_height()]
del play_button_1
play_button = DynamicButton(play_button_fn[0], play_button_fn[1], (shape[0]-play_button_shape[0]-50, 50+generate_button_shape[1]))

restart_button_1 = pygame.image.load(restart_button_fn[0])
restart_button_shape = [restart_button_1.get_width(), restart_button_1.get_height()]
del restart_button_1
restart_button = DynamicButton(restart_button_fn[0], restart_button_fn[1], (50, 50))


lo = gui.Container()

table = gui.Table()
table.tr()
table.td(gui.Label("PARAMETERS"), colspan=4)

table.tr()
table.td(gui.Label(" "))
table.tr()
table.td(gui.Label("SHAPE"))
slider_shape = gui.HSlider(value=16, min=5, max=40, size=20, width=120, height=20)
table.td(slider_shape, colspan=3)


table.tr()
table.td(gui.Label(" "))
table.tr()
table.td(gui.Label("OBSTACLE"))
slider_level = gui.HSlider(value=5, min=1, max=9, size=20, width=120, height=20)
table.td(slider_level, colspan=3)


lo.add(table, shape[0]-120-300, start_button_shape[1]+50)
desktop.init(lo)

m = 30
n = 30

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
                    state = STATE_GENERATE
    elif state == STATE_GENERATE:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.mixer.music.stop()
                pygame.quit()
                sys.exit()
            elif event.type == MOUSEBUTTONDOWN:
                if generate_button.mouse_on_button():
                    DISPLAYSURF.fill(WHITE)
                    pygame.display.flip()
                    puzzle_map = PuzzleMap(slider_shape.value, slider_shape.value, 'square', slider_level.value)
                    puzzle_map.map_generator()
                    agent = Agent(puzzle_map)
                    state = STATE_START
                    break
            desktop.event(event)
        lo.paint(DISPLAYSURF)
        # puzzle_map.display(DISPLAYSURF)
        generate_button.display(DISPLAYSURF)

        pass
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
                elif generate_button.mouse_on_button():
                    DISPLAYSURF.fill(WHITE)
                    pygame.display.flip()
                    del puzzle_map
                    puzzle_map = PuzzleMap(slider_shape.value, slider_shape.value, 'square', slider_level.value)
                    puzzle_map.map_generator()
            desktop.event(event)
        lo.paint(DISPLAYSURF)
        puzzle_map.display(DISPLAYSURF)
        generate_button.display(DISPLAYSURF)
        play_button.display(DISPLAYSURF)
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
                    state = STATE_GENERATE
                    break
    else:
        pass
    pygame.display.update()
    fpsClock.tick(FPS)
