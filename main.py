import pygame
from src.game.player import Player  # Importa la clase Player
from src.game.fire import Fire
from src.game.animals import Bear, Monkey, Bird
from src.game.water_station import WaterStation
from src.game.powerup import WaterRefillPowerUp, ExtraLifePowerUp, SpeedBoostPowerUp, ShieldPowerUp
from src.core.settings import SCREEN_WIDTH, SCREEN_HEIGHT, FPS, SPRITE_SCALE
from src.core.utils import generate_random_fire
# Agregar las importaciones necesarias para los niveles
from src.game.level import create_level_1, create_level_2, create_level_3, create_level_4, create_level_5

def load_level(level_number):
    if level_number == 1:
        return create_level_1()
    elif level_number == 2:
        return create_level_2()
    elif level_number == 3:
        return create_level_3()
    elif level_number == 4:
        return create_level_4()
    elif level_number == 5:
        return create_level_5()

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

    # Inicializar nivel
    level_number = 1
    fires, animals, powerups, water_station = load_level(level_number)
    player = Player(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)

    # Bucle principal
    running = True
    while running:
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
            fire.update_spread(dt, fires, 10, player)

        # Dibujar elementos en pantalla
        screen.fill((34, 139, 34))  # Fondo verde
        water_station.draw(screen)
        player.draw(screen)         # Dibujar jugador
        player.draw_water_bar(screen)  # Dibujar barra de agua
        player.draw_lives(screen)      # Dibujar corazones de vida

        for fire in fires:
            fire.draw(screen)  # Dibujar el fuego

        for animal in animals:
            animal.update(dt)
            animal.draw(screen)
        player.interact_with_animals(animals, keys)

        for powerup in powerups:
            powerup.draw(screen)
        player.interact_with_powerups(powerups)

        # Actualizar pantalla
        pygame.display.flip()

        # Si el jugador completa el nivel, cargar el siguiente
        if player.player_complete_level():  # Llamar al método correctamente desde la instancia del jugador
            level_number += 1
            if level_number > 5:  # Si se completaron todos los niveles, termina el juego
                running = False
            else:
                fires, animals, powerups, water_station = load_level(level_number)

    pygame.quit()

if __name__ == "__main__":
    main()
