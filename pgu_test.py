import pygame
from pgu import gui
from pygame.locals import *
import sys

pygame.init()
app = gui.App()
DISPLAYSURF = pygame.display.set_mode((500, 500))

lo = gui.Container(width=200)
lo.resize(200, 200)
e = gui.Button("Hello World")


s = gui.Select()
s.add("Goat",'goat')
s.add("Horse",'horse')
s.add("Dog",'dog')
s.add("Pig",'pig')


lo.add(e, 50, 50)
lo.add(s, 100, 100)
app.init(lo, DISPLAYSURF, (100, 100, 300, 300))


while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        app.event(event)
    print s.value
    DISPLAYSURF.fill((255, 255, 255))
    app.paint(DISPLAYSURF)
    pygame.display.flip()
