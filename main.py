import pygame
import asyncio
from src.game.player import Player
from src.game.fire import Fire
from src.game.animals import Bear, Monkey, Bird
from src.game.water_station import WaterStation
from src.game.powerup import WaterRefillPowerUp, ExtraLifePowerUp, SpeedBoostPowerUp, ShieldPowerUp
from src.core.settings import SCREEN_WIDTH, SCREEN_HEIGHT, FPS, SPRITE_SCALE
from src.core.utils import generate_random_fire


def initialize_game_objects():
    """
    Inicializa los objetos principales del juego.
    """
    player = Player(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)

    animals = [
        Bear(300, 300),
        Monkey(300, 200),
        Bird(300, 100),
    ]

    water_station = WaterStation(100, 100)

    powerups = [
        WaterRefillPowerUp(100, 200),
        ExtraLifePowerUp(100, 300),
        SpeedBoostPowerUp(100, 400),
        ShieldPowerUp(100, 500),
    ]

    num_fires = 5
    fire_width = 16 * SPRITE_SCALE
    fire_height = 16 * SPRITE_SCALE
    player_position = (player.x, player.y)
    min_distance = 100
    min_fire_distance = 50

    fire_positions = generate_random_fire(
        num_fires,
        fire_width,
        fire_height,
        player_position=player_position,
        min_distance=min_distance,
        min_fire_distance=min_fire_distance,
    )
    fires = [Fire(x, y) for x, y in fire_positions]

    return player, animals, water_station, powerups, fires


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

    # Inicializar objetos del juego
    player, animals, water_station, powerups, fires = initialize_game_objects()
    max_fires = 10
    running = True

    # Configuración del temporizador
    font = pygame.font.Font("assets/fonts/ascii-sector-16x16-tileset.ttf", 16 * (SPRITE_SCALE - 4))
    time_left = 61  # Temporizador en segundos

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

        # Actualizar lógica del juego
        player.update(dt, keys, water_station, animals)
        player.interact_with_fire(fires, keys)
        player.handle_collision(fires, dt)
        player.recharge_water(water_station, keys, dt=dt)

        for fire in fires:
            fire.update(dt)
            fire.update_spread(dt, fires, max_fires, player)

        for animal in animals:
            animal.update(dt)

        player.interact_with_animals(animals, keys)

        for powerup in powerups:
            player.interact_with_powerups(powerups)

        # Dibujar elementos en pantalla
        screen.fill((34, 139, 34))  # Fondo verde
        water_station.draw(screen)
        player.draw(screen)
        player.draw_hud(screen)

        for fire in fires:
            fire.draw(screen)

        for animal in animals:
            animal.draw(screen)

        for powerup in powerups:
            powerup.draw(screen)
        
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
