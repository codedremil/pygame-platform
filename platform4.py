'''
Implémentation des sauts (jumping): le saut n'est pas du "vol"
donc on implémente la gestion de la touche de saut dans la boucle
principale.
'''
import pygame


# jeu vertical et moyennement rapide
WIDTH = 480
HEIGHT = 600
FPS = 30        # nombre d'affichage par secondes

# mes couleurs
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)

# caractéristiques du joueur
PLAYER_ACC = 0.5
PLAYER_FRICTION = -0.12
PLAYER_GRAV = 0.5       # /part4/

# initialisation du programme
pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Mon jeu !")
clock = pygame.time.Clock()

# pour utiliser des vecteurs (des couples de nombres)
vec = pygame.math.Vector2


class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((30, 40))
        self.image.fill(YELLOW)
        self.rect = self.image.get_rect()
        self.rect.center = (WIDTH / 2, HEIGHT / 2)
        self.pos = vec(WIDTH / 2, HEIGHT / 2)
        self.vel = vec(0, 0)
        self.acc = vec(0, 0)

        
    def update(self):
        self.acc = vec(0, PLAYER_GRAV)  # /part4/
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.acc.x = -PLAYER_ACC
        if keys[pygame.K_RIGHT]:
            self.acc.x = PLAYER_ACC
            
        self.acc.x += self.vel.x * PLAYER_FRICTION
        # la vitesse augmente ou diminue en fonction de l'accélération
        self.vel += self.acc
        # la position dépend de la vitesse et de l'accélération
        self.pos += self.vel + 0.5 * self.acc
        self.rect.center = self.pos
        
        # gestion des bords de l'écran (wrapping)
        if self.pos.x > WIDTH:
            self.pos.x = 0
        if self.pos.x < 0:
            self.pos.x = WIDTH
            
        
    # /part4/2 - fonction de saut
    def jump(self):
        # 1ère version: on ne retombe pas forcément !
        self.vel.y = -20
        
      

class Platform(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height):
        super().__init__()
        self.image = pygame.Surface((width, height))
        self.image.fill(GREEN)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y


# liste de tous les Sprites (=objets animés)        
all_sprites = pygame.sprite.Group()
player = Player()
all_sprites.add(player)

all_platforms = pygame.sprite.Group()
p1 = Platform(0, HEIGHT - 40, WIDTH, 40)
all_sprites.add(p1)
all_platforms.add(p1)

p2 = Platform(WIDTH / 2 - 50, HEIGHT * 3 / 4, 100, 20)
all_sprites.add(p2)
all_platforms.add(p2)

# boucle du jeu
running = True
while running:
    # assure que la vitesse est correcte
    clock.tick(FPS)
    
    # gère les événements du clavier, de la souris...
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            
        # /part4/1 - touche de saut
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                player.jump()
                
    # met à jour la position des Sprites 
    all_sprites.update()
    
    # test de collision
    hits = pygame.sprite.spritecollide(player, all_platforms, False)
    if hits:
        player.pos.y = hits[0].rect.top
        # mais ça ne suffit pas: le joueur s'enfonce lentement dans la plateforme
        # que faut-il faire en plus ?
        player.vel.y = 0
        # mais la moitié du joueur disparait dans la plateforme
        player.rect.bottom = hits[0].rect.top
    
    # affiche le fond de jeu et les Sprites
    screen.fill(BLACK)
    all_sprites.draw(screen)
    
    # après avoir dessiné, on échange le buffer et l'écran
    pygame.display.flip()

pygame.quit()