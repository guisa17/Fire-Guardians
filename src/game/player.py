"""
Controles del jugador

- Movimientos básicos
- Animaciones
- Tanque de agua
"""

import pygame

class Player:
    def __init__(self):
        self.x = 100
        self.y = 100
        self.size = 30
        self.color = (0, 0, 255)  # Azul
        self.speed = 5

    def move(self, keys):
        """Controla el movimiento del jugador."""
        if keys[pygame.K_UP]:
            self.y -= self.speed
        if keys[pygame.K_DOWN]:
            self.y += self.speed
        if keys[pygame.K_LEFT]:
            self.x -= self.speed
        if keys[pygame.K_RIGHT]:
            self.x += self.speed

    def draw(self, screen):
        """Dibuja el jugador en pantalla."""
        pygame.draw.rect(screen, self.color, (self.x, self.y, self.size, self.size))
