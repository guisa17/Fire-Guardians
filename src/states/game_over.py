import pygame

class GameOver:
    def __init__(self, screen):
        """
        Inicializa la pantalla de Game Over.
        """
        self.screen = screen
        # Cargar la fuente personalizada 'font.ttf'
        self.font_title = pygame.font.Font('assets/fonts/font.ttf', 80)  # Fuente para el texto "Game Over"
        self.font_option = pygame.font.Font('assets/fonts/font.ttf', 50)  # Fuente para las opciones
        self.selected_option = 0  # Índice de la opción seleccionada
        self.options = ["Intentar de nuevo", "Salir"]
        self.blink_timer = 0
        self.blink_visible = True
        self.input_cooldown = 0.2  # Tiempo entre cambios de opción
        self.cooldown_timer = 0

    def update(self, dt):
        """Actualiza el estado del texto parpadeante y el tiempo de entrada."""
        self.blink_timer += dt
        self.cooldown_timer += dt
        if self.blink_timer >= 0.5:  # Alternar visibilidad del texto parpadeante
            self.blink_visible = not self.blink_visible
            self.blink_timer = 0

    def draw(self):
        """Dibuja la pantalla de Game Over."""
        self.screen.fill((0, 0, 0))  # Fondo negro

        # Texto "Game Over" parpadeante
        if self.blink_visible:
            title_text = self.font_title.render("Game Over", True, (255, 0, 0))
            title_rect = title_text.get_rect(center=(self.screen.get_width() // 2, 150))
            self.screen.blit(title_text, title_rect)

        # Dibujar las opciones
        for i, option in enumerate(self.options):
            color = (0, 255, 0) if i == self.selected_option else (255, 255, 255)  # Verde para la opción seleccionada
            bg_color = (50, 50, 50) if i == self.selected_option else (0, 0, 0)  # Fondo gris para la opción seleccionada

            # Calcular el tamaño del recuadro en función del tamaño del texto
            option_text = self.font_option.render(option, True, color)
            option_width, option_height = option_text.get_size()

            # Crear un rectángulo ajustado al texto
            option_rect = pygame.Rect(self.screen.get_width() // 2 - option_width // 2, 300 + i * 80, option_width + 20, option_height + 10)

            # Dibujar el recuadro con bordes pixelados
            pygame.draw.rect(self.screen, bg_color, option_rect, border_radius=5)  # Fondo del recuadro
            pygame.draw.rect(self.screen, (255, 255, 255), option_rect, 2, border_radius=5)  # Borde blanco

            # Texto de la opción
            text_rect = option_text.get_rect(center=option_rect.center)
            self.screen.blit(option_text, text_rect)

    def handle_input(self, keys):
        """Maneja la entrada del usuario para cambiar y seleccionar opciones."""
        if self.cooldown_timer >= self.input_cooldown:
            if keys[pygame.K_UP]:
                self.selected_option = (self.selected_option - 1) % len(self.options)
                self.cooldown_timer = 0
            elif keys[pygame.K_DOWN]:
                self.selected_option = (self.selected_option + 1) % len(self.options)
                self.cooldown_timer = 0
            elif keys[pygame.K_SPACE]:
                return self.selected_option  # Retorna la opción seleccionada
        return None
