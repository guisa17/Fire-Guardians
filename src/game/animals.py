"""
Animales Rescatables

- Oso de Anteojos
- Mono de Cola Amarilla
- Colibrí / Ave de la Selva
"""

import pygame
from src.core.utils import load_image
from src.core.settings import SPRITE_SCALE
from src.game.powerup import ShieldPowerUp, WaterRefillPowerUp, SpeedBoostPowerUp


class Animal:
    def __init__(self, x, y, life, sprite_path, frame_count, sprite_size, spawn_time=0, powerup_class=None):
        """
        Inicialización base para los animales.
        """
        self.x = x
        self.y = y
        self.life = life
        self.max_life = life

        self.current_frame = 0
        self.animation_timer = 0
        self.frame_duration = 0.3
        self.frames = self.load_spritesheet(sprite_path, frame_count, sprite_size)

        self.sprite_width, self.sprite_height = sprite_size
        self.is_active = True
        self.is_rescued = False
        self.has_been_rescued = False
        self.spawn_time = spawn_time

        # Animación de salvado
        self.heart_frames = self.load_spritesheet("animals/saved.png", 3, (16, 16))
        self.heart_timer = 0
        self.heart_duration = 1
        self.show_heart = False

        # Drop de powerup
        self.notify_powerup = False
        self.powerup_class = powerup_class


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
                self.is_rescued = True
                self.show_heart = True
                self.heart_timer = 0


    def update(self, dt):
        """
        Actualiza la animación del animal.
        """
        if self.is_active:
            self.animation_timer += dt
            if self.animation_timer >= self.frame_duration:
                self.animation_timer = 0
                self.current_frame = (self.current_frame + 1) % len(self.frames)
        
        if self.show_heart and self.is_rescued:
            self.heart_timer += dt
            if self.heart_timer >= self.heart_duration:
                self.show_heart = False
                self.is_rescued = False
                self.has_been_rescued = True
                                

    def draw(self, screen):
        """
        Dibuja el animal en pantalla.
        """
        if self.show_heart and self.is_rescued:
            heart_frame = int((self.heart_timer / self.heart_duration) * len(self.heart_frames))
            heart_frame = min(heart_frame, len(self.heart_frames) - 1)
            heart_sprite = self.heart_frames[heart_frame]
            screen.blit(heart_sprite, (self.x, self.y - 20))
        
        elif self.is_active:
            screen.blit(self.frames[self.current_frame], (self.x, self.y))

            # Barra de progreso para el rescate
            bar_width = self.sprite_width * SPRITE_SCALE // 2
            bar_height = 6
            progress = self.life / self.max_life
            pygame.draw.rect(screen, (147, 177, 38), (self.x + self.sprite_width - 8, self.y - 10, bar_width, bar_height))
            pygame.draw.rect(screen, (120, 44, 115), (self.x + self.sprite_width - 8, self.y - 10, bar_width * progress, bar_height))


class Bear(Animal):
    def __init__(self, x, y, spawn_time=0):
        super().__init__(x, y, 200, "animals/bear.png", 4, (20, 20), spawn_time, ShieldPowerUp)


class Monkey(Animal):
    def __init__(self, x, y, spawn_time=0):
        super().__init__(x, y, 150, "animals/monkey.png", 4, (16, 16), spawn_time, SpeedBoostPowerUp)


class Bird(Animal):
    def __init__(self, x, y, spawn_time=0):
        super().__init__(x, y, 150, "animals/bird.png", 4, (14, 14), spawn_time, WaterRefillPowerUp)
