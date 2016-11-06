import pygame, random, sys
from pygame.locals import *
pygame.init()

width = 1200
height = 600

flame_velocity = 25

class dragon:
    global firerect, imagerect, Canvas
    up = False
    down = True
    velocity = 20

    def __init__(self):
        self.dragonimage = load_image('ImagesSprites/dragon.png')
        self.dragonimage_rect = self.dragonimage.get_rect(center = (1100, height/2))

    def update(self):
        if (self.dragonimage_rect.top < cactusrect.bottom):
            self.up = False
            self.down = True

        if (self.dragonimage_rect.bottom > firerect.top):
            self.up = True
            self.down = False
            
        if (self.down):
            self.dragonimage_rect.bottom += self.velocity

        if (self.up):
            self.dragonimage_rect.top -= self.velocity

        Canvas.blit(self.dragonimage, self.dragonimage_rect)

    def return_height(self):

        height = self.dragonimage_rect.top
        return height

class flames:
    flamespeed = 20

    def __init__(self):
        self.flameimage = load_image('ImagesSprites/fireball.png')
        self.flameimage_rect = self.flameimage.get_rect()
        self.height = Dragon.return_height() + 15
        self.surface = pygame.transform.scale(self.flameimage, (15,15))
        self.flameimage_rect = pygame.Rect(width - 100, self.height, 15, 15)

    def update(self):
        self.flameimage_rect.left -= self.flamespeed

    def collision(self):
        if self.flameimage_rect == 0:
            return True
        else:
            return False
class maryo:
    global moveup, movedown, gravity, cactusrect, firerect
    speed = 15
    downspeed = 20

    def __init__(self):
        self.marioimage = load_image('ImagesSprites/maryo.png')
        self.marioimage_rect = self.marioimage.get_rect(center = (80, height/2))
        self.score = 0

    def update(self):
        if (moveup and (self.marioimage_rect.top > cactusrect.bottom)):
            self.marioimage_rect.top -= self.speed
            self.score += 1
            
        if (movedown and (self.marioimage_rect.bottom < firerect.top)):
            self.marioimage_rect.bottom += self.downspeed
            self.score += 1
            
        if (gravity and (self.marioimage_rect.bottom < firerect.top)):
            self.marioimage_rect.bottom += self.speed

        
def terminate():
    pygame.quit()
    sys.exit()

def waitforkey():
    while True :                                        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            if event.type == pygame.KEYDOWN:     
                if event.key == pygame.K_ESCAPE:
                    terminate()
                return

def flamehitsmario(playerrect, flames):
    for flame in flame_list:
        if playerrect.colliderect(flame.flameimage_rect):
            return True
        return False

def drawtext(text, font, surface, x, y):
    textobj = font.render(text, 1, (255,255,255))
    textrect = textobj.get_rect()
    textrect.topleft = (x,y)
    surface.blit(textobj, textrect)

def check_level(score):
    global height, level, cactusrect, firerect
    if score in range(0,250):
        firerect.top = height - 40
        cactusrect.bottom = 40
        level = 1
    elif score in range(250, 500):
        firerect.top = height - 80
        cactusrect.bottom = 80
        level = 2
    elif score in range(500,750):
        level = 3
        firerect.top = height- 120
        cactusrect.bottom = 120
    elif score in range(750,1000):
        level = 4
        firerect.top = height - 160
        cactusrect.bottom = 160

def load_image(imagename):
    return pygame.image.load(imagename)

mainClock = pygame.time.Clock()
Canvas = pygame.display.set_mode((width, height))
pygame.display.set_caption('MARYO')

font = pygame.font.SysFont(None, 50)
scorefont = pygame.font.SysFont(None, 35)

fireimage = load_image('ImagesSprites/fire_bricks.png')
firerect = fireimage.get_rect()

cactusimage = load_image('ImagesSprites/cactus_bricks.png')
cactusrect = cactusimage.get_rect()

startimage = load_image('ImagesSprites/start.png')
startimagerect = startimage.get_rect(center = (width/2, height/2))
#startimagerect.centerx = width/2
#startimagerect.centery = height/2

endimage = load_image('ImagesSprites/end.png')
endimagerect = startimage.get_rect(center = (width/2, height/2))
#endimagerect.centerx = width/2
#endimagerect.centery = height/2

pygame.mixer.music.load('MusicSprites/mario_theme.wav')
gameover_music = pygame.mixer.Sound('MusicSprites/mario_dies.wav')

drawtext('Mario', font, Canvas, (width/3), (height/3))
Canvas.blit(startimage, startimagerect)

pygame.display.update()
waitforkey()
topscore = 0
Dragon = dragon()

while True:
    flame_list = []
    player = maryo()
    moveup = movedown = gravity = False
    flameaddcounter = 0

    gameover_music.stop()
    pygame.mixer.music.play(-1,0.0)

    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                terminate()        
            if event.type == KEYDOWN:
                if event.key == K_UP:
                    movedown = False
                    moveup = True
                    gravity = False
                if event.key == K_DOWN:
                    movedown = True
                    moveup = False
                    gravity = False

            if event.type == KEYUP:
                if event.key == K_UP:
                    moveup = False
                    gravity = True
                if event.key == K_DOWN:
                    movedown = False
                    gravity = True
                if event.key == K_ESCAPE:
                    terminate()

        flameaddcounter += 1
        check_level(player.score)

        if flameaddcounter == flame_velocity:
            flameaddcounter = 0
            newflame = flames()
            flame_list.append(newflame)

        for flame in flame_list:
            flames.update(flame)

        for flame in flame_list:
            if flame.flameimage_rect.left <= 0:
                flame_list.remove(flame)
        player.update()
        Dragon.update()

        Canvas.fill((0,0,0))
        Canvas.blit(fireimage, firerect)
        Canvas.blit(cactusimage, cactusrect)
        Canvas.blit(player.marioimage, player.marioimage_rect)
        Canvas.blit(Dragon.dragonimage, Dragon.dragonimage_rect)

        drawtext('Score : %s | Top score : %s | Level : %s' %(player.score, topscore, level), scorefont, Canvas, 350, cactusrect.bottom + 10)

        for flame in flame_list:
            Canvas.blit(flame.surface, flame.flameimage_rect)

        if flamehitsmario(player.marioimage_rect, flame_list):
            if player.score > topscore:
                topscore = player.score
            break

        if((player.marioimage_rect.top <= cactusrect.bottom) or (player.marioimage_rect.bottom >= firerect.top)):
            if player.score > topscore:
                topscore = player.score
            break

        pygame.display.update()
        
        mainClock.tick(25)

    pygame.mixer.music.stop()
    gameover_music.play()
    Canvas.blit(endimage, endimagerect)
    pygame.display.update()
    waitforkey()


















