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


# liste de tous les Sprites (=objets animés)        
all_sprites = pygame.sprite.Group()

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