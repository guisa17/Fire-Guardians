import pygame

class MainMenu:
    def __init__(self, screen):
        self.screen = screen
        self.font_title = pygame.font.Font(None, 72)  # Fuente para el título
        self.font_subtitle = pygame.font.Font(None, 36)  # Fuente para subtítulos
        self.font_notice = pygame.font.Font(None, 30)  # Fuente para el aviso
        self.blink_timer = 0
        self.blink_visible = True

    def update(self, dt):
        """Actualiza el estado del aviso intermitente."""
        self.blink_timer += dt
        if self.blink_timer >= 0.5:  # Cambiar visibilidad cada 0.5 segundos
            self.blink_visible = not self.blink_visible
            self.blink_timer = 0

    def draw(self):
        """Dibuja el menú principal en pantalla."""
        self.screen.fill((0, 0, 0))  # Fondo negro

        # Título
        title_text = self.font_title.render("Fire Peruvian Guardians", True, (255, 255, 255))
        title_rect = title_text.get_rect(center=(self.screen.get_width() // 2, 150))
        self.screen.blit(title_text, title_rect)

        # Subtítulo
        subtitle_text = self.font_subtitle.render("BST Studios", True, (255, 255, 255))
        subtitle_rect = subtitle_text.get_rect(center=(self.screen.get_width() // 2, 220))
        self.screen.blit(subtitle_text, subtitle_rect)

        # Aviso intermitente
        if self.blink_visible:
            notice_text = self.font_notice.render("Presione ESPACIO para empezar", True, (255, 255, 255))
            notice_rect = notice_text.get_rect(center=(self.screen.get_width() // 2, 350))
            self.screen.blit(notice_text, notice_rect)
