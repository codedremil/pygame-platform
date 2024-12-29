'''
Amélioration des collisions pour éviter d'avoir l'impression
d'être "en l'air" à côté de la pf
Réglage du volume des sons et musique
Ajout des powerups
Refactoring pour ajouter les sprites dans leurs groupes
'''
import pygame
import random
from os import path
from itertools import chain


# jeu vertical et moyennement rapide
WIDTH = 480
HEIGHT = 600
FPS = 60       
FONT_NAME = "arial"
TITLE = "Jumpy"
HS_FILE = "highscore.txt"
SPRITESHEET = "spritesheet_jumper.png"

# mes couleurs
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
LIGHTBLUE = (0, 155, 155)
BGCOLOR = LIGHTBLUE

# caractéristiques du joueur
PLAYER_ACC = 0.5
PLAYER_FRICTION = -0.12
PLAYER_GRAV = 0.5     
PLAYER_JUMP = -18

# part15/5: caractéristiques du jeu
BOOST_POWER = 60
POW_SPAWN_PCT = 18   # fréquence d'apparition des powerups

# liste des PF (x, y, w, h)
PLATFORM_THICKNESS = 20
PLATFORM_LIST = [
    # on veut que la 1ère plateforme soit "décollée" du bas
    (0, HEIGHT - 60, WIDTH, PLATFORM_THICKNESS * 2),
    (WIDTH / 2 - 50, HEIGHT * 3 / 4, 100, PLATFORM_THICKNESS),
    (125, HEIGHT - 350, 100, PLATFORM_THICKNESS),
    (350, 200, 100, PLATFORM_THICKNESS),
    (175, 100, 100, PLATFORM_THICKNESS),    
]

# initialisation du programme
pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption(TITLE)
clock = pygame.time.Clock()
font_name = pygame.font.match_font(FONT_NAME) 

# pour utiliser des vecteurs (des couples de nombres)
vec = pygame.math.Vector2


