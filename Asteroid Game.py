import pygame, random, math

#Inicializar pygame
pygame.init()

#ventana
size = 1000,500
width, height = 1000,500
screen = pygame.display.set_mode(size)
pygame.display.set_caption("AstroBlast: Asteroid Annihilation")

#variables
score = 1
WHITE = 255, 255, 255
BLACK = 0, 0, 0
RED = 242, 99, 99
GREEN = 83, 240, 80
cooldown_time = 200
last_shot = 0
last_asteroid = 0
last_reload = 0
reload_time = 10000
cargador = 10
font = pygame.font.Font(None, int((width+height)/50))
listaDisparo = []
listaCaida = []
bar_height = 25
bar_width = 250
nivel = 1
dificultad = 1

#objeto
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("nave30.png")
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.x = width/2
        self.rect.y = height-100
        
    def dibujar(self, superficie):
        superficie.blit(self.image, self.rect)

class Bullet(pygame.sprite.Sprite):
    def __init__(self, posx, posy):
        super().__init__()
        self.image = pygame.Surface((4,8))
        self.image.fill((255,128,0))
        self.rect = self.image.get_rect()
        self.velocidadDisparo = 5
        
        self.rect.top = posy
        self.rect.left = posx
    
    def trayectoria(self):
        self.rect.top = self.rect.top - self.velocidadDisparo
        
    def dibujar(self, superficie):
        superficie.blit(self.image, self.rect)

class Asteroid(pygame.sprite.Sprite):
    def __init__(self, posx, posy):
        super().__init__()
        self.image = pygame.image.load("asteroide.png")
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.velocidadAsteroide = -6

        self.radius = 10  # Ajusta el radio del círculo según tu imagen de asteroide
        self.posx = posx
        self.posy = posy

        self.rect.center = (self.posx, self.posy)  # Configura el centro del rectángulo

    def trayectoria(self):
        self.posy = self.posy - self.velocidadAsteroide
        self.rect.center = (self.posx, self.posy)  # Actualiza la posición del círculo

    def dibujar(self, superficie):
        superficie.blit(self.image, self.rect)
        
def shoot(x,y):
    bullet = Bullet(x,y)
    listaDisparo.append(bullet)
    all_sprite_list.add(bullet)
    bullet_sprite_list.add(bullet)
    
def fall(x,y):
    asteroid = Asteroid(x,y)
    listaCaida.append(asteroid)
    all_sprite_list.add(asteroid)
    asteroid_sprite_list.add(asteroid)
    
def barra():
    percentage = (reload_time - (now - last_reload)) / reload_time
    bar2_width = int(percentage * bar_width)
    
    pygame.draw.rect(screen,GREEN,(width-bar_width-20,20,bar_width,bar_height))
    pygame.draw.rect(screen,RED,(width-bar2_width-20,20,bar2_width,bar_height))
    
#grupo sprites
all_sprite_list = pygame.sprite.Group()
bullet_sprite_list = pygame.sprite.Group()
asteroid_sprite_list = pygame.sprite.Group()
nave_sprite_list = pygame.sprite.Group()
explosion_group = pygame.sprite.Group()

#Player
player = Player()
all_sprite_list.add(player)
nave_sprite_list.add(player)

#reloj
clock = pygame.time.Clock()

# Game loop
run = True
paused = False  # Add a pause state

while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    if not paused:  # Only update the game if not paused
        clock.tick(60)

        now = pygame.time.get_ticks()
        if now % 3 == 0:
            score += 1

        text1 = font.render("AMMO: {0}".format(cargador), True, WHITE)
        text2 = font.render("SCORE: {0}".format(score), True, WHITE)
        level_text = font.render(f"LEVEL {nivel}", True, WHITE)  # Update the level text

        # Limit bullets
        for bullet in listaDisparo.copy():
            bullet.dibujar(screen)
            bullet.trayectoria()
            if bullet.rect.top < -10:
                listaDisparo.remove(bullet)
                all_sprite_list.remove(bullet)
                bullet_sprite_list.remove(bullet)

        # Asteroids
        if now - last_asteroid > 500 / dificultad:
            x = random.randint(0, width - 30)
            y = 0
            fall(x, y)
            last_asteroid = now

        for asteroid in listaCaida.copy():
            asteroid.dibujar(screen)
            asteroid.trayectoria()
            if asteroid.rect.top > height:
                listaCaida.remove(asteroid)
                all_sprite_list.remove(asteroid)
                asteroid_sprite_list.remove(asteroid)

        # Player boundaries
        if player.rect.x > width - 2:
            player.rect.x = -20
        if player.rect.x < -20:
            player.rect.x = width

        # Calculate collisions between bullets and asteroids
        for bullet in bullet_sprite_list:
            lista_colisiones1 = pygame.sprite.spritecollide(bullet, asteroid_sprite_list, True)
            if lista_colisiones1:
                all_sprite_list.remove(bullet)
                bullet_sprite_list.remove(bullet)
                score += 50

        # Calculate collisions between asteroids and the player
        for asteroid in asteroid_sprite_list:
            lista_colisiones2 = math.sqrt((asteroid.posx - player.rect.centerx) ** 2 + (asteroid.posy - player.rect.centery) ** 2)
            if lista_colisiones2 < (asteroid.radius + player.rect.width / 2):
                paused = True  # Pause the game when collision occurs

        # Level up
        if score >= nivel * 500:
            nivel += 1
            dificultad = nivel / 2

        # Keyboard input
        keys = pygame.key.get_pressed()
        if keys[pygame.K_w] or keys[pygame.K_UP]:
            if now - last_shot > cooldown_time and cargador > 0:
                x, y = player.rect.center
                shoot(x, y)
                last_shot = now
                cargador -= 1
        if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
            player.rect.x += 10
        if keys[pygame.K_a] or keys[pygame.K_LEFT]:
            player.rect.x -= 10
        if keys[pygame.K_e] or keys[pygame.K_DOWN]:
            if now - last_reload > reload_time and cargador != 10:
                cargador = 10 + int(nivel // 5) * 5
                last_reload = now

    # Update the screen
    screen.fill((43, 40, 46))
    all_sprite_list.draw(screen)
    screen.blit(text1, (20, 20))
    screen.blit(text2, (20, 50))
    screen.blit(level_text, (20, 80))
    barra()
    pygame.display.flip()

pygame.quit()