import pygame
from src.core.utils import load_image

def render_text_with_outline(text, font, main_color, outline_color, outline_width):
    text_surface = font.render(text, True, main_color)
    outline_surface = font.render(text, True, outline_color)

    # Crear una superficie con transparencia
    size = (text_surface.get_width() + 2 * outline_width, text_surface.get_height() + 2 * outline_width)
    final_surface = pygame.Surface(size, pygame.SRCALPHA)

    # Renderizar el contorno desplazado en todas las direcciones
    for dx in range(-outline_width, outline_width + 1):
        for dy in range(-outline_width, outline_width + 1):
            if dx != 0 or dy != 0:
                final_surface.blit(outline_surface, (dx + outline_width, dy + outline_width))

    # Renderizar el texto principal encima
    final_surface.blit(text_surface, (outline_width, outline_width))

    return final_surface


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
        self.font_prompt = pygame.font.Font("assets/fonts/font.ttf", 40)
        self.blink_timer = 0
        self.blink_visible = True
        self.title_text = "Forest Guardians"
        self.title_display = ""
        self.title_index = 0

        self.background = BackgroundMoving(screen.get_width(), screen.get_height())


    def update(self, dt):
        # Animación del título (escribir letra por letra)
        if self.title_index < len(self.title_text):
            self.title_display += self.title_text[self.title_index]
            self.title_index += 1

        # Parpadeo del mensaje de inicio
        self.blink_timer += dt
        if self.blink_timer >= 0.5:
            self.blink_visible = not self.blink_visible
            self.blink_timer = 0

        self.background.update(self.screen)


    def draw(self):
        # Dibujar título centrado con contorno
        title_surface = render_text_with_outline(
            self.title_display,
            self.font_title,
            main_color=(255, 69, 0),            # Color principal (naranja)
            outline_color=(0, 0, 0),            # Color del contorno (negro)
            outline_width=3                     # Grosor del contorno
        )
        title_rect = title_surface.get_rect(center=(self.screen.get_width() // 2, 150))
        self.screen.blit(title_surface, title_rect)

        # Mensaje parpadeante para iniciar el juego con contorno
        if self.blink_visible:
            prompt_surface = render_text_with_outline(
                "Presiona ESPACIO para iniciar",
                self.font_prompt,
                main_color=(255, 255, 10),          # Color principal (amarillo)
                outline_color=(0, 0, 0),            # Color del contorno (negro)
                outline_width=3                     # Grosor del contorno
            )
            prompt_rect = prompt_surface.get_rect(center=(self.screen.get_width() // 2, self.screen.get_height() - 100))
            self.screen.blit(prompt_surface, prompt_rect)


    def handle_input(self, keys):
        # Detectar si se presiona la barra espaciadora para iniciar el juego
        if keys[pygame.K_SPACE]:
            return "start_game"
        return None
