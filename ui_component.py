import sys
import pygame
from pygame.locals import *
from color_map import *


class DynamicButton(object):
    def __init__(self, button_fn_1, button_fn_2, position):
        self.button_1 = pygame.image.load(button_fn_1).convert_alpha()
        self.button_2 = pygame.image.load(button_fn_2).convert_alpha()
        self.position = position
        self.shape = [self.button_1.get_width(), self.button_1.get_height()]
        print('button range: ')
        print(position[0], position[0]+self.shape[0])
        print(position[1], position[1]+self.shape[1])
        return

    def mouse_on_button(self):
        mouse_pos = pygame.mouse.get_pos()

        if mouse_pos[0] <= self.position[0] or mouse_pos[0] >= self.position[0] + self.shape[0]:
            return False
        elif mouse_pos[1] <= self.position[1] or mouse_pos[1] >= self.position[1] + self.shape[1]:
            return False
        return True

    def display(self, screen):
        pygame.draw.rect(screen, WHITE, (*self.position, *self.shape))
        if self.mouse_on_button() is True:
            screen.blit(self.button_2, self.position)
        else:
            screen.blit(self.button_1, self.position)
        pygame.display.update()
        return
