import pygame
import sys
from pygame.locals import *
import pygame.mixer
import time

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)

pygame.init()

FPS = 30 # frames per second setting
fpsClock = pygame.time.Clock()


DISPLAYSURF = pygame.display.set_mode((600, 500))
pygame.display.set_caption('Cat Animation')
myfront = pygame.font.Font(None, 60)
textSurfaceObj = myfront.render("Hello Pygame", True, RED, BLUE)
textRectObj = textSurfaceObj.get_rect()
textRectObj.center = (400, 300)

catImg = pygame.image.load('./img/cat.png')
catx = 10
caty = 10
direction = 'right'

# set sound effect
# soundObj = pygame.mixer.Sound('sound_effect.wav')
# soundObj.play()

# set BGM
pygame.mixer.music.load('./music/white_album.wav')
pygame.mixer.music.set_volume(0.9)
pygame.mixer.music.play(-1, 0.0)

'''
DISPLAYSURF.fill(WHITE)
DISPLAYSURF.blit(textImage, (100, 100))
pygame.draw.rect(DISPLAYSURF, RED, (200, 150, 100, 50))
pygame.draw.polygon(DISPLAYSURF, BLUE, ((111, 0), (213, 254), (114, 26), (254, 30), (500, 11)))

# lock DISPLAYSURF to control single pixel
# now you can't use blit to draw jpeg or png
pixObj = pygame.PixelArray(DISPLAYSURF)
pixObj[480][380] = BLUE
pixObj[482][382] = BLUE
pixObj[484][384] = BLUE
pixObj[486][386] = BLUE
pixObj[488][388] = BLUE

# release DISPLAYSURF
del pixObj
'''

# run the game loop
while True:
    DISPLAYSURF.fill(WHITE)
    DISPLAYSURF.blit(textSurfaceObj, textRectObj)

    if direction == 'right':
        catx += 5
        if catx == 280:
            direction = 'down'
    elif direction == 'down':
        caty += 5
        if caty == 220:
            direction = 'left'
    elif direction == 'left':
        catx -= 5
        if catx == 10:
            direction = 'up'
    elif direction == 'up':
        caty -= 5
        if caty == 10:
            direction = 'right'

    DISPLAYSURF.blit(catImg, (catx, caty))

    for event in pygame.event.get():
        if event.type in (QUIT, KEYDOWN):
            pygame.mixer.music.stop()
            pygame.quit()
            sys.exit()
    # only draw display surface(which is declared by pygame.display.set_mode()) onto screen
    # if you want to draw another surface onto screen, use blit
    pygame.display.update()
    fpsClock.tick(FPS)