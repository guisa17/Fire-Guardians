import pygame

class InstructionsPage:
    def __init__(self, screen):
        self.screen = screen
        self.font = pygame.font.Font(None, 40)

    def draw(self):
        """Dibuja la pantalla de instrucciones."""
        self.screen.fill((0, 0, 0))  # Fondo negro
        text = self.font.render("Instrucciones: Use las flechas para moverse.", True, (255, 255, 255))
        text_rect = text.get_rect(center=(self.screen.get_width() // 2, self.screen.get_height() // 2))
        self.screen.blit(text, text_rect)
