import pygame
import random
from src.core.settings import SCREEN_WIDTH, SCREEN_HEIGHT

class Fire:
    def __init__(self, x, y, size=20):
        self.x = x
        self.y = y
        self.size = size
        self.color = (255, 0, 0)  # Rojo
        self.extinguished = False  # Estado del fuego

    def draw(self, screen):
        """Dibuja el fuego si no ha sido apagado."""
        if not self.extinguished:
            pygame.draw.rect(screen, self.color, (self.x, self.y, self.size, self.size))

    def is_extinguished_by(self, player):
        """Verifica si el fuego está siendo apagado por el jugador."""
        player_rect = pygame.Rect(player.x, player.y, player.run_sprites[0][0].get_width(), player.run_sprites[0][0].get_height())
        fire_rect = pygame.Rect(self.x, self.y, self.size, self.size)

        if fire_rect.colliderect(player_rect) and player.water > 0:
            self.extinguished = True
            return True
        return False

    @staticmethod
    def spawn_random_fires(amount):
        """Genera una lista de fuegos en posiciones aleatorias."""
        fires = []
        for _ in range(amount):
            x = random.randint(0, SCREEN_WIDTH - 20)
            y = random.randint(0, SCREEN_HEIGHT - 20)
            fires.append(Fire(x, y))
        return fires
