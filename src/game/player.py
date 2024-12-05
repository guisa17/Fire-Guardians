"""
Controles del jugador

- Movimientos básicos
- Animaciones
- Tanque de agua
"""

import pygame
from src.core.utils import load_image
from src.core.settings import PLAYER_SPEED, PLAYER_INITIAL_WATER, SPRITE_SCALE, SCREEN_HEIGHT, SCREEN_WIDTH
from src.game.level_loader import load_level, is_tile_walkable


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

        self.powerup_timer = 0
        
        self.time_left = 61
        self.total_time = 61

        self.space_press_count = 0      # interacciones con spacebar

        """
        Carga de sprites
        """
        self.idle_sprites = self.load_spritesheet("player/idle.png", 4, 3)
        self.run_sprites = self.load_spritesheet("player/run.png", 8, 3)
        self.clock_icon = load_image("hud/clock.png")
        self.clock_icon = pygame.transform.scale(self.clock_icon, (11 * (SPRITE_SCALE), 11 * (SPRITE_SCALE)))

    
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


    def handle_collision(self, fires, dt, level_data, tile_size):
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
                
                if self.collision_timer >= 0.3:     # damage timer
                    self.take_damage(1, fire, level_data, tile_size)
                    self.invulnerable_timer = 1
                    self.collision_timer = 0
                    break
        
        if not collided:
            self.collision_timer = 0


    def is_within_distance(self, rect1, rect2, interaction_dist):
        cx1, cy1 = rect1.center
        cx2, cy2 = rect2.center
        return abs(cx1 - cx2) < interaction_dist and abs(cy1 - cy2) < interaction_dist


    def interact_with_fire(self, fires, keys, interaction_dist=60):
        """
        Interactuar con fuego
        """
        if keys[pygame.K_SPACE]:
            for fire in fires:
                right_dist = self.is_within_distance(self.get_rect(), fire.get_rect(), interaction_dist)
                if fire.is_active and right_dist:
                    if self.water > 0:
                        if self.space_press_count < 1:
                            self.space_press_count += 1
                            fire.extinguish(15)
                            self.water -= 3     # diminuye agua !
        else:
            self.space_press_count = 0


    def take_damage(self, amount=1, source=None, level_data=None, tile_size=None):
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
        if source and level_data and tile_size:
            # Dirección del retroceso
            dx = self.x - source.x
            dy = self.y - source.y

            offset = 50  # Distancia de retroceso
            new_x, new_y = self.x, self.y

            if abs(dx) > abs(dy):
                new_x += offset if dx > 0 else -offset
            else:
                new_y += offset if dy > 0 else -offset

            # Verificar si la nueva posición es walkable
            future_rect = self.get_rect().move(new_x - self.x, new_y - self.y)
            if is_tile_walkable(level_data, future_rect, tile_size):
                self.x, self.y = new_x, new_y


    def recharge_water(self, water_stations, keys, recharge_rate=20, dt=1, interaction_dist=60):
        """
        Recargar agua con "R" presionado
        """
        if keys[pygame.K_r]:
            for station in water_stations:
                right_dist = self.is_within_distance(self.get_rect(), station.get_rect(), interaction_dist)

                if right_dist:
                    if self.water < PLAYER_INITIAL_WATER:
                        self.water += recharge_rate * dt
                        if self.water > PLAYER_INITIAL_WATER:
                            self.water = PLAYER_INITIAL_WATER
    

    def interact_with_powerups(self, powerups):
        """
        Interactúa con los powerups disponibles
        """
        for powerup in powerups:
            if powerup.is_active and self.get_rect().colliderect(powerup.get_rect()):
                powerup.apply_effect(self)


    def interact_with_animals(self, animals, keys, interaction_dist=100):
        """
        Interactúa con los animales para rescatarlos
        """
        for animal in animals:
            if animal.is_active:
                player_cx, player_cy = self.get_rect().center
                animal_cx, animal_cy = animal.get_rect().center

                distance_x = abs(player_cx - animal_cx)
                distance_y = abs(player_cy - animal_cy)

                if distance_x < interaction_dist and distance_y < interaction_dist:
                    if keys[pygame.K_z] and keys[pygame.K_x]:  # ambas teclas
                        animal.rescue(3)


    def handle_animal_collision(self, animals, dx, dy):
        """
        Maneja la colisión entre el jugador y los animales.
        """
        for animal in animals:
            if animal.is_active and self.get_rect().move(dx, dy).colliderect(animal.get_rect()):
                dx, dy = 0, 0
        return dx, dy


    def update(self, dt, keys, level_data, tile_size, water_stations=None, animals=None):
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
        
        # Prevenir colisiones con la estación de agua
        for station in water_stations:
            if station is not None:
                future_rect = self.get_rect().move(dx, dy)
                if future_rect.colliderect(station.get_rect()):
                    dx, dy = 0, 0
        
        # Colisión con los animales
        if animals is not None:
            dx, dy = self.handle_animal_collision(animals, dx, dy)

        # Rectángulo de colisión actual
        current_rect = self.get_rect()

        # Verificar movimiento horizontal
        future_rect_x = current_rect.move(dx, 0)  # Solo mover horizontalmente
        if is_tile_walkable(level_data, future_rect_x, tile_size):
            self.x += dx
        else:
            dx = 0

        # Verificar movimiento vertical
        future_rect_y = current_rect.move(0, dy)  # Solo mover verticalmente
        if is_tile_walkable(level_data, future_rect_y, tile_size):
            self.y += dy
        else:
            dy = 0

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
        
        # Reducir temporizador del power-up de velocidad
        if self.powerup_timer > 0:
            self.powerup_timer -= dt
            if self.powerup_timer <= 0:
                self.speed = PLAYER_SPEED

    
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

        # self.draw_collision_box(screen)


    def draw_hud(self, screen):
        """
        Dibuja el HUD con las barras de vida y agua.
        """
        # Coordenadas iniciales y tamaños
        icon_size = 7 * (SPRITE_SCALE + 1)  # Tamaño del ícono con escala
        bar_width = 35 * (SPRITE_SCALE + 1)
        bar_height = 5 * (SPRITE_SCALE + 1)
        bar_inner_width = 33 * (SPRITE_SCALE + 1)
        bar_inner_height = 3 * (SPRITE_SCALE + 1)
        time_bar_width = bar_width * 4

        # Colores
        border_color = (0, 0, 0)
        empty_color = (69, 61, 69)
        life_color = (237, 28, 36)
        water_color = (112, 154, 209)
        time_color = (147, 177, 38) if self.time_left >= 10 else (188, 51, 74)

        # Cargar íconos
        heart_icon = load_image("hud/heart.png")
        heart_icon = pygame.transform.scale(heart_icon, (icon_size, icon_size))

        drop_icon = load_image("hud/drop.png")
        drop_icon = pygame.transform.scale(drop_icon, (icon_size, icon_size))

        # Coordenadas del HUD
        hud_x = 10
        hud_y = 10
        hud_time_icon_x = SCREEN_WIDTH - (icon_size + 10)
        hud_time_bar_x = hud_time_icon_x - (time_bar_width + 15)

        # Dibujar barra de vida
        screen.blit(heart_icon, (hud_x, hud_y))
        self.draw_progress_bar(
            screen,
            hud_x + icon_size + 15,
            hud_y + (icon_size - bar_height) // 2,
            bar_width,
            bar_height,
            bar_inner_width,
            bar_inner_height,
            self.current_lives / self.max_lives,
            life_color,
            empty_color,
            border_color
        )

        # Dibujar barra de agua
        screen.blit(drop_icon, (hud_x, hud_y + icon_size + 10))  # Debajo de la vida
        self.draw_progress_bar(
            screen,
            hud_x + icon_size + 15,
            hud_y + icon_size + 10 + (icon_size - bar_height) // 2,
            bar_width,
            bar_height,
            bar_inner_width,
            bar_inner_height,
            self.water / PLAYER_INITIAL_WATER,
            water_color,
            empty_color,
            border_color
        )

        # Dibujar barra de tiempo
        screen.blit(self.clock_icon, (hud_time_icon_x, hud_y - 5))
        self.draw_progress_bar(
            screen,
            hud_time_bar_x,
            hud_y + (icon_size - bar_height) // 2,
            time_bar_width,
            bar_height,
            time_bar_width - 2 * SPRITE_SCALE,
            bar_inner_height,
            self.time_left / self.total_time,
            time_color,
            empty_color,
            border_color
        )


    def draw_progress_bar(self, screen, x, y, bar_width, bar_height, inner_width, inner_height, progress, fill_color, empty_color, border_color):
        # Dibujar borde negro de la barra
        pygame.draw.rect(screen, border_color, (x, y, bar_width, bar_height))

        # Dibujar parte vacía 
        pygame.draw.rect(
            screen,
            empty_color,
            (x + 1 * SPRITE_SCALE, y + 1 * SPRITE_SCALE, inner_width, inner_height)
        )

        # Dibujar parte llena
        pygame.draw.rect(
            screen,
            fill_color,
            (x + 1 * SPRITE_SCALE, y + 1 * SPRITE_SCALE, int(inner_width * progress), inner_height)
        )