# pour charger et gérer la spritesheet
class Spritesheet:
    def __init__(self, filename):
        self.spritesheet = pygame.image.load(filename).convert()
        
    def get_image(self, x, y, width, height):
        # charge une image
        # x, y, w et h donnent les coord. de l'image dans la feuille
        image = pygame.Surface((width, height))
        image.blit(self.spritesheet, (0, 0), (x, y, width, height))
        # resizeing
        image = pygame.transform.scale(image, (width // 2, height // 2))
        return image
        
        
class Player(pygame.sprite.Sprite):
    def __init__(self, platforms):
        # part15/4: l'ajout dans les groupes est ici
        self.groups = all_sprites
        super().__init__(self.groups)
        
        self.platforms = platforms
                
        # ajout de l'état pour marcher
        self.walking = False
        self.jumping = False
        self.current_frame = 0
        self.last_update = 0    # pour ne pas changer l'image à toutes les frames !
        self.load_images()
        self.image = self.standing_frames[0]        
        #self.image = spritesheet.get_image(614, 1063, 120, 191)
        #self.image.set_colorkey(BLACK)
        
        self.rect = self.image.get_rect()
        # on veut que le joueur soit positionné sur la 1ère pf
        self.rect.center = (40, HEIGHT - 140)
        self.pos = vec(40, HEIGHT - 140)
        self.vel = vec(0, 0)
        self.acc = vec(0, 0)

    # chargement des images du Player
    def load_images(self):
        self.standing_frames = [
            spritesheet.get_image(614, 1063, 120, 191),
            spritesheet.get_image(690, 406, 120, 201),
        ]
        self.walk_frames_r = [
            spritesheet.get_image(678, 860, 120, 201),
            spritesheet.get_image(692, 1458, 120, 207),            
        ]
        self.walk_frames_l = []
        for frame in self.walk_frames_r:
            # flip horiz pas vertical
            self.walk_frames_l.append(pygame.transform.flip(frame, True, False))
        self.jump_frame = spritesheet.get_image(382, 763, 150, 181)
        
        # ne pas le faire tout de suite pour voir le bug
        for frame in chain(self.standing_frames, self.walk_frames_r, self.walk_frames_l, [self.jump_frame]):
            frame.set_colorkey(BLACK)
          
    def update(self):
        # ajout de l'animation des images
        self.animate()
        
        self.acc = vec(0, PLAYER_GRAV)  # /part4/
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.acc.x = -PLAYER_ACC
        if keys[pygame.K_RIGHT]:
            self.acc.x = PLAYER_ACC
            
        self.acc.x += self.vel.x * PLAYER_FRICTION
        # la vitesse augmente ou diminue en fonction de l'accélération
        self.vel += self.acc
        
        # définit un seuil minimal
        if abs(self.vel.x) < 0.1:
            self.vel.x = 0
            
        # la position dépend de la vitesse et de l'accélération
        self.pos += self.vel + 0.5 * self.acc
        self.rect.center = self.pos
        
        # gestion des bords de l'écran (wrapping)
        if self.pos.x > WIDTH:
            self.pos.x = 0
        if self.pos.x < 0:
            self.pos.x = WIDTH
            
        # amélioration de la gestion des bords
        if self.pos.x > WIDTH + self.rect.width / 2:
            self.pos.x = 0 - self.rect.width / 2
        if self.pos.x < 0 - self.rect.width / 2:
            self.pos.x = WIDTH + self.rect.width / 2
            
        #self.rect.midbottom = self.pos

    # animation
    def animate(self):
        now = pygame.time.get_ticks()
        
        # détermine si on marche
        if self.vel.x != 0:
            self.walking = True
        else:
            self.walking = False
            
        if self.walking:
            if now - self.last_update > 200:
                self.last_update = now
                self.current_frame = (self.current_frame + 1) % len(self.walk_frames_l)
                bottom = self.rect.bottom
                if self.vel.x > 0:
                    self.image = self.walk_frames_r[self.current_frame]
                else:
                    self.image = self.walk_frames_l[self.current_frame]
                self.rect = self.image.get_rect()
                self.rect.bottom = bottom
                # on peut tester, mais il y a un bug: quand on ne déplace pas
                # le Player, il continue à marcher "sur place". Le pb vient
                # du calcul de la vitesse qui décroit petit à petit (friction)
                # et qui tend vers zéro. Il faut donc définir un seuil
                # dans la fonction update()
                
        if not self.jumping and not self.walking:
            if now - self.last_update > 400:
                self.last_update = now
                self.current_frame = (self.current_frame + 1) % len(self.standing_frames)
                self.image = self.standing_frames[self.current_frame]
                
                # le bas de l'animation est mal positionné
                bottom = self.rect.bottom
                self.rect = self.image.get_rect()
                self.rect.bottom = bottom
                
                
    def jump_cut(self):
        if self.jumping:
            if self.vel.y < -3:
                self.vel.y = -3
        
    # fonction de saut
    def jump(self):
        # on teste qu'on est sur une plateforme !
        # si on trouve que le saut ne marche pas bien on change les valeurs 1 en 2
        self.rect.y += 1
        hits = pygame.sprite.spritecollide(self, self.platforms, False)
        self.rect.y -= 1
        
        if hits and not self.jumping:
            self.jumping = True
            self.vel.y = PLAYER_JUMP
            jump_sound.play()
        

class Platform(pygame.sprite.Sprite):
    # depuis part12 width et height ne servent plus à rien
    def __init__(self, x, y, width, height):
        # part15/4: l'ajout dans les groupes est ici
        self.groups = all_sprites, all_platforms
        super().__init__(self.groups)
        
        # charge les images des plateformes
        images = [
            spritesheet.get_image(0, 288, 380, 94),
            spritesheet.get_image(213, 1662, 201, 100),
        ]
        # on choisit une image alétoirement
        #self.image = pygame.Surface((width, height))
        #self.image.fill(GREEN)
        self.image = random.choice(images)
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        
        # part15/6: on crée un powerup aléatoirement
        if random.randrange(100) < POW_SPAWN_PCT:
            Powerup(self)


# part15/2: les powerups sont affichés sur des pf
class Powerup(pygame.sprite.Sprite):
    def __init__(self, platform):
        # part15/4: l'ajout dans les groupes est ici
        self.groups = all_sprites, all_powerups
        super().__init__(self.groups)
        
        self.platform = platform
        self.type = random.choice(['boost'])
        images = {
            'boost': spritesheet.get_image(820, 1805, 71, 70),
        }
        self.image = images[self.type]
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.centerx = self.platform.rect.centerx
        self.rect.bottom = self.platform.rect.top - 5
        
    def update(self):
        # si la pf bouge, il faut que le powerup la suive
        self.rect.bottom = self.platform.rect.top - 5
        
        # si la pf disparait de l'écran, il faut supprimer le powerup
        if not all_platforms.has(self.platform):
            self.kill()        


# Fonction d'affichage de texte
def draw_text(text, size, color, x, y):
    font = pygame.font.Font(font_name, size)
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x, y)
    screen.blit(text_surface, text_rect)
    

    
# Il faut gérer l'appui sur une touche    
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
                
    
# affichage des consignes de départ
def show_start_screen():
    play_start_screen()
    screen.fill(BGCOLOR)
    draw_text(TITLE, 48, WHITE, WIDTH / 2, HEIGHT / 4)
    draw_text("Les flèches pour se déplacer, Espace pour sauter", 22, WHITE, WIDTH / 2, HEIGHT / 2)
    draw_text("Appuyez sur une touche pour commencer !", 22, WHITE, WIDTH / 2, HEIGHT * 3 / 4)
    load_hs()
    load_images()
    load_sounds()
    draw_text(f"High Score: {highscore}", 22, WHITE, WIDTH /2, 15)
    pygame.display.flip()
    wait_for_key()
    pygame.mixer.music.fadeout(500)
    
    
# affichage du game over/continue screen
def show_go_screen():
    global highscore
    # montrer que si on ne fait pas ce test, le fait de quitter
    # en cours de jeu affiche l'écran de game over !
    # if not running:  # ne marche pas
    #     return 
    
    screen.fill(BGCOLOR)
    draw_text("GAME OVER", 48, WHITE, WIDTH / 2, HEIGHT / 4)
    draw_text("Score " + str(score), 22, WHITE, WIDTH / 2, HEIGHT / 2)
    draw_text("Appuyez sur une touche pour rejouer !", 22, WHITE, WIDTH / 2, HEIGHT * 3 / 4)
    # sauvegarde du score
    if score > highscore:
        highscore = score
        draw_text("Nouveau High Score !", 22, WHITE, WIDTH / 2, HEIGHT / 2 + 40)
        save_hs()
    else:
        draw_text(f"High Score: {highscore}", 22, WHITE, WIDTH /2, HEIGHT / 2 + 50)        
        
    pygame.display.flip()
    wait_for_key()
    
    
# affichage des high scores
highscore = 0

def load_hs():
    global highscore
    dir = path.dirname(__file__)
    with open(path.join(dir, HS_FILE), 'w') as f:
        try:
            highscore = int(f.read())
        except:
            highscore = 0
            
# sauvegarde du Highscore
def save_hs():
    dir = path.dirname(__file__)
    with open(path.join(dir, HS_FILE), 'w') as f:
        f.write(str(highscore))
    
    
# charge les images
spritesheet = None

def load_images():
    global spritesheet
    dir = path.dirname(__file__)
    img_dir = path.join(dir, 'img')
    spritesheet = Spritesheet(path.join(img_dir, SPRITESHEET))
    
# charge les sons
jump_sound = None
boost_sound = None      # part15/8

def load_sounds():
    global jump_sound, boost_sound
    dir = path.dirname(__file__)
    snd_dir = path.join(dir, 'snd')
    jump_sound = pygame.mixer.Sound(path.join(snd_dir, "Jump33.wav")) 
    jump_sound.set_volume(.3)
    
    # part15/8: son pour powerup
    boost_sound = pygame.mixer.Sound(path.join(snd_dir, "Boost16.wav")) 
    boost_sound.set_volume(.3)
    
# joue la musique
def play_happy_tune():
    dir = path.dirname(__file__)
    snd_dir = path.join(dir, 'snd')
    pygame.mixer.music.load(path.join(snd_dir, 'Happy Tune.ogg'))
    pygame.mixer.music.play(loops=-1)
    pygame.mixer.music.set_volume(.3)
    
# musique du start screen
def play_start_screen():
    dir = path.dirname(__file__)
    snd_dir = path.join(dir, 'snd')
    pygame.mixer.music.load(path.join(snd_dir, 'Yippee.ogg'))
    pygame.mixer.music.play(loops=-1)
    pygame.mixer.music.set_volume(.3)
    

# on veut pouvoir jouer plusieurs fois: on ajoute une boucle !
# il faut ajouter une nouvelle variable qui sera mise à False dans la
# fonction wait_for_key !
want_to_play = True
while want_to_play:    
    # liste de tous les Sprites (=objets animés) 
    # ce sont les initialisations qu'il faut faire à chaque tour de jeu 
    show_start_screen()     
    all_sprites = pygame.sprite.Group()
    all_platforms = pygame.sprite.Group()
    all_powerups = pygame.sprite.Group()    # part15/3
    score = 0

    # construit la liste des PF
    for platform in PLATFORM_LIST:
        Platform(*platform)     # part15/4
        #pf = Platform(*platform)
        #all_sprites.add(pf)
        #all_platforms.add(pf)
    
    player = Player(all_platforms)
    #all_sprites.add(player)    # part15/4
    
    # ajout de la musique
    play_happy_tune()

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
                    
            # touche arrêt de saut
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_SPACE:
                    player.jump_cut()
                
        # met à jour la position des Sprites 
        all_sprites.update()
        
        # test de collision mais uniquement si le joueur tombe
        if player.vel.y > 0:
            hits = pygame.sprite.spritecollide(player, all_platforms, False)
            if hits:
                # il faut trouver la pf la plus basse
                lowest = hits[0]
                for hit in hits:
                    if hit.rect.bottom > lowest.rect.bottom:
                        lowest = hit
                        
                # part15/1: on teste que la position x du joueur est 
                # entre les bornes de la pf (on ajuste avec 10):
                if lowest.rect.left - 10 < player.pos.x < lowest.rect.right + 10:
                    if player.pos.y < lowest.rect.centery:
                        player.pos.y = lowest.rect.top
                        
                        # mais ça ne suffit pas: le joueur s'enfonce lentement dans la plateforme
                        # que faut-il faire en plus ?
                        player.vel.y = 0
                        player.jumping = False
                        
                        # mais la moitié du joueur disparait dans la plateforme
                        player.rect.bottom = lowest.rect.top
            
        # si le joueur atteint le 1er quart de l'écran, on scrolle
        if player.rect.top <= HEIGHT / 4:
            # on veut un scroll plus "doux" qui recentre l'écran
            # même si le joueur ne bouge pas
            #player.pos.y += abs(player.vel.y)
            player.pos.y += max(abs(player.vel.y), 2)
            for platform in all_platforms:
                # recentrage "doux"
                #platform.rect.y += abs(player.vel.y)
                platform.rect.y += max(abs(player.vel.y), 2)
                
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
                    
        # part15/7: teste si le joueur touche un powerup
        pow_hits = pygame.sprite.spritecollide(player, all_powerups, True)
        for pow in pow_hits:
             if pow.type == 'boost':
                 boost_sound.play()     # part15/9 (après le 8)
                 player.vel.y = -BOOST_POWER
                 player.jumping = False
                 
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
            
            # part15/4
            Platform(x, y, width, PLATFORM_THICKNESS)
            #pf = Platform(x, y, width, PLATFORM_THICKNESS)
            #all_sprites.add(pf)
            #all_platforms.add(pf)
            
        
        # affiche le fond de jeu et les Sprites
        # on change la couleur de fond
        screen.fill(BGCOLOR)
        all_sprites.draw(screen)
        
        #parfois le joueur passe "derrière" les PF: on le
        # redessine pour qu'il apparaisse toujours au 1er plan
        screen.blit(player.image, player.rect)
        
        # on affiche le score
        draw_text(str(score), 22, WHITE, WIDTH /2 , 15)
        
        # après avoir dessiné, on échange le buffer et l'écran
        pygame.display.flip()

    # arrêt musique
    pygame.mixer.music.fadeout(500) # 500 ms
        
    # fin d'une partie
    show_go_screen()


pygame.quit()