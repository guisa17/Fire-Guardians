import pygame

class BackgroundMoving:
    def __init__(self, width, height):
        self.image_bg = pygame.image.load("assets/images/fire/fondo2.jpg")
        self.x = 0
        self.y = 0  # Fijo en 0 para evitar desplazamiento vertical
        self.dx = 2  # Velocidad horizontal
        self.bg_width = self.image_bg.get_width()
        self.bg_height = self.image_bg.get_height()

    def update(self, screen):
        self.x -= self.dx  # Solo mover en la dirección horizontal
        if self.x <= -self.bg_width:
            self.x = 0
        # Dibujar el fondo para crear el efecto de repetición horizontal
        screen.blit(self.image_bg, (self.x, self.y))
        screen.blit(self.image_bg, (self.x + self.bg_width, self.y))

        # Cubrir cualquier espacio vacío en la pantalla
        if self.x < 0:
            screen.blit(self.image_bg, (self.x + self.bg_width, self.y))


class MainMenu:
    def __init__(self, screen):
        self.screen = screen
        self.font_title = pygame.font.Font("assets/fonts/font.ttf", 72)  # Fuente para el título
        self.font_option = pygame.font.Font("assets/fonts/font.ttf", 40)  # Fuente personalizada para las opciones
        self.blink_timer = 0
        self.blink_visible = True
        self.selected_option = 0  # Índice de la opción seleccionada
        self.title_text = "Forest Guardians"
        self.title_display = ""  # Texto del título que se irá mostrando letra por letra
        self.title_index = 0  # Índice para animación del título

        # Opciones del menú (eliminada la opción de créditos)
        self.options = ["Iniciar Juego", "Instrucciones"]

        # Fondo animado
        self.background = BackgroundMoving(screen.get_width(), screen.get_height())

    def update(self, dt):
        """Actualiza el estado del menú."""
        # Animación de título, mostrando una letra cada vez
        if self.title_index < len(self.title_text):
            self.title_display += self.title_text[self.title_index]
            self.title_index += 1

        # Parpadeo de "Presiona ESPACIO para empezar"
        self.blink_timer += dt
        if self.blink_timer >= 0.5:  # Cambiar visibilidad cada 0.5 segundos
            self.blink_visible = not self.blink_visible
            self.blink_timer = 0

        # Actualizar el fondo
        self.background.update(self.screen)

    def draw(self):
        """Dibuja el menú principal en pantalla."""
        # Fondo animado ya actualizado

        # Título con animación
        title_text = self.font_title.render(self.title_display, True, (255, 69, 0))
        title_rect = title_text.get_rect(center=(self.screen.get_width() // 2, 150))
        self.screen.blit(title_text, title_rect)

        # Opción "Presiona ESPACIO para empezar" intermitente
        if self.blink_visible:
            start_text = self.font_option.render("Presiona ESPACIO para seleccionar", True, (255, 255, 10))
            start_rect = start_text.get_rect(center=(self.screen.get_width() // 2, self.screen.get_height() - 50))
            self.screen.blit(start_text, start_rect)

        # Opciones del menú con la tipografía adecuada
        for i, option in enumerate(self.options):
            color = (255, 97, 0) if i == self.selected_option else (255, 255, 255)  # Resaltar opción seleccionada
            option_text = self.font_option.render(option, True, color)
            option_rect = option_text.get_rect(center=(self.screen.get_width() // 2, 300 + i * 50))
            self.screen.blit(option_text, option_rect)

    def handle_input(self, keys):
        """Maneja la entrada del usuario."""
        if keys[pygame.K_UP]:
            self.selected_option = (self.selected_option - 1) % len(self.options)
        elif keys[pygame.K_DOWN]:
            self.selected_option = (self.selected_option + 1) % len(self.options)
        elif keys[pygame.K_SPACE]:
            if self.selected_option == 0:
                return "start_game"  # Iniciar juego
            elif self.selected_option == 1:
                return "instructions"  # Ir a instrucciones
        return None
