import pygame
import asyncio
from src.states.game_play import GamePlay
from src.game.levels import LEVELS
from src.core.settings import SCREEN_WIDTH, SCREEN_HEIGHT


class MainGame:
    def __init__(self):
        """
        Inicializa la configuración principal del juego.
        """
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Fire Guardians")
        self.level_index = 4
        self.running = True
        self.state = None

    def load_level(self):
        """
        Carga el nivel actual y pasa la configuración desde levels.py.
        """
        level_config = LEVELS[self.level_index]
        self.state = GamePlay(
            screen=self.screen,
            level_config=level_config,
            on_game_over=self.game_over,
            on_level_complete=self.next_level,
            level_index=self.level_index
        )

    def game_over(self):
        """
        Manejo del fin del juego.
        """
        print("Game over")
        self.running = False

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
        self.load_level()
        clock = pygame.time.Clock()

        while self.running:
            # Procesar eventos
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

            # Delta time y actualización del juego
            dt = clock.tick(60) / 1000  # Limitar a 60 FPS
            keys = pygame.key.get_pressed()

            if self.state:
                self.state.update(dt, keys)
                self.state.draw()
                pygame.display.flip()  # Actualizar pantalla

            await asyncio.sleep(0)  # Permitir otras tareas del sistema

        pygame.quit()


if __name__ == "__main__":
    game = MainGame()
    asyncio.run(game.run())
