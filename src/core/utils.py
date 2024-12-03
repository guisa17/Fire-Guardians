"""
Gestión de controles
"""

import pygame
import os
import random
import math
from src.core.settings import SCREEN_HEIGHT, SCREEN_WIDTH


def load_image(path, scale=None):
    full_path = os.path.join("assets", "images", path)
    if not os.path.exists(full_path):
        raise FileNotFoundError(f"No se encontró la imagen en {full_path}")
    image = pygame.image.load(full_path).convert_alpha()
    if scale:
        image = pygame.transform.scale(image, scale)
    return image


def load_sound(path):
    full_path = os.path.join("assets", "sounds", path)
    if not os.path.exists(full_path):
        raise FileNotFoundError(f"No se encontró el sonido en {full_path}")
    return pygame.mixer.Sound(full_path)


def draw_text(screen, text, font_path, size, color, x, y):
    full_path = os.path.join("assets", "fonts", font_path)
    if not os.path.exists(full_path):
        raise FileNotFoundError(f"No se encontró la fuente en {full_path}")
    font = pygame.font.Font(full_path, size)
    text_surface = font.render(text, True, color)
    screen.blit(text_surface, (x, y))


def generate_random_fire(num_fires, fire_width, fire_height, padding=20, player_position=(0, 0), min_distance=100):
    positions = []
    player_x, player_y = player_position

    for _ in range(num_fires):
        while True:
            x = random.randint(padding, SCREEN_WIDTH - fire_width - padding)
            y = random.randint(padding, SCREEN_HEIGHT - fire_height - padding)
            
            distance = math.sqrt((x - player_x) ** 2 + (y - player_y) ** 2)

            if distance >= min_distance:
                positions.append((x, y))
                break

    return positions
