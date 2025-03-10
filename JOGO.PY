import pygame, random
from pygame.locals import *

SCREEN_LARGURA = 500
SCREEN_ALTURA = 700
VELOCIDADE = 10
GRAVIDADE = 1
VELOCIDADE_DO_JOGO = 10

LARGURA_DO_CHAO = 2 * SCREEN_LARGURA
ALTURA_DO_CHAO = 100
OBSTACULO_LARGURA = 80
OBSTACULO_ALTURA = 500
LACUNA_DO_TUBO = 200

class Bird(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)

        self.images = [pygame.image.load('redbird-upflap.png').convert_alpha(),
                       pygame.image.load('redbird-midflap.png').convert_alpha(),
                       pygame.image.load('redbird-downflap.png').convert_alpha()]
        
        self.velocidade = VELOCIDADE
        
        self.current_image = 0
        self.image = pygame.image.load('redbird-upflap.png').convert_alpha()
        self.mask = pygame.mask.from_surface(self.image)

        self.rect = self.image.get_rect()
        self.rect[0] = SCREEN_LARGURA / 2
        self.rect[1] = SCREEN_ALTURA / 2

    def update(self):
        self.current_image = (self.current_image + 1) % 3
        self.image = self.images[self.current_image]
        self.velocidade += GRAVIDADE
        self.rect[1] += self.velocidade

    def bump(self):
        self.velocidade = -VELOCIDADE

class Obstaculos(pygame.sprite.Sprite):
    def __init__(self, inverted, xpos, ysize):
        pygame.sprite.Sprite.__init__(self)

        self.image = pygame.image.load('pipe-green.png').convert_alpha()
        self.image = pygame.transform.scale(self.image, (OBSTACULO_LARGURA, OBSTACULO_ALTURA))

        self.rect = self.image.get_rect()
        self.rect[0] = xpos

        if inverted:
            self.image = pygame.transform.flip(self.image, False, True)
            self.rect[1] = -(self.rect.height - ysize)  # Correção aqui
        else:
            self.rect[1] = SCREEN_ALTURA - ysize

        self.mask = pygame.mask.from_surface(self.image)

    def update(self):
        self.rect[0] -= VELOCIDADE_DO_JOGO

class Ground(pygame.sprite.Sprite):
    def __init__(self, xpos):
        pygame.sprite.Sprite.__init__(self)

        self.image = pygame.image.load('base.png').convert_alpha()
        self.image = pygame.transform.scale(self.image, (LARGURA_DO_CHAO, ALTURA_DO_CHAO))
        self.mask = pygame.mask.from_surface(self.image)

        self.rect = self.image.get_rect()
        self.rect[0] = xpos
        self.rect[1] = SCREEN_ALTURA - ALTURA_DO_CHAO

    def update(self):
        self.rect[0] -= VELOCIDADE_DO_JOGO

def is_off_screen(sprite):
    return sprite.rect[0] < -(sprite.rect.width)

def get_random_obstaculos(xpos):
    size = random.randint(100, 300)
    obstaculo = Obstaculos(False, xpos, size)
    obstaculo_inverted = Obstaculos(True, xpos, SCREEN_ALTURA - (size + LACUNA_DO_TUBO))  # Correção aqui
    return (obstaculo, obstaculo_inverted)

pygame.init()
screen = pygame.display.set_mode((SCREEN_LARGURA, SCREEN_ALTURA))

FUNDO = pygame.image.load('background-night.png')
FUNDO = pygame.transform.scale(FUNDO, (SCREEN_LARGURA, SCREEN_ALTURA))

bird_group = pygame.sprite.Group()
bird = Bird()
bird_group.add(bird)

ground_group = pygame.sprite.Group()
for i in range(2):
    ground = Ground(LARGURA_DO_CHAO * i)
    ground_group.add(ground)

obstaculos_group = pygame.sprite.Group()
for i in range(2):
    obstaculos = get_random_obstaculos(SCREEN_LARGURA * i + 800)
    obstaculos_group.add(obstaculos[0])
    obstaculos_group.add(obstaculos[1])

clock = pygame.time.Clock()

while True:
    clock.tick(10)
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            exit()

        if event.type == KEYDOWN:
            if event.key == K_SPACE:
                bird.bump()

    screen.blit(FUNDO, (0, 0))

    if is_off_screen(ground_group.sprites()[0]):
        ground_group.remove(ground_group.sprites()[0])
        new_ground = Ground(LARGURA_DO_CHAO - 20)
        ground_group.add(new_ground)

    if is_off_screen(obstaculos_group.sprites()[0]):
        obstaculos_group.remove(obstaculos_group.sprites()[0])
        obstaculos_group.remove(obstaculos_group.sprites()[0])
        obstaculos = get_random_obstaculos(SCREEN_LARGURA * 2)
        obstaculos_group.add(obstaculos[0])
        obstaculos_group.add(obstaculos[1])

    bird_group.update()
    ground_group.update()
    obstaculos_group.update()

    bird_group.draw(screen)
    ground_group.draw(screen)
    obstaculos_group.draw(screen)

    pygame.display.update()

    if (pygame.sprite.groupcollide(bird_group, ground_group, False, False, pygame.sprite.collide_mask) or 
        pygame.sprite.groupcollide(bird_group, obstaculos_group, False, False, pygame.sprite.collide_mask)):
        print("Game Over!")
        pygame.quit()
        exit()
