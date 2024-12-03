import pygame
from src.game.player import Player
from src.game.fire import Fire
from src.core.settings import SCREEN_WIDTH, SCREEN_HEIGHT, FPS


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

    # Crear fuego
    fires = [
        Fire(300, 200),
        Fire(100, 300),
        Fire(400, 100)
    ]

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
        player.update(dt, keys)
        player.interact_with_fire(fires, keys)
        player.handle_collision(fires, dt)  # Manejar colisiones con el fuego

        # Actualizar lógica del fuego
        for fire in fires:
            fire.update(dt)

        # Dibujar elementos en pantalla
        screen.fill((34, 139, 34))  # Fondo verde
        player.draw(screen)         # Dibujar jugador
        player.draw_water_bar(screen)  # Dibujar barra de agua
        player.draw_lives(screen)      # Dibujar corazones de vida

        for fire in fires:
            fire.draw(screen)  # Dibujar el fuego

        # Actualizar pantalla
        pygame.display.flip()

    # Finalizar Pygame
    pygame.quit()


if __name__ == "__main__":
    main()
