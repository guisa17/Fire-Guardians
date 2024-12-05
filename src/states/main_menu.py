import pygame

class MainMenu:
    def __init__(self, screen):
        self.screen = screen
        self.font_title = pygame.font.Font(None, 100)  # Fuente para el título
        self.font_option = pygame.font.Font(None, 50)  # Fuente para las opciones
        self.selected_option = 0  # Índice de la opción seleccionada

        # Opciones del menú
        self.options = ["Iniciar Juego", "Instrucciones", "Créditos"]

        # Control de tiempo para entrada
        self.input_cooldown = 0.3  # 300 ms entre cambios
        self.cooldown_timer = 0

    def update(self, dt):
        """Actualiza el temporizador para el control de entrada."""
        self.cooldown_timer += dt

    def draw_gradient_background(self):
        """Dibuja un fondo degradado."""
        for i in range(self.screen.get_height()):
            color = (
                34,
                139 + int(i / self.screen.get_height() * 116),
                34,
            )  # Degradado verde
            pygame.draw.line(self.screen, color, (0, i), (self.screen.get_width(), i))

    def draw(self):
        """Dibuja el menú principal en pantalla."""
        self.draw_gradient_background()

        # Título
        title_text = self.font_title.render("Fire Guardians", True, (255, 255, 255))
        title_rect = title_text.get_rect(center=(self.screen.get_width() // 2, 150))
        self.screen.blit(title_text, title_rect)

        # Opciones del menú
        for i, option in enumerate(self.options):
            color = (0, 255, 0) if i == self.selected_option else (255, 255, 255)
            bg_color = (50, 150, 50) if i == self.selected_option else (0, 0, 0)

            # Dibujar fondo de opción
            option_rect = pygame.Rect(
                self.screen.get_width() // 2 - 150,
                300 + i * 60,
                300,
                50,
            )
            pygame.draw.rect(self.screen, bg_color, option_rect, border_radius=10)
            pygame.draw.rect(self.screen, (0, 255, 0), option_rect, 2, border_radius=10)

            # Dibujar texto de opción
            option_text = self.font_option.render(option, True, color)
            option_text_rect = option_text.get_rect(center=option_rect.center)
            self.screen.blit(option_text, option_text_rect)

    def handle_input(self, keys):
        """Maneja la entrada del usuario."""
        if self.cooldown_timer >= self.input_cooldown:
            if keys[pygame.K_UP]:
                self.selected_option = (self.selected_option - 1) % len(self.options)
                self.cooldown_timer = 0  # Reinicia el temporizador
            elif keys[pygame.K_DOWN]:
                self.selected_option = (self.selected_option + 1) % len(self.options)
                self.cooldown_timer = 0  # Reinicia el temporizador
            elif keys[pygame.K_SPACE]:
                return self.selected_option  # Retorna la opción seleccionada
        return None

