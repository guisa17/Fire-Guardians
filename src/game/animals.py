"""
Animales Rescatables

- Oso de Anteojos
"""

import pygame
from src.core.utils import load_image
from src.core.settings import SPRITE_SCALE


class Bear:
    def __init__(self, x, y):
        """
        Inicialización del Oso de Anteojos en una posición específica.
        """
        self.x = x
        self.y = y
        self.life = 200  # El doble de vida que el fuego
        self.is_rescued = False

        self.current_frame = 0
        self.animation_timer = 0
        self.frame_duration = 0.3
        self.frames = self.load_spritesheet("animals/bear.png", 4)

        self.is_active = True


    def load_spritesheet(self, path, frame_count):
        """
        Carga el spritesheet y divide los frames.
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
        Devuelve el rectángulo de colisión del oso.
        """
        collision_width = 20 * SPRITE_SCALE
        collision_height = 20 * SPRITE_SCALE
        return pygame.Rect(self.x, self.y, collision_width, collision_height)


    def rescue(self, amount):
        """
        Reduce la vida del oso hasta que sea rescatado.
        """
        if self.is_active:
            self.life -= amount
            if self.life <= 0:
                self.life = 0
                self.is_active = False


    def update(self, dt):
        """
        Actualiza la animación del oso.
        """
        if not self.is_rescued:
            self.animation_timer += dt
            if self.animation_timer >= self.frame_duration:
                self.animation_timer = 0
                self.current_frame = (self.current_frame + 1) % len(self.frames)


    def draw(self, screen):
        """
        Dibuja el oso en pantalla.
        """
        if self.is_active:
            screen.blit(self.frames[self.current_frame], (self.x, self.y))

            # Barra de progreso para el rescate
            bar_width = 32 * SPRITE_SCALE // 6
            bar_height = 6
            progress = self.life / 200
            pygame.draw.rect(screen, (255, 0, 0), (self.x + 32, self.y - 10, bar_width, bar_height))
            pygame.draw.rect(screen, (0, 255, 0), (self.x + 32, self.y - 10, bar_width * progress, bar_height))


class Monkey:
    def __init__(self, x, y):
        """
        Inicialización del Mono Choro de Cola Amarilla en una posición específica.
        """
        self.x = x
        self.y = y
        self.life = 150  # Vida ajustada, menor que el oso pero significativa
        self.is_rescued = False

        self.current_frame = 0
        self.animation_timer = 0
        self.frame_duration = 0.3
        self.frames = self.load_spritesheet("animals/monkey.png", 4)  # Ajusta el número de frames según el spritesheet

        self.is_active = True

    def load_spritesheet(self, path, frame_count):
        """
        Carga el spritesheet y divide los frames.
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
        Devuelve el rectángulo de colisión del mono.
        """
        collision_width = 16 * SPRITE_SCALE
        collision_height = 16 * SPRITE_SCALE
        return pygame.Rect(self.x, self.y, collision_width, collision_height)

    def rescue(self, amount):
        """
        Reduce la vida del mono hasta que sea rescatado.
        """
        if self.is_active:
            self.life -= amount
            if self.life <= 0:
                self.life = 0
                self.is_active = False

    def update(self, dt):
        """
        Actualiza la animación del mono.
        """
        if not self.is_rescued:
            self.animation_timer += dt
            if self.animation_timer >= self.frame_duration:
                self.animation_timer = 0
                self.current_frame = (self.current_frame + 1) % len(self.frames)

    def draw(self, screen):
        """
        Dibuja el mono en pantalla.
        """
        if self.is_active:
            screen.blit(self.frames[self.current_frame], (self.x, self.y))

            # Barra de progreso para el rescate
            bar_width = 32 * SPRITE_SCALE // 6
            bar_height = 6
            progress = self.life / 150
            pygame.draw.rect(screen, (255, 0, 0), (self.x + 32, self.y - 10, bar_width, bar_height))
            pygame.draw.rect(screen, (0, 255, 0), (self.x + 32, self.y - 10, bar_width * progress, bar_height))


class Bird:
    def __init__(self, x, y):
        """
        Inicialización del ave verde en una posición específica.
        """
        self.x = x
        self.y = y
        self.life = 150  # Menor vida que el oso para equilibrar
        self.is_rescued = False

        self.current_frame = 0
        self.animation_timer = 0
        self.frame_duration = 0.2
        self.frames = self.load_spritesheet("animals/bird.png", 4)

        self.is_active = True


    def load_spritesheet(self, path, frame_count):
        """
        Carga el spritesheet y divide los frames.
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
        Devuelve el rectángulo de colisión del ave.
        """
        collision_width = 14 * SPRITE_SCALE
        collision_height = 14 * SPRITE_SCALE
        return pygame.Rect(self.x, self.y, collision_width, collision_height)


    def rescue(self, amount):
        """
        Reduce la vida del ave hasta que sea rescatada.
        """
        if self.is_active:
            self.life -= amount
            if self.life <= 0:
                self.life = 0
                self.is_active = False


    def update(self, dt):
        """
        Actualiza la animación del ave.
        """
        if not self.is_rescued:
            self.animation_timer += dt
            if self.animation_timer >= self.frame_duration:
                self.animation_timer = 0
                self.current_frame = (self.current_frame + 1) % len(self.frames)


    def draw(self, screen):
        """
        Dibuja el ave en pantalla.
        """
        if self.is_active:
            screen.blit(self.frames[self.current_frame], (self.x, self.y))

            # Barra de progreso para el rescate
            bar_width = 30 * SPRITE_SCALE // 6
            bar_height = 6
            progress = self.life / 150
            pygame.draw.rect(screen, (255, 0, 0), (self.x + 20, self.y - 10, bar_width, bar_height))
            pygame.draw.rect(screen, (0, 255, 0), (self.x + 20, self.y - 10, bar_width * progress, bar_height))