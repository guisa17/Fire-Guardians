"""
Gestión de controles
"""

import pygame
import os


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

def draw_status(screen, player):
    font = pygame.font.Font(None, 36)
    score_text = font.render(f"Puntaje: {player.score}", True, (255, 255, 255))
    water_text = font.render(f"Agua: {player.water}", True, (255, 255, 255))
    screen.blit(score_text, (10, 10))
    screen.blit(water_text, (10, 50))
