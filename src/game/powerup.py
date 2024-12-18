"""
Potenciadores

- Recarga de agua
- Aumentar una vida
- Aumentar velocidad
- Escudo de invencibilidad
"""

import pygame
from src.core.utils import load_image
from src.core.settings import SPRITE_SCALE, PLAYER_INITIAL_WATER, POWERUP_SPEED_MULTIPLIER, POWERUP_DURATION


class PowerUp:
    def __init__(self, x, y, image_path):
        """
        Inicializa el power-up en una posición específica
        """
        self.x = x
        self.y = y
        self.width = 16 * (SPRITE_SCALE)
        self.height = 16 * (SPRITE_SCALE)
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
        super().__init__(x, y, "powerups/water_bucket.png")

    def apply_effect(self, player):
        """
        Llena la barra de agua del jugador al máximo
        """
        if self.is_active:
            player.water = PLAYER_INITIAL_WATER
            self.is_active = False


class ExtraLifePowerUp(PowerUp):
    def __init__(self, x, y):
        super().__init__(x, y, "powerups/extra_heart.png")

    def apply_effect(self, player):
        """
        Aumenta la vida del jugador, hasta el máximo permitido
        """
        if self.is_active and player.current_lives < player.max_lives:
            player.current_lives += 1
            self.is_active = False


class SpeedBoostPowerUp(PowerUp):
    def __init__(self, x, y):
        super().__init__(x, y, "powerups/coffee.png")
        self.duration = POWERUP_DURATION

    def apply_effect(self, player):
        """
        Incrementa temporalmente la velocidad del jugador
        """
        if self.is_active:
            player.speed *= POWERUP_SPEED_MULTIPLIER
            player.powerup_timer = self.duration
            self.is_active = False


class ShieldPowerUp(PowerUp):
    def __init__(self, x, y):
        """
        Inicializa el power-up de escudo
        """
        super().__init__(x, y, "powerups/shield.png")

    def apply_effect(self, player):
        """
        Aplica el efecto del escudo: invulnerabilidad temporal
        """
        if self.is_active:
            player.invulnerable_timer = POWERUP_DURATION
            self.is_active = False
