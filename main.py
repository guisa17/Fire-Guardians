import pygame
from src.core.settings import SCREEN_WIDTH, SCREEN_HEIGHT, FPS
from src.game.fire import Fire
from src.game.player import Player
from src.core.utils import draw_status
from src.game.animals import Animal  # Importamos la clase Animal
from src.states.main_menu import MainMenu  # Importamos la clase MainMenu

def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Fire Guardians")
    clock = pygame.time.Clock()

    # Crear instancias del menú y el juego principal
    menu = MainMenu(screen)
    game_started = False

    # Instancias necesarias para el juego principal
    GREEN = (34, 139, 34)
    player = Player(x=100, y=100)
    fires = Fire.spawn_random_fires(amount=5)
    animals = Animal.spawn_random_animals(amount=3)  # Generamos 3 animales aleatorios

    running = True
    while running:
        dt = clock.tick(FPS) / 1000
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        keys = pygame.key.get_pressed()

        if not game_started:
            # Actualizar y dibujar el menú principal
            menu.update(dt)
            menu.draw()
            if keys[pygame.K_SPACE]:
                game_started = True  # Iniciar el juego principal
        else:
            # Actualizar el juego principal
            player.update(dt, keys, fires)

            if keys[pygame.K_SPACE]:
                player.extinguish_fire(fires)

            # Verificar si el jugador está en el área del fuego y reducir vida
            for fire in fires:
                fire.check_player_in_fire(player, dt)

            # Actualizar el estado de los animales
            for animal in animals:
                animal.update(dt, pygame.Rect(player.x, player.y, player.run_sprites[0][0].get_width(), player.run_sprites[0][0].get_height()))

                # Si el jugador está cerca y presiona R, rescatar al animal
                if animal.is_rescuing and keys[pygame.K_r]:
                    animal.rescue()

            # Dibujar fondo, fuegos, animales, jugador y estado
            screen.fill(GREEN)
            for fire in fires:
                fire.draw(screen)
            for animal in animals:
                animal.draw(screen)
            player.draw(screen)
            draw_status(screen, player)

        pygame.display.flip()

    pygame.quit()

if __name__ == "__main__":
    main()
