import sys
import pygame
from pygame.locals import *


class DynamicButton(object):
    def __init__(self, button_fn_1, button_fn_2, position):
        self.button_1 = pygame.image.load(button_fn_1).convert_alpha()
        self.button_2 = pygame.image.load(button_fn_2).convert_alpha()
        self.position = position
        print('button range: ')
        print(position[0], position[0]+self.button_1.get_width())
        print(position[1], position[1]+self.button_1.get_height())
        return

    def mouse_on_button(self, mouse_pos):
        width = self.button_1.get_width()
        height = self.button_1.get_height()

        if mouse_pos[0] <= self.position[0] or mouse_pos[0] >= self.position[0] + width:
            return False
        elif mouse_pos[1] <= self.position[1] or mouse_pos[1] >= self.position[1] + height:
            return False
        return True

    def display(self, mouse_pos, screen):
        if self.mouse_on_button(mouse_pos) is True:
            screen.blit(self.button_2, self.position)
        else:
            screen.blit(self.button_1, self.position)
        return self.position, [self.button_1.get_width(), self.button_1.get_height()]
