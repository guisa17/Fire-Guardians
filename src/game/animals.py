"""
Animales Rescatables

- Oso de Anteojos
- Mono de Cola Amarilla
- Colibrí / Ave de la Selva
"""

import pygame
from src.core.utils import load_image
from src.core.settings import SPRITE_SCALE


class Animal:
    def __init__(self, x, y, life, sprite_path, frame_count, sprite_size):
        """
        Inicialización base para los animales.
        """
        self.x = x
        self.y = y
        self.life = life
        self.max_life = life
        self.is_rescued = False

        self.current_frame = 0
        self.animation_timer = 0
        self.frame_duration = 0.3
        self.frames = self.load_spritesheet(sprite_path, frame_count, sprite_size)

        self.sprite_width, self.sprite_height = sprite_size
        self.is_active = True


    def load_spritesheet(self, path, frame_count, sprite_size):
        """
        Carga el spritesheet y divide los frames.
        """
        spritesheet = load_image(path)
        sheet_width, sheet_height = spritesheet.get_size()
        frame_width = sprite_size[0]
        frame_height = sprite_size[1]

        frames = []
        for i in range(frame_count):
            frame = spritesheet.subsurface(pygame.Rect(i * frame_width, 0, frame_width, frame_height))
            frame = pygame.transform.scale(frame, (frame_width * SPRITE_SCALE, frame_height * SPRITE_SCALE))
            frames.append(frame)

        return frames


    def get_rect(self):
        """
        Devuelve el rectángulo de colisión del animal.
        """
        collision_width = self.sprite_width * SPRITE_SCALE
        collision_height = self.sprite_height * SPRITE_SCALE
        return pygame.Rect(self.x, self.y, collision_width, collision_height)


    def rescue(self, amount):
        """
        Reduce la vida del animal hasta que sea rescatado.
        """
        if self.is_active:
            self.life -= amount
            if self.life <= 0:
                self.life = 0
                self.is_active = False
                print("rescued")


    def update(self, dt):
        """
        Actualiza la animación del animal.
        """
        if self.is_active:
            self.animation_timer += dt
            if self.animation_timer >= self.frame_duration:
                self.animation_timer = 0
                self.current_frame = (self.current_frame + 1) % len(self.frames)


    def draw(self, screen):
        """
        Dibuja el animal en pantalla.
        """
        if self.is_active:
            screen.blit(self.frames[self.current_frame], (self.x, self.y))

            # Barra de progreso para el rescate
            bar_width = self.sprite_width * SPRITE_SCALE // 3
            bar_height = 6
            progress = self.life / self.max_life
            pygame.draw.rect(screen, (255, 0, 0), (self.x + self.sprite_width, self.y - 10, bar_width, bar_height))
            pygame.draw.rect(screen, (0, 255, 0), (self.x + self.sprite_width, self.y - 10, bar_width * progress, bar_height))


class Bear(Animal):
    def __init__(self, x, y):
        super().__init__(x, y, 200, "animals/bear.png", 4, (20, 20))


class Monkey(Animal):
    def __init__(self, x, y):
        super().__init__(x, y, 150, "animals/monkey.png", 4, (16, 16))


class Bird(Animal):
    def __init__(self, x, y):
        super().__init__(x, y, 150, "animals/bird.png", 4, (14, 14))
