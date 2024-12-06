import pygame
from src.core.utils import load_image

class BackgroundMoving:
    def __init__(self, width, height):
        self.image_bg = load_image("menu/back.jpg")  # Ajustar ruta si es necesario
        self.x = 0
        self.y = 0
        self.dx = 2
        self.bg_width = self.image_bg.get_width()
        self.bg_height = self.image_bg.get_height()

    def update(self, screen):
        self.x -= self.dx
        if self.x <= -self.bg_width:
            self.x = 0
        screen.blit(self.image_bg, (self.x, self.y))
        screen.blit(self.image_bg, (self.x + self.bg_width, self.y))


class MainMenu:
    def __init__(self, screen):
        self.screen = screen
        # Asegúrate de tener la fuente en assets/fonts/font.ttf
        self.font_title = pygame.font.Font("assets/fonts/font.ttf", 72)
        self.font_option = pygame.font.Font("assets/fonts/font.ttf", 40)
        self.blink_timer = 0
        self.blink_visible = True
        self.selected_option = 0
        self.title_text = "Forest Guardians"
        self.title_display = ""
        self.title_index = 0
        self.options = ["Iniciar Juego", "Instrucciones"]

        self.background = BackgroundMoving(screen.get_width(), screen.get_height())

    def update(self, dt):
        # Animación del título
        if self.title_index < len(self.title_text):
            self.title_display += self.title_text[self.title_index]
            self.title_index += 1

        # Parpadeo
        self.blink_timer += dt
        if self.blink_timer >= 0.5:
            self.blink_visible = not self.blink_visible
            self.blink_timer = 0

        self.background.update(self.screen)

    def draw(self):
        # Dibujar título
        title_text = self.font_title.render(self.title_display, True, (255, 69, 0))
        title_rect = title_text.get_rect(center=(self.screen.get_width() // 2, 150))
        self.screen.blit(title_text, title_rect)

        # Mensaje parpadeante
        if self.blink_visible:
            start_text = self.font_option.render("Presiona ESPACIO para seleccionar", True, (255, 255, 10))
            start_rect = start_text.get_rect(center=(self.screen.get_width() // 2, self.screen.get_height() - 50))
            self.screen.blit(start_text, start_rect)

        # Opciones
        for i, option in enumerate(self.options):
            color = (255, 97, 0) if i == self.selected_option else (255, 255, 255)
            option_text = self.font_option.render(option, True, color)
            option_rect = option_text.get_rect(center=(self.screen.get_width() // 2, 300 + i * 50))
            self.screen.blit(option_text, option_rect)

    def handle_input(self, keys):
        # Navegar menú
        if keys[pygame.K_UP]:
            self.selected_option = (self.selected_option - 1) % len(self.options)
        elif keys[pygame.K_DOWN]:
            self.selected_option = (self.selected_option + 1) % len(self.options)
        elif keys[pygame.K_SPACE]:
            if self.selected_option == 0:
                return "start_game"
            elif self.selected_option == 1:
                return "instructions"
        return None
