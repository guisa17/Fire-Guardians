"""
Potenciadores

- Recarga de agua
- Aumentar una vida
- Aumentar velocidad
- Escudo de invencibilidad
"""

import pygame
from src.core.utils import load_image
from src.core.settings import SPRITE_SCALE, PLAYER_INITIAL_WATER


class PowerUp:
    def __init__(self, x, y, image_path):
        """
        Inicializa el power-up en una posición específica
        """
        self.x = x
        self.y = y
        self.width = 16 * (SPRITE_SCALE - 2)
        self.height = 16 * (SPRITE_SCALE - 2)
        self.sprite = load_image(image_path)
        self.sprite = pygame.transform.scale(self.sprite, (self.width, self.height))
        self.is_active = True  # power-up está disponible


    def get_rect(self):
        """
        Devuelve el rectángulo de colisión.
        """
        return pygame.Rect(self.x, self.y, self.width, self.height)


    def apply_effect(self, player):
        """
        Aplica el efecto del power-up al jugador
        Debe ser implementado por las subclases.
        """
        raise NotImplementedError("Este método debe ser implementado en subclases")


    def draw(self, screen):
        """
        Dibuja el power-up en pantalla.
        """
        if self.is_active:
            screen.blit(self.sprite, (self.x, self.y))


class WaterRefillPowerUp(PowerUp):
    def __init__(self, x, y):
        super().__init__(x, y, "canteen/canteen.png")

    def apply_effect(self, player):
        """
        Llena la barra de agua del jugador al máximo
        """
        if self.is_active:
            player.water = PLAYER_INITIAL_WATER
            self.is_active = False


class ExtraLifePowerUp(PowerUp):
    def __init__(self, x, y):
        super().__init__(x, y, "heart/extra_heart.png")

    def apply_effect(self, player):
        """
        Aumenta la vida del jugador, hasta el máximo permitido
        """
        if self.is_active and player.current_lives < player.max_lives:
            player.current_lives += 1
            self.is_active = False
