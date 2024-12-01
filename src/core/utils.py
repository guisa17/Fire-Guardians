"""
Gestión de controles
"""

import pygame

def load_images(path):
    return pygame.image.load(path).convert_alpha()
