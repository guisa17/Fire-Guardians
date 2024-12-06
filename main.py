import pygame
import asyncio
from src.states.game_play import GamePlay
from src.game.levels import LEVELS
from src.core.settings import SCREEN_WIDTH, SCREEN_HEIGHT, FPS
from src.states.main_menu import MainMenu
from src.states.game_over import GameOver


class MainGame:
    def __init__(self):
        """
        Inicializa la configuración principal del juego.
        """
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Fire Guardians")
        self.level_index = 0
        self.running = True
        self.state = "menu"  # Estados: "menu", "game", "game_over"
        self.current_gameplay = None
        self.main_menu = MainMenu(self.screen)
        self.game_over_screen = None

    def load_level(self):
        """
        Carga el nivel actual y pasa la configuración desde levels.py.
        """
        level_config = LEVELS[self.level_index]
        self.current_gameplay = GamePlay(
            screen=self.screen,
            level_config=level_config,
            on_game_over=self.trigger_game_over,
            on_level_complete=self.next_level,
        )

    def trigger_game_over(self):
        """
        Cambia el estado a Game Over.
        """
        self.state = "game_over"
        self.game_over_screen = GameOver(self.screen)

    def next_level(self):
        """
        Manejo de la transición entre niveles.
        """
        self.level_index += 1
        if self.level_index < len(LEVELS):
            print(f"Loading level {self.level_index + 1}")
            self.load_level()
        else:
            print("Congratulations! You completed all levels.")
            self.running = False

    async def run(self):
        """
        Bucle principal del juego.
        """
        clock = pygame.time.Clock()

        while self.running:
            dt = clock.tick(FPS) / 1000

            if self.state == "menu":
                # Manejo del menú principal
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        self.running = False

                selected = self.main_menu.handle_input(pygame.key.get_pressed())
                if selected == "start_game":
                    self.load_level()
                    self.state = "game"
                elif selected == "instructions":
                    print("Ir a instrucciones")
                elif selected == "credits":
                    print("Ir a créditos")

                self.main_menu.update(dt)
                self.main_menu.draw()
                pygame.display.flip()

            elif self.state == "game":
                # Manejo del juego
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        self.running = False

                keys = pygame.key.get_pressed()
                if self.current_gameplay:
                    self.current_gameplay.update(dt, keys)
                    self.current_gameplay.draw()
                    pygame.display.flip()

                # Verificar si el jugador pierde todas las vidas
                if self.current_gameplay.player.current_lives <= 0:
                    self.trigger_game_over()

            elif self.state == "game_over":
                # Manejo de la pantalla Game Over
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        self.running = False

                keys = pygame.key.get_pressed()
                selected = self.game_over_screen.handle_input(keys)

                if selected == 0:  # Intentar de nuevo
                    self.level_index = 0
                    self.load_level()
                    self.state = "game"
                elif selected == 1:  # Salir
                    self.running = False

                self.game_over_screen.update(dt)
                self.game_over_screen.draw()
                pygame.display.flip()

        pygame.quit()


if __name__ == "__main__":
    game = MainGame()
    asyncio.run(game.run())
