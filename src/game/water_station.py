"""
Mecánica de estación de agua
"""

import pygame
from src.core.utils import load_image
from src.core.settings import SPRITE_SCALE


class WaterStation:
    def __init__(self, x, y):
        """
        Inicialización del punto de recarga de agua
        """
        self.x = x
        self.y = y
        self.width = 16 * SPRITE_SCALE
        self.height = 16 * SPRITE_SCALE
        self.sprite = load_image("hydrant/hydrant.png")
        self.sprite = pygame.transform.scale(self.sprite, (self.width, self.height))
    

    def get_rect(self):
        """
        Rectángulo de colisión
        """
        return pygame.Rect(self.x, self.y, self.width, self.height)
    

    # TMP !
    def draw_collision_box(self, screen):
        """
        Dibujar rectángulo de colisión
        """
        collision_rect = self.get_rect()
        pygame.draw.rect(screen, (255, 0, 0), collision_rect, 1)


    def draw(self, screen):
        """
        Dibujar hidrante en pantalla
        """
        screen.blit(self.sprite, (self.x, self.y))
        self.draw_collision_box(screen)
