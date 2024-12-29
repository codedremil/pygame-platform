'''
On crée la classe Player qui va permettre de créer et gérer les
déplacements du joueur.
On voit que le joueur est placé en haut à gauche et qu'on peut le
diriger avec les flèches, mais il peut sortir de l'écran et il n'y a
pas de notion d'accélération ou décélération.'
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


class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((30, 40))
        self.image.fill(YELLOW)
        self.rect = self.image.get_rect()
        self.vx = 0
        self.vy = 0
        
    def update(self):
        self.vx = 0
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.vx -= 5
        if keys[pygame.K_RIGHT]:
            self.vx += 5
            
        self.rect.x += self.vx
        self.rect.y += self.vy
        


# liste de tous les Sprites (=objets animés)        
all_sprites = pygame.sprite.Group()
player = Player()
all_sprites.add(player)

# boucle du jeu
running = True
while running:
    # assure que la vitesse est correcte
    clock.tick(FPS)
    
    # gère les événements du clavier, de la souris...
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            
    # met à jour la position des Sprites 
    all_sprites.update()
    
    # affiche le fond de jeu et les Sprites
    screen.fill(BLACK)
    all_sprites.draw(screen)
    
    # après avoir dessiné, on échange le buffer et l'écran
    pygame.display.flip()

pygame.quit()