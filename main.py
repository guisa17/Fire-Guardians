import pygame
import asyncio
from src.core.settings import FPS
from src.states.game_play import GamePlay
from src.game.levels import LEVELS
from src.core.settings import SCREEN_WIDTH, SCREEN_HEIGHT
from src.states.main_menu import MainMenu
from src.states.game_over import GameOver
from src.states.interstitial import InterstitialState
from src.core.utils import load_sound
import os


class MainGame:
    def __init__(self):
        """
        Inicializa la configuración principal del juego.
        """
        pygame.init()
        pygame.mixer.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Fire Guardians")
        self.level_index = 0
        self.running = True
        self.state = "menu"     # "menu", "game", "game_over"
        self.current_gameplay = None
        self.main_menu = MainMenu(self.screen)
        self.game_over_screen = None
        self.interstitial = None

        # Cargar sonidos
        self.sounds = {
            "fire": load_sound("fire.wav"),
            "game_over": load_sound("game_over.wav"),
            "powerup": load_sound("powerup.wav"),
            "steps": load_sound("steps.wav"),
            "bird": load_sound("bird.wav"),
            "bear": load_sound("bear.wav"),
            "monkey": load_sound("monkey.wav"),
            "recharge": load_sound("recharge.wav"),
            "extinguish": load_sound("extinguish.wav")
        }

        # Música de fondo (gameplay.wav) se usa en el menú y juego
        # Cargar música de fondo
        bg_music_path = os.path.join("assets", "sounds", "gameplay.wav")
        if not os.path.exists(bg_music_path):
            raise FileNotFoundError("No se encontró gameplay.wav")
        pygame.mixer.music.load(bg_music_path)
        pygame.mixer.music.play(-1)  # loop


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
            level_index=self.level_index,
            sounds=self.sounds
        )
        self.state = "game"

        # pygame.mixer.music.stop()
        # pygame.mixer.music.play(-1)


    def trigger_game_over(self):
        """
        Manejo del fin del juego.
        """
        print("Game over")
        self.sounds["game_over"].play()
        self.state = "interstitial"
        self.interstitial = InterstitialState(self.screen, "game_over")
        self.game_over_screen = GameOver(self.screen)


    def next_level(self):
        """
        Manejo de la transición entre niveles.
        """
        self.level_index += 1
        if self.level_index < len(LEVELS):
            print(f"Loading level {self.level_index + 1}")
            self.state = "interstitial"
            self.interstitial = InterstitialState(self.screen, "next_level")
        else:
            print("Congratulations! You completed all levels.")
            self.running = False


    async def run(self):
        """
        Bucle principal del juego.
        """
        clock = pygame.time.Clock()

        while self.running:
            # Procesar eventos
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

            # Delta time y actualización del juego
            dt = clock.tick(FPS) / 1000  # Limitar a 60 FPS
            keys = pygame.key.get_pressed()

            if self.state == "menu":
                self.main_menu.update(dt)
                selected = self.main_menu.handle_input(keys)

                if selected == "start_game":
                    self.level_index = 0
                    self.load_level()
                    # self.state = "game"
                elif selected == "instructions":
                    print("Mostrar instrucciones!")
                
                self.main_menu.draw()
                pygame.display.flip()

            elif self.state == "game":
                if self.current_gameplay:
                    self.current_gameplay.update(dt, keys)
                    self.current_gameplay.draw()
                    pygame.display.flip()

                    if self.current_gameplay.player.current_lives <= 0:
                        self.trigger_game_over()
            
            elif self.state == "interstitial":
                self.interstitial.update(dt)
                self.interstitial.draw()
                pygame.display.flip()

                if self.interstitial.is_finished():
                    if self.interstitial.mode == "next_level":
                        self.load_level()
                    elif self.interstitial.mode == "game_over":
                        self.state = "game_over"
                        self.game_over_screen = GameOver(self.screen)

            elif self.state == "game_over":
                if self.game_over_screen:
                    selected = self.game_over_screen.handle_input(keys)

                    if selected == 0:
                        self.level_index = 0
                        self.load_level()
                        self.state = "game"
                    elif selected == 1:
                        self.running = False
                    
                    self.game_over_screen.update(dt)
                    self.game_over_screen.draw()
                    pygame.display.flip()

            await asyncio.sleep(0)  # Permitir otras tareas del sistema

        pygame.quit()


if __name__ == "__main__":
    game = MainGame()
    asyncio.run(game.run())
