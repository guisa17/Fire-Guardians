import pygame
import asyncio
import random
from src.states.main_menu import MainMenu
from src.states.instructions import InstructionsPage
from src.states.credits import CreditsPage
from src.game.player import Player
from src.game.fire import Fire
from src.game.water_station import WaterStation
from src.core.settings import SCREEN_WIDTH, SCREEN_HEIGHT, FPS, SPRITE_SCALE
from src.game.level_loader import load_level, draw_tiles, draw_elements, is_tile_walkable


def load_element_sprites():
    """
    Carga los sprites para los elementos adicionales (como hidrantes).
    """
    hydrant_sprite = pygame.image.load("assets/images/hydrant/hydrant.png").convert_alpha()
    hydrant_sprite = pygame.transform.scale(hydrant_sprite, (16 * SPRITE_SCALE, 16 * SPRITE_SCALE))
    return {
        "hydrant": hydrant_sprite,
    }


def initialize_game(level_data):
    """
    Inicializa todos los elementos necesarios para el juego.
    """
    player = Player(0, 0)
    start_position = level_data["player_start"]
    player.x = start_position["x"]
    player.y = start_position["y"]

    # Crear fuegos y estaciones de agua
    water_stations = initialize_water_stations(level_data)
    fires = create_random_fires(level_data, num_fires=5, tile_size=16 * SPRITE_SCALE, water_stations=water_stations)

    return player, fires, water_stations


def initialize_water_stations(level_data):
    """
    Crea los hidrantes basados en los elementos del nivel.
    """
    water_stations = []
    for element in level_data["elements"]:
        if element["type"] == "hydrant":
            water_stations.append(WaterStation(element["x"], element["y"]))
    return water_stations


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


async def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Fire Guardians")
    clock = pygame.time.Clock()

    # Inicializar pantallas
    main_menu = MainMenu(screen)
    instructions = InstructionsPage(screen)
    credits = CreditsPage(screen)

    # Cargar nivel
    level_data = load_level("level.json")
    tiles_spritesheet = pygame.image.load("assets/images/tiles/tiles.png").convert_alpha()
    element_sprites = load_element_sprites()

    # Estados del juego
    state = "menu"
    player, fires, water_stations = None, None, None

    running = True
    while running:
        dt = clock.tick(FPS) / 1000
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        keys = pygame.key.get_pressed()

        if state == "menu":
            # Actualizar y dibujar el menú principal
            main_menu.update(dt)
            main_menu.draw()
            selected = main_menu.handle_input(keys)
            if selected == 0:  # Iniciar juego
                state = "game"
                player, fires, water_stations = initialize_game(level_data)
            elif selected == 1:  # Instrucciones
                state = "instructions"
            elif selected == 2:  # Créditos
                state = "credits"
        elif state == "instructions":
            # Dibujar la pantalla de instrucciones
            instructions.draw()
            if keys[pygame.K_ESCAPE]:  # Volver al menú
                state = "menu"
        elif state == "credits":
            # Dibujar la pantalla de créditos
            credits.draw()
            if keys[pygame.K_ESCAPE]:  # Volver al menú
                state = "menu"
        elif state == "game":
            # Actualizar lógica del juego principal
            player.update(dt, keys, level_data, 16 * SPRITE_SCALE, water_stations)
            player.interact_with_fire(fires, keys)
            player.handle_collision(fires, dt, level_data, 16 * SPRITE_SCALE)
            player.recharge_water(water_stations, keys, dt=dt)

            # Actualizar lógica de los fuegos
            for fire in fires:
                fire.update(dt)
                fire.update_spread(dt, fires, 10, player, water_stations, level_data, 16 * SPRITE_SCALE)

            # Dibujar nivel y elementos
            screen.fill((0, 0, 0))  # Fondo negro
            draw_tiles(screen, level_data["level"], tiles_spritesheet, 16, SPRITE_SCALE)
            draw_elements(screen, level_data["elements"], element_sprites)

            # Dibujar jugador, fuegos e hidrantes
            player.draw(screen)
            for fire in fires:
                fire.draw(screen)
            for water_station in water_stations:
                water_station.draw(screen)

            # Dibujar HUD del jugador
            player.draw_hud(screen)

        pygame.display.flip()
        await asyncio.sleep(0)

    pygame.quit()


if __name__ == "__main__":
    asyncio.run(main())
