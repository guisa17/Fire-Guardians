import pygame
from src.core.settings import SCREEN_WIDTH, SCREEN_HEIGHT, FPS

def main():
    pygame.init()
    
    # Configurar la pantalla
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Fire Guardians")

    # Configurar el reloj para controlar FPS
    clock = pygame.time.Clock()

    # Colores de prueba
    WHITE = (255, 255, 255)
    GREEN = (34, 139, 34)

    # Bucle principal
    running = True
    while running:
        # Manejar eventos
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Actualizar la lógica del juego (vacío por ahora)

        # Dibujar la pantalla
        screen.fill(GREEN)  # Fondo verde
        pygame.draw.rect(screen, WHITE, (SCREEN_WIDTH // 2 - 50, SCREEN_HEIGHT // 2 - 50, 100, 100))  # Cuadrado blanco

        # Actualizar la pantalla
        pygame.display.flip()

        # Controlar el FPS
        clock.tick(FPS)

    # Salir de Pygame
    pygame.quit()

if __name__ == "__main__":
    main()
