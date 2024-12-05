import pygame
import json

# Configuración básica
TILE_SIZE = 16 * 2  # Tamaño de cada tile (escalado)
GRID_WIDTH = 20  # Ancho de la cuadrícula (número de tiles)
GRID_HEIGHT = 15  # Alto de la cuadrícula (número de tiles)
SCREEN_WIDTH = TILE_SIZE * GRID_WIDTH
SCREEN_HEIGHT = TILE_SIZE * GRID_HEIGHT + TILE_SIZE  # Espacio para el tileset

# Inicializar Pygame
pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Editor de Niveles")
clock = pygame.time.Clock()

# Cargar tileset
tileset = pygame.image.load("assets/images/tiles/tiles.png")
tileset = pygame.transform.scale(tileset, (tileset.get_width() * 2, tileset.get_height() * 2))
TILE_COUNT = tileset.get_width() // TILE_SIZE

# Cargar íconos para los elementos
icons = {
    "hydrant": pygame.image.load("assets/images/hydrant/hydrant.png"),
    "powerup_life": pygame.image.load("assets/images/powerups/extra_heart.png"),
    "powerup_water": pygame.image.load("assets/images/powerups/canteen.png"),
}
for key in icons:
    icons[key] = pygame.transform.scale(icons[key], (TILE_SIZE, TILE_SIZE))

# Propiedades de los tiles
TILE_PROPERTIES = {
    0: {"walkable": True},  # Pasto
    1: {"walkable": True},
    2: {"walkable": True},
    3: {"walkable": True},
    4: {"walkable": True},
    5: {"walkable": False, "animated": True},  # Árbol (animado)
    6: {"walkable": False, "animated": True},  # Árbol (animado)
    7: {"walkable": False},  # Tronco seco
    8: {"walkable": False},  # Agua
    9: {"walkable": False},  # Agua
    10: {"walkable": True},  # Puente
}

# Nivel inicial (vacío)
level = [[0 for _ in range(GRID_WIDTH)] for _ in range(GRID_HEIGHT)]
player_start = {"x": None, "y": None}  # Posición inicial del jugador
elements = []  # Lista de elementos en el mapa

# Variables del editor
selected_tile = 0  # Tile seleccionado
selecting_player_start = False  # Modo de selección del inicio del jugador
selected_element = None  # Elemento seleccionado


def draw_grid():
    """Dibuja la cuadrícula del nivel."""
    for x in range(0, SCREEN_WIDTH, TILE_SIZE):
        pygame.draw.line(screen, (200, 200, 200), (x, 0), (x, SCREEN_HEIGHT - TILE_SIZE))
    for y in range(0, SCREEN_HEIGHT - TILE_SIZE, TILE_SIZE):
        pygame.draw.line(screen, (200, 200, 200), (0, y), (SCREEN_WIDTH, y))


def draw_tiles():
    """Dibuja los tiles del nivel."""
    for row in range(GRID_HEIGHT):
        for col in range(GRID_WIDTH):
            tile_id = level[row][col]
            tile_x = (tile_id % TILE_COUNT) * TILE_SIZE
            tile_y = (tile_id // TILE_COUNT) * TILE_SIZE
            screen.blit(tileset, (col * TILE_SIZE, row * TILE_SIZE), (tile_x, tile_y, TILE_SIZE, TILE_SIZE))


def draw_tileset():
    """Dibuja el tileset para seleccionar tiles."""
    for i in range(TILE_COUNT):
        tile_x = i * TILE_SIZE
        screen.blit(tileset, (tile_x, SCREEN_HEIGHT - TILE_SIZE), (i * TILE_SIZE, 0, TILE_SIZE, TILE_SIZE))
        if i == selected_tile:
            pygame.draw.rect(screen, (255, 0, 0), (tile_x, SCREEN_HEIGHT - TILE_SIZE, TILE_SIZE, TILE_SIZE), 2)


def load_player_sprite():
    """Carga y recorta el primer sprite del spritesheet del jugador."""
    spritesheet = pygame.image.load("assets/images/player/idle.png")  # Ruta al spritesheet
    sprite_width, sprite_height = 20, 20  # Tamaño de cada sprite
    first_sprite = spritesheet.subsurface(pygame.Rect(0, 0, sprite_width, sprite_height))  # Extraer el primer sprite
    return pygame.transform.scale(first_sprite, (sprite_width * 2, sprite_height * 2))  # Escalar si es necesario


def draw_player_start():
    """Dibuja el punto de inicio del jugador con el primer sprite del spritesheet."""
    if player_start["x"] is not None and player_start["y"] is not None:
        player_sprite = load_player_sprite()  # Cargar el sprite del jugador
        screen.blit(player_sprite, (player_start["x"], player_start["y"]))  # Dibujar el sprite en la posición seleccionada


def draw_elements():
    """Dibuja los elementos en el mapa."""
    for element in elements:
        icon = icons[element["type"]]
        screen.blit(icon, (element["x"], element["y"]))


def save_level():
    """Guarda el nivel en un archivo JSON."""
    with open("level.json", "w") as file:
        json.dump({"level": level, "player_start": player_start, "elements": elements}, file)
    print("Nivel guardado en level.json")


def load_level():
    """Carga el nivel desde un archivo JSON."""
    global level, player_start, elements
    try:
        with open("level.json", "r") as file:
            data = json.load(file)
            level = data["level"]
            player_start = data["player_start"]
            elements = data["elements"]
        print("Nivel cargado desde level.json")
    except FileNotFoundError:
        print("No se encontró el archivo level.json")


def main():
    global selected_tile, selecting_player_start, player_start, selected_element
    running = True

    while running:
        screen.fill((0, 0, 0))

        # Dibujar nivel
        draw_tiles()

        # Dibujar cuadrícula
        draw_grid()

        # Dibujar tileset
        draw_tileset()

        # Dibujar punto de inicio del jugador
        draw_player_start()

        # Dibujar elementos
        draw_elements()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            # Cambiar el tile seleccionado con el mouse
            if event.type == pygame.MOUSEBUTTONDOWN:
                x, y = pygame.mouse.get_pos()
                if y >= SCREEN_HEIGHT - TILE_SIZE:  # Clic en el tileset
                    selected_tile = x // TILE_SIZE
                    selected_element = None
                else:  # Clic en la cuadrícula
                    if selecting_player_start:
                        player_start["x"] = x
                        player_start["y"] = y
                        selecting_player_start = False
                    elif selected_element:
                        elements.append({"type": selected_element, "x": x, "y": y})
                    else:
                        grid_x = x // TILE_SIZE
                        grid_y = y // TILE_SIZE
                        if grid_y < GRID_HEIGHT:
                            level[grid_y][grid_x] = selected_tile

            # Seleccionar elemento
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_s:  # Guardar nivel
                    save_level()
                elif event.key == pygame.K_l:  # Cargar nivel
                    load_level()
                elif event.key == pygame.K_p:  # Alternar modo de selección del punto de inicio
                    selecting_player_start = not selecting_player_start
                elif event.key == pygame.K_h:  # Seleccionar hidrante
                    selected_element = "hydrant"
                elif event.key == pygame.K_w:  # Seleccionar power-up agua
                    selected_element = "powerup_water"
                elif event.key == pygame.K_e:  # Seleccionar power-up vida
                    selected_element = "powerup_life"

        # Actualizar pantalla
        pygame.display.flip()
        clock.tick(60)

    pygame.quit()


if __name__ == "__main__":
    main()
