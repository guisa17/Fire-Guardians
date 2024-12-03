"""
Mecánicas del fuego

- Estado inicial
- Interacción con el jugador
"""

import pygame
from src.core.utils import load_image
from src.core.settings import SPRITE_SCALE


class Fire:
    def __init__(self, x, y):
        """
        Inicialización del fuego en posiciones específicas
        """
        self.x = x
        self.y = y
        self.intensity = 100    # vida del fuego

        self.current_frame = 0
        self.animation_timer = 0
        self.frame_duration = 0.2
        self.is_active = True

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
            self.intensity -= amount
            if self.intensity <= 0:
                self.is_active = False  # se apaga

    
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
            bar_width = 32 * SPRITE_SCALE // 6
            bar_height = 6
            progress = self.intensity / 100
            pygame.draw.rect(screen, (255, 0, 0), (self.x + 32, self.y - 10, bar_width, bar_height))
            pygame.draw.rect(screen, (0, 255, 0), (self.x + 32, self.y - 10, bar_width * progress, bar_height))

            self.draw_collision_box(screen)

    