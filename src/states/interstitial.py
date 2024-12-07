import pygame
import random
import textwrap

class InterstitialState:
    def __init__(self, screen, mode):
        """
        mode: "next_level" o "game_over" para saber qué hacer al terminar.
        """
        self.screen = screen
        self.mode = mode
        self.font = pygame.font.Font("assets/fonts/font.ttf", 30)
        self.timer = 5.0  # 10 segundos

        # Cargar frases desde el txt
        with open("assets/phrases.txt", "r", encoding="utf-8") as f:
            lines = [line.strip() for line in f if line.strip()]

        # Escoger una frase al azar
        self.phrase = random.choice(lines)

        # Ajustar el texto al ancho de la pantalla
        self.lines = self.wrap_text(self.phrase, self.font, int(self.screen.get_width() * 0.8))

    def wrap_text(self, text, font, max_width):
        """
        Ajusta el texto para que no exceda max_width, devolviendo una lista de líneas.
        """
        words = text.split(' ')
        lines = []
        current_line = []

        for word in words:
            test_line = ' '.join(current_line + [word])
            width, _ = font.size(test_line)
            if width <= max_width:
                current_line.append(word)
            else:
                # Guardar la línea actual y empezar una nueva
                lines.append(' '.join(current_line))
                current_line = [word]

        if current_line:
            lines.append(' '.join(current_line))

        return lines

    def update(self, dt):
        self.timer -= dt

    def draw(self):
        self.screen.fill((0,0,0))

        # Renderizar las líneas y centrarlas verticalmente
        line_surfaces = [self.font.render(line, True, (255,255,255)) for line in self.lines]
        total_height = sum(s.get_height() for s in line_surfaces)
        y_start = (self.screen.get_height() - total_height) // 2

        x_center = self.screen.get_width() // 2
        y_pos = y_start
        for surf in line_surfaces:
            rect = surf.get_rect(center=(x_center, y_pos + surf.get_height()//2))
            self.screen.blit(surf, rect)
            y_pos += surf.get_height() + 5  # 5px de espacio entre líneas

    def is_finished(self):
        return self.timer <= 0
