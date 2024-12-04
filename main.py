import pygame
from src.game.player import Player
from src.game.fire import Fire
from src.game.animals import Bear, Monkey, Bird
from src.game.water_station import WaterStation
from src.game.powerup import WaterRefillPowerUp, ExtraLifePowerUp, SpeedBoostPowerUp, ShieldPowerUp
from src.core.settings import SCREEN_WIDTH, SCREEN_HEIGHT, FPS, SPRITE_SCALE
from src.core.utils import generate_random_fire


def main():
    """
    Bucle principal del juego para probar la funcionalidad del jugador.
    """
    # Inicializar Pygame
    pygame.init()

    # Configurar pantalla
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Fire Guardians - Prueba del Jugador")
    
    # Configurar reloj para controlar FPS
    clock = pygame.time.Clock()

    # Crear al jugador en el centro de la pantalla
    player = Player(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)

    animals = [
        Bear(300, 300), 
        Monkey(300, 200),
        Bird(300, 100)
        ]

    # Crear estación de agua
    water_station = WaterStation(100, 100)

    powerups = [
        WaterRefillPowerUp(100, 200),
        ExtraLifePowerUp(100, 300), 
        SpeedBoostPowerUp(100, 400),
        ShieldPowerUp(100, 500)
        ]


    # Crear fuegos aleatorios evitando al jugador
    num_fires = 5
    fire_width = 16 * SPRITE_SCALE
    fire_height = 16 * SPRITE_SCALE
    player_position = (player.x, player.y)
    min_distance = 100  # Distancia mínima del fuego al jugador
    min_fire_distance = 50
    fire_positions = generate_random_fire(num_fires, fire_width, fire_height, player_position=player_position, 
                                          min_distance=min_distance, min_fire_distance=min_fire_distance)

    fires = [Fire(x, y) for x, y in fire_positions]
    max_fires = 10

    # Bucle principal
    running = True
    while running:
        # Delta time
        dt = clock.tick(FPS) / 1000  # Tiempo entre cuadros en segundos

        # Manejar eventos
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Obtener teclas presionadas
        keys = pygame.key.get_pressed()

        # Actualizar lógica del jugador
        player.update(dt, keys, water_station, animals)
        player.interact_with_fire(fires, keys)
        player.handle_collision(fires, dt)  # Manejar colisiones con el fuego
        player.recharge_water(water_station, keys, dt=dt)

        # Actualizar lógica del fuego
        for fire in fires:
            fire.update(dt)
            fire.update_spread(dt, fires, max_fires, player)


        # Dibujar elementos en pantalla
        screen.fill((34, 139, 34))  # Fondo verde
        water_station.draw(screen)
        player.draw(screen)         # Dibujar jugador
        player.draw_water_bar(screen)  # Dibujar barra de agua
        player.draw_lives(screen)      # Dibujar corazones de vida
        

        for fire in fires:
            fire.draw(screen)  # Dibujar el fuego

        # Dentro del bucle principal
        for animal in animals:
            animal.update(dt)
            animal.draw(screen)
        player.interact_with_animals(animals, keys)

        for powerup in powerups:
            powerup.draw(screen)
        player.interact_with_powerups(powerups)

        # Actualizar pantalla
        pygame.display.flip()

    # Finalizar Pygame
    pygame.quit()


if __name__ == "__main__":
    main()