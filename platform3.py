'''
On ajoute maintenant de la gravit� pour que le joueur puisse
sauter et retomber.
On cr�e notre 1�re plateforme et on arr�te la chute du joueur
en cas de collision avec la plateforme !
(montrer le sch�ma en JPG)
Puis on ajoute une 2�me plateforme...
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

# caract�ristiques du joueur
PLAYER_ACC = 0.5
PLAYER_FRICTION = -0.12

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
        # /part3/1
        # pour faire "tomber" le joueur, il faut que la valeur des "y"
        # augmente. Il faut donc un acc�l�ration positive sur les "y"
        #self.acc = vec(0, 0)
        self.acc = vec(0, 0.5)
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.acc.x = -PLAYER_ACC
        if keys[pygame.K_RIGHT]:
            self.acc.x = PLAYER_ACC
            
        # prise en compte de la friction
        # /part3/2
        # le pb maintenant c'est que la friction emp�che la chute
        # du joueur de s'acc�l�rer. On applique la friction uniquement
        # horizontalement
        #self.acc += self.vel * PLAYER_FRICTION
        self.acc.x += self.vel.x * PLAYER_FRICTION
        # la vitesse augmente ou diminue en fonction de l'acc�l�ration
        self.vel += self.acc
        # la position d�pend de la vitesse et de l'acc�l�ration
        self.pos += self.vel + 0.5 * self.acc
        self.rect.center = self.pos
        
        # gestion des bords de l'�cran (wrapping)
        if self.pos.x > WIDTH:
            self.pos.x = 0
        if self.pos.x < 0:
            self.pos.x = WIDTH
      

# /part3/3 - cr�ation des plateformes
class Platform(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height):
        super().__init__()
        self.image = pygame.Surface((width, height))
        self.image.fill(GREEN)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y


# liste de tous les Sprites (=objets anim�s)        
all_sprites = pygame.sprite.Group()
player = Player()
all_sprites.add(player)

# /part3/4 - on cr�e un groupe pour les plateformes (pour tester
# les futures collisions), puis on cr�e une plateforme et on l'ajoute
# aux groupes
all_platforms = pygame.sprite.Group()
p1 = Platform(0, HEIGHT - 40, WIDTH, 40)
all_sprites.add(p1)
all_platforms.add(p1)

# /part3/6 - on ajoute une 2�me plateforme pour voir l'effet
p2 = Platform(WIDTH / 2 - 50, HEIGHT * 3 / 4, 100, 20)
all_sprites.add(p2)
all_platforms.add(p2)

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
    
    # /part3/5 - test de collision
    hits = pygame.sprite.spritecollide(player, all_platforms, False)
    if hits:
        player.pos.y = hits[0].rect.top
        # mais �a ne suffit pas: le joueur s'enfonce lentement dans la plateforme
        # que faut-il faire en plus ?
        player.vel.y = 0
        # mais la moiti� du joueur disparait dans la plateforme
        player.rect.bottom = hits[0].rect.top
    
    # affiche le fond de jeu et les Sprites
    screen.fill(BLACK)
    all_sprites.draw(screen)
    
    # apr�s avoir dessiné, on �change le buffer et l'�cran
    pygame.display.flip()

pygame.quit()