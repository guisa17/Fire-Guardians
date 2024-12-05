import json
import pygame
from src.editor import TILE_PROPERTIES

def load_level(filename):
    """
    Carga los datos del nivel desde un archivo JSON.
    """
    with open(filename, "r") as file:
        level_data = json.load(file)
    return level_data


def is_tile_walkable(level_data, rect, tile_size):
    """
    Verifica si todas las esquinas y el centro del rectángulo están sobre tiles "walkable"
    """
    # Obtener las coordenadas de las esquinas y el centro del rectángulo
    points_to_check = [
        (rect.left, rect.top),      # ^ <
        (rect.right, rect.top),     # ^ >
        (rect.left, rect.bottom),   # v <
        (rect.right, rect.bottom),  # v >
        (rect.centerx, rect.centery)  # Centro
    ]

    # Verificar si cada punto está en un tile "walkable"
    for x, y in points_to_check:
        tile_x = int(x // tile_size)
        tile_y = int(y // tile_size)

        # Verificar límites del nivel
        if 0 <= tile_x < len(level_data["level"][0]) and 0 <= tile_y < len(level_data["level"]):
            tile_id = level_data["level"][tile_y][tile_x]
            if not TILE_PROPERTIES.get(tile_id, {}).get("walkable", False):
                return False  # no es walkable
        else:
            return False  # fuera de los límites del nivel

    return True


def draw_tiles(screen, tiles, spritesheet, tile_size, scale, animation_timer):
    """
    Dibuja los tiles del nivel en la pantalla.
    """
    scaled_tile_size = tile_size * scale

    tree_frame = 5 if int(animation_timer * 2) % 2 == 0 else 6

    for row_idx, row in enumerate(tiles):
        for col_idx, tile_id in enumerate(row):
            if tile_id < 0:  # Saltar tiles vacíos (por ejemplo, -1)
                continue

            if tile_id == 5:
                tile_id = tree_frame

            # Calcular posición y recortar el tile del spritesheet
            x = col_idx * scaled_tile_size
            y = row_idx * scaled_tile_size
            src_x = (tile_id % 11) * tile_size
            src_y = (tile_id // 11) * tile_size

            tile = spritesheet.subsurface(pygame.Rect(src_x, src_y, tile_size, tile_size))
            tile = pygame.transform.scale(tile, (scaled_tile_size, scaled_tile_size))

            # Dibujar tile en la posición calculada
            screen.blit(tile, (x, y))


def draw_elements(screen, elements, element_sprites):
    """
    Dibuja los elementos adicionales del nivel.
    """
    for element in elements:
        element_type = element["type"]
        x = element["x"]
        y = element["y"]

        # Dibujar el sprite correspondiente al elemento
        if element_type in element_sprites:
            sprite = element_sprites[element_type]
            screen.blit(sprite, (x, y))
