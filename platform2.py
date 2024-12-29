'''
On place le joueur au milieu de l'�cran.
On g�re aussi une acc�l�ration, mais le probl�me c'est que le mobile
ne s'arr�te pas !
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
        # self.vx = 0
        # self.vy = 0
        
    def update(self):
        # self.vx = 0
        self.acc = vec(0, 0)
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            # self.vx -= 5
            self.acc.x = -0.5
        if keys[pygame.K_RIGHT]:
            # self.vx += 5
            self.acc.x = 0.5
            
        # self.rect.x += self.vx
        # self.rect.y += self.vy
        # la vitesse augmente ou diminue en fonction de l'acc�l�ration
        self.vel += self.acc
        # la position d�pend de la vitesse et de l'acc�l�ration
        self.pos += self.vel + 0.5 * self.acc
        self.rect.center = self.pos
        


# liste de tous les Sprites (=objets anim�s)        
all_sprites = pygame.sprite.Group()
player = Player()
all_sprites.add(player)

# boucle du jeu
running = True
while running:
    # assure que la vitesse est correcte
    clock.tick(FPS)
    
    # g�re les �v�nements du clavier, de la souris...
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            
    # met � jour la position des Sprites 
    all_sprites.update()
    
    # affiche le fond de jeu et les Sprites
    screen.fill(BLACK)
    all_sprites.draw(screen)
    
    # apr�s avoir dessin�, on �change le buffer et l'�cran
    pygame.display.flip()

pygame.quit()