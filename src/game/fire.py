"""
Mecánicas del fuego

- Estado inicial
- Interacción con el jugador
"""

import pygame
import random
from src.core.utils import load_image
from src.core.settings import SPRITE_SCALE
from src.game.level_loader import is_tile_walkable


class Fire:
    def __init__(self, x, y):
        """
        Inicialización del fuego en posiciones específicas
        """
        self.x = x
        self.y = y
        self.intensity = 100    # vida del fuego
        self.has_interacted = False

        self.current_frame = 0
        self.animation_timer = 0
        self.frame_duration = 0.2
        self.is_active = True

        self.time_to_spread = 5
        self.spread_timer = 0
        self.spread_radius = 50

        """
        Carga de sprites
        """
        self.frames = self.load_spritesheet("fire/fire.png", 4)

    
    def load_spritesheet(self, path, frame_count):
        """
        Dividir el spritesheet en sus respectivos sprites
        """
        spritesheet = load_image(path)
        sheet_width, sheet_height = spritesheet.get_size()
        frame_width = sheet_width // frame_count
        frame_height = sheet_height

        frames = []
        for i in range(frame_count):
            frame = spritesheet.subsurface(pygame.Rect(i * frame_width, 0, frame_width, frame_height))
            frame = pygame.transform.scale(frame, (frame_width * SPRITE_SCALE, frame_height * SPRITE_SCALE))
            frames.append(frame)
        
        return frames

    
    def get_rect(self):
        """
        Devuelve rectángulo de colisión
        """
        collision_width = 10 * SPRITE_SCALE
        collision_height = 10 * SPRITE_SCALE

        offset_x = 3 * SPRITE_SCALE
        offset_y = 6 * SPRITE_SCALE

        return pygame.Rect(
            self.x + offset_x,
            self.y + offset_y,
            collision_width,
            collision_height
        )


    def draw_collision_box(self, screen):
        """
        Dibujar rectángulo de colisión
        """
        collision_rect = self.get_rect()
        pygame.draw.rect(screen, (255, 0, 0), collision_rect, 1)


    def extinguish(self, amount):
        """
        Reducimos la intensidad del fuego con la interacción del jugador
        """
        if self.is_active:
            self.has_interacted = True
            self.intensity -= amount
            if self.intensity <= 0:
                self.is_active = False  # se apaga


    def spread(self, fire_list, max_fires, player, hydrants, level_data, tile_size, min_fire_distance=60):
        """
        Propaga el fuego si no se apaga a tiempo
        """
        if len(fire_list) >= max_fires:
            return
        
        hydrant_positions = {(hydrant.x, hydrant.y) for hydrant in hydrants}
        spread_attempts = 5

        for _ in range(spread_attempts):
            new_x = self.x + random.randint(-self.spread_radius, self.spread_radius)
            new_y = self.y + random.randint(-self.spread_radius, self.spread_radius)
            new_fire = Fire(new_x, new_y)

            player_dist_x = abs(new_x - player.x)
            player_dist_y = abs(new_y - player.y)
            
            if player_dist_x < 50 and player_dist_y < 50:
                continue
            
            close_to_fires = False
            for fire in fire_list:
                fire_dist_x = abs(new_x - fire.x)
                fire_dist_y = abs(new_y - fire.y)
                fire_dist = (fire_dist_x ** 2 + fire_dist_y ** 2) ** 0.5

                if fire_dist < min_fire_distance:
                    close_to_fires = True
                    break
            
            if close_to_fires:
                continue

            # Verificar que no se propague sobre un hidrante
            collides_with_hydrant = any(new_fire.get_rect().colliderect(hydrant.get_rect()) for hydrant in hydrants)
            if collides_with_hydrant:
                continue

            # Verificar que el nuevo fuego esté sobre un tile "walkable"
            fire_rect = new_fire.get_rect()
            if not is_tile_walkable(level_data, fire_rect, tile_size):
                continue

            fire_list.append(new_fire)
            break

    
    def update_spread(self, dt, fire_list, max_fires, player, hydrants, level_data, tile_size):
        """
        Actualizar temporizador de propagación
        """
        if not self.is_active:
            return

        self.spread_timer += dt
        if self.spread_timer >= self.time_to_spread:
            self.spread_timer = 0
            self.spread(fire_list, max_fires, player, hydrants, level_data, tile_size)

    
    def update(self, dt):
        """
        Actualizar animación del fuego
        """
        if not self.is_active:
            return
        
        self.animation_timer += dt
        if self.animation_timer >= self.frame_duration:
            self.animation_timer = 0
            self.current_frame = (self.current_frame + 1) % len(self.frames)
        

    def draw(self, screen):
        """
        Dibujar fuego en pantalla
        """
        if self.is_active:
            screen.blit(self.frames[self.current_frame], (self.x, self.y))

            # Barra de vida
            if self.has_interacted:
                bar_width = 32 * SPRITE_SCALE // 6
                bar_height = 6
                progress = self.intensity / 100
                pygame.draw.rect(screen, (188, 51, 74), (self.x + 16, self.y - 10, bar_width, bar_height))
                pygame.draw.rect(screen, (242, 188, 82), (self.x + 16, self.y - 10, bar_width * progress, bar_height))

            self.draw_collision_box(screen)
