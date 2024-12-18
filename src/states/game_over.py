import pygame

class GameOver:
    def __init__(self, screen, message="Game Over"):
        self.screen = screen
        self.message = message
        self.font_title = pygame.font.Font("assets/fonts/font.ttf", 72)
        self.font_option = pygame.font.Font("assets/fonts/font.ttf", 40)
        self.selected_option = 0
        self.options = ["Reintentar", "Salir"]

    def update(self, dt):
        pass

    def draw(self):
        self.screen.fill((0,0,0))
        title_text = self.font_title.render(self.message, True, (255, 0, 0))
        title_rect = title_text.get_rect(center=(self.screen.get_width() // 2, 150))
        self.screen.blit(title_text, title_rect)

        for i, option in enumerate(self.options):
            color = (255, 255, 0) if i == self.selected_option else (255, 255, 255)
            option_text = self.font_option.render(option, True, color)
            option_rect = option_text.get_rect(center=(self.screen.get_width() // 2, 300 + i * 50))
            self.screen.blit(option_text, option_rect)

    def handle_input(self, keys):
        if keys[pygame.K_UP]:
            self.selected_option = (self.selected_option - 1) % len(self.options)
        elif keys[pygame.K_DOWN]:
            self.selected_option = (self.selected_option + 1) % len(self.options)
        elif keys[pygame.K_SPACE]:
            return self.selected_option
        return None
