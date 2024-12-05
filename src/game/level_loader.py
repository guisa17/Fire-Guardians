import json
import pygame


def load_level(filename):
    """
    Carga los datos del nivel desde un archivo JSON.
    """
    with open(filename, "r") as file:
        level_data = json.load(file)
    return level_data


def draw_tiles(screen, tiles, spritesheet, tile_size, scale):
    """
    Dibuja los tiles del nivel en la pantalla.
    - `screen`: Superficie de Pygame para dibujar.
    - `tiles`: Matriz de tiles del nivel.
    - `spritesheet`: Spritesheet que contiene los tiles.
    - `tile_size`: Tamaño original de cada tile (sin escala).
    - `scale`: Escala aplicada a los tiles.
    """
    scaled_tile_size = tile_size * scale
    for row_idx, row in enumerate(tiles):
        for col_idx, tile_id in enumerate(row):
            if tile_id < 0:  # Saltar tiles vacíos (por ejemplo, -1)
                continue

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
    Dibuja los elementos adicionales del nivel (como hidrantes).
    - `screen`: Superficie de Pygame para dibujar.
    - `elements`: Lista de elementos con posiciones y tipos.
    - `element_sprites`: Diccionario de sprites de los elementos.
    """
    for element in elements:
        element_type = element["type"]
        x = element["x"]
        y = element["y"]

        # Dibujar el sprite correspondiente al elemento
        if element_type in element_sprites:
            sprite = element_sprites[element_type]
            screen.blit(sprite, (x, y))
