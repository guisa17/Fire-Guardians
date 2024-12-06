import pygame
import asyncio
from src.states.game_play import GamePlay
from src.game.levels import LEVELS
from src.core.settings import SCREEN_WIDTH, SCREEN_HEIGHT, FPS
from src.states.main_menu import MainMenu


async def main():
    """
    Bucle principal del juego.
    """
    # Inicializar Pygame
    pygame.init()

    # Configurar pantalla y reloj
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Fire Guardians")
    clock = pygame.time.Clock()

    # Variables de control del juego
    current_level = 1  # Iniciar desde el nivel 1
    running = True
    runningmenu = True
    
    # Crear el menú principal
    main_menu = MainMenu(screen)

    # Bucle del menú principal
    while runningmenu:
        # Delta time
        dt = clock.tick(FPS) / 1000

        # Manejar eventos
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                runningmenu = False
            elif main_menu.handle_input(pygame.key.get_pressed()) == "start_game":
                runningmenu = False  # Salir del menú y comenzar el juego
                break
            elif main_menu.handle_input(pygame.key.get_pressed()) == "instructions":
                print("Ir a instrucciones")  # Implementa las instrucciones si lo deseas
            elif main_menu.handle_input(pygame.key.get_pressed()) == "credits":
                print("Ir a créditos")  # Implementa los créditos si lo deseas

        # Actualizar el menú
        main_menu.update(dt)

        # Dibujar el menú
        main_menu.draw()

        # Actualizar pantalla
        pygame.display.flip()
    
    while running:
        # Configurar el nivel actual
        game_play = GamePlay(current_level)
        game_play.setup_level()

        # Bucle del nivel
        while game_play.running:
            # Delta time
            dt = clock.tick(FPS) / 1000

            # Manejar eventos
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    game_play.running = False

            # Actualizar lógica del nivel
            game_play.update(dt)

            # Dibujar en pantalla
            game_play.draw(screen)

            # Actualizar pantalla
            pygame.display.flip()

            await asyncio.sleep(0)

        # Si el tiempo se acabó, pasar al siguiente nivel o terminar el juego
        if game_play.player.time_left <= 0:
            current_level += 1
            if current_level > len(LEVELS):
                running = False  # No hay más niveles, terminar el juego

    # Finalizar Pygame
    pygame.quit()


if __name__ == "__main__":
    asyncio.run(main())