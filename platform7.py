'''
On affiche le splash-screen et le game over screen
'''
import pygame
import random


# jeu vertical et moyennement rapide
WIDTH = 480
HEIGHT = 600
FPS = 60       
FONT_NAME = "arial"
TITLE = "Jumpy"

# mes couleurs
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
# /part7/1
LIGHTBLUE = (0, 155, 155)
BGCOLOR = LIGHTBLUE

# caractéristiques du joueur
PLAYER_ACC = 0.5
PLAYER_FRICTION = -0.12
PLAYER_GRAV = 0.5     
PLAYER_JUMP = -18

# liste des PF (x, y, w, h)
PLATFORM_THICKNESS = 20
PLATFORM_LIST = [
    (0, HEIGHT - 40, WIDTH, PLATFORM_THICKNESS * 2),
    (WIDTH / 2 - 50, HEIGHT * 3 / 4, 100, PLATFORM_THICKNESS),
    (125, HEIGHT - 350, 100, PLATFORM_THICKNESS),
    (350, 200, 100, PLATFORM_THICKNESS),
    (175, 100, 100, PLATFORM_THICKNESS),    
]

# initialisation du programme
pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption(TITLE)   # /part7
clock = pygame.time.Clock()
font_name = pygame.font.match_font(FONT_NAME)   # /part6

# pour utiliser des vecteurs (des couples de nombres)
vec = pygame.math.Vector2


class Player(pygame.sprite.Sprite):
    def __init__(self, platforms):
        super().__init__()
        self.platforms = platforms       
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
        # la position dÃ©pend de la vitesse et de l'accélération
        self.pos += self.vel + 0.5 * self.acc
        self.rect.center = self.pos
        
        # gestion des bords de l'écran (wrapping)
        if self.pos.x > WIDTH:
            self.pos.x = 0
        if self.pos.x < 0:
            self.pos.x = WIDTH
            
        
    # fonction de saut
    def jump(self):
        # on teste qu'on est sur une plateforme !
        self.rect.y += 1
        hits = pygame.sprite.spritecollide(self, self.platforms, False)
        self.rect.y -= 1
        if hits:
            self.vel.y = PLAYER_JUMP
        

class Platform(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height):
        super().__init__()
        self.image = pygame.Surface((width, height))
        self.image.fill(GREEN)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y


# Fonction d'affichage de texte
def draw_text(text, size, color, x, y):
    font = pygame.font.Font(font_name, size)
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x, y)
    screen.blit(text_surface, text_rect)
    

    
# /part7/3 - Il faut gérer l'appui sur une touche    
def wait_for_key():
    global want_to_play
    waiting = True
    while waiting:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                waiting = False
                #want_to_play = False # on n'a pas encore cette variable
                want_to_play = False
            if event.type == pygame.KEYUP:
                waiting = False
                
    
# /part7/2 - affichage des consignes de départ
def show_start_screen():
    screen.fill(BGCOLOR)
    draw_text(TITLE, 48, WHITE, WIDTH / 2, HEIGHT / 4)
    draw_text("Les flèches pour se déplacer, Espace pour sauter", 22, 
              WHITE, WIDTH / 2, HEIGHT / 2)
    draw_text("Appuyez sur une touche pour commencer !", 22, 
              
              WHITE, WIDTH / 2, HEIGHT * 3 / 4)
    pygame.display.flip()
    wait_for_key()
    
    
# /part7/5 - affichage du game over/continue screen
def show_go_screen():
    # /part7/8 - montrer que si on ne fait pas ce test, le fait de quitter
    # en cours de jeu affiche l'écran de game over !
    # if not running:  # ne marche pas
    #     return 
    
    screen.fill(BGCOLOR)
    draw_text("GAME OVER", 48, WHITE, WIDTH / 2, HEIGHT / 4)
    draw_text("Score " + str(score), 22, WHITE, WIDTH / 2, HEIGHT / 2)
    draw_text("Appuyez sur une touche pour rejouer !", 22, 
              WHITE, WIDTH / 2, HEIGHT * 3 / 4)
    pygame.display.flip()
    wait_for_key()
    
    

# /part7/6 - on veut pouvoir jouer plusieurs fois: on ajoute une boucle !
# il faut ajouter une nouvelle variable qui sera mise à False dans la
# fonction wait_for_key !
want_to_play = True
while want_to_play:    
    # liste de tous les Sprites (=objets animés) 
    # ce sont les initialisations qu'il faut faire à chaque tour de jeu 
    show_start_screen()     # /part7/4      
    all_sprites = pygame.sprite.Group()
    all_platforms = pygame.sprite.Group()
    score = 0

    # construit la liste des PF
    for platform in PLATFORM_LIST:
        pf = Platform(*platform)
        all_sprites.add(pf)
        all_platforms.add(pf)
    
    player = Player(all_platforms)
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
                
            # touche de saut
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    player.jump()
                
        # met à jour la position des Sprites 
        all_sprites.update()
        
        # test de collision mais uniquement si le joueur tombe
        if player.vel.y > 0:
            hits = pygame.sprite.spritecollide(player, all_platforms, False)
            if hits:
                player.pos.y = hits[0].rect.top
                # met ça ne suffit pas: le joueur s'enfonce lentement dans la plateforme
                # que faut-il faire en plus ?
                player.vel.y = 0
                # mais la moitié du joueur disparait dans la plateforme
                player.rect.bottom = hits[0].rect.top
            
        # si le joueur atteint le 1er quart de l'écran, on scrolle
        if player.rect.top <= HEIGHT / 4:
            player.pos.y += abs(player.vel.y)
            for platform in all_platforms:
                platform.rect.y += abs(player.vel.y)
                
                # mais il y a un pb: on ne gère pas la descente ni
                # l'apparition de nouvelles plates-formes
                # de plus, les plateformes qui disparaissent sont toujours
                # dans la liste des PF testées pour les collisions : à force
                # d'en ajouter il y aura un problème de performances, donc
                # on supprime les PF qui disparaissent de l'écran
                if platform.rect.top >= HEIGHT:
                    platform.kill()
                    # on augmente le score
                    score += 10
                
        # teste si le joueur meurt
        if player.rect.bottom > HEIGHT:
            # on pourrait juste faire ceci
            #running = False
            # mais on va déplacer les plateformes vers le haut
            for sprite in all_sprites:
                sprite.rect.y -= max(player.vel.y, 10)
                if sprite.rect.bottom < 0:
                    sprite.kill()
                    
            # du coup, il y aura game over quand toutes les plateformes auront disparu
            if len(all_platforms) == 0:
                running = False
                
        # Crée de nouvelles PF pour en avoir toujours 5
        while len(all_platforms) < len(PLATFORM_LIST):
            width = random.randrange(50, 100)
            x = random.randrange(0, WIDTH - width)
            y = random.randrange(-75, -30)  # au-dessus de l'écran
            pf = Platform(x, y, width, PLATFORM_THICKNESS)
            all_sprites.add(pf)
            all_platforms.add(pf)
            
        
        # affiche le fond de jeu et les Sprites
        # /part7/1 - on change la couleur de fond
        screen.fill(BGCOLOR)
        all_sprites.draw(screen)
        
        # on affiche le score
        draw_text(str(score), 22, WHITE, WIDTH /2 , 15)
        
        # après avoir dessiné, on échange le buffer et l'écran
        pygame.display.flip()
        
    # /part7/7 - fin d'une partie
    show_go_screen()

pygame.quit()