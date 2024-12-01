"""
Mecánicas del fuego

- Estado inicial
- Interacción con el jugador
"""

import random
import pygame
from src.core.settings import SCREEN_WIDTH, SCREEN_HEIGHT

class Fire:
    def __init__(self, x, y, size=20):
        self.x = x
        self.y = y
        self.size = size
        self.color = (255, 0, 0)  # Rojo

    def draw(self, screen):
        """Dibuja el fuego en pantalla."""
        pygame.draw.rect(screen, self.color, (self.x, self.y, self.size, self.size))

    @staticmethod
    def spawn_random_fires(amount):
        """Genera una lista de fuegos en posiciones aleatorias."""
        fires = []
        for _ in range(amount):
            x = random.randint(0, SCREEN_WIDTH - 20)  # Evitar salir del borde
            y = random.randint(0, SCREEN_HEIGHT - 20)
            fires.append(Fire(x, y))
        return fires
