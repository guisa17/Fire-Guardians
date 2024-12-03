"""
Controles del jugador

- Movimientos básicos
- Animaciones
- Tanque de agua
"""

import pygame
from src.core.utils import load_image
from src.core.settings import PLAYER_SPEED, PLAYER_INITIAL_WATER, SPRITE_SCALE


class Player:
    def __init__(self, x, y):

        """
        Inicialización del jugador
        """
        self.x = x
        self.y = y
        self.speed = PLAYER_SPEED
        self.water = PLAYER_INITIAL_WATER
        self.direction = 0      # 0: ->, 1: v, 2: ^, 3: <-
        self.is_running = False
        self.animation_timer = 0
        self.frame_index = 0

        self.max_lives = 5
        self.current_lives = 5

        self.collision_timer = 0
        self.invulnerable_timer = 0
        self.blink_timer = 0
        self.blink_state = True

        self.space_press_count = 0      # interacciones con spacebar

        """
        Carga de sprites
        """
        self.idle_sprites = self.load_spritesheet("player/idle.png", 4, 3)
        self.run_sprites = self.load_spritesheet("player/run.png", 8, 3)
        self.heart_sprite = self.load_heart_sprite()

    
    def load_spritesheet(self, path, cols, rows):
        """
        Dividir el spritesheet en sus respectivos sprites
        """
        spritesheet = load_image(path)
        sheet_width, sheet_height = spritesheet.get_size()
        sprite_width = sheet_width // cols
        sprite_height = sheet_height // rows

        sprites = []
        for row in range(rows):
            row_sprites = []
            for col in range(cols):
                x = col * sprite_width
                y = row * sprite_height
                
                sprite = spritesheet.subsurface(pygame.Rect(x, y, sprite_width, sprite_height))
                sprite = pygame.transform.scale(sprite, (sprite_width * SPRITE_SCALE, sprite_height * SPRITE_SCALE))
                row_sprites.append(sprite)

            sprites.append(row_sprites)

        return sprites


    def get_sprite(self, sprite_list, index, flipped=False):
        """
        Obtiene el sprite, invirtiéndolo si es necesario
        """
        sprite = sprite_list[index]
        return pygame.transform.flip(sprite, True, False) if flipped else sprite


    def load_heart_sprite(self):
        """
        Cargar sprite para las vidas
        """
        heart_sprite = load_image("heart/heart.png")
        return pygame.transform.scale(heart_sprite, (7 * (SPRITE_SCALE - 2), 7 * (SPRITE_SCALE - 2)))


    def get_rect(self):
        """
        Devuelve el rectángulo de colisión
        """
        collision_width = 10 * SPRITE_SCALE
        collision_height = 14 * SPRITE_SCALE
        
        offset_x = 5 * SPRITE_SCALE
        offset_y = 6 * SPRITE_SCALE

        return pygame.Rect(
            self.x + offset_x,
            self.y + offset_y,
            collision_width,
            collision_height
        )


    # TMP !
    def draw_collision_box(self, screen):
        """
        Dibujar rectángulo de colisión
        """
        collision_rect = self.get_rect()
        pygame.draw.rect(screen, (255, 0, 0), collision_rect, 1)


    def handle_collision(self, fires, dt):
        """
        Manejo de colisiones con el fuego
        """
        if self.invulnerable_timer > 0:
            self.invulnerable_timer -= dt
            self.collision_timer = 0
            return
        
        collided = False
        for fire in fires:
            if fire.is_active and self.get_rect().colliderect(fire.get_rect()):
                collided = True
                self.collision_timer += dt
                
                if self.collision_timer >= 0.5:
                    print("damage")
                    self.take_damage(1, fire)
                    self.invulnerable_timer = 1
                    self.collision_timer = 0
                    break
        
        if not collided:
            self.collision_timer = 0


    def interact_with_fire(self, fires, keys):
        """
        Interactuar con fuego
        """
        if keys[pygame.K_SPACE]:
            for fire in fires:
                if fire.is_active:
                    distance_x = abs(self.x - fire.x)
                    distance_y = abs(self.y - fire.y)

                    if distance_x < 100 and distance_y < 100:
                        if self.water > 0:
                            if self.space_press_count < 1:
                                self.space_press_count += 1
                                fire.extinguish(10)
                                self.water -= 3     # diminuye agua !
        else:
            self.space_press_count = 0


    def take_damage(self, amount=1, source=None):
        """
        Reduce la cantidad de vidas del jugador
        """
        self.current_lives -= amount
        if self.current_lives <= 0:
            self.current_lives = 0
            print("Game over")

        """
        Retroceso tras recibir daño
        """
        if source:
            dx = self.x - source.x
            dy = self.y - source.y

            if abs(dx) > abs(dy):
                self.x += 30 if dx > 0 else -30
            else:
                self.y += 30 if dy > 0 else -30


    def draw_water_bar(self, screen):
        """
        Dibuja la barra de agua disponible
        """
        bar_width = 200
        bar_height = 20
        bar_x = 10
        bar_y = 10 + (7 * (SPRITE_SCALE - 2)) + 10

        pygame.draw.rect(screen, (255, 0, 0), (bar_x, bar_y, bar_width, bar_height))
        water_percentage = self.water / PLAYER_INITIAL_WATER
        pygame.draw.rect(screen, (116,204,244), (bar_x, bar_y, bar_width * water_percentage, bar_height))


    def update(self, dt, keys):
        """
        Actualizar estado del jugador
        """
        dx, dy = 0, 0
        previous_running = self.is_running      # detecta cambios de estado
        self.is_running = False

        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            dx += self.speed
            self.direction = 0
            self.is_running = True

        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            dx -= self.speed
            self.direction = 3
            self.is_running = True
        
        if keys[pygame.K_DOWN] or keys[pygame.K_s]:
            dy += self.speed
            if dx == 0:
                self.direction = 1
            self.is_running = True
        
        if keys[pygame.K_UP] or keys[pygame.K_w]:
            dy -= self.speed
            if dx == 0:
                self.direction = 2
            self.is_running = True

        
        # Normalizar velocidad diagonal -> dx**2 + dy**2 = 1
        if dx != 0 and dy != 0:
            diagonal_scale = 1 / (2 ** 0.5)
            dx *= diagonal_scale
            dy *= diagonal_scale
        
        self.x += dx
        self.y += dy

        # Animación
        self.animation_timer += dt
        frame_rate = 0.1 if self.is_running else 0.3
        
        if self.animation_timer >= frame_rate:
            current_sprites = self.run_sprites if self.is_running else self.idle_sprites
            max_frames = len(current_sprites[0])
            self.frame_index = (self.frame_index + 1) % max_frames
            self.animation_timer = 0

        if previous_running != self.is_running:
            self.frame_index = 0

    
    def draw(self, screen):
        """
        Dibuja al jugador en pantalla.
        """
        # Parpadeo de invulnerabilidad
        if self.invulnerable_timer > 0:
            self.blink_timer += 0.1
            if self.blink_timer >= 0.2:
                self.blink_state = not self.blink_state
                self.blink_timer = 0
            if not self.blink_state:
                return

        current_sprites = self.run_sprites if self.is_running else self.idle_sprites
        flipped = self.direction == 3  # Invertir para la izquierda
        sprite = self.get_sprite(current_sprites[0] if flipped else current_sprites[self.direction], self.frame_index, flipped)

        screen.blit(sprite, (self.x, self.y))

        self.draw_collision_box(screen)


    def draw_lives(self, screen):
        """
        Dibuja los corazones de vida en pantalla
        """
        heart_spacing = 10 * (SPRITE_SCALE - 2)
        for i in range(self.current_lives):
            x = 10 + i * heart_spacing
            y = 10
            screen.blit(self.heart_sprite, (x, y))
        