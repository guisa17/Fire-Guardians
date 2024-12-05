import pygame
import asyncio
from src.game.player import Player
from src.game.fire import Fire
from src.game.animals import Bear, Monkey, Bird
from src.game.water_station import WaterStation
from src.game.powerup import WaterRefillPowerUp, ExtraLifePowerUp, SpeedBoostPowerUp, ShieldPowerUp
from src.core.settings import SCREEN_WIDTH, SCREEN_HEIGHT, FPS, SPRITE_SCALE
from src.game.level_loader import load_level, draw_tiles, draw_elements


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

    # Configuración del temporizador
    font = pygame.font.Font("assets/fonts/ascii-sector-16x16-tileset.ttf", 16 * (SPRITE_SCALE - 4))
    time_left = 61  # Temporizador en segundos

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
        time_left -= dt
        if time_left < 0:
            time_left = 0

        # Obtener teclas presionadas
        keys = pygame.key.get_pressed()

        # Actualizar lógica del jugador
        player.update(dt, keys)

        # Dibujar nivel
        screen.fill((0, 0, 0))  # Fondo negro
        draw_tiles(screen, level_data["level"], tiles_spritesheet, 16, SPRITE_SCALE)
        draw_elements(screen, level_data["elements"], element_sprites)

        # Dibujar jugador
        player.draw(screen)

        # Dibujar temporizador en la esquina superior derecha
        timer_text = f"{int(time_left):02d}s"
        timer_surface = font.render(timer_text, True, (255, 255, 255))  # Blanco
        timer_x = SCREEN_WIDTH - timer_surface.get_width() - 10
        timer_y = 10
        screen.blit(timer_surface, (timer_x, timer_y))

        # Actualizar pantalla
        pygame.display.flip()

        await asyncio.sleep(0)

    # Finalizar Pygame
    pygame.quit()


if __name__ == "__main__":
    asyncio.run(main())
