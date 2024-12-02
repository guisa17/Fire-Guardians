import pygame
import random
from src.core.settings import SCREEN_WIDTH, SCREEN_HEIGHT
from src.core.utils import load_image

class Fire:
    def __init__(self, x, y, size=60):
        self.x = x
        self.y = y
        self.size = size
        self.extinguished = False  # Estado del fuego
        self.player_in_fire_time = 0  # Tiempo acumulado con el jugador dentro del fuego
        self.animation_timer = 0
        self.frame_index = 0

        # Cargar los sprites del fuego
        self.sprites = self.load_spritesheet("items/fire/fire_sprite.png", 8, 4)

    def load_spritesheet(self, path, cols, rows):
        """
        Divide el spritesheet en subimágenes individuales.
        """
        spritesheet = load_image(path)
        sheet_width, sheet_height = spritesheet.get_size()
        sprite_width = sheet_width // cols
        sprite_height = sheet_height // rows

        sprites = []
        for row in range(rows):
            for col in range(cols):
                x = col * sprite_width
                y = row * sprite_height
                sprite = spritesheet.subsurface(pygame.Rect(x, y, sprite_width, sprite_height))
                sprite = pygame.transform.scale(sprite, (self.size, self.size))
                sprites.append(sprite)
        return sprites

    def update(self, dt):
        """
        Actualiza el índice de animación para crear el efecto animado.
        """
        if not self.extinguished:
            self.animation_timer += dt
            if self.animation_timer >= 0.03:  # Cambiar el frame cada 0.1 segundos
                self.frame_index = (self.frame_index + 1) % len(self.sprites)
                self.animation_timer = 0

    def draw(self, screen):
        """
        Dibuja el fuego animado si no está apagado.
        """
        if not self.extinguished:
            current_sprite = self.sprites[self.frame_index]
            screen.blit(current_sprite, (self.x, self.y))

    def is_extinguished_by(self, player):
        """
        Verifica si el fuego está siendo apagado por el jugador.
        """
        player_rect = pygame.Rect(
            player.x, player.y, player.run_sprites[0][0].get_width(), player.run_sprites[0][0].get_height()
        )
        fire_rect = pygame.Rect(self.x, self.y, self.size, self.size)

        # Verificar colisión y que el jugador tenga suficiente agua
        if fire_rect.colliderect(player_rect) and player.water > 0 and not self.extinguished:
            self.extinguished = True
            return True
        return False

    def check_player_in_fire(self, player, dt):
        """
        Detecta si el jugador está dentro del fuego y actualiza el temporizador.
        Reduce la vida del jugador si ha estado dentro del área por más de 1 segundo.
        """
        player_rect = pygame.Rect(
            player.x, player.y, player.run_sprites[0][0].get_width(), player.run_sprites[0][0].get_height()
        )
        fire_rect = pygame.Rect(self.x, self.y, self.size, self.size)

        if fire_rect.colliderect(player_rect) and not self.extinguished:
            self.player_in_fire_time += dt
            if self.player_in_fire_time >= 1.0:  # 1 segundo
                player.life -= 10
                self.player_in_fire_time = 0  # Reinicia el temporizador
        else:
            self.player_in_fire_time = 0  # Reinicia si el jugador no está en el fuego

    @staticmethod
    def spawn_random_fires(amount):
        """
        Genera una lista de fuegos en posiciones aleatorias.
        """
        fires = []
        for _ in range(amount):
            x = random.randint(0, SCREEN_WIDTH - 16)
            y = random.randint(0, SCREEN_HEIGHT - 16)
            fires.append(Fire(x, y))
        return fires
