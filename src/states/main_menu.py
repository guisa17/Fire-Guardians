import pygame

class MainMenu:
    def __init__(self, screen):
        self.screen = screen
        self.font_title = pygame.font.Font(None, 72)  # Fuente para el título
        self.font_option = pygame.font.Font(None, 40)  # Fuente para las opciones
        self.blink_timer = 0
        self.blink_visible = True
        self.selected_option = 0  # Índice de la opción seleccionada

        # Opciones del menú
        self.options = ["Iniciar Juego", "Instrucciones", "Créditos"]

        # Control de tiempo para entrada
        self.input_cooldown = 0.2  # 200 ms entre cambios
        self.cooldown_timer = 0

    def update(self, dt):
        """Actualiza el estado del menú."""
        self.blink_timer += dt
        self.cooldown_timer += dt

        if self.blink_timer >= 0.5:  # Cambiar visibilidad cada 0.5 segundos
            self.blink_visible = not self.blink_visible
            self.blink_timer = 0

    def draw(self):
        """Dibuja el menú principal en pantalla."""
        self.screen.fill((0, 0, 0))  # Fondo negro

        # Título
        title_text = self.font_title.render("Fire Guardians", True, (255, 255, 255))
        title_rect = title_text.get_rect(center=(self.screen.get_width() // 2, 150))
        self.screen.blit(title_text, title_rect)

        # Opciones del menú
        for i, option in enumerate(self.options):
            color = (255, 255, 0) if i == self.selected_option else (255, 255, 255)  # Resaltar opción seleccionada
            option_text = self.font_option.render(option, True, color)
            option_rect = option_text.get_rect(center=(self.screen.get_width() // 2, 300 + i * 50))
            self.screen.blit(option_text, option_rect)

    def handle_input(self, keys):
        """Maneja la entrada del usuario."""
        if self.cooldown_timer >= self.input_cooldown:  # Verificar si pasó el cooldown
            if keys[pygame.K_UP]:
                self.selected_option = (self.selected_option - 1) % len(self.options)
                self.cooldown_timer = 0  # Reiniciar el cooldown
            elif keys[pygame.K_DOWN]:
                self.selected_option = (self.selected_option + 1) % len(self.options)
                self.cooldown_timer = 0  # Reiniciar el cooldown
            elif keys[pygame.K_SPACE]:
                return self.selected_option  # Retorna la opción seleccionada
        return None
