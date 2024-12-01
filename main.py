import pygame
from src.core.settings import SCREEN_WIDTH, SCREEN_HEIGHT, FPS
from src.game.fire import Fire
from src.game.player import Player


def main():
    pygame.init()

    # Configurar la pantalla
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Fire Guardians")

    # Configurar el reloj para controlar FPS
    clock = pygame.time.Clock()

    # Colores de prueba
    GREEN = (34, 139, 34)

    # Inicializar jugador y fuegos
    player = Player()
    fires = Fire.spawn_random_fires(amount=5)  # Generar 5 fuegos aleatorios

    # Bucle principal
    running = True
    while running:
        # Manejar eventos
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Detectar entradas del teclado
        keys = pygame.key.get_pressed()
        player.move(keys)

        # Dibujar la pantalla
        screen.fill(GREEN)  # Fondo verde

        # Dibujar fuegos
        for fire in fires:
            fire.draw(screen)

        # Dibujar jugador
        player.draw(screen)

        # Actualizar la pantalla
        pygame.display.flip()

        # Controlar el FPS
        clock.tick(FPS)

    # Salir de Pygame
    pygame.quit()


if __name__ == "__main__":
    main()
