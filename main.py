import pygame
import asyncio
import random
from src.game.player import Player
from src.game.fire import Fire
from src.game.water_station import WaterStation
from src.core.settings import SCREEN_WIDTH, SCREEN_HEIGHT, FPS, SPRITE_SCALE
from src.game.level_loader import load_level, draw_tiles, draw_elements, is_tile_walkable


def initialize_player(level_data):
    """
    Inicializa al jugador en la posición inicial definida en el nivel.
    """
    player = Player(0, 0)
    start_position = level_data["player_start"]
    player.x = start_position["x"]
    player.y = start_position["y"]
    return player


def load_element_sprites():
    """
    Carga los sprites para los elementos adicionales (hidrantes, etc.).
    """
    hydrant_sprite = pygame.image.load("assets/images/hydrant/hydrant.png").convert_alpha()
    hydrant_sprite = pygame.transform.scale(hydrant_sprite, (16 * SPRITE_SCALE, 16 * SPRITE_SCALE))
    return {
        "hydrant": hydrant_sprite,
    }


def create_random_fires(level_data, num_fires, tile_size, water_stations):
    """
    Crea fuegos en posiciones aleatorias dentro del nivel.
    """
    fires = []
    hydrant_positions = {(ws.x // tile_size, ws.y // tile_size) for ws in water_stations}

    for _ in range(num_fires):
        while True:
            col = random.randint(0, len(level_data["level"][0]) - 1)
            row = random.randint(0, len(level_data["level"]) - 1)

            if (col, row) in hydrant_positions:
                continue

            x = col * tile_size
            y = row * tile_size
            fire_rect = pygame.Rect(x, y, tile_size, tile_size)

            # Solo colocar fuego en tiles "walkable"
            if is_tile_walkable(level_data, fire_rect, tile_size):
                fires.append(Fire(x, y))
                break
    return fires


def initialize_water_stations(level_data):
    """
    Crea los hidrantes basados en los elementos del nivel.
    """
    water_stations = []
    for element in level_data["elements"]:
        if element["type"] == "hydrant":
            water_stations.append(WaterStation(element["x"], element["y"]))
    return water_stations


async def main():
    """
    Bucle principal del juego.
    """
    # Inicializar Pygame
    pygame.init()

    # Configurar pantalla y reloj
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Fire Guardians - Prueba del Jugador")
    clock = pygame.time.Clock()

    # Cargar nivel
    level_data = load_level("level.json")

    # Cargar spritesheet de tiles
    tiles_spritesheet = pygame.image.load("assets/images/tiles/tiles.png").convert_alpha()

    # Cargar sprites para elementos adicionales
    element_sprites = load_element_sprites()

    # Inicializar jugador en la posición inicial del nivel
    player = initialize_player(level_data)

    # Inicializar hidrantes desde el nivel
    water_stations = initialize_water_stations(level_data)

    # Crear fuegos aleatorios
    fires = create_random_fires(level_data, num_fires=5, tile_size=16 * SPRITE_SCALE, water_stations=water_stations)

    # Configuración del temporizador
    # font = pygame.font.Font("assets/fonts/ascii-sector-16x16-tileset.ttf", 16 * (SPRITE_SCALE - 1))
    # time_left = 61  # Temporizador en segundos

    max_fires = 10
    running = True

    # Bucle principal
    while running:
        # Delta time
        dt = clock.tick(FPS) / 1000

        # Manejar eventos
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Actualizar el temporizador
        player.time_left -= dt
        if player.time_left < 0:
            player.time_left = 0

        # Obtener teclas presionadas
        keys = pygame.key.get_pressed()

        # Actualizar lógica del jugador
        player.update(dt, keys, level_data, 16 * SPRITE_SCALE, water_stations)
        player.interact_with_fire(fires, keys)
        player.handle_collision(fires, dt, level_data, 16 * SPRITE_SCALE)
        player.recharge_water(water_stations, keys, dt=dt)

        # Actualizar lógica de los fuegos
        for fire in fires:
            fire.update(dt)
            fire.update_spread(dt, fires, max_fires, player, water_stations, level_data, 16 * SPRITE_SCALE)

        # Dibujar nivel
        screen.fill((0, 0, 0))  # Fondo negro
        draw_tiles(screen, level_data["level"], tiles_spritesheet, 16, SPRITE_SCALE)
        draw_elements(screen, level_data["elements"], element_sprites)

        # Dibujar jugador
        player.draw(screen)

        # Dibujar fuegos
        for fire in fires:
            fire.draw(screen)
        
        # Dibujar hidrantes
        for water_station in water_stations:
            water_station.draw(screen)

        # Dibujar HUD del jugador
        player.draw_hud(screen)

        # Actualizar pantalla
        pygame.display.flip()

        await asyncio.sleep(0)

    # Finalizar Pygame
    pygame.quit()


if __name__ == "__main__":
    asyncio.run(main())
